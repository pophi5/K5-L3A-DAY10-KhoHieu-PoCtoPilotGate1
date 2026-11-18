"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
import re
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _current_policy(ctx):
    """Lấy đúng phiên bản chính sách có hiệu lực tại ngày ctx.as_of."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _valid_approval(ctx, order_id: str, amount_vnd: int):
    """Tìm phê duyệt hợp lệ cho đúng ticket, đơn hàng, còn hạn và đủ hạn mức."""
    tid = ctx.ticket.get("ticket_id")
    for appr in ctx.tools.lookup_approvals(ticket_id=tid, order_id=order_id):
        if (
            appr.get("status") == "valid"
            and appr.get("expires_at", "") >= ctx.as_of
            and appr.get("max_vnd", 0) >= amount_vnd
        ):
            return appr
    return None


def _gate_issue_refund(ctx, action):
    """Cổng 1: đối chiếu hoàn tiền theo DB, chặn hoàn trùng và kiểm tra phê duyệt/trần ngày."""
    order_id = action.get("order_id")
    order = ctx.tools.lookup_order(order_id)
    pol = _current_policy(ctx)
    if order is None or pol is None:
        return Verdict.escalate("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực")
    if order.get("customer_id") != ctx.ticket.get("customer_id"):
        return Verdict.escalate("người gửi không khớp chủ đơn hàng")

    # Chặn hoàn trùng cả khi cờ đối soát đêm chưa kịp cập nhật hoặc có write_retry
    if order.get("refund_status") == "REFUNDED" or ctx.tools.ledger_rows(order_id=order_id):
        ctx.log("block_duplicate_refund", order_id=order_id)
        return Verdict.deny("đơn hàng đã được hoàn tiền trước đó")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    if parcel.get("status") == "DELIVERED" and not parcel.get("delivered_date"):
        ctx.log("deny_missing_delivery_date", parcel_id=parcel.get("parcel_id"))
        return Verdict.deny("dữ liệu tracking không đầy đủ (thiếu delivered_date)")
    delay = H.db_delay_days(parcel, ctx.as_of)
    true_amt = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    if true_amt <= 0:
        ctx.log("block_unentitled_refund", order_id=order_id, db_delay=delay, cause=parcel.get("delay_cause"))
        return Verdict.deny("không đủ điều kiện hoàn theo dữ liệu tracking và chính sách")

    approval_id = None
    if true_amt > pol["auto_limit_vnd"]:
        appr = _valid_approval(ctx, order_id, true_amt)
        if appr is None:
            return Verdict.escalate("vượt hạn mức tự động, thiếu phê duyệt hợp lệ")
        approval_id = appr["approval_id"]
    else:
        limits = ctx.tools.ops_limits()
        cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        cust_today = sum(
            r["amount_vnd"]
            for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
            if not r.get("approval_id") and not str(r.get("ticket_id", "")).startswith("T-OLD-")
        )
        if cust_cap is not None and cust_today + true_amt > cust_cap:
            return Verdict.escalate("vượt trần hoàn tự động theo khách trong ngày")

        spent_today = ctx.tools.auto_refund_today_vnd()
        gate_cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
        ops_budget = limits.get("daily_auto_refund_budget_vnd")
        caps = [c for c in (gate_cap, ops_budget) if c is not None]
        if caps and spent_today + true_amt > min(caps):
            return Verdict.escalate("vượt trần hoàn tự động trong ngày")

    if (
        action.get("amount_vnd") != true_amt
        or action.get("payer") != "LOGIX"
        or action.get("approval_id") != approval_id
    ):
        ctx.log("correct_refund_params", asked=action.get("amount_vnd"), true_amt=true_amt)
        return Verdict.modify(
            "chuẩn hoá khoản hoàn, bên trả và mã phê duyệt theo nguồn sự thật",
            amount_vnd=true_amt,
            payer="LOGIX",
            approval_id=approval_id,
            basis="policy",
        )
    return Verdict.allow()


def _gate_file_carrier_fault(ctx, action):
    """Cổng 2: chỉ ghi lỗi hãng khi tracking DB xác nhận đủ trễ, đúng nguyên nhân và còn trong trần ngày."""
    order = ctx.tools.lookup_order(action.get("order_id"))
    pol = _current_policy(ctx)
    if order is None or pol is None:
        return Verdict.deny("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực")
    if ctx.tools.fault_rows(ticket_id=ctx.ticket.get("ticket_id")):
        return Verdict.deny("đã ghi lỗi hãng cho ticket này")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    if parcel.get("status") == "DELIVERED" and not parcel.get("delivered_date"):
        ctx.log("deny_fault_missing_delivery_date", parcel_id=parcel.get("parcel_id"))
        return Verdict.deny("không ghi lỗi hãng khi dữ liệu tracking thiếu delivered_date")
    db_delay = H.db_delay_days(parcel, ctx.as_of)
    if not H.carrier_at_fault(pol, parcel, db_delay):
        ctx.log("block_wrongful_carrier_fault", parcel_id=parcel["parcel_id"], cause=parcel.get("delay_cause"))
        return Verdict.deny("không đủ điều kiện ghi lỗi hãng theo tracking DB và chính sách")

    max_strikes = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if max_strikes is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= max_strikes:
        ctx.log("block_carrier_strike_cap", carrier_id=parcel["carrier_id"])
        return Verdict.deny("vượt trần ghi lỗi tự động cho hãng trong ngày")

    if (
        action.get("parcel_id") != parcel["parcel_id"]
        or action.get("carrier_id") != parcel["carrier_id"]
        or action.get("driver_id") != parcel.get("driver_id")
        or action.get("delay_days") != db_delay
    ):
        return Verdict.modify(
            "chuẩn hoá kiện hàng, hãng và số ngày trễ theo tracking DB",
            parcel_id=parcel["parcel_id"],
            carrier_id=parcel["carrier_id"],
            driver_id=parcel.get("driver_id"),
            delay_days=db_delay,
        )
    return Verdict.allow()


def _gate_notify_carrier(ctx, action):
    """Cổng 3: chỉ giữ các trường được phép gửi hãng vận chuyển, chặn rò rỉ PII."""
    pol = _current_policy(ctx)
    allowed = set(pol["carrier_notice_fields"]) if pol and pol.get("carrier_notice_fields") else {
        "order_id",
        "parcel_id",
        "district",
        "delay_days",
    }
    payload = action.get("payload") or {}
    clean_payload = {k: v for k, v in payload.items() if k in allowed}
    if clean_payload != payload:
        ctx.log("strip_carrier_pii", removed=sorted(set(payload) - set(clean_payload)))
        return Verdict.modify(
            "chỉ giữ trường hợp lệ trong carrier_notice_fields, chặn lộ PII sang hãng",
            payload=clean_payload,
        )
    return Verdict.allow()


def pre_guard(ctx):
    pol = _current_policy(ctx)
    pinned_policy = pol["policy_id"] if pol else None

    # S1: Kiện hàng DELIVERED nhưng thiếu delivered_date -> dữ liệu tracking không hoàn chỉnh, escalate cho người
    order_id = ctx.ticket.get("order_id")
    if order_id:
        order = ctx.tools.lookup_order(order_id)
        if order:
            for p in order.get("parcels", []):
                if p.get("status") == "DELIVERED" and not p.get("delivered_date"):
                    ctx.log("escalate_missing_delivery_date", parcel_id=p.get("parcel_id"), order_id=order_id)
                    return Verdict.escalate("kiện hàng đã giao nhưng thiếu ngày giao trong dữ liệu tracking")

    # S1 & Prompt/Claim: Loại bỏ số ngày khách tự khai để không ghi đè nguồn sự thật DB
    orig_text = ctx.ticket.get("text", "")
    clean_text = re.sub(
        r"((?:trễ|tre|chậm|muộn|late|delay(?:ed)?)\D{0,24}?)\d{1,3}(\s*(?:ngày|ngay|days?|hôm))",
        r"\1\2",
        orig_text,
        flags=re.IGNORECASE,
    )
    if clean_text != orig_text:
        ctx.log("strip_claimed_delay", orig_text=orig_text, clean_text=clean_text)
        if pinned_policy:
            return Verdict.rewrite("bỏ số ngày khách tự khai để dùng dữ liệu tracking DB", clean_text, policy_id=pinned_policy)
        return Verdict.rewrite("bỏ số ngày khách tự khai để dùng dữ liệu tracking DB", clean_text)

    if pinned_policy:
        ctx.log("policy_pinned", policy_id=pinned_policy)
        return Verdict.allow(policy_id=pinned_policy)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_file_carrier_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify_carrier(ctx, action)
    return Verdict.allow()

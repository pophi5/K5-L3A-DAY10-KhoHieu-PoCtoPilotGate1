"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def carrier_fault_rate(trials):
    """Tỉ lệ ticket dẫn tới việc ghi lỗi hãng vận chuyển (bắt được chùm lỗi hãng)."""
    return sum(len(t.get("faults", [])) > 0 for t in trials) / max(1, len(trials))


def delivered_without_date_rate(trials):
    """Tỉ lệ ticket có kiện hàng DELIVERED nhưng thiếu delivered_date."""
    count = 0
    for t in trials:
        events = t.get("events", [])
        if any(e.get("type") in ("escalate_missing_delivery_date", "deny_missing_delivery_date") for e in events):
            count += 1
    return count / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_fault_rate": carrier_fault_rate,
    "delivered_without_date_rate": delivered_without_date_rate,
}
STARTER_MONITORS = ("escalation_rate",)

# PHÂN CHIA CÔNG VIỆC NHÓM 4 NGƯỜI · LAB 10 (From PoC to Pilot — Gate 1)

Tài liệu này tổng hợp lộ trình làm bài từ [`README.md`](README.md), [`problem-set.md`](problem-set.md), [`templates/README.md`](templates/README.md) và [`submission/README.md`](submission/README.md) cho nhóm **4 thành viên**.

---

## 1. Làm song song hay làm từng thành viên một?

**Câu trả lời ngắn gọn: LÀM SONG SONG cả 4 người, kết hợp 3 CHỐT CHẶN ĐỒNG BỘ (Synchronization Checkpoints).**

Trong `problem-set.md` đã thiết kế sẵn cơ chế làm song song (ví dụ Khối 2A chia ba vai làm song song 10 phút đầu rồi mới ghép bàn làm pre-mortem). Tuy nhiên, **không thể làm song song hoàn toàn tự do từ đầu đến cuối** vì có các ràng buộc kỹ thuật và logic sau:

1. **Ràng buộc 1 — Quy tắc "Ký trước, đo sau" (Chốt chặn 1 · Phút 60–65):**
   - Lệnh `lab10.eval` và `lab10.grade` từ chối chạy nếu chưa ký tiêu chí.
   - `lab10.check_submission` đối chiếu thời điểm lần chạy đầu tiên trong `runs/journal.jsonl` với thời điểm ký (`acceptance_criteria.lock`) và commit `'Sign acceptance criteria'`. Do đó **Khối 1 phải xong và ký xong trước** thì mọi người mới bước sang Khối 2 (đo `base`).
2. **Ràng buộc 2 — Quy tắc đóng băng mốc `prepared` (Chốt chặn 2 · Phút 105–115):**
   - Lệnh `lab10.checkpoint` chụp lại `lab10/guards.py` và `config/operating_gates.json` thành bản vòng 1 (`lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`).
   - Toàn bộ phần code vòng 1 và cấu hình `business`/`operations`/`legal` vòng 1 phải gom xong trước phút 105 để chốt `v1` trước khi nghỉ và nhận thẻ sự cố ở phút 125.
3. **Ràng buộc 3 — Chạy lệnh chính thức trên 1 máy (tránh mất log `runs/journal.jsonl`):**
   - Thư mục `/runs/` nằm trong `.gitignore` (không được đẩy lên Git bằng thao tác bình thường; chỉ được lệnh `--collect` gom vào `submission/runs/`).
   - Vì vậy, **1 máy chính (Người 1 · Trưởng nhóm)** nên phụ trách chạy toàn bộ các lệnh ghi nhận kết quả chính thức (`criteria sign`, `eval`, `checkpoint`, `grade`, `check_submission --collect`).
   - Các thành viên khác vẫn có thể tự mở code, đọc `data/world.json`, chạy `trace` hoặc `unittest` trên máy mình để kiểm tra, nhưng phần ghi vào các file dùng chung nên phối hợp nhịp nhàng để tránh **Git merge conflict**.

### Cách chống Git conflict khi 4 người làm song song
- **Code & JSON tách rạch ròi theo người:**
  - `lab10/guards.py` → chỉ **Người 1** sửa.
  - `lab10/monitors.py` → chỉ **Người 2** sửa.
  - `config/acceptance_criteria.json` & mục `business` của `config/operating_gates.json` → **Người 3** chuẩn bị giá trị.
  - Mục `operations` và `legal` của `config/operating_gates.json`, `submission/submission.json` → **Người 4** chuẩn bị giá trị.
- **3 Phiếu Markdown (`templates/form-a-criteria.md`, `form-b-evaluation-gates.md`, `form-c-incident.md`):**
  - Vì 1 phiếu có nhiều người cùng điền ở các mục khác nhau, nhóm nên chọn **1 trong 2 cách**:
    - *Cách khuyến nghị (an toàn nhất):* Mỗi người gõ câu trả lời phần mình vào Google Docs / Notion / nhắn nhóm (ghi rõ mã câu như `Câu 1.3`, `Mục B4`, `Mục C8`...), rồi **1 người giữ repo chính (hoặc 1 người phụ trách từng phiếu)** dán vào file `.md` và commit.
    - *Cách dùng Git trực tiếp:* Mỗi người pull mới nhất trước khi sửa, chỉ sửa đúng ô của mình, và commit tuần tự theo từng khối.

---

## 2. Tổng quan các file ĐƯỢC PHÉP sửa & Luật khóa file

> **Cảnh báo:** Lệnh `lab10.grade` kiểm tra `integrity` đối chiếu hash trong `lab10/MANIFEST.json`. Tuyệt đối **không sửa** agent, tools, data, tests hay các file bị khóa.

| File được phép sửa | Phụ trách chính | Vai trò |
|---|---|---|
| [`TEAM.md`](TEAM.md) | Trưởng nhóm + Cả 4 người | Bảng thành viên + mỗi người viết mục `## HoVaTen-MSSV` |
| [`templates/form-a-criteria.md`](templates/form-a-criteria.md) | Người 3 chủ trì + Cả bàn | Trả lời câu 1.1–1.6, A5 |
| [`templates/form-b-evaluation-gates.md`](templates/form-b-evaluation-gates.md) | Cả bàn (theo từng mục B0–B8) | Trả lời câu 2.1–2.10, Quyết định v1 |
| [`templates/form-c-incident.md`](templates/form-c-incident.md) | Cả bàn (theo từng mục C0–C12) | Ghi `Thẻ đã bốc:`, câu 3.0–3.7, Quyết định v2 + 3 dòng bắt buộc |
| [`config/acceptance_criteria.json`](config/acceptance_criteria.json) | Người 3 | Điền ngưỡng, **ký 1 lần ở phút 60–65**, sau đó **không chạm lại** |
| [`lab10/guards.py`](lab10/guards.py) | Người 1 | Viết `pre_guard(ctx)` và `write_gate(ctx, action)` (Vòng 1 & Vòng 2) |
| [`config/operating_gates.json`](config/operating_gates.json) | Người 3 (`business`) & Người 4 (`operations`, `legal`) | Điền con số vận hành, hạn mức, tên PIC, điều kiện dừng, ràng buộc pháp lý |
| [`lab10/monitors.py`](lab10/monitors.py) | Người 2 | Thêm ít nhất 1 hàm monitor mới vào dict `MONITORS` ở Vòng 2 |
| [`submission/submission.json`](submission/submission.json) | Người 4 | Điền thông tin gom bài nộp cuối buổi |

**Các file tự sinh KHÔNG ĐƯỢC SỬA sau khi tạo:**
- `config/acceptance_criteria.lock` (do lệnh `criteria sign` tạo)
- `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock` (do lệnh `checkpoint` tạo)

---

## 3. Phân công chi tiết cho 4 thành viên

### 👤 Người 1 — Kỹ sư cổng 1 (Trưởng nhóm · Git, Cổng `guards.py`, Chạy lệnh chính)
- **File chính:** [`lab10/guards.py`](lab10/guards.py), quản lý Git & điều phối máy chạy lệnh chính.
- **Phút 0–15 (Cài đặt):**
  - Tạo repo từ template theo đúng tên `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1` (Private), mời tài khoản team chấm (quyền Read trở lên).
  - Gắn `upstream`, cấu hình `git config user.name` / `user.email`, chạy `python -m unittest discover -s tests` (xác nhận `Ran 13 tests ... OK`).
- **Khối 1 (Phút 15–65):**
  - Soát kỹ thuật cho `config/acceptance_criteria.json` cùng Người 3.
  - Phút 60–65: Chạy `python -m lab10.criteria sign`, commit & push ngay lập tức theo đúng lệnh máy in ra; gửi mã commit cho Phiếu A mục **A5**.
- **Khối 2 (Phút 65–115):**
  - **Câu 2.1 (Phiếu B · B0, B1):** Chạy `eval --suite base --stage base` và `gate`; đọc khối "kinh doanh và vận hành" & "theo kho và hãng"; viết lập luận tự chặn vs. người duyệt.
  - **Câu 2.5 (Phiếu B · B6):** Cùng cả bàn đóng góp **lăng kính Kỹ thuật** trong Pre-mortem.
  - **Câu 2.6 (Phiếu B · B7.1):** Code 2–3 cổng phòng ngừa (`pre_guard`, `write_gate`) trong `lab10/guards.py` (dùng `lab10/helpers.py`, trả `Verdict.allow/deny/escalate/modify`), chạy thử `eval --suite base --stage after` và `unittest` đảm bảo không làm hỏng 22 ticket của bộ nền.
  - **Câu 2.7 (Phiếu B · B7.2):** Viết 2 bước cụ thể tránh rò rỉ dữ liệu (gắn với bộ nền, gói sự cố, bài kiểm tra ẩn).
  - Phút 105–115: Chạy `lab10.checkpoint`, `eval --suite base --stage prepared`, `lab10.gate`, sau khi điền **B8** thì commit & push.
- **Khối 3 (Phút 125–200):**
  - **Câu 3.0 (Phiếu C · C0, C1):** Pull thẻ từ `upstream`, chạy ngay `python -m lab10.grade --incident Sx` (khi chưa sửa gì), ghi mã `prepared` vào C0 và phân tích cổng vòng 1 đã đỡ được gì vào C1.
  - **Câu 3.5 (Phiếu C · C7):** Sửa code `lab10/guards.py` cho nguyên nhân kỹ thuật của thẻ `Sx`; chạy lại `eval --suite Sx --stage after`, `eval --suite base --stage after`, và `grade --incident Sx`.
  - Cuối buổi: Chạy `python -m lab10.check_submission --collect` tới khi báo `ĐỦ THÀNH PHẦN` và push bài cuối buổi.

---

### 👤 Người 2 — Kỹ sư cổng 2 (Phân tích Trace, Behavioral Test & `monitors.py`)
- **File chính:** [`lab10/monitors.py`](lab10/monitors.py), dò trace và kiểm thử hành vi.
- **Phút 0–15 (Chuẩn bị):**
  - Đọc sẵn `lab10/helpers.py`, `lab10/guards.py`, `lab10/monitors.py` và Phụ lục C của [`docs/guide.md`](docs/guide.md).
- **Khối 1 (Phút 15–65):**
  - **Câu 1.3 (Phiếu A · A2 cột Offline):** Chọn 1 bước của agent và thiết kế 1 offline metric (Thước đo → Dữ liệu → Cách tính).
  - **Câu 1.5 (Phiếu A · A3):** Tính/đọc hiểu khoảng tin cậy 95% (số minh họa) và viết giải thích cùng bàn.
- **Khối 2 (Phút 65–115):**
  - **Câu 2.2 (Phiếu B · B2):** Chạy `python -m lab10.trace --suite base --ticket T-002 --seed 55`, điền bảng soát lỗi cho `T-002@55`.
  - **Câu 2.5 (Phiếu B · B6):** Cùng cả bàn thảo luận Pre-mortem (bổ sung góc nhìn edge-case/trace).
  - **Câu 2.8 (Phiếu B · B7.3):** Phối hợp với Người 3 hoặc Người 4 (người không viết code) viết 1 câu tính chất (behavioral test) + tạo 2 "ticket hiểm" chạy bằng `--adhoc` để kiểm thử và giữ lại đi phản biện nhóm khác lúc Demo.
- **Khối 3 (Phút 125–200):**
  - **Câu 3.1 (Phiếu C · C2):** Chạy `lab10.trace --suite Sx --ticket <ID> --seed 11` dò ≥ 2 ticket hỏng theo 2 kiểu khác nhau (có ≥ 1 lỗi chìm); điền bảng soát lỗi và mô tả tác hại ở mốc base.
  - **Câu 3.4 (Phiếu C · C6):** Chủ trì vẽ **Fault tree trước khi sửa** (đỉnh là tác hại, ≥ 2 nhánh ở ≥ 2 tầng khác nhau, mỗi lá gắn bằng chứng `ticket@seed` / trường dữ liệu / dòng report).
  - **Câu 3.6 (Phiếu C · C8):** Viết ít nhất 1 hàm monitor mới phía trên dict `MONITORS` trong `lab10/monitors.py` và đăng ký vào `MONITORS` (bắt được sự cố, "sáng đèn" giữa `base` và `Sx`); điền 3 ô Thước đo → Dữ liệu → Cách tính vào **C8**.
  - **Câu 3.7 (Phiếu C · C9):** Cập nhật **Fault tree sau khi sửa** (chỉ rõ cổng nằm ở nhánh nào, tầng nào, nhánh nào còn hở).

---

### 👤 Người 3 — Sản phẩm và kinh doanh (Tiêu chí, Chi phí/ROI, Cổng `business` & Quyết định v1/v2)
- **File chính:** [`config/acceptance_criteria.json`](config/acceptance_criteria.json), mục `business` trong [`config/operating_gates.json`](config/operating_gates.json), chủ trì [`templates/form-a-criteria.md`](templates/form-a-criteria.md).
- **Phút 0–15 (Chuẩn bị):**
  - Mở `data/world.json` (xem `ops_facts`, `ops_limits`, `policies`), `config/acceptance_criteria.example.json`, eval card và PRD v1.1 từ Lab 9.
- **Khối 1 (Phút 15–65):**
  - **Câu 1.1 (Phiếu A · A1):** Viết mục tiêu cấp hệ thống của trợ lý (khác "model trả lời đúng", bám PRD v1.1 §3).
  - **Câu 1.6 (Phiếu A · A4 & `acceptance_criteria.json`):** Viết câu tiêu chí "Nếu … thì chúng tôi sẽ …", trả lời 4 câu soát, viết 2 câu ranh giới đầu ra (không thêm trường JSON), và điền toàn bộ giá trị vào `config/acceptance_criteria.json` (`team`, `signed_by`, `required`, `nice_to_have`, `business_ops`, `stop_condition`, `decision_rule`).
  - **A5:** Ghi giờ ký và mã commit ký tiêu chí vào Phiếu A.
- **Khối 2 (Phút 65–115):**
  - **Câu 2.3 (Phiếu B · B3):** Điền bản đồ dữ liệu (trường then chốt, nguồn sự thật vs. bản sao, nơi thực tế làm lệch) và viết 1 ví dụ drift cụ thể trong 3 tháng tới.
  - **Câu 2.5 (Phiếu B · B6):** Đóng góp **lăng kính Kinh doanh** trong Pre-mortem.
  - **Câu 2.9 (Phiếu B · B7.4):** Điền mục `business` trong `config/operating_gates.json` (`daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`), kèm 1 câu lý do cho mỗi số từ `data/world.json`.
  - **Chốt v1 (Phiếu B · B8):** Dựa vào report mốc `prepared`, cùng cả bàn chốt và viết **Quyết định v1** (một trong 4 quyết định, 3 bằng chứng có mã lần chạy, dòng `decision_rule`, kho/hãng xấu nhất, ngày quyết định lại).
- **Khối 3 (Phút 125–200):**
  - **Câu 3.2 (Phiếu C · C5):** Viết 1 specification mà nếu bị vi phạm sẽ gây ra tác hại trên thẻ (kiểm được bằng code hoặc 1 con số trong report).
  - **Câu 3.5 (Phiếu C · C7):** Điều chỉnh mục `business` trong `config/operating_gates.json` (ví dụ `pilot_scope`, trần tiền, ngân sách) nếu thẻ liên quan đến chi phí/phạm vi.
  - **Chốt v2 (Phiếu C · C12):** Tổng hợp số liệu 3 mốc `base · prepared · after`, chốt cùng bàn và viết **Quyết định v2**, mục "Chỉ ở v2", và **3 dòng bắt buộc** (`environment_assumption`, `reduce_or_prevent`, `measure_in_pilot`).

---

### 👤 Người 4 — Vận hành và pháp lý (HAZOP, Checklist, Runbook, `operations`/`legal` & Gom bài)
- **File chính:** Mục `operations` & `legal` trong [`config/operating_gates.json`](config/operating_gates.json), [`submission/submission.json`](submission/submission.json), bảng thành viên [`TEAM.md`](TEAM.md).
- **Phút 0–15 (Chuẩn bị):**
  - Điền thông tin chung và bảng thành viên trong `TEAM.md`; đọc `data/world.json` → `staff` và cấu trúc `config/operating_gates.json`.
- **Khối 1 (Phút 15–65):**
  - **Câu 1.2 (Phiếu A · A1):** Viết mục tiêu nhìn từ chị Oanh (kế toán đối soát) và chị Hạnh (trưởng ca CSKH) dựa vào PRD v1.1 §2, §6 và `data/world.json` → `staff`.
  - **Câu 1.4 (Phiếu A · A2 cột Telemetry production):** Thiết kế telemetry production (Thước đo → Dữ liệu → Cách tính → Khung thời gian → Ngưỡng báo động, lưu ý production không có nhãn).
- **Khối 2 (Phút 65–115):**
  - **Câu 2.4 (Phiếu B · B4, B5):** Viết **HAZOP mở rộng vòng 1** (≥ 3 dòng trên 1 tool ghi + ≥ 2 dòng ngoài kỹ thuật) và điền **Checklist 9 nhóm việc go-live lần 1** (mỗi dòng có trạng thái, bằng chứng, và **PIC có tên cụ thể**).
  - **Câu 2.5 (Phiếu B · B6):** Đóng góp **lăng kính Con người/Vận hành & Pháp lý** trong Pre-mortem.
  - **Câu 2.10 (Phiếu B · B7.5, B7.6):** Điền mục `operations` (`pic`, `approver_id`, `reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`, `stop_conditions`, `alert_channel`) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause`) trong `config/operating_gates.json`; viết **Runbook phần 1–3** (có thời hạn dừng từ tín hiệu đỏ tới khi dừng xong) và mục **Giờ cao điểm** khớp đúng các con số đã điền.
- **Khối 3 (Phút 125–200):**
  - **Câu 3.1 (Phiếu C · C3, C4):** Ghi số thẻ vào `Thẻ đã bốc:` ở đầu Phiếu C; hoàn thành **mục C3 (phần riêng theo đúng số thẻ đã bốc)** và **mục C4 (HAZOP của thẻ ≥ 3 dòng)**.
  - **Câu 3.3 (Phiếu C · C5):** Nêu 1 giả định về môi trường mà người thiết kế ngầm tin nhưng dễ sai ngoài thực tế.
  - **Câu 3.5 (Phiếu C · C7):** Điều chỉnh mục `operations`/`legal` trong `config/operating_gates.json` (`reviewers_on_shift`, `review_sampling_pct`, `decision_note`, `legal.*`) nếu sự cố thuộc vận hành/con người/pháp lý.
  - **Câu 3.7 (Phiếu C · C10, C11):** Thêm ≥ 1 dòng Risk register (C10), cập nhật Checklist 9 nhóm việc, viết **Runbook phần 4–5** (C11).
  - **Gom bài nộp (Phút 185–200):** Điền đầy đủ [`submission/submission.json`](submission/submission.json) (`team`, `members` khớp `TEAM.md`, `incident`, `decision_v1`, `decision_v2`, `three_lines` chép từ C12) để Người 1 chạy `--collect`.

---

## 4. Lịch phối hợp song song & 3 Chốt chặn đồng bộ (Timeline 240 phút)

| Mốc giờ | Người 1 (KS Cổng 1) | Người 2 (KS Cổng 2) | Người 3 (SP & KD) | Người 4 (VH & PL) |
|---|---|---|---|---|
| **0–15'** | Tạo repo, gắn `upstream`, chạy 13 tests | Đọc `helpers.py`, `guards.py`, `guide.md` | Đọc `world.json`, PRD, example criteria | Điền bảng thành viên trong `TEAM.md` |
| **15–60'** | Soát ngưỡng JSON cùng Người 3 | Làm **Câu 1.3** (A2) & **1.5** (A3) | Làm **Câu 1.1** (A1), **1.6** (A4) & `acceptance_criteria.json` | Làm **Câu 1.2** (A1) & **1.4** (A2) |
| **🛑 CHỐT 1 (60–65')** | **Chạy `criteria sign`, commit & push ngay** | Soát lại Phiếu A | Ghi giờ ký & hash vào **A5** | Soát lại Phiếu A |
| **65–75'** *(2A song song)* | Chạy `eval base`, làm **Câu 2.1** (B0, B1) | Trace `T-002@55`, làm **Câu 2.2** (B2) | Làm Bản đồ dữ liệu **Câu 2.3** (B3) | Làm HAZOP + Checklist **Câu 2.4** (B4, B5) |
| **75–85'** *(2A ghép bàn)* | **Cả 4 người cùng họp nhanh 10 phút** làm **Pre-mortem 4 lăng kính — Câu 2.5 (B6)** và chọn 2–3 lý do làm cổng | | | |
| **85–105'** *(2B song song)* | Code `guards.py` (**Câu 2.6, 2.7** · B7.1, B7.2) + test `after` | Viết tính chất + 2 ticket `--adhoc` (**Câu 2.8** · B7.3) | Điền `business` trong `operating_gates.json` (**Câu 2.9** · B7.4) | Điền `operations`/`legal` + Runbook 1–3 & Giờ cao điểm (**Câu 2.10** · B7.5, B7.6) |
| **🛑 CHỐT 2 (105–115')** | **Chạy `checkpoint`, `eval prepared`, `gate`** | Soát test & kết quả | **Cả bàn chốt & viết Quyết định v1 (B8)** | Soát Phiếu B, commit & push |
| **115–125'** | *Nghỉ giải lao* | | | |
| **125–135'** *(Nhận thẻ)* | Pull thẻ từ `upstream`, chạy `grade --incident Sx` (**Câu 3.0** · C0, C1) | Đọc thẻ `incidents/Sx/card.md` | Đọc thẻ `incidents/Sx/card.md` | Ghi `Thẻ đã bốc:` vào đầu Phiếu C & `TEAM.md` |
| **135–155'** *(Phân tích)* | Hỗ trợ phân tích nguyên nhân kỹ thuật | Trace ≥ 2 ticket hỏng (**Câu 3.1** · C2) & vẽ Fault tree trước (**Câu 3.4** · C6) | Viết Specification (**Câu 3.2** · C5) | Làm phần riêng **C3**, HAZOP thẻ (**C4**), Giả định (**Câu 3.3** · C5) |
| **155–185'** *(Sửa & đo)* | Sửa `guards.py`, chạy `eval Sx`, `eval base`, `grade Sx` (**Câu 3.5** · C7) | Code `monitors.py` (**Câu 3.6** · C8) & Fault tree sau (**Câu 3.7** · C9) | Sửa `business` trong `operating_gates.json` (**Câu 3.5** · C7) | Sửa `operations`/`legal`, viết Risk register (**C10**) & Runbook 4–5 (**C11**) |
| **🛑 CHỐT 3 (185–200')** | Chạy `check_submission --collect` tới khi `ĐỦ THÀNH PHẦN` | Viết mục cá nhân `TEAM.md` | **Cả bàn chốt & viết Quyết định v2 + 3 dòng (C12)** | Điền `submission/submission.json` & rà đủ mục phiếu |
| **200–230'** *(Demo)* | Trình bày 3 mốc `base · prepared · after` | Mang 2 ticket `--adhoc` đi phản biện bàn ghép cặp | Giải thích số liệu kinh doanh & quyết định v2 | Giải thích vận hành, con người & runbook |
| **230–240'** *(Nộp bài)* | Nếu demo có đổi thử số → trả về v2, chạy lại `grade` + `--collect`, **commit & push** | Viết mục cá nhân + Exit ticket `TEAM.md` & **tự nộp link trên LMS** | Viết mục cá nhân + Exit ticket `TEAM.md` & **tự nộp link trên LMS** | Viết mục cá nhân + Exit ticket `TEAM.md` & **tự nộp link trên LMS** |

---

## 5. Tra cứu nhanh 7 lệnh & Các lưu ý bắt buộc

> Trên Windows, nếu `python3` không chạy được thì thay bằng `python`.

| # | Lệnh | Khi nào chạy |
|---|---|---|
| 1 | `python -m lab10.criteria sign` | Ký tiêu chí **1 lần duy nhất** (phút 60–65), xong phải commit & push ngay |
| 2 | `python -m lab10.eval --suite <base\|Sx> --stage <base\|prepared\|after> --note "..."` | Chạy đánh giá trên bộ `base` hoặc thẻ `Sx` |
| 3 | `python -m lab10.trace --suite <base\|Sx> --ticket <ID> --seed <11\|22\|33\|44\|55> [--stage after]` *(hoặc `--adhoc "..." --order O-.... --customer C-..`)* | Dò từng bước trợ lý xử lý 1 ticket |
| 4 | `python -m lab10.gate --run runs/<mã lần chạy>/report.json` | So kết quả lần chạy với tiêu chí đã ký |
| 5 | `python -m lab10.checkpoint` | Chốt cổng vòng 1 **1 lần duy nhất** (phút 105–115) |
| 6 | `python -m lab10.grade --incident Sx` | Tự kiểm tra sự cố trên 3 mốc `base · prepared · after` (từ phút 125) |
| 7 | `python -m lab10.check_submission --collect` | Gom file vào `submission/` và kiểm `ĐỦ THÀNH PHẦN` |

### 6 nguyên tắc sống còn khi chấm bài
1. **Ký xong mới đo, ký xong không sửa:** Không bao giờ sửa `config/acceptance_criteria.json` (kể cả thêm dấu cách) sau commit `'Sign acceptance criteria'`.
2. **Không sửa bản chụp vòng 1:** Không động vào `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`.
3. **Không hardcode theo ticket/câu chữ mẫu:** Bộ test ẩn có đơn khác, khách khác, cách diễn đạt khác, ngày khác.
4. **Không over-block / không làm hỏng ca đúng:** Chặn toàn bộ hoặc thu hẹp phạm vi về 0 sẽ làm rớt độ phủ, chi phí/ROI hoặc lỗi `regression`.
5. **Trả lại bản v2 sau khi Demo:** Nếu lúc demo có thử đổi số trong `config/operating_gates.json`, nhớ đổi lại bản v2 rồi chạy lại lệnh 6 (`grade`) và lệnh 7 (`check_submission --collect`) trước khi push cuối.
6. **Nộp bài đủ cả hai phía:** Đẩy code lên repo chung (`git add -u && git add submission templates TEAM.md && git commit -m "LAB 10: bài nộp" && git push -u origin main`), gửi link cho team chấm, và **từng thành viên (cả 4 người)** phải tự nộp link repo lên LMS trước deadline.

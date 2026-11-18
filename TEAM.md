# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `KhoHieu`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-KhoHieu-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Lê Thái Dương | 2A202603415 | Kỹ sư cổng | Có |
|   2 | Nguyễn Trung Duy | 2A202603387 | Kỹ sư cổng | |
|   3 | Phạm Quang Trường | 2A202603378 | Sản phẩm và kinh doanh | |
|   4 | Nguyễn Vũ Khanh | 2A202603427 | Vận hành và pháp lý | | 

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## LeThaiDuong-2A202603415

### Phần việc phụ trách

Kỹ sư cổng 1 (Trưởng nhóm): khởi tạo repo, cấu hình `upstream` và Git; chạy các lệnh `criteria sign`, `eval`, `gate`, `checkpoint`, `grade`, `check_submission --collect`; viết cổng phòng ngừa trong `lab10/guards.py`; phụ trách câu 2.1, 2.5 (lăng kính Kỹ thuật), 2.6, 2.7 trong `templates/form-b-evaluation-gates.md` (mục B0, B1, B7.1, B7.2) và phần sửa kỹ thuật ở Vòng 2.

### Đóng góp cụ thể

- Cài đặt repo, gắn `upstream`, cấu hình danh tính Git (`2A202603415`) và kiểm tra 13 unit tests đạt `OK`.
- Triển khai `pre_guard` (ghim chính sách theo `ctx.as_of`) và 3 cổng trong `write_gate` của `lab10/guards.py` (đối chiếu hoàn tiền theo tracking DB & chống hoàn trùng, chặn ghi lỗi hãng oan, lọc allowlist PII trước `notify_carrier`).
- Ký tiêu chí trước khi đo, chốt cổng vòng 1 (`lab10.checkpoint`) và hoàn thiện các mục B0, B1, B6 (Kỹ thuật), B7.1, B7.2 trong `templates/form-b-evaluation-gates.md`. *(Có sử dụng trợ lý AI hỗ trợ rà soát code và biên tập câu chữ trên phiếu.)*

### Bằng chứng

- Commits: `98f7906`, `b83fbc8` (`Sign acceptance criteria`, hash `5a509fea`), `da80ecc` (`LAB 10: chốt cổng vòng 1, quyết định v1`, checkpoint hash `20be4844`).
- Mã lần chạy: `R-base-before-20261118-153409-7e3962`, `R-base-after-20261118-153525-849a9a`, `R-base-prepared-20261118-153633-849a9a`.
- Phiếu: `templates/form-b-evaluation-gates.md` (mục B0, B1, B6, B7.1, B7.2).

### Exit ticket

- Điều học được: Cổng bảo vệ ở tầng hệ thống (`pre_guard`, `write_gate`) đối chiếu trực tiếp nguồn sự thật giúp chặn được lỗi LLM (`model_override`, `directive`, rò rỉ PII) mà không làm hỏng các ca hợp lệ.
- Điều còn chưa chắc: Hiệu quả thực tế của cổng vòng 1 trên các tình huống bất ngờ như quá tải giờ cao điểm hoặc thay đổi chính sách ngoài bộ 22 ticket nền (sẽ kiểm chứng ở Vòng 2 sau khi bốc thẻ sự cố).

## NguyenTrungDuy-2A202603387

### Phần việc phụ trách

Kỹ sư cổng 2: phụ trách câu 1.3, 1.5 trong `templates/form-a-criteria.md` (mục A2 cột Offline, A3); câu 2.2 (bảng soát lỗi `T-002@55`, mục B2) và câu 2.8 (behavioral test `--adhoc`, mục B7.3) trong `templates/form-b-evaluation-gates.md`; ở Vòng 2 phụ trách dò trace sự cố, thêm chỉ số theo dõi mới trong `lab10/monitors.py` và vẽ fault tree (Phiếu C mục C2, C6, C8, C9).

### Đóng góp cụ thể

- Thiết kế offline metric cho bước `file_carrier_fault` ở mục A2 và phân tích khoảng tin cậy 95% ở mục A3 (`templates/form-a-criteria.md`).
- Rà soát trace `T-002@55`, hoàn thành bảng soát lỗi 3 phần ở mục B2 và thiết kế 2 ticket `--adhoc` (`O-1002/C-02`, `O-1001/C-01`) kiểm tra tính chất bảo toàn quyền lợi DB và lọc PII ở mục B7.3 (`templates/form-b-evaluation-gates.md`). *(Có sử dụng trợ lý AI hỗ trợ kiểm tra trace và tổng hợp bảng.)*

### Bằng chứng

- Phiếu: `templates/form-a-criteria.md` (mục A2 cột Offline, A3), `templates/form-b-evaluation-gates.md` (mục B2, B7.3).
- Kiểm chứng qua `R-base-before-20261118-153409-7e3962` (`T-002@55`) và kết quả chạy `--adhoc` ở mốc `after` (commit `da80ecc`).

### Exit ticket

- Điều học được: So sánh khoảng tin cậy 95% và chỉ số `pass^k` giúp tránh kết luận vội vàng khi mẫu nhỏ; phân tích trace từng bước giúp tách lỗi hiển nhiên và lỗi chìm.
- Điều còn chưa chắc: Cần theo dõi thêm chỉ số nào trong `lab10/monitors.py` để "sáng đèn" sớm nhất cho loại sự cố nhóm sắp bốc ở Vòng 2.

## PhamQuangTruong-2A20260378

### Phần việc phụ trách

Sản phẩm và kinh doanh: phụ trách câu 1.1, 1.6 và điền ngưỡng vào `config/acceptance_criteria.json` (Phiếu A mục A1, A4, A5); câu 2.3 (bản đồ dữ liệu & drift, mục B3), câu 2.5 (lăng kính Kinh doanh, mục B6), câu 2.9 (`config/operating_gates.json` mục `business`, mục B7.4) và tổng hợp Quyết định v1 (mục B8) trong `templates/form-b-evaluation-gates.md`; ở Vòng 2 phụ trách câu 3.2, điều chỉnh `business` và viết Quyết định v2 (Phiếu C mục C5, C12).

### Đóng góp cụ thể

- Xác định mục tiêu cấp hệ thống, viết bộ câu tiêu chí "Nếu … thì chúng tôi sẽ …", ranh giới đầu ra và điền đủ ngưỡng `required`, `nice_to_have`, `business_ops`, `decision_rule` vào `config/acceptance_criteria.json` trước khi đo.
- Xây dựng bản đồ dữ liệu, kịch bản drift chính sách `REFUND-v4` ngày `2026-12-01` (mục B3), đặt ngưỡng `business` (`daily_refund_cap_vnd: 1500000`, `cost_budget_per_ticket_vnd: 1200`, `pilot_scope: all`, `roi_min: 0.3`) và chốt Quyết định `v1: Tiếp tục` ở mục B8. *(Có sử dụng trợ lý AI hỗ trợ đối chiếu số liệu từ `data/world.json`.)*

### Bằng chứng

- File: `config/acceptance_criteria.json` (commit ký `b83fbc8`, hash `5a509fea`), `config/operating_gates.json` mục `business`.
- Phiếu: `templates/form-a-criteria.md` (A1, A4, A5), `templates/form-b-evaluation-gates.md` (B3, B6 Kinh doanh, B7.4, B8).

### Exit ticket

- Điều học được: Phải chốt tiêu chí chấp nhận bằng con số và hành động đi kèm trước khi chạy đánh giá để tránh tự nới ngưỡng theo kết quả đẹp.
- Điều còn chưa chắc: Mức trần ngân sách ngày và phạm vi `pilot_scope: all` có còn giữ được `ROI >= 0.3` khi lượng ticket hoặc tỷ lệ kiểm mẫu tăng cao ở Vòng 2 hay không.

## NguyenVuKhanh-2A202603427

### Phần việc phụ trách

Vận hành và pháp lý: phụ trách câu 1.2, 1.4 trong `templates/form-a-criteria.md` (mục A1 góc nhìn kế toán/CSKH, A2 cột Telemetry production); câu 2.4 (HAZOP vòng 1 và Checklist 9 nhóm việc, mục B4, B5), câu 2.5 (lăng kính Con người/Vận hành & Pháp lý, mục B6), câu 2.10 (`config/operating_gates.json` mục `operations` & `legal`, Runbook 1–3, Giờ cao điểm, mục B7.5–B7.6) trong `templates/form-b-evaluation-gates.md`; ở Vòng 2 phụ trách mục C3, C4, C5 (giả định môi trường), C10, C11 và `submission/submission.json`.

### Đóng góp cụ thể

- Xác định yêu cầu đối soát kế toán (`NV-OANH`) và tải hàng chờ CSKH (`NV-HANH`), thiết kế telemetry production không cần nhãn ở mục A2.
- Hoàn thiện bảng HAZOP vòng 1 (cả 5 guideword kỹ thuật + 3 dòng ngoài kỹ thuật), Checklist 9 nhóm việc gắn PIC có tên (mục B5), điền `operations` & `legal` trong `config/operating_gates.json`, viết Runbook 1–3 và kịch bản Giờ cao điểm (mục B7.5–B7.6). *(Có sử dụng trợ lý AI hỗ trợ rà soát Runbook khớp số liệu config.)*

### Bằng chứng

- File: `config/operating_gates.json` mục `operations` và `legal` (commit `da80ecc`), `submission/submission.json`.
- Phiếu: `templates/form-a-criteria.md` (A1 câu 1.2, A2 Telemetry), `templates/form-b-evaluation-gates.md` (B4, B5, B6 Vận hành & Pháp lý, B7.5, B7.6).

### Exit ticket

- Điều học được: Rủi ro ở Gate 1 không chỉ nằm trong code mà còn ở năng lực hàng chờ người duyệt (6 ca/giờ/người), độ trễ batch đối soát và trách nhiệm pháp lý với bên thứ ba.
- Điều còn chưa chắc: Ngưỡng gọi thêm người ở Runbook Giờ cao điểm (1 → 2 người) đã đủ tránh `queue_stuck > 0` khi gặp sự cố đột biến hay chưa.


# Hướng dẫn trình bày portfolio — 03/11/2026

**Lưu ý:** Tất cả dữ liệu trên GitHub là giả lập. Bộ ZIP phỏng vấn riêng có dữ liệu mẫu quy mô khác, vì vậy số liệu giữa hai bộ **không giống nhau**. Không trộn số liệu.

## 1. Hotel Revenue Analysis

**Vấn đề:** Hiểu hiệu quả bán phòng theo tháng.

**KPI:** Occupancy = sold / available room nights; ADR = room revenue / sold room nights; RevPAR = room revenue / available room nights. Khi tính KPI cả năm, dùng tổng tử số chia tổng mẫu số, không lấy trung bình KPI tháng.

**Kiểm tra dữ liệu:** available > 0, 0 ≤ sold ≤ available, revenue ≥ 0. Tiếp theo nên kiểm tra tháng trùng/thiếu và nguồn doanh thu.

**Trình bày:** “Em dùng Python để chuẩn hóa KPI khách sạn, xác định tháng công suất cao/thấp và đưa ra giả thuyết cần kiểm chứng bằng dữ liệu kênh bán, giá và sự kiện.”

## 2. E-commerce Metrics

**Vấn đề:** GMV tăng do số đơn hay AOV? Khách mua lại thế nào?

**KPI:** GMV demo = tổng giá trị đơn completed; AOV = GMV / số đơn completed; repeat purchase = khách có ≥2 đơn completed / khách có ≥1 đơn completed. Đây không phải cohort retention.

**Kiểm tra dữ liệu:** order ID unique, status hợp lệ, doanh thu không âm. Cần bổ sung refund, voucher, traffic và chi phí nếu phân tích dữ liệu thật.

**Trình bày:** “Em dùng SQLite và SQL để lọc đơn hoàn tất, tổng hợp theo tháng/ngành hàng, phân tích số đơn và AOV; không suy diễn lợi nhuận khi thiếu chi phí.”

## 3. Python + Excel Automation

**Vấn đề:** CSV đầu vào lỗi làm báo cáo Excel sai.

**Quy trình:** CSV → schema validation → kiểm tra duplicate/date/revenue → Clean Data + Summary + Validation Errors → log.

**Trình bày:** “Em tách lỗi khỏi dữ liệu hợp lệ và dùng kiểm thử để giảm rủi ro báo cáo sai. Script chạy thủ công; chưa triển khai tự động theo lịch hoặc đo thời gian tiết kiệm thực tế.”

## Cách demo

```bash
pip install -r portfolio/requirements.txt
python portfolio/hotel-revenue-analysis/analyze.py
python portfolio/ecommerce-metrics/analyze.py
python portfolio/excel-automation/pipeline.py
python -m unittest discover -s portfolio/excel-automation -p 'test_*.py'
```

**Metric.vn:** tập trung SQL, GMV, AOV và giới hạn phân tích. **MH Solution:** tập trung yêu cầu kinh doanh, KPI, data quality, báo cáo và nghiệm thu.

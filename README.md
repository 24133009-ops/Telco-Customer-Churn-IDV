# 📡 ĐỒ ÁN MÔN HỌC: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN (DATA VISUALIZATION)
## ĐỀ TÀI SỐ 5: DỰ ĐOÁN VÀ TRỰC QUAN HÓA TỶ LỆ RỜI BỎ CỦA KHÁCH HÀNG (CUSTOMER CHURN) TRONG NGÀNH VIỄN THÔNG

> **Bộ môn:** Kỹ thuật Dữ liệu & Trí tuệ Nhân tạo - Khoa Công nghệ Thông tin  
> **Trường:** Đại học Công nghệ Kỹ thuật TP. Hồ Chí Minh (HCM-UTE)  
> **Nhóm thực hiện:** Nhóm 22  
> **Thành viên:**  
> - **Trương Quốc Duy** - MSSV: 24133009 (Trưởng nhóm)  
> - **Đỗ Trọng Khôi** - MSSV: 20133056 (Thành viên)  
> - **Bùi Đức Huy** - MSSV: 24133021 (Thành viên)  
## 📊 CÁC TÍNH NĂNG CHÍNH CỦA DASHBOARD (STREAMLIT + PLOTLY)
1. **Bộ Lọc Đa Chiều (Sidebar Filters):**
   - Lọc theo Bang viễn thông (State): Đầy đủ **50 bang Hoa Kỳ** hiển thị tên hoàn chỉnh kèm mã bang (ví dụ: *California (CA)*, *Washington (WA)*...).
   - Lọc theo Loại hợp đồng (Month-to-month, One year, Two year).
   - Lọc theo Công nghệ Internet (Fiber optic, DSL, No).
   - Lọc theo Phương thức thanh toán (Electronic check, Credit card, Bank transfer...).
   - Lọc theo Đối tượng người cao tuổi (Senior Citizen).
   - Thanh trượt Thâm niên (Tenure: 0 - 72 tháng) và Cước phí (Monthly Charges: 18$ - 120$).
2. **Khối Thẻ KPI Thời Gian Thực:** Thiết kế chuẩn Enterprise BI Dashboard (Dark/Light adaptive) cập nhật tự động Tổng khách hàng, Tỷ lệ rời mạng Churn %, ARPU, Doanh thu tích lũy và Điểm hài lòng CSKH.
3. **Tab 1 - Tổng Quan & Phân Phối:** Donut Chart, Contract Bar Chart, Histogram phân phối thâm niên, Boxplot ngoại lai cước phí.
4. **Tab 2 - Bản Đồ Địa Lý & Vùng Miền (50 Bang):** Bản đồ nhiệt không gian US Choropleth Map (phủ khắp 50 bang) và Bubble Map theo tọa độ, xếp hạng Top 10 bang nguy cơ cao và Top 10 bang trung thành.
5. **Tab 3 - Dịch Vụ & Tương Quan Đa Chiều:** Scatter plot Tenure vs Charges, Cây phân cấp Treemap, Ma trận tương quan Pearson Heatmap, Grouped bar biểu đồ dịch vụ GTGT.
6. **Tab 4 - Dự Báo AI & Trình Mô Phỏng:** Biểu đồ Feature Weights & Odds Ratio, Đường cong xu hướng Churn theo chu kỳ vòng đời, và **Trình mô phỏng What-If Simulator** cho phép nhập thông số khách hàng để dự báo ngay xác suất rời mạng và gợi ý giải pháp giữ chân kịp thời.
7. **Tab 5 - Bảng Dữ Liệu & Drill-down:** Bảng dữ liệu tương tác, tính năng chọn mã khách hàng hiển thị hồ sơ cá nhân 360 độ và nút xuất file CSV.
8. **Tab 6 - Kiến Trúc Data Pipeline (Chuẩn Data Engineer):** Sơ đồ Data Lineage từ 4 bảng nguồn RDBMS, kiểm định Data Quality (0 nulls, IQR Outliers) và các Calculated Fields.
---
*© 2026 Nhóm 22 - Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE).*

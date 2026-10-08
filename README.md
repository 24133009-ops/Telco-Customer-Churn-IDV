# 📡 ĐỒ ÁN MÔN HỌC: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN (DATA VISUALIZATION)
## ĐỀ TÀI SỐ 5: DỰ ĐOÁN VÀ TRỰC QUAN HÓA TỶ LỆ RỜI BỎ CỦA KHÁCH HÀNG (CUSTOMER CHURN) TRONG NGÀNH VIỄN THÔNG

> **Bộ môn:** Kỹ thuật Dữ liệu & Trí tuệ Nhân tạo - Khoa Công nghệ Thông tin  
> **Trường:** Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh (HCMUTE)  
> **Nhóm thực hiện:** Nhóm 22  
> **Thành viên:**  
> - **Trương Quốc Duy** - MSSV: 24133009 (Trưởng nhóm)  
> - **Đỗ Trọng Khôi** - MSSV: 20133056 (Thành viên)  
> - **Bùi Đức Huy** - MSSV: 24133021 (Thành viên)  

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```text
c:\Tương Tác dữ liệu trực quan\
├── data\
│   ├── raw\                                # 4 bảng dữ liệu quan hệ thô
│   │   ├── telco_demographics.csv          # Nhân khẩu học & Tọa độ địa lý (7,043 dòng)
│   │   ├── telco_services.csv              # Các dịch vụ viễn thông đã đăng ký (7,043 dòng)
│   │   ├── telco_contracts.csv             # Kỳ hạn hợp đồng & Cước phí (7,043 dòng)
│   │   └── telco_churn_status.csv          # Nhãn Churn, Lý do hủy & Điểm CSKH (7,043 dòng)
│   └── processed\                          # Dữ liệu sạch sau Pipeline ETL
│       └── telco_churn_clean.csv           # Tập dữ liệu đã join & feature engineering (34 cột)
├── src\
│   ├── data_pipeline.py                    # ETL Pipeline: Join 4 bảng, làm sạch, IQR, calculated fields
│   ├── eda_analysis.py                     # Sinh 10 biểu đồ tĩnh Matplotlib/Seaborn chuẩn báo cáo
│   ├── model_training.py                   # Huấn luyện Logistic Regression, ROC-AUC, Odds Ratio, export model
│   └── app.py                              # Streamlit Interactive Dashboard (Bộ lọc, drill-down, 10+ biểu đồ, simulator)
├── models\
│   └── telco_logistic_model.pkl            # Mô hình máy học Scikit-Learn đã đóng gói
├── reports\
│   ├── figures\                            # 14 hình ảnh biểu đồ tĩnh và biểu đồ mô hình chuẩn IEEE
│   │   ├── eda_1_churn_distribution.png
│   │   ├── eda_2_tenure_distribution.png
│   │   ├── eda_3_monthly_charges_distribution.png
│   │   ├── eda_4_contract_type_churn.png
│   │   ├── eda_5_internet_service_churn.png
│   │   ├── eda_6_correlation_heatmap.png
│   │   ├── eda_7_boxplot_outliers.png
│   │   ├── eda_8_value_added_services.png
│   │   ├── eda_9_payment_methods.png
│   │   ├── eda_10_tenure_cohort_trend.png
│   │   ├── model_1_confusion_matrix.png
│   │   ├── model_2_roc_curve.png
│   │   ├── model_3_feature_importance.png
│   │   └── model_4_churn_probability_dist.png
│   ├── generate_report_doc.py              # Script tự động tạo Báo cáo Word .docx chuẩn IEEE
│   ├── BAO_CAO_DO_AN_NHOM_22.docx          # File Word Báo Cáo Đồ Án chính thức (chuẩn học thuật IEEE)
│   └── BAO_CAO_DO_AN_NHOM_22.md            # File Markdown Báo Cáo Đồ Án đầy đủ 7 phần
├── requirements.txt                        # Danh mục thư viện Python phụ thuộc
└── README.md                               # Hướng dẫn tổng quan và hướng dẫn chạy hệ thống
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & CHẠY ỨNG DỤNG

### 1. Cài đặt các thư viện cần thiết
Mở terminal (PowerShell hoặc Command Prompt) tại thư mục đồ án:
```bash
pip install -r requirements.txt
```

### 2. Chạy Pipeline tiền xử lý và kết nối nhiều bảng
```bash
py src/data_pipeline.py
```
*Kết quả:* Tự động tải/tạo dữ liệu, phân rã 4 bảng quan hệ, thực hiện Inner Join, làm sạch missing values và lưu tập dữ liệu `telco_churn_clean.csv`.

### 3. Sinh các biểu đồ tĩnh phục vụ phân tích EDA
```bash
py src/eda_analysis.py
```
*Kết quả:* Xuất 10 hình ảnh biểu đồ chuẩn khoa học vào thư mục `reports/figures/`.

### 4. Huấn luyện mô hình Hồi quy Logistic
```bash
py src/model_training.py
```
*Kết quả:* Huấn luyện mô hình, in báo cáo đánh giá (Accuracy 80.77%, ROC-AUC 0.8421), xuất ma trận nhầm lẫn, đường cong ROC và lưu model vào `models/telco_logistic_model.pkl`.

### 5. Khởi chạy Dashboard Tương Tác Streamlit
```bash
streamlit run src/app.py
```
*Trình duyệt web sẽ tự động mở tại:* `http://localhost:8501`

### 6. Biên dịch lại file Báo cáo Word (.docx) chuẩn IEEE
```bash
py reports/generate_report_doc.py
```
*Kết quả:* Tạo file `reports/BAO_CAO_DO_AN_NHOM_22.docx` tích hợp đầy đủ bảng biểu, hình ảnh minh họa và trích dẫn IEEE.

---

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

## 📑 BÁO CÁO KHOA HỌC  (7 MỤC BẮT BUỘC)

Báo cáo được trình bày chi tiết trong 2 định dạng:
- **Tài liệu Word chính thức:** [`reports/BAO_CAO_DO_AN_NHOM_22.docx`](reports/BAO_CAO_DO_AN_NHOM_22.docx)
- **Tài liệu Markdown:** [`reports/BAO_CAO_DO_AN_NHOM_22.md`](reports/BAO_CAO_DO_AN_NHOM_22.md)


## 🎥 ĐƯỜNG DẪN LIÊN KẾT & VIDEO DEMO
- **Video Demo chính thức:** 
- **Google Drive Backup:** 
- **GitHub Repository:** 

---
*© 2026 Nhóm 22 - Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE).*

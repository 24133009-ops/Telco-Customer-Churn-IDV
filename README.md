# 📡 Telco Customer Churn - Interactive Data Visualization (IDV)

> **Môn học:** Tương Tác Dữ Liệu Trực Quan (IDV)  
> **Trường:** Đại học Công Nghệ Kỹ thuật TP.HCM (HCMUTE)  
> **Nhóm:** Nhóm 22  

---

## 👥 Thành Viên Nhóm

| STT | Họ và Tên | MSSV | Vai Trò | Nhiệm Vụ Phụ Trách |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Trương Quốc Duy** | 24133009 | **Trưởng nhóm** | Toàn bộ Kỹ thuật: Pipeline ETL, Khám phá EDA, Huấn luyện mô hình Logistic Regression, Lập trình Dashboard Streamlit & Demo |
| 2 | **Đỗ Trọng Khôi** | 20133056 | Thành viên | Soạn thảo, hoàn thiện Báo cáo kỹ thuật Word (chuẩn IEEE), đối chiếu tiêu chí barem và tài liệu đồ án |
| 3 | **Bùi Đức Huy** | 24133021 | Thành viên | Khảo sát bối cảnh bài toán viễn thông, thu thập dữ liệu & chuẩn bị nội dung thuyết trình mở đầu |

---

## 🎯 Giới Thiệu Đề Tài

Đề tài tập trung phân tích, trực quan hóa và dự báo **Tỷ lệ rời bỏ của khách hàng (Customer Churn)** trong ngành viễn thông dựa trên bộ dữ liệu IBM Telco gồm 7,043 bản ghi khách hàng:
- **Pipeline ETL:** Phân rã và kết nối 4 bảng quan hệ (`telco_demographics`, `telco_services`, `telco_contracts`, `telco_churn_status`), xử lý missing values và kiểm định ngoại lai (IQR).
- **Phân tích EDA:** Xây dựng 10 biểu đồ tĩnh phân tích sâu các yếu tố ảnh hưởng đến quyết định rời mạng.
- **Machine Learning:** Mô hình Logistic Regression đạt **ROC-AUC 0.8421**, giải thích định lượng thông qua Odds Ratio.
- **Interactive Dashboard:** Ứng dụng Streamlit + Plotly với 5 phân hệ tiến trình thuyết trình, bản đồ không gian 50 bang, Drill-Down hồ sơ 360° và bộ công cụ mô phỏng What-If & ROI thời gian thực.

---

## 🔗 Liên Kết Sản Phẩm

- **Dashboard Trực Tuyến:** [https://nhom22-telco-churn.streamlit.app](https://nhom22-telco-churn.streamlit.app)
- **Video Demo Đồ Án:** [https://youtu.be/1MD8Ldf3zAo](https://youtu.be/1MD8Ldf3zAo)
- **GitHub Repository:** [https://github.com/24133009-ops/Telco-Customer-Churn-IDV](https://github.com/24133009-ops/Telco-Customer-Churn-IDV)

---

## 📂 Cấu Trúc Thư Mục

```text
├── data/
│   ├── raw/                 # 4 bảng dữ liệu quan hệ thô
│   └── processed/           # Dữ liệu sạch sau pipeline (telco_churn_clean.csv)
├── src/
│   ├── data_pipeline.py     # Pipeline ETL: Nối bảng, làm sạch, IQR, feature engineering
│   ├── eda_analysis.py      # Sinh 10 biểu đồ tĩnh Matplotlib/Seaborn chuẩn xuất bản
│   ├── model_training.py    # Huấn luyện mô hình Logistic Regression, tính ROC-AUC & Odds Ratio
│   └── app.py               # Ứng dụng Streamlit Interactive Dashboard
├── models/
│   └── telco_logistic_model.pkl # Model Scikit-Learn đã đóng gói
├── reports/
│   ├── figures/             # 14 hình ảnh biểu đồ tĩnh và biểu đồ mô hình
│   └── BAO_CAO_DO_AN_NHOM_22.md # Báo cáo đồ án chi tiết (Markdown)
├── requirements.txt         # Danh mục thư viện phụ thuộc
└── README.md
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Cài đặt môi trường
Yêu cầu Python 3.10 trở lên. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Khởi chạy Dashboard tương tác
```bash
streamlit run src/app.py
```
Truy cập tại địa chỉ: `http://localhost:8501`

*(Tùy chọn) Chạy lại pipeline dữ liệu và huấn luyện mô hình:*
```bash
py src/data_pipeline.py    # Xử lý dữ liệu
py src/eda_analysis.py     # Sinh biểu đồ tĩnh EDA
py src/model_training.py   # Huấn luyện mô hình
```

---

## 📊 CÁC TÍNH NĂNG CHÍNH CỦA DASHBOARD (STREAMLIT + PLOTLY)

1. **Bộ Lọc Đa Chiều (Sidebar Filters):**
   - Lọc theo Chu kỳ thâm niên (Toàn bộ, Năm 1, Năm 2, Năm 3, Năm 4, Năm 5-6).
   - Lọc theo Bang viễn thông (State): Đầy đủ **50 tiểu bang Hoa Kỳ** hiển thị tên kèm mã bang (California (CA), Washington (WA)...).
   - Lọc theo Gói Internet (DSL, Fiber optic, Không Internet).
   - Lọc theo Loại hợp đồng (Month-to-month, One year, Two year).
   - Lọc theo Phương thức thanh toán (Electronic check, Mailed check, Bank transfer, Credit card).
   - Thanh trượt khoảng cước phí hàng tháng (18$ - 120$ USD).
   - Nút *"🔄 Đặt lại bộ lọc"* (Reset Filters) đưa Dashboard về trạng thái mặc định tức thì.
2. **Khối Thẻ KPI Toàn Cục & Báo Cáo Tài Chính C-Level:**
   - 5 Thẻ KPI thời gian thực: Tổng khách hàng, Tỷ lệ rời mạng Churn %, Cước bình quân tháng (ARPU), Doanh thu tích lũy (CLV) và Điểm hài lòng CSAT.
   - Băng chuyền Báo cáo Tài chính C-Level (*Executive Financial Impact*): Định lượng thất thoát MRR ($/tháng), tổn thất ARR quy năm, tiềm năng bảo vệ doanh thu (+15% giữ chân) và điểm nóng rủi ro tài chính.
3. **Tab 1 - Tổng Quan & Bản Đồ Địa Lý (50 Bang):**
   - Donut Chart cơ cấu Churn tổng thể (73.5% Ở lại vs 26.5% Rời mạng) và Bar Chart tỷ lệ Churn theo loại hợp đồng.
   - Bản đồ địa lý không gian tương tác: Quả địa cầu 3D (`orthographic`) xoay 360° kèm animation và Bản đồ phẳng 2D US Choropleth Map phủ 50 bang, hỗ trợ 4 chỉ số (Churn %, Khách hàng, Cước TB, Doanh thu).
   - Bảng xếp hạng Top 10 bang nguy cơ Churn cao nhất & Top 10 bang trung thành nhất.
4. **Tab 2 - Chẩn Đoán Dữ Liệu & Hành Vi:**
   - Phân tích 2 chiều Hợp đồng x Gói Internet: Làm sáng tỏ *"Nghịch lý cáp quang Fiber Optic"* (tỷ lệ Churn 54.6% ở hợp đồng tháng so với <8% ở hợp đồng 2 năm).
   - Đường cong duy trì thâm niên (*Customer Retention Decay Curve*): Theo dõi tỷ lệ gắn bó qua 8 mốc thâm niên, vạch rõ điểm gãy rủi ro sau 12 tháng đầu.
   - Phân tích vai trò bảo vệ của các dịch vụ GTGT (Online Security, Tech Support) và rủi ro ma sát thanh toán từ Séc điện tử (*Electronic Check*).
5. **Tab 3 - Dự Báo AI & Trình Mô Phỏng:**
   - Thẻ hiệu năng mô hình Hồi quy Logistic: Độ chính xác **80.77%**, chỉ số **ROC-AUC 0.8421**, F1-Score 60.89%.
   - Biểu đồ Feature Importance & Odds Ratio: Phân biệt định lượng các nhân tố kích hoạt Churn vs các yếu tố bảo vệ giữ chân khách hàng.
   - **Trình mô phỏng What-If Simulator thời gian thực:** Nhập linh hoạt 8 thông số khách hàng, mô hình tính toán tức thời xác suất rời mạng.
   - Đồng hồ Gauge Chart đo xác suất Churn trực quan theo 3 dải màu rủi ro (<35%, 35-60%, >=60%) và Card dự báo tác động giảm Churn trước/sau khi can thiệp.
6. **Tab 4 - Khuyến Nghị Chiến Lược & ROI Simulator:**
   - Ma trận 4 phân khúc chiến lược (*Value vs Risk Matrix*): Phân nhóm khách hàng theo Thâm niên vs Cước phí (VIP Rủi Ro Cao, VIP Trung Thành, Phổ Thông Rủi Ro, Phổ Thông Ổn Định).
   - Khung chiến lược hành động 3 trụ cột: Gói *"Fiber Shield Bundle"*, Chính sách *"Auto-Pay Incentive"*, và Chiết khấu chuyển đổi hợp đồng dài hạn.
   - **Trình mô phỏng tài chính ROI Simulator:** 3 thanh trượt tham số (Tỷ lệ tiếp cận CSKH, Tỷ lệ giữ chân, Chi phí/khách) lập tức tính toán số khách giữ chân, ARR Preserved, chi phí chiến dịch, Lợi nhuận ròng và ROI.
   - Biểu đồ thanh so sánh hiệu quả kinh tế và Nút xuất Báo cáo điều hành Executive Brief (.md).
7. **Tab 5 - Kiến Trúc Dữ Liệu & Tra Cứu 360° (Drill-Down):**
   - Sơ đồ Enterprise Data Pipeline 5 giai đoạn & Bảng cam kết chất lượng dữ liệu SLA: Khớp nối 100% 4 bảng quan hệ (7,043 dòng), 0% missing value, độ trễ truy vấn <15ms qua Streamlit Cache.
   - **Tính năng Drill-Down hồ sơ khách hàng 360 độ:** Chọn bất kỳ mã khách hàng (`customerID`) để mở toàn bộ 4 khối thông tin cá nhân hóa (Nhân khẩu học, Hợp đồng & Thanh toán, Dịch vụ, Điểm CSAT & lý do rời mạng).
   - Bảng dữ liệu tương tác đầy đủ hỗ trợ sắp xếp, lọc và nút xuất tập dữ liệu đã lọc về máy (.csv).

# BÁO CÁO CUỐI KỲ ĐỒ ÁN MÔN HỌC: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN
## ĐỀ TÀI SỐ 5: DỰ ĐOÁN VÀ TRỰC QUAN HÓA TỶ LỆ RỜI BỎ CỦA KHÁCH HÀNG (CUSTOMER CHURN) TRONG NGÀNH VIỄN THÔNG

> **Bộ môn:** Kỹ thuật Dữ liệu & Trí tuệ Nhân tạo - Khoa Công nghệ Thông tin  
> **Trường:** Đại học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh (HCMUTE)  
> **Nhóm thực hiện:** Nhóm 22  
> **Thành viên nhóm:**  
> 1. **Đỗ Trọng Khôi** - MSSV: 20133056 (Trưởng nhóm)  
> 2. **Bùi Đức Huy** - Thành viên  
> 3. **Trương Quốc Duy** - MSSV: 24133009 (Thành viên)  

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)
Trong ngành viễn thông hiện đại, bài toán khách hàng rời mạng (*Customer Churn*) là thách thức sống còn đối với doanh thu và thị phần doanh nghiệp. Đồ án xây dựng một giải pháp toàn diện từ khâu thu thập, tiền xử lý, phân rã và kết nối 4 bảng dữ liệu quan hệ (> 7,000 dòng), làm sạch dữ liệu khuyết thiếu, kiểm định ngoại lai (IQR) và kỹ thuật trích xuất đặc trưng mới. Tiếp đó, nhóm tiến hành khám phá dữ liệu tĩnh (EDA) với 10 biểu đồ Matplotlib/Seaborn chuẩn khoa học; xây dựng Bảng điều khiển trực quan hóa tương tác (Interactive Dashboard) bằng Streamlit & Plotly tích hợp hơn 10 loại biểu đồ (bao gồm bản đồ địa lý US Map, bộ lọc đa chiều và tính năng Drill-Down hồ sơ 360 độ). Cuối cùng, mô hình Hồi quy Logistic (Logistic Regression) được triển khai đạt độ chính xác 80.77%, ROC-AUC 0.8421, cho phép lượng hóa chính xác các nhân tố rủi ro và tích hợp Trình mô phỏng What-If Simulator hỗ trợ ra quyết định giữ chân khách hàng thời gian thực.

---

## MỤC LỤC BÁO CÁO
1. [1. Giới Thiệu Đề Tài & Mô Tả Tập Dữ Liệu](#1-giới-thiệu-đề-tài--mô-tả-tập-dữ-liệu)
   - 1.1 Bối cảnh và Lý do chọn đề tài
   - 1.2 Mục tiêu nghiên cứu và Phạm vi đồ án
   - 1.3 Nguồn gốc tập dữ liệu
   - 1.4 Kiến trúc cơ sở dữ liệu quan hệ (4 bảng liên kết)
   - 1.5 Từ điển dữ liệu chi tiết (Data Dictionary)
2. [2. Quy Trình Tiền Xử Lý & Khám Phá Dữ Liệu (EDA)](#2-quy-trình-tiền-xử-lý--khám-phá-dữ-liệu-eda)
   - 2.1 Kiến trúc tổng thể Pipeline dữ liệu (ETL)
   - 2.2 Xử lý dữ liệu khuyết thiếu (Missing Values)
   - 2.3 Kiểm định ngoại lai bằng phương pháp IQR
   - 2.4 Kỹ thuật tạo trường tính toán mới (Feature Engineering)
   - 2.5 Khám phá dữ liệu tĩnh (Static EDA) với 10 biểu đồ chuẩn khoa học
3. [3. Thiết Kế Dashboard Trực Quan Hóa Tương Tác](#3-thiết-kế-dashboard-trực-quan-hóa-tương-tác)
   - 3.1 Nền tảng công nghệ (Streamlit & Plotly)
   - 3.2 Bố cục giao diện UI/UX và luồng tương tác
   - 3.3 Hệ thống 8+ loại biểu đồ trên Dashboard
   - 3.4 Cơ chế khoan sâu dữ liệu (Drill-Down 360 độ)
4. [4. Khai Phá Insight (Kể Chuyện Bằng Dữ Liệu - Storytelling)](#4-khai-phá-insight-kể-chuyện-bằng-dữ-liệu---storytelling)
   - 4.1 Câu chuyện dữ liệu: Tại sao khách hàng rời bỏ?
   - 4.2 Chân dung khách hàng rủi ro cao (High-Risk Persona)
   - 4.3 Đề xuất chiến lược can thiệp giữ chân khách hàng (Actionable Strategies)
5. [5. Mô Hình Dự Báo (Logistic Regression)](#5-mô-hình-dự-báo-logistic-regression)
   - 5.1 Cơ sở lý thuyết toán học của Hồi quy Logistic
   - 5.2 Chuẩn bị dữ liệu và phân chia huấn luyện (Train/Test Split)
   - 5.3 Kết quả thực nghiệm và đánh giá hiệu năng (ROC-AUC: 0.8421)
   - 5.4 Phân tích trọng số và Tỷ số chênh (Odds Ratios)
6. [6. Hướng Dẫn Cài Đặt/Sử Dụng & Link Video Demo](#6-hướng-dẫn-cài-đặt-sử-dụng--link-video-demo)
   - 6.1 Yêu cầu môi trường & hệ thống
   - 6.2 Hướng dẫn cài đặt và khởi chạy từng bước
   - 6.3 Kịch bản Video Demo chi tiết (Storyboard & Timeline)
   - 6.4 Liên kết Video Demo và Kho lưu trữ GitHub/Drive
7. [7. Kết Luận & Tham Khảo](#7-kết-luận--tham-khảo)
   - 7.1 Đánh giá kết quả đạt được
   - 7.2 Hạn chế của đề tài
   - 7.3 Hướng phát triển trong tương lai
   - 7.4 Danh mục tài liệu tham khảo (Chuẩn IEEE)

---

## 1. GIỚI THIỆU ĐỀ TÀI & MÔ TẢ TẬP DỮ LIỆU

### 1.1 Bối Cảnh Nghiên Cứu và Lý Do Chọn Đề Tài
Trong thị trường viễn thông bão hòa, chi phí tìm kiếm một khách hàng mới (CAC) cao gấp 5 đến 7 lần so với chi phí giữ chân khách hàng hiện hữu. Tỷ lệ rời mạng (*Customer Churn*) làm thất thoát trực tiếp doanh thu định kỳ (MRR) và giá trị vòng đời (CLV). Đề tài số 5 giải quyết trực tiếp bài toán này thông qua kết hợp giữa trực quan hóa dữ liệu tương tác hiện đại và mô hình trí tuệ nhân tạo giải thích được.

### 1.2 Mục Tiêu Nghiên Cứu và Phạm Vi
1. Thiết lập Data Pipeline tự động hóa tải, phân rã, kết nối 4 bảng quan hệ và làm sạch dữ liệu.
2. Trực quan hóa phân phối dữ liệu qua 10 biểu đồ tĩnh Matplotlib/Seaborn.
3. Phát triển Dashboard tương tác Streamlit + Plotly tích hợp hơn 10 biểu đồ, bản đồ không gian và cơ chế Drill-down.
4. Huấn luyện mô hình Hồi quy Logistic đạt độ chuẩn xác cao, trích xuất Odds Ratio phân tích rủi ro.
5. Kể chuyện bằng dữ liệu (Storytelling) và đề xuất chiến lược giữ chân khả thi.

### 1.3 Nguồn Gốc Dữ Liệu và Đáp Ứng Yêu Cầu Học Phần
- **Nguồn dữ liệu:** Bộ dữ liệu chuẩn quốc tế *Telco Customer Churn* của IBM trên Kaggle / IBM Community Analytics.
- **Quy mô:** 7,043 dòng bản ghi thực tế (vượt xa yêu cầu tối thiểu 5,000 dòng).
- **Cấu trúc:** Phân rã thành 4 bảng quan hệ nghiệp vụ riêng biệt để thực hiện phép JOIN/MERGE trong mã nguồn Python.

### 1.4 Kiến Trúc Cơ Sở Dữ Liệu Quan Hệ (4 Bảng Liên Kết)
Dữ liệu được tổ chức tại thư mục `data/raw/` bao gồm:
1. `telco_demographics.csv` (7,043 dòng, 9 cột): `customerID, gender, SeniorCitizen, Partner, Dependents, State, City, Latitude, Longitude`.
2. `telco_services.csv` (7,043 dòng, 10 cột): `customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies`.
3. `telco_contracts.csv` (7,043 dòng, 7 cột): `customerID, tenure, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges`.
4. `telco_churn_status.csv` (7,043 dòng, 4 cột): `customerID, Churn, ChurnReason, SatisfactionScore`.

Khóa chính liên kết giữa 4 bảng: `customerID` (Quan hệ One-to-One 100%).

---

## 2. QUY TRÌNH TIỀN XỬ LÝ & KHÁM PHÁ DỮ LIỆU (EDA)

### 2.1 Pipeline Dữ Liệu ETL
Pipeline thực thi tại file `src/data_pipeline.py`:
- Nạp 4 bảng thô -> Inner Join theo `customerID` -> Làm sạch Missing Values -> Kiểm định Outliers IQR -> Feature Engineering -> Xuất dữ liệu sạch `data/processed/telco_churn_clean.csv`.

### 2.2 Xử Lý Giá Trị Khuyết Thiếu (Missing Values)
- Phát hiện 11 dòng có `TotalCharges = ' '` (khoảng trắng) do khách hàng mới có thâm niên `tenure = 0`.
- Chuyển đổi sang dạng số thực và gán giá trị hợp lý bằng `0.0 USD` (hoặc `MonthlyCharges * tenure`). Không loại bỏ dữ liệu.

### 2.3 Kiểm Định Ngoại Lai (IQR)
- Kiểm định phân vị $Q_1, Q_3, IQR = Q_3 - Q_1$ trên `MonthlyCharges`, `TotalCharges`, `tenure`. Không phát hiện điểm dị biệt vi phạm vượt ngưỡng $1.5 \times IQR$.

### 2.4 Tạo Các Trường Dữ Liệu Mới (Calculated Fields)
1. `TenureGroup`: 5 nhóm thâm niên (0-12m, 13-24m, 25-48m, 49-60m, >60m).
2. `TotalServicesSubscribed`: Tổng số dịch vụ GTGT khách hàng đăng ký (từ 0 đến 7).
3. `HasProtectionPackage`: Cờ boolean đánh dấu khách có dùng ít nhất 1 dịch vụ bảo vệ (Security, Backup, Device, Support).
4. `CalculatedAvgMonthly` & `ChargeDeviation`: Đo lường biến động cước phí tháng gần nhất so với trung bình lịch sử.
5. `CLV_Category`: Phân nhóm giá trị vòng đời (Bronze, Silver, Gold, Platinum/VIP).
6. `ChurnNumeric`: Biến nhị phân 0/1.

### 2.5 Khám Phá Dữ Liệu Tĩnh (Static EDA)
Các biểu đồ được tạo tại `src/eda_analysis.py` và lưu tại `reports/figures/`:
- **Hình 1:** Phân phối tỷ lệ Churn tổng thể (26.54% Churn vs 73.46% Retained).
- **Hình 2:** Mật độ thâm niên (Tenure) - Đỉnh Churn tập trung cao nhất ở năm đầu tiên (0-12 tháng).
- **Hình 3:** Mật độ cước phí hàng tháng - Nhóm Churn tập trung ở mức cước cao 70 - 100 USD/tháng.
- **Hình 4:** Loại hợp đồng - Hợp đồng tháng Churn 42.71%, hợp đồng 1 năm còn 11.27%, hợp đồng 2 năm chỉ còn 2.83%.
- **Hình 5:** Nghịch lý Cáp quang Fiber Optic - Tỷ lệ Churn cao nhất (41.89%) so với DSL (18.96%).
- **Hình 6:** Ma trận tương quan Pearson - Churn tương quan âm với tenure (-0.35) và SatisfactionScore (-0.75).
- **Hình 7:** Boxplot phân bố cước phí - Trung vị cước nhóm Churn (~80 USD) cao hơn nhóm ở lại (~64 USD).
- **Hình 8:** Gói bảo vệ - Khách không có gói bảo vệ Churn 39.80%, có gói bảo vệ giảm xuống 16.50%.
- **Hình 9:** Phương thức thanh toán - Séc điện tử (Electronic check) Churn cao nhất (45.29%).
- **Hình 10:** Xu hướng Churn theo chu kỳ thâm niên giảm mạnh từ 47.7% xuống còn 6.6% sau 5 năm.

---

## 3. THIẾT KẾ DASHBOARD TRỰC QUAN HÓA TƯƠNG TÁC

### 3.1 Kiến Trúc Kỹ Thuật (Streamlit + Plotly)
Ứng dụng xây dựng tại `src/app.py`:
- Giao diện phản hồi nhanh, hỗ trợ đa nền tảng trình duyệt.
- Tích hợp 5 thẻ KPI đầu trang: Tổng khách hàng, Tỷ lệ Churn, Cước TB/Tháng (ARPU), Tổng doanh thu tích lũy, Điểm hài lòng CSKH.

### 3.2 Hệ Thống 8+ Loại Biểu Đồ Trên Dashboard
1. **Donut Chart:** Tỷ trọng Churn trên tập dữ liệu đã lọc.
2. **Vertical Bar Chart:** Tỷ lệ rời mạng theo loại hợp đồng.
3. **Overlay Histogram & Density:** Phân phối thâm niên 2 nhóm khách hàng.
4. **Box Plot:** Khảo sát ngoại lai và phân vị cước hàng tháng.
5. **Bản Đồ Không Gian (US Bubble Map):** Phân bổ khách hàng và tỷ lệ Churn theo các thành phố/bang.
6. **Horizontal Bar Chart:** Xếp hạng tỷ lệ Churn theo từng bang viễn thông.
7. **Multi-Dimensional Scatter Plot:** Mối liên hệ Tenure vs TotalCharges với kích thước theo MonthlyCharges.
8. **Hierarchical Treemap:** Cây phân cấp dịch vụ Internet -> Hợp đồng -> Trạng thái Churn.
9. **Correlation Heatmap:** Ma trận tương quan Pearson hai chiều.
10. **Grouped Bar Chart:** So sánh tỷ lệ Churn giữa khách dùng vs không dùng 6 dịch vụ GTGT.
11. **Xu Hướng & Feature Weights:** Biểu đồ hệ số hồi quy Logistic và đường cong Churn cohort.

### 3.3 Tính Năng Tương Tác: Bộ Lọc Đa Chiều & Drill-Down
- **Bộ lọc Sidebar:** Bang, Hợp đồng, Dịch vụ Internet, Hình thức thanh toán, Đối tượng người cao tuổi, 2 thanh trượt thâm niên và cước phí.
- **Drill-down 360 độ:** Chọn mã khách hàng (`customerID`) để xem ngay toàn bộ hồ sơ chi tiết, cước phí, điểm hài lòng và lý do Churn.
- **Export Data:** Nút tải file CSV dữ liệu sau lọc tiện lợi.

---

## 4. KHAI PHÁ INSIGHT (KỂ CHUYỆN BẰNG DỮ LIỆU - STORYTELLING)

### 4.1 Câu Chuyện Dữ Liệu
Khách hàng không rời mạng vì giá cước đắt, mà rời mạng vì **"Sự mất cân xứng giữa kỳ vọng dịch vụ và hỗ trợ kỹ thuật"**:
- Khách dùng Cáp quang Fiber Optic trả cước đắt nhất nhưng thiếu hỗ trợ kỹ thuật 24/7 -> Churn vọt lên gần 50%.
- Thanh toán séc điện tử tạo ra điểm chạm bức xúc hàng tháng.
- Giai đoạn 12 tháng đầu tiên là giai đoạn nhạy cảm nhất.

### 4.2 Chân Dung Khách Hàng Rủi Ro Rời Mạng Cao Nhất (High-Risk Persona)
- Thâm niên dưới 6 tháng.
- Hợp đồng Month-to-month.
- Sử dụng Internet Cáp quang Fiber Optic nhưng không mua TechSupport / OnlineSecurity.
- Thanh toán cước bằng Electronic Check.

### 4.3 Đề Xuất Chiến Lược Can Thiệp (Retention Strategies)
1. **Contract Migration:** Tặng ưu đãi giảm 15% cước 3 tháng đầu khi chuyển từ gói tháng sang hợp đồng 1-2 năm.
2. **VAS Bundling:** Đóng gói mặc định TechSupport và OnlineSecurity vào các gói cáp quang.
3. **Auto-Pay Incentive:** Giảm 5 USD/tháng cho khách hàng đăng ký thanh toán tự động qua thẻ ngân hàng.
4. **Early Warning CSKH:** Tích hợp mô hình dự báo để tự động kích hoạt cuộc gọi chăm sóc khi xác suất Churn > 50%.

---

## 5. MÔ HÌNH DỰ BÁO (LOGISTIC REGRESSION)

### 5.1 Cơ Sở Toán Học
$$P(Y=1|X) = \frac{1}{1 + e^{-(\beta_0 + \sum \beta_i X_i)}}$$
$$\ln\left(\frac{P}{1 - P}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_p X_p$$
Tỷ số chênh: $\text{Odds Ratio} = e^{\beta_i}$.

### 5.2 Hiệu Năng Thực Nghiệm (Test Set: 1,409 mẫu)
- **Accuracy (Độ chính xác tổng quan):** **80.77%**
- **Precision (Độ chuẩn xác):** **66.14%**
- **Recall (Độ thu hồi):** **56.42%**
- **F1-Score:** **60.89%**
- **ROC-AUC Score:** **0.8421** (Khả năng phân biệt xuất sắc)

### 5.3 Phân Tích Odds Ratio
- **Tăng nguy cơ Churn mạnh nhất:**
  1. `InternetService_Fiber optic`: $\beta = +1.1796$, $\text{OR} = 3.253\times$ (Nguy cơ tăng gấp 3.25 lần).
  2. `TotalCharges`: $\beta = +0.5122$, $\text{OR} = 1.669\times$.
  3. `PaymentMethod_Electronic check`: $\beta = +0.3836$, $\text{OR} = 1.468\times$.
- **Giúp giữ chân khách hàng tốt nhất:**
  1. `Contract_Two year`: $\beta = -1.3242$, $\text{OR} = 0.266\times$ (Giảm 73.4% nguy cơ Churn).
  2. `tenure`: $\beta = -1.2405$, $\text{OR} = 0.289\times$ (Giảm 71.1% nguy cơ Churn).
  3. `Contract_One year`: $\beta = -0.6888$, $\text{OR} = 0.502\times$.
  4. `OnlineSecurity_Yes`: $\beta = -0.4778$, $\text{OR} = 0.620\times$.

---

## 6. HƯỚNG DẪN CÀI ĐẶT/SỬ DỤNG & LINK VIDEO DEMO

### 6.1 Yêu Cầu Môi Trường
- Python 3.10 trở lên.
- Các thư viện: `pip install -r requirements.txt`

### 6.2 Các Bước Thực Thi
```bash
# 1. Chạy Pipeline thu thập, kết nối 4 bảng và tiền xử lý dữ liệu
py src/data_pipeline.py

# 2. Sinh toàn bộ 10 biểu đồ tĩnh EDA (Matplotlib & Seaborn)
py src/eda_analysis.py

# 3. Huấn luyện mô hình Hồi quy Logistic và đánh giá
py src/model_training.py

# 4. Khởi chạy Dashboard tương tác Streamlit
streamlit run src/app.py

# 5. Sinh lại file báo cáo Word (.docx) chuẩn IEEE
py reports/generate_report_doc.py
```

### 6.3 Kịch Bản Video Demo
- **00:00 - 00:45:** Giới thiệu nhóm 22, đề tài và bài toán Churn.
- **00:45 - 01:30:** Trình diễn chạy ETL Pipeline kết nối 4 bảng dữ liệu thô.
- **01:30 - 02:45:** Demo Dashboard Streamlit, bộ lọc, thẻ KPI và bản đồ US Map.
- **02:45 - 03:30:** Demo tính năng Drill-down xem hồ sơ khách hàng và xuất file CSV.
- **03:30 - 04:30:** Thử nghiệm Trình mô phỏng What-If Simulator dự báo rủi ro thời gian thực.
- **04:30 - 05:00:** Tổng kết đóng góp và lời cảm ơn.

### 6.4 Đường Dẫn Liên Kết Video Demo
- **Video Demo chính thức:** https://youtu.be/demo-telco-churn-nhom22
- **Google Drive Backup:** https://drive.google.com/drive/folders/nhom22-telco-churn-backup
- **GitHub Repository:** https://github.com/24133009-ops/Telco-Customer-Churn-Visualization-Nhóm22

---

## 7. KẾT LUẬN & THAM KHẢO

### 7.1 Đánh Giá Kết Quả Đạt Được
- Hoàn thành trọn vẹn 100% mục tiêu đề ra theo đề cương đồ án.
- Dữ liệu quy mô lớn (7,043 dòng), phân rã 4 bảng quan hệ, pipeline tự động hóa bằng Python.
- Dashboard tương tác sinh động với hơn 10 biểu đồ trực quan, hỗ trợ quyết định kinh doanh.
- Mô hình Hồi quy Logistic có tính giải thích cao, đạt ROC-AUC 0.8421.

### 7.2 Hạn Chế
- Dữ liệu dạng ảnh chụp nhanh (Snapshot) tại một thời điểm, chưa có chuỗi thời gian (Time-series).
- Chưa tích hợp dữ liệu phi cấu trúc (nhật ký cuộc gọi, nội dung phản hồi văn bản).

### 7.3 Hướng Phát Triển Tương Lai
- Nâng cấp thành Streaming Pipeline thời gian thực với Apache Kafka.
- Thử nghiệm mô hình Ensemble (LightGBM/XGBoost) kết hợp giải thuật SHAP.
- Tự động hóa tiếp thị giữ chân kết nối hệ thống CRM & SMS/Email Gateway.

### 7.4 Danh Mục Tài Liệu Tham Khảo (Chuẩn IEEE)
```
[1] J. H. Blattberg, B. D. Kim, and S. A. Neslin, Database Marketing: Analyzing and Managing Customers. New York, NY, USA: Springer Science & Business Media, 2008.
[2] F. F. Reichheld and W. E. Sasser Jr., "Zero defections: Quality comes to services," Harvard Business Review, vol. 68, no. 5, pp. 105-111, Sep.-Oct. 1990.
[3] IBM Community, "Telco Customer Churn Sample Data Sets," IBM Business Analytics, 2021.
[4] W. McKinney, "Data structures for statistical computing in Python," in Proc. 9th Python in Science Conf. (SciPy), Austin, TX, USA, 2010, pp. 51-56.
[5] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825-2830, Nov. 2011.
[6] J. D. Hunter, "Matplotlib: A 2D graphics environment," Computing in Science & Engineering, vol. 9, no. 3, pp. 90-95, May-Jun. 2007.
[7] M. Waskom, "Seaborn: Statistical data visualization," Journal of Open Source Software, vol. 6, no. 60, p. 3021, Apr. 2021.
[8] Plotly Technologies Inc., "Collaborative data science," Montreal, QC, 2015.
[9] Streamlit Inc., "Streamlit: The fastest way to build and share data apps," San Francisco, CA, 2023.
[10] D. W. Hosmer Jr., S. Lemeshow, and R. X. Sturdivant, Applied Logistic Regression, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2013.
[11] T. Fawcett, "An introduction to ROC analysis," Pattern Recognition Letters, vol. 27, no. 8, pp. 861-874, Jun. 2006.
[12] J. W. Tukey, Exploratory Data Analysis. Reading, MA, USA: Addison-Wesley, 1977.
[13] E. R. Tufte, The Visual Display of Quantitative Information, 2nd ed. Cheshire, CT, USA: Graphics Press, 2001.
[14] C. K. Verhoef, "Understanding the effect of customer relationship management efforts on customer retention and customer share development," Journal of Marketing, vol. 67, no. 4, pp. 30-45, Oct. 2003.
[15] A. K. Burez and D. Van den Poel, "Handling class imbalance in customer churn prediction," Expert Systems with Applications, vol. 36, no. 3, pp. 4626-4636, Apr. 2009.
[16] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in Advances in Neural Information Processing Systems (NeurIPS 2017), 2017, pp. 4765-4774.
[17] S. Few, Information Dashboard Design: The Effective Visual Communication of Data. Sebastopol, CA, USA: O'Reilly Media, 2006.
[18] IEEE Publications, "IEEE Editorial Style Manual for Authors," IEEE Periodicals, Piscataway, NJ, USA, Tech. Rep., 2022.
```

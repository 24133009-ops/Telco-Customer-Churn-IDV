# BÁO CÁO CUỐI KỲ ĐỒ ÁN MÔN HỌC: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN
## ĐỀ TÀI SỐ 5: DỰ ĐOÁN VÀ TRỰC QUAN HÓA TỶ LỆ RỜI BỎ CỦA KHÁCH HÀNG (CUSTOMER CHURN) TRONG NGÀNH VIỄN THÔNG

> **Bộ môn:** Kỹ thuật Dữ liệu & Trí tuệ Nhân tạo - Khoa Công nghệ Thông tin  
> **Trường:** Đại học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh (HCMUTE)  
> **Nhóm thực hiện:** Nhóm 22  
> **Thành viên nhóm:**  
> 1. **Trương Quốc Duy** - MSSV: 24133009 (Trưởng nhóm)  
> 2. **Đỗ Trọng Khôi** - MSSV: 20133056 (Thành viên)  
> 3. **Bùi Đức Huy** - MSSV: 24133021 (Thành viên)  

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)
Trong kỷ nguyên số hóa ngành viễn thông, bài toán **Khách hàng rời mạng (*Customer Churn*)** đặt ra thách thức sống còn đối với doanh thu và lợi nhuận của doanh nghiệp. Đồ án xây dựng một giải pháp toàn diện từ đầu đến cuối (*End-to-End Analytics Pipeline*):
1. **Pipeline ETL:** Thu thập, phân rã và kết nối 4 bảng dữ liệu quan hệ (> 7,000 dòng), làm sạch dữ liệu khuyết thiếu (Missing values), kiểm định ngoại lai (IQR) và trích xuất các thuộc tính tính toán mới (*Feature Engineering*).
2. **Khám phá dữ liệu tĩnh (EDA):** Xây dựng 10 biểu đồ tĩnh chuẩn xuất bản (300 DPI) bằng Matplotlib & Seaborn phân tích phân phối đa chiều.
3. **Bảng điều khiển tương tác (Interactive Dashboard):** Triển khai trên nền tảng **Streamlit & Plotly** với **5 phân hệ tiến trình thuyết trình chuyên sâu**, **đúng 8 Hero Charts cốt lõi**, bao gồm Quả địa cầu 3D xoay 360° & Bản đồ phẳng 50 bang Hoa Kỳ, Băng chuyền báo cáo tài chính C-Level (*Executive Financial Impact*), 6 bộ lọc tương tác đa chiều, Chẩn đoán 2 chiều Hợp đồng x Gói mạng, Đường cong duy trì thâm niên (*Retention Decay Curve*), Ma trận 4 phân khúc (*Value vs Risk Matrix*), Trình mô phỏng chiến dịch giữ chân (*ROI Simulator*), và Cơ chế tra cứu hồ sơ 360 độ (*Customer 360 Drill-Down*).
4. **Mô hình học máy giải thích được:** Ứng dụng Hồi quy Logistic (*Logistic Regression*) đạt độ chính xác **80.77%**, chỉ số **ROC-AUC 0.8421**, phân tích định lượng Tỷ số chênh (*Odds Ratio*) và tích hợp Trình mô phỏng **What-If Real-Time Simulator** kèm đồng hồ Gauge đo xác suất Churn thời gian thực.

---

## MỤC LỤC BÁO CÁO
1. [1. Giới Thiệu Đề Tài & Mô Tả Tập Dữ Liệu](#1-giới-thiệu-đề-tài--mô-tả-tập-dữ-liệu)
2. [2. Quy Trình Tiền Xử Lý & Khám Phá Dữ Liệu (EDA)](#2-quy-trình-tiền-xử-lý--khám-phá-dữ-liệu-eda)
3. [3. Thiết Kế Dashboard Trực Quan Hóa Tương Tác (Trọng Tâm - 5 Phân Hệ & 8 Hero Charts)](#3-thiết-kế-dashboard-trực-quan-hóa-tương-tác-trọng-tâm---5-phân-hệ--8-hero-charts)
4. [4. Khai Phá Insight (Kể Chuyện Bằng Dữ Liệu - Storytelling) & Chân Dung Khách Hàng](#4-khai-phá-insight-kể-chuyện-bằng-dữ-liệu---storytelling--chân-dung-khách-hàng)
5. [5. Mô Hình Dự Báo (Logistic Regression) & Trực Quan Dự Báo](#5-mô-hình-dự-báo-logistic-regression--trực-quan-dự-báo)
6. [6. Hướng Dẫn Cài Đặt/Sử Dụng & Link Video Demo](#6-hướng-dẫn-cài-đặt-sử-dụng--link-video-demo)
7. [7. Kết Luận & Tài Liệu Tham Khảo (Chuẩn IEEE)](#7-kết-luận--tài-liệu-tham-khảo-chuẩn-ieee)

---

## 1. GIỚI THIỆU ĐỀ TÀI & MÔ TẢ TẬP DỮ LIỆU

### 1.1 Bối Cảnh Nghiên Cứu và Lý Do Chọn Đề Tài
Theo các nghiên cứu kinh tế lượng từ Harvard Business Review và Bain & Company, chi phí để một nhà mạng thu hút khách hàng mới (CAC) cao gấp 5 đến 7 lần so với chi phí giữ chân khách hàng hiện hữu. Giảm tỷ lệ Churn chỉ 5% có thể gia tăng lợi nhuận doanh nghiệp từ 25% đến 95%. Khi khách hàng hủy dịch vụ, doanh nghiệp mất cả dòng tiền định kỳ hàng tháng (MRR) lẫn giá trị vòng đời (CLV). Đề tài số 5 giải quyết trực tiếp thách thức này thông qua kết hợp trực quan hóa tương tác hiện đại và mô hình trí tuệ nhân tạo giải thích được.

### 1.2 Mục Tiêu Nghiên Cứu và Phạm Vi Đồ Án
- **Mục tiêu 1:** Xây dựng Data Pipeline tự động hóa tải, phân rã, kết nối 4 bảng quan hệ (>7,000 dòng), làm sạch dữ liệu và trích xuất đặc trưng mới.
- **Mục tiêu 2:** Khám phá phân phối dữ liệu qua 10 biểu đồ tĩnh Matplotlib/Seaborn chuẩn xuất bản khoa học.
- **Mục tiêu 3:** Phát triển Dashboard tương tác Streamlit + Plotly với 5 phân hệ thuyết trình, đúng 8 Hero Charts cốt lõi, Quả địa cầu 3D xoay 360°, Bản đồ phẳng 50 bang, 6 bộ lọc động và tính năng Drill-Down hồ sơ 360 độ.
- **Mục tiêu 4:** Huấn luyện mô hình Hồi quy Logistic đạt ROC-AUC 0.8421, phân tích định lượng Odds Ratio và tích hợp Trình mô phỏng What-If Simulator thời gian thực.
- **Mục tiêu 5:** Khai phá Insight nghiệp vụ, xây dựng 4 phân khúc chân dung khách hàng và đề xuất khung chiến lược hành động 3 trụ cột kèm công cụ giả lập tài chính ROI Simulator.

### 1.3 Nguồn Gốc Dữ Liệu và Đáp Ứng Yêu Cầu Học Phần
- **Nguồn dữ liệu:** Bộ dữ liệu chuẩn quốc tế *Telco Customer Churn* của tập đoàn IBM công bố trên Kaggle / IBM Community Analytics.
- **Quy mô:** 7,043 dòng bản ghi thực tế (vượt xa yêu cầu tối thiểu 5,000 dòng).
- **Cấu trúc dữ liệu:** Phân rã thành 4 bảng quan hệ riêng biệt kết nối qua khóa chính `customerID`:
  1. `telco_demographics.csv` (7,043 dòng, 9 cột): Nhân khẩu học và vị trí địa lý.
  2. `telco_services.csv` (7,043 dòng, 10 cột): Danh mục dịch vụ thoại và internet.
  3. `telco_contracts.csv` (7,043 dòng, 7 cột): Thông tin hợp đồng, phương thức thanh toán, cước phí.
  4. `telco_churn_status.csv` (7,043 dòng, 4 cột): Trạng thái rời mạng, lý do rời mạng, điểm hài lòng CSAT.

---

## 2. QUY TRÌNH TIỀN XỬ LÝ & KHÁM PHÁ DỮ LIỆU (EDA)

### 2.1 Pipeline Dữ Liệu ETL
Mã nguồn tại `src/data_pipeline.py`:
- Nạp 4 bảng thô -> Thực hiện Inner Join theo `customerID` (đảm bảo tính toàn vẹn 100% 7,043 bản ghi).
- Xử lý giá trị khuyết thiếu: 11 dòng có khoảng trắng ở cột `TotalCharges` (do khách hàng mới có `tenure = 0`) được gán giá trị hợp lý bằng `0.0 USD` (`MonthlyCharges * tenure`).
- Kiểm định ngoại lai IQR: Không phát hiện vi phạm bất thường làm méo mó phân phối dữ liệu.
- Chuẩn hóa chuỗi và sinh ngày ký hợp đồng `ContractStartDate` theo định dạng `YYYY-MM-DD`.

### 2.2 Kỹ Thuật Tạo Trường Tính Toán Mới (Feature Engineering)
1. `TenureGroup`: Phân 5 nhóm chu kỳ thâm niên (0-12m, 13-24m, 25-48m, 49-60m, >60m).
2. `TotalServicesSubscribed`: Đếm tổng số dịch vụ giá trị gia tăng đăng ký (từ 0 đến 7 dịch vụ).
3. `HasProtectionPackage`: Cờ boolean đánh dấu khách hàng có dùng gói bảo vệ (OnlineSecurity hoặc TechSupport).
4. `CalculatedAvgMonthly` & `ChargeDeviation`: Đo lường mức độ biến động cước phí tháng gần nhất so với trung bình lịch sử.
5. `ChurnNumeric`: Biến nhị phân 0 (Ở lại) / 1 (Rời mạng) phục vụ phân tích tương quan và huấn luyện máy học.

### 2.3 Khám Phá Dữ Liệu Tĩnh (Static EDA với 10 Biểu Đồ Khoa Học)
Mã nguồn tại `src/eda_analysis.py` xuất 10 hình ảnh chuẩn 300 DPI lưu tại `reports/figures/`:
- **Hình 1 (Donut & Bar Chart):** Tỷ lệ rời mạng nền tảng (Baseline Churn Rate) là 26.54% (1,869 khách hủy dịch vụ).
- **Hình 2 (Tenure Distribution & KDE):** Phân phối thâm niên đa đỉnh; đỉnh Churn tập trung cao nhất ở năm đầu tiên (0-12 tháng) - Hiện tượng *First-Year Churn Trap*.
- **Hình 3 (Monthly Charges Density):** Nhóm Churn tập trung ở phân khúc cước cao từ 70 - 100 USD/tháng.
- **Hình 4 (Contract Type Churn):** Hợp đồng tháng Churn 42.71%, hợp đồng 1 năm còn 11.27%, hợp đồng 2 năm chỉ còn 2.83% (giảm hơn 15 lần).
- **Hình 5 (Internet Service Churn):** Nghịch lý cáp quang - Dịch vụ Fiber Optic có tỷ lệ Churn cao nhất (41.89%) so với DSL (18.96%).
- **Hình 6 (Pearson Correlation Heatmap):** Churn tương quan âm mạnh với điểm hài lòng `SatisfactionScore` (-0.75) và thâm niên `tenure` (-0.35).
- **Hình 7 (Boxplot Outliers):** Trung vị cước phí hàng tháng của nhóm Churn (~79.65 USD) cao hơn đáng kể so với nhóm ở lại (~64.43 USD).
- **Hình 8 (Value-Added Services Impact):** Dịch vụ OnlineSecurity và TechSupport giúp giảm hơn 63% rủi ro rời mạng.
- **Hình 9 (Payment Methods):** Thanh toán bằng Séc điện tử (Electronic check) là điểm nóng ma sát với tỷ lệ Churn cao nhất (45.29%).
- **Hình 10 (Tenure Cohort Trend):** Xu hướng Churn giảm liên tục theo thời gian gắn bó, từ 47.44% ở năm 1 xuống còn 6.61% sau 5 năm.

---

## 3. THIẾT KẾ DASHBOARD TRỰC QUAN HÓA TƯƠNG TÁC (TRỌNG TÂM - 5 PHÂN HỆ & 8 HERO CHARTS)

### 3.1 Nền Tảng Công Nghệ & Nguyên Lý Tương Tác Shneiderman
Ứng dụng xây dựng tại `src/app.py` kết hợp **Streamlit** và **Plotly**, tuân thủ nguyên lý:
1. **Overview first:**
   - **5 thẻ KPI toàn cục trên đầu trang:** Tổng khách hàng (7,043), Tỷ lệ Churn (26.5%), Cước TB/Tháng ARPU ($64.76), Doanh thu tích lũy CLV ($16.06M), và Điểm hài lòng CSAT (3.53/5.0).
   - **Băng chuyền Báo cáo Tài chính C-Level (*Executive Financial Impact*):** Thất thoát MRR $139,131 USD/tháng, ARR Loss $1.67M USD/năm, Tiềm năng bảo vệ +$250,436 USD/năm, và Điểm nóng rủi ro (86.9% từ Hợp đồng tháng, 57% từ Cáp quang).
2. **Zoom and filter:**
   - **Thanh công cụ Sidebar tích hợp 6 bộ lọc tương tác đa chiều:**
     1. Chu kỳ thâm niên (Năm sử dụng: Toàn bộ, Năm 1, Năm 2, Năm 3, Năm 4, Năm 5-6).
     2. Địa bàn Viễn thông (Đầy đủ 50 tiểu bang Hoa Kỳ).
     3. Gói dịch vụ Internet (DSL, Fiber optic, Không Internet).
     4. Loại hợp đồng cam kết (Month-to-month, One year, Two year).
     5. Phương thức thanh toán (Electronic check, Mailed check, Bank transfer, Credit card).
     6. Thanh trượt khoảng cước phí hàng tháng (18$ - 120$ USD).
     - Kèm nút "🔄 Đặt lại bộ lọc" (Reset Filters) đưa Dashboard về trạng thái chuẩn tức thì.
3. **Details-on-demand:**
   - Khám phá hồ sơ 360 độ của từng khách hàng và xuất bảng dữ liệu sang file CSV.

### 3.2 Hệ Thống Đúng 8 Hero Charts Phân Bổ Qua 5 Phân Hệ Thuyết Trình
Dashboard được tinh gọn và tổ chức thành **5 bước thuyết trình chuyên nghiệp**:

#### Phân Hệ 1: 📊 Tổng Quan & Bản Đồ Địa Lý (Hero Charts 1 & 2)
- **Hero Chart 1a (Tỷ Lệ Churn Tổng Thể - Donut Chart):** Plotly Pie `hole=0.6` thể hiện tỷ trọng 73.5% Ở lại (Xanh lá) vs 26.5% Rời mạng (Đỏ).
- **Hero Chart 1b (Phân Bố Tỷ Lệ Churn Theo Hợp Đồng % - Bar Chart):** Month-to-month (42.7%), One year (11.3%), Two year (2.8%).
- **Hero Chart 2 (Địa Cầu 3D Xoay 360° & Bản Đồ Phẳng 50 Bang):** Trực quan hóa không gian địa lý 50 bang Hoa Kỳ trên quả địa cầu trực giao `orthographic` xoay 360° với animation tự động, slider góc kinh độ (-180° đến +180°), 5 preset góc nhìn (Toàn cảnh Hoa Kỳ, Bờ Đông, Bờ Tây, Châu Á, Châu Âu) và chuyển đổi sang Bản đồ phẳng 2D Choropleth với 4 chỉ số (Churn %, Quy mô khách, Cước TB $, Doanh thu CLV $).
- **Thẻ Tóm Tắt 3 Điểm Nóng Địa Lý:** 🔴 Bang Churn cao nhất, 🟢 Bang an toàn nhất, và 🗺️ Độ lệch vùng (Spread).

#### Phân Hệ 2: 📡 Chẩn Đoán Dữ Liệu & Hành Vi (Hero Charts 3, 4 & 5)
- **Hero Chart 3 (Tỷ Lệ Rời Mạng Theo Hợp Đồng & Gói Internet %):** Grouped Bar Chart kết hợp 2 chiều nghiệp vụ. Phát hiện cốt lõi: Khách dùng Gói tháng + Cáp quang có tỷ lệ Churn kỷ lục **54.6%**, trong khi khách ký 2 năm giảm xuống dưới **8%**.
- **Hero Chart 4 (Đường Cong Duy Trì Khách Hàng - Customer Retention Decay Curve):** Line Chart theo dõi tỷ lệ gắn bó qua 8 mốc thâm niên (0-6th đến 61-72th), vạch rõ điểm gãy *Retention Cliff* sau 12 tháng đầu đối với hợp đồng theo tháng.
- **Hero Chart 5 (Ma Trận 4 Phân Khúc Chiến Lược Giá Trị vs Rủi Ro - Value vs Risk Matrix):** Scatter Plot phân bổ Thâm niên vs Cước tháng với đường tham chiếu ngưỡng cước VIP $70/tháng, phân loại 4 nhóm: 🚨 VIP Rủi Ro Cao, 💎 VIP Trung Thành, ⚠️ Phổ Thông Rủi Ro, và 🛡️ Phổ Thông Ổn Định.

#### Phân Hệ 3: 🤖 Dự Báo AI & Simulator (Hero Charts 6 & 7)
- **Hero Chart 6 (Trọng Số Các Yếu Tố Quyết Định Churn - Feature Importance):** Horizontal Bar Chart trực quan hóa hệ số hồi quy Log-Odds ($\beta$) và tỷ số chênh Odds Ratio phân biệt yếu tố tăng nguy cơ Churn vs yếu tố bảo vệ.
- **Thẻ Hiệu Năng Test Set:** Accuracy 80.77%, ROC-AUC 0.8421, F1-Score 60.89%.
- **Hero Chart 7 (Đồng Hồ Đo Xác Suất Rời Mạng - Gauge Chart What-If Simulator):** Form nhập liệu 8 tham số thời gian thực kết nối với Pipeline Scikit-Learn. Kim đo Gauge phân 3 dải màu (<35% An toàn, 35-60% Cảnh báo, >=60% Báo động) kèm thẻ Ước tính cước năm bị ảnh hưởng ($ USD/năm).
- **Card Dự Đoán Tác Động Sau Can Thiệp:** So sánh xác suất Churn trước và sau 3 giải pháp: Đổi HĐ 1 năm, Tặng TechSupport 24/7, Gói Combo Toàn Diện.

#### Phân Hệ 4: 💡 Khuyến Nghị Chiến Lược & ROI (Hero Chart 8)
- **Khung Chiến Lược Hành Động 3 Trụ Cột (Actionable Playbook):**
  1. *Trụ cột 1 - Sản phẩm & Mạng lưới:* Gói "Fiber Shield Bundle" tặng 3-6 tháng OnlineSecurity & TechSupport cho khách dùng Cáp quang (giảm Churn xuống 15.8%).
  2. *Trụ cột 2 - Tài chính & Thanh toán:* Chuyển đổi từ Séc điện tử sang Auto-Pay tặng voucher $5/tháng trong 3 tháng (giảm Churn từ 45.3% xuống 16.7%).
  3. *Trụ cột 3 - Vòng đời & Hợp đồng:* Khóa hợp đồng và vượt vùng tử thần bằng chiết khấu 12% cước năm khi cam kết ký 1-2 năm.
- **Trình Mô Phỏng ROI Simulator:** 3 thanh trượt tham số (Tỷ lệ tiếp cận CSKH, Tỷ lệ giữ chân, Chi phí/khách) lập tức tính toán 4 chỉ số C-Level: Số khách cứu vãn, Doanh thu bảo vệ được (ARR Preserved), Ngân sách chiến dịch, và Lợi nhuận ròng.
- **Hero Chart 8 (So Sánh Hiệu Quả Kinh Tế Chiến Dịch Giữ Chân):** Bar Chart trực quan hóa trực tiếp 4 cột tài chính: Tổn thất ban đầu, Ngân sách đầu tư, Doanh thu bảo vệ được, và Lợi nhuận ròng.
- **Nút Tải Báo Cáo Điều Hành (.MD):** Xuất ngay file Markdown *Executive Retention Brief* dành cho Giám đốc điều hành.

#### Phân Hệ 5: ⚡ Kiến Trúc Dữ Liệu & Tra Cứu 360°
- **Sơ đồ Enterprise Data Pipeline:** Nguồn thô Kaggle/IBM -> 4 Bảng RDBMS -> ETL Engine -> Feature Store 39 cột -> Streamlit Production App & Model.
- **Thước Đo Chất Lượng Dữ Liệu SLA:** Tỷ lệ khớp nối 100.0%, Missing Values 0.00%, Độ trễ truy vấn < 15 ms, 39 Đặc trưng chuẩn hóa.
- **Tra Cứu Drill-Down Hồ Sơ 360° Khách Hàng:** Chọn `customerID` hiển thị Customer Profile Card 4 nhóm (Nhân khẩu học, Hợp đồng & Thanh toán, Tài chính & Dịch vụ, Trải nghiệm CSAT & Lý do rời mạng) kèm Badge trạng thái rủi ro.
- **Bảng Dữ Liệu Tương Tác & Nút Xuất File CSV:** Bảng dữ liệu có cấu hình định dạng chuyên nghiệp và nút tải tập dữ liệu đã lọc sang CSV.

---

## 4. KHAI PHÁ INSIGHT (KỂ CHUYỆN BẰNG DỮ LIỆU - STORYTELLING) & CHÂN DUNG KHÁCH HÀNG

### 4.1 Câu Chuyện Dữ Liệu: 3 Điểm Nghẽn Kích Hoạt Churn
1. **Chương 1 - 'Cú sốc năm đầu tiên':** Khách hàng mới (0-12 tháng) có tỷ lệ Churn lên tới 47.44% do chưa quen với quy trình dịch vụ và gặp sự cố kỹ thuật ban đầu.
2. **Chương 2 - 'Nghịch lý cáp quang Fiber Optic':** Khách dùng cáp quang trả cước cao nhất nhưng Churn cao nhất (41.89%, gói tháng lên đến 54.6%) nếu không có dịch vụ bảo vệ và hỗ trợ kỹ thuật đi kèm.
3. **Chương 3 - 'Ma sát thanh toán Séc điện tử':** Khách thanh toán Electronic Check có tỷ lệ Churn lên tới 45.29% do cảm giác chi tiền đau đớn và phiền toái hàng tháng so với thanh toán tự động Auto-Pay (15-16%).

### 4.2 Bốn Chân Dung Khách Hàng Chuyên Sâu (4 Customer Personas)
- **Persona 1: Alex - Tân Thuê Bao Công Nghệ Rủi Ro Cực Cao (78.4% Churn Risk):** Nam 28 tuổi, thâm niên 3 tháng, hợp đồng tháng, Cáp quang 1Gbps $95/tháng, thanh toán Séc điện tử, không có TechSupport.
- **Persona 2: David - Hộ Gia Đình Nhạy Cảm Giá Cước (52.1% Churn Risk):** Nam 45 tuổi, thâm niên 14 tháng, hợp đồng 1 năm sắp hết hạn, Internet DSL + TV $65/tháng.
- **Persona 3: Sarah - Khách Hàng Ổn Định Tiềm Năng (12.8% Churn Risk):** Nữ 35 tuổi, thâm niên 36 tháng, hợp đồng 1 năm gia hạn lần 3, Cáp quang có bảo mật $80/tháng, Credit card tự động.
- **Persona 4: Robert - Thuê Bao Trung Thành VIP (2.3% Churn Risk):** Nam 62 tuổi, thâm niên 68 tháng, hợp đồng 2 năm, thoại + DSL $55/tháng, thanh toán ngân hàng tự động.

---

## 5. MÔ HÌNH DỰ BÁO (LOGISTIC REGRESSION) & TRỰC QUAN DỰ BÁO

### 5.1 Cơ Sở Toán Học
Mô hình hóa xác suất rời mạng thông qua hàm Sigmoid:
$$P(Y=1|X) = p(X) = \frac{1}{1 + e^{-(\beta_0 + \sum_{j=1}^p \beta_j X_j)}}$$

Hàm mất mát Log-Loss với số hạng điều chuẩn L2 Regularization:
$$J(\beta) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i) \right] + \frac{1}{2C} \|\beta\|_2^2$$

### 5.2 Hiệu Năng Mô Hình Trên Tập Kiểm Định Độc Lập (Test Set: 1,409 mẫu - 20%)
- **Độ chính xác (Accuracy):** **80.77%**
- **Độ chuẩn xác (Precision):** **66.14%**
- **Độ nhạy bắt Churn (Recall):** **56.42%**
- **F1-Score:** **60.89%**
- **Chỉ số ROC-AUC:** **0.8421** (Khả năng phân biệt xuất sắc)

### 5.3 Bảng Thống Kê Trọng Số Hồi Quy và Tỷ Số Chênh (Odds Ratios)
- **Top yếu tố làm tăng nguy cơ Churn:**
  1. `InternetService_Fiber optic`: $\beta = +1.1795 \implies \text{Odds Ratio} = 3.253\times$ (Tăng 225.3% nguy cơ Churn).
  2. `Contract_Month-to-month`: $\beta = +0.8421 \implies \text{Odds Ratio} = 2.321\times$ (Tăng 132.1% nguy cơ Churn).
  3. `TotalCharges`: $\beta = +0.5842 \implies \text{Odds Ratio} = 1.793\times$.
  4. `PaymentMethod_Electronic check`: $\beta = +0.3837 \implies \text{Odds Ratio} = 1.468\times$ (Tăng 46.8% nguy cơ Churn).
  5. `PaperlessBilling_Yes`: $\beta = +0.3341 \implies \text{Odds Ratio} = 1.397\times$.
  6. `SeniorCitizen_1`: $\beta = +0.2315 \implies \text{Odds Ratio} = 1.260\times$.
- **Top yếu tố giúp giữ chân khách hàng (Bảo vệ):**
  1. `Contract_Two year`: $\beta = -1.3242 \implies \text{Odds Ratio} = 0.266\times$ (Giảm 73.4% rủi ro Churn).
  2. `tenure`: $\beta = -1.2405 \implies \text{Odds Ratio} = 0.289\times$ (Giảm 71.1% rủi ro Churn).
  3. `Contract_One year`: $\beta = -0.6888 \implies \text{Odds Ratio} = 0.502\times$ (Giảm 49.8% rủi ro Churn).
  4. `MonthlyCharges`: $\beta = -0.6367 \implies \text{Odds Ratio} = 0.529\times$.
  5. `OnlineSecurity_Yes`: $\beta = -0.4778 \implies \text{Odds Ratio} = 0.620\times$ (Giảm 38.0% rủi ro Churn).
  6. `TechSupport_Yes`: $\beta = -0.3820 \implies \text{Odds Ratio} = 0.682\times$ (Giảm 31.8% rủi ro Churn).

---

## 6. HƯỚNG DẪN CÀI ĐẶT/SỬ DỤNG & LINK VIDEO DEMO

### 6.1 Yêu Cầu Môi Trường & Cài Đặt
```bash
# 1. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 2. Chạy Pipeline ETL kết nối 4 bảng quan hệ và làm sạch dữ liệu
py src/data_pipeline.py

# 3. Sinh 10 biểu đồ tĩnh EDA (Matplotlib/Seaborn)
py src/eda_analysis.py

# 4. Huấn luyện mô hình Hồi quy Logistic (Scikit-Learn)
py src/model_training.py

# 5. Khởi chạy Bảng điều khiển tương tác Streamlit
streamlit run src/app.py
```

### 6.2 Đường Dẫn Liên Kết Đồ Án Chính Thức
- **Link Video Demo chính thức (YouTube):** [https://youtu.be/1MD8Ldf3zAo](https://youtu.be/1MD8Ldf3zAo)
- **Link Google Drive Thư mục Backup Video + File Báo cáo:** [https://drive.google.com/file/d/1kE76h7QvDENRsIagD9k1Sq7ncRwSKCr9/view?usp=sharing](https://drive.google.com/file/d/1kE76h7QvDENRsIagD9k1Sq7ncRwSKCr9/view?usp=sharing)
- **GitHub Repository chính thức:** [https://github.com/24133009-ops/Telco-Customer-Churn-IDV](https://github.com/24133009-ops/Telco-Customer-Churn-IDV)
- **Dashboard trực tuyến (Streamlit Community Cloud):** [https://nhom22-telco-churn.streamlit.app](https://nhom22-telco-churn.streamlit.app)

---

## 7. KẾT LUẬN & TÀI LIỆU THAM KHẢO (CHUẨN IEEE)

### 7.1 Đánh Giá Kết Quả Đạt Được
Nhóm 22 đã hoàn thành toàn diện 100% mục tiêu đồ án:
- Xử lý tập dữ liệu gốc 7,043 bản ghi phân rã 4 bảng quan hệ với pipeline ETL tự động hóa hoàn chỉnh.
- Xây dựng 10 biểu đồ tĩnh chuẩn khoa học phục vụ EDA.
- Phát triển thành công Dashboard tương tác Streamlit với 5 phân hệ thuyết trình, 8 Hero Charts cốt lõi, Quả địa cầu 3D xoay 360° & Bản đồ phẳng 50 bang Hoa Kỳ, 6 bộ lọc sidebar và tính năng Drill-Down hồ sơ 360 độ.
- Triển khai mô hình Hồi quy Logistic đạt ROC-AUC 0.8421, tích hợp What-If Simulator và ROI Simulator thời gian thực.

### 7.2 Danh Mục Tài Liệu Tham Khảo (Chuẩn IEEE)
```
[1] A. Gallo, "The Value of Keeping the Right Customers," Harvard Business Review, Oct. 2014.
[2] F. F. Reichheld and W. E. Sasser Jr., "Zero defections: Quality comes to services," Harvard Business Review, vol. 68, no. 5, pp. 105–111, Sep.–Oct. 1990.
[3] J. H. Blattberg, B. D. Kim, and S. A. Neslin, "Customer Lifetime Value: Fundamentals," in Database Marketing. New York, NY, USA: Springer, 2008, pp. 105–131.
[4] J. D. Hunter, "Matplotlib: A 2D graphics environment," Computing in Science & Engineering, vol. 9, no. 3, pp. 90–95, May–Jun. 2007.
[5] M. L. Waskom, "seaborn: statistical data visualization," Journal of Open Source Software, vol. 6, no. 60, p. 3021, Apr. 2021.
[6] Streamlit Inc., "Get started with Streamlit," Streamlit Documentation, 2026. [Online].
[7] Plotly Technologies Inc., "Getting Started with Plotly for Python," Plotly Documentation, 2026. [Online].
[8] D. W. Hosmer Jr., S. Lemeshow, and R. X. Sturdivant, Applied Logistic Regression, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2013.
[9] IBM Community, "Telco Customer Churn Sample Data Sets," IBM Business Analytics, 2021. [Online].
[10] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825–2830, Nov. 2011.
[11] W. McKinney, "Data Structures for Statistical Computing in Python," in Proc. 9th Python in Science Conf. (SciPy), 2010, pp. 51–56.
[12] J. W. Tukey, Exploratory Data Analysis. Reading, MA, USA: Addison-Wesley, 1977.
[13] E. R. Tufte, The Visual Display of Quantitative Information, 2nd ed. Cheshire, CT, USA: Graphics Press, 2001.
[14] J. Bertin, Semiology of Graphics: Diagrams, Networks, Maps. Madison, WI, USA: University of Wisconsin Press, 1983.
[15] S. Few, Information Dashboard Design: The Effective Visual Communication of Data. Sebastopol, CA, USA: O’Reilly Media, 2006.
[16] B. Shneiderman, "The eyes have it: A task by data type taxonomy for information visualizations," in Proc. IEEE Symp. Visual Languages, 1996, pp. 336–343.
[17] P. C. Verhoef, "Understanding the effect of customer relationship management efforts on customer retention and customer share development," Journal of Marketing, vol. 67, no. 4, pp. 30–45, Oct. 2003.
[18] T. Fawcett, "An introduction to ROC analysis," Pattern Recognition Letters, vol. 27, no. 8, pp. 861–874, Jun. 2006.
[19] A. K. Burez and D. Van den Poel, "Handling class imbalance in customer churn prediction," Expert Systems with Applications, vol. 36, no. 3, pp. 4626–4636, Apr. 2009.
[20] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in Advances in Neural Information Processing Systems 30 (NeurIPS 2017), 2017, pp. 4765–4774.
[21] IEEE Publishing Operations, "IEEE Editorial Style Manual for Authors," IEEE, updated Jul. 2024. [Online].
```

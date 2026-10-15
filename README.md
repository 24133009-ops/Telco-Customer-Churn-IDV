# 📡 Telco Customer Churn - Interactive Data Visualization (IDV)

> **Môn học:** Tương Tác Dữ Liệu Trực Quan (IDV)  
> **Trường:** Đại học Công Nghệ Kỹ thuật TP.HCM (HCMUTE)  
> **Nhóm:** Nhóm 22  
> **Đề Tài** 5
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

- **Dashboard Trực Tuyến:** (https://nhom22-telco-churn.streamlit.app)
- **Video Demo Đồ Án:**    https://youtu.be/TpKI7MAMJtM
- **GitHub Repository:** (https://github.com/24133009-ops/Telco-Customer-Churn-IDV)

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
│   ├── BAO_CAO_DO_AN_NHOM_22.md # Báo cáo đồ án chi tiết (Markdown)
│   └── TRINH_BAY_TIEN_XU_LY_VA_HOI_QUY.md # Tài liệu tóm tắt thuyết minh nhanh cho giảng viên
├── requirements.txt         # Danh mục thư viện phụ thuộc
└── README.md
```

---

## 🔬 1. QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING PIPELINE)

Toàn bộ quy trình được tự động hóa tại file mã nguồn [`src/data_pipeline.py`](src/data_pipeline.py), bao gồm 4 công đoạn cốt lõi:

```
[4 Bảng Thô RDBMS] ──> [Inner Join (customerID)] ──> [Data Cleaning & Imputation] ──> [Outlier Detection (IQR)] ──> [Feature Engineering] ──> [telco_churn_clean.csv]
```

### 1.1 Phân Rã & Kết Nối Dữ Liệu Quan Hệ (Relational Database Modeling)
* **Thao tác thực hiện:**
  * Bộ dữ liệu gốc 7,043 bản ghi được phân rã thành **4 bảng dữ liệu quan hệ** chuẩn hóa đặt tại `data/raw/`:
    1. `telco_demographics.csv`: Thuộc tính nhân khẩu học và tọa độ địa lý 50 tiểu bang Hoa Kỳ.
    2. `telco_services.csv`: Danh mục 10 dịch vụ viễn thông (thoại, internet, bảo mật, streaming...).
    3. `telco_contracts.csv`: Loại hợp đồng cam kết, phương thức thanh toán, chu kỳ cước.
    4. `telco_churn_status.csv`: Nhãn mục tiêu `Churn`, lý do rời mạng và điểm hài lòng CSAT.
  * Thực hiện **Inner Join liên tiếp 4 bảng qua khóa chính `customerID`**.
* **Giải thích lý do xử lý:**
  * **Chuẩn hóa RDBMS (3NF):** Trong môi trường doanh nghiệp thực tế, dữ liệu viễn thông luôn được lưu trữ phân tán ở các hệ thống nghiệp vụ khác nhau (CRM, Billing, Network NOC). Phân tách và ghép nối bằng khóa chính đảm bảo tính toàn vẹn dữ liệu, đạt tỷ lệ khớp nối **100% (7,043 dòng)**, không làm phát sinh bản ghi trùng hay mất mát dữ liệu.
  * **Phục vụ trực quan hóa địa lý 50 bang:** Bổ sung trường tọa độ (`Latitude`, `Longitude`), mã bang (`StateCode`), tên bang (`StateName`) theo trọng số dân số thực tế để kích hoạt Bản đồ Quả địa cầu 3D xoay 360° và Bản đồ 2D US Choropleth.

### 1.2 Làm Sạch Dữ Liệu (Data Cleaning & Imputation)
* **Chuẩn hóa chuỗi (String Stripping):**
  * Quét toàn bộ cột kiểu chuỗi (`object`) và áp dụng `.str.strip()` để triệt tiêu ký tự khoảng trắng thừa đầu/cuối.
  * *Lý do:* Ngăn chặn lỗi phân mảnh dữ liệu khi thực hiện Group-by, Filter hoặc hiển thị nhãn trên biểu đồ.
* **Xử lý giá trị khuyết thiếu ở `TotalCharges`:**
  * Cột `TotalCharges` trong dữ liệu gốc có **11 dòng chứa chuỗi khoảng trắng `' '`**, khiến pandas nhận diện nhầm là kiểu dữ liệu văn bản (`object`).
  * Sử dụng `pd.to_numeric(..., errors='coerce')` để chuyển đổi chuỗi rỗng thành `NaN`.
  * **Điền khuyết thiếu bằng logic nghiệp vụ:** Gán `TotalCharges = MonthlyCharges * tenure`. Với 11 khách hàng này có `tenure == 0`, kết quả được gán chính xác là **`0.0 USD`**.
  * *Lý do:* 11 khách hàng này là **thuê bao mới đăng ký trong tháng đầu tiên (`tenure = 0`)**, chưa trải qua kỳ đối soát cước nào nên tổng cước phát sinh thực tế là 0. Việc gán giá trị theo bản chất kế toán viễn thông giúp **bảo toàn trọn vẹn 100% cỡ mẫu (7,043 khách hàng)** mà không cần phải xóa dòng (drop row).
* **Chuẩn hóa trường Ngày tháng (Date/Time Parsing):**
  * Quy đổi thâm niên `tenure` thành ngày kích hoạt hợp đồng `ContractStartDate` (định dạng chuẩn `YYYY-MM-DD`) dựa trên mốc tham chiếu (`2026-10-01`), đồng thời tính toán số ngày hoạt động `DaysActive`.
  * *Lý do:* Cho phép Dashboard phân tích nhóm thuần tập theo thời gian (Cohort Retention Curve) và lọc dữ liệu linh hoạt theo mốc ngày tháng.
* **Kiểm định ngoại lai bằng phương pháp IQR (Interquartile Range):**
  * Áp dụng trên 3 biến định lượng: `MonthlyCharges`, `TotalCharges`, `tenure`.
  * Tính $IQR = Q_3 - Q_1$, biên dưới $Q_1 - 1.5 \times IQR$, biên trên $Q_3 + 1.5 \times IQR$.
  * *Lý do:* Xác thực độ tin cậy của dữ liệu; kết quả kiểm định cho thấy dải cước ($18.25 - $118.75/tháng) và thâm niên (0 - 72 tháng) hoàn toàn nằm trong giới hạn thực tế của ngành viễn thông, không có điểm dị biệt làm sai lệch mô hình.

### 1.3 Kỹ Thuật Trích Xuất Đặc Trưng Mới (Feature Engineering)
Nhóm đã trích xuất 6 trường dữ liệu tính toán mới giúp làm sâu sắc thêm năng lực phân tích hành vi:

| Đặc trưng mới | Công thức / Quy tắc tính | Ý nghĩa nghiệp vụ & Lý do tạo |
| :--- | :--- | :--- |
| **`TenureGroup`** | Rời rạc hóa `tenure` thành 5 giỏ: `0-12 Tháng`, `13-24 Tháng`, `25-48 Tháng`, `49-60 Tháng`, `>60 Tháng`. | Phân tích nhóm thuần tập vòng đời; làm sáng tỏ hiện tượng **"First-Year Churn Trap"** (rủi ro rời mạng tập trung cao nhất ở năm đầu tiên). |
| **`TotalServicesSubscribed`** | Đếm tổng số dịch vụ khách hàng kích hoạt (Phone + 6 dịch vụ GTGT). Thang điểm 0 - 7. | Đo lường mức độ thâm nhập dịch vụ. Số lượng dịch vụ sử dụng càng nhiều thì **Chi phí chuyển đổi (Switching Cost)** càng cao, giảm nguy cơ rời mạng. |
| **`HasProtectionPackage`** | Cờ nhị phân: `Có gói bảo vệ` (nếu dùng OnlineSecurity, Backup, DeviceProtection hoặc TechSupport) vs `Không gói bảo vệ`. | Chứng minh vai trò của dịch vụ hỗ trợ & an toàn kỹ thuật như một **"chiếc mỏ neo" giữ chân khách hàng** (giảm hơn 60% tỷ lệ Churn). |
| **`CalculatedAvgMonthly` & `ChargeDeviation`** | $Avg = \frac{TotalCharges}{tenure}$<br>$Deviation = MonthlyCharges - Avg$ | Đo lường mức độ biến động cước phí tháng gần nhất so với lịch sử để phát hiện hiện tượng **"Sốc cước phí" (Bill Shock)** khiến khách hàng bức xúc hủy dịch vụ. |
| **`CLV_Category`** | Phân vị `TotalCharges` thành 4 hạng: Bronze, Silver, Gold, Platinum/VIP. | Cung cấp dữ liệu phân khúc phục vụ **Ma trận Giá trị vs Rủi ro** (Hero Chart 5) và tối ưu hóa ngân sách chiến dịch giữ chân khách hàng (ROI Simulator). |
| **`ChurnNumeric`** | Ánh xạ nhãn: `Yes -> 1`, `No -> 0`. | Biến số nhị phân phục vụ tính toán ma trận tương quan Pearson và làm biến mục tiêu cho thuật toán học máy. |

---

## 🤖 2. MÔ HÌNH HỒI QUY LOGISTIC & PIPELINE MACHINE LEARNING

Mã nguồn triển khai tại [`src/model_training.py`](src/model_training.py), được huấn luyện và lưu trữ dưới dạng artifact tại `models/telco_logistic_model.pkl`.

### 2.1 Cơ Sở Lý Thuyết & Công Thức Toán Học
Bài toán dự báo khách hàng rời mạng là bài toán **Phân loại nhị phân (Binary Classification)** với $Y \in \{0, 1\}$. Nhóm lựa chọn **Mô hình Hồi quy Logistic (Logistic Regression)** - một dạng mô hình tuyến tính tổng quát (*Generalized Linear Model - GLM*) vì vừa đem lại độ chính xác cao vừa có **khả năng giải thích định lượng minh bạch (Explainable AI / White-Box Model)** cho các cấp quản lý viễn thông.

* **Hàm kích hoạt Sigmoid chuyển đổi tổ hợp tuyến tính thành xác suất:**
  $$P(Y = 1 | X) = \sigma(z) = \frac{1}{1 + e^{-z}} \quad \text{với} \quad z = \beta_0 + \sum_{j=1}^p \beta_j X_j$$
* **Hàm mất mát Log-Loss có số hạng điều chuẩn $L_2$ (Ridge Regularization):**
  $$J(\beta) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i) \right] + \frac{1}{2C} \|\beta\|_2^2$$
  *(Tham số điều chuẩn $C = 1.0$, bộ giải tối ưu hóa gradient `lbfgs`, số vòng lặp tối đa `max_iter = 1000`)*.

### 2.2 Quy Trình Tiền Xử Lý Dành Riêng Cho Machine Learning (Scikit-Learn Pipeline)
Để đảm bảo mô hình vận hành chuẩn xác và tích hợp mượt mà vào Dashboard tương tác thời gian thực:

1. **Phân chia tập dữ liệu có phân tầng (Stratified Train-Test Split 80/20):**
   * Sử dụng `stratify=y` với `random_state=42` chia thành: Tập Train (**5,634 mẫu**) và Tập Test (**1,409 mẫu**).
   * *Lý do:* Tỷ lệ nhãn Churn trong tập dữ liệu bị mất cân bằng nhẹ (~26.5% Churn vs 73.5% Non-Churn). Kỹ thuật phân tầng bảo đảm tỷ lệ phân phối nhãn ở cả 2 tập hoàn toàn đồng nhất, tránh hiện tượng lệch dữ liệu (Data Drift).
2. **Chuẩn hóa biến số định lượng bằng `StandardScaler`:**
   * Áp dụng biến đổi $Z = \frac{X - \mu}{\sigma}$ trên 5 biến số liên tục (`tenure`, `MonthlyCharges`, `TotalCharges`, `TotalServicesSubscribed`, `CalculatedAvgMonthly`).
   * *Lý do:* Giúp thuật toán tối ưu hóa L-BFGS hội tụ nhanh chóng; đồng thời ngăn chặn biến có độ lớn hàng nghìn USD (`TotalCharges`) lấn át các biến có miền giá trị nhỏ (`tenure` từ 0 - 72).
3. **Mã hóa biến phân loại One-Hot Encoding với tham số `drop='first'`:**
   * Mã hóa toàn bộ các thuộc tính định danh danh mục (`Contract`, `InternetService`, `PaymentMethod`,...).
   * *Lý do bắt buộc:* Thiết lập `drop='first'` giúp loại bỏ cột cơ sở đầu tiên, **triệt tiêu hoàn toàn hiện tượng Đa cộng tuyến hoàn hảo (Multicollinearity / Dummy Variable Trap)**. Đây là điều kiện tiên quyết trong kinh tế lượng để ma trận hiệp phương sai khả nghịch, đảm bảo các hệ số hồi quy Log-Odds $\beta$ và Tỷ số chênh (**Odds Ratio = $e^\beta$**) có ý nghĩa thống kê và diễn giải được.
4. **Đóng gói khép kín qua `ColumnTransformer` & `Pipeline`:**
   * *Lý do:* Tránh tuyệt đối hiện tượng **Rò rỉ dữ liệu (Data Leakage)** từ tập Test sang tập Train. Pipeline này được lưu lại để phục vụ trực tiếp cho công cụ **What-If Real-Time Simulator** trên Dashboard Streamlit (tham số nhập vào được tự động scale và encode đúng chuẩn).

### 2.3 Hiệu Năng Mô Hình Trên Tập Kiểm Định Độc Lập (Test Set: 1,409 mẫu)

| Chỉ số đánh giá | Giá trị đạt được | Nhận xét chuyên môn |
| :--- | :---: | :--- |
| **Độ chính xác (Accuracy)** | **80.77%** | Tỷ lệ dự báo đúng hơn 8 trên 10 trường hợp khách hàng. |
| **Chỉ số ROC-AUC** | **0.8421** | Năng lực phân biệt khách hàng rời mạng vs ở lại ở mức **Xuất sắc** (Chuẩn phân loại y tế & tài chính thường yêu cầu > 0.80). |
| **Độ chuẩn xác (Precision)** | **66.14%** | Trong số các khách hàng mô hình gắn cờ nguy cơ Churn, có 66.14% thực sự rời mạng. |
| **Độ nhạy bắt Churn (Recall)** | **56.42%** | Bắt trúng hơn 56% tổng lượng khách hàng thực tế sẽ rời mạng. |
| **F1-Score** | **60.89%** | Điểm trung bình điều hòa cân đối giữa Precision và Recall. |

### 2.4 Bảng Trọng Số Hồi Quy & Tỷ Số Chênh (Odds Ratios - Phân Tích Định Lượng)
Mô hình cung cấp khả năng diễn giải nguyên nhân gốc rễ (Root-Cause Analysis) thông qua Tỷ số chênh $\text{Odds Ratio} = e^\beta$:

* **Top Yếu Tố Làm Tăng Nguy Cơ Rời Mạng Cao Nhất (Churn Drivers):**
  1. `InternetService_Fiber optic`: $\beta = +1.1795 \implies \mathbf{Odds\ Ratio = 3.253\times}$ (Khách dùng cáp quang có **nguy cơ Churn cao gấp 3.25 lần** so với dùng DSL).
  2. `Contract_Month-to-month`: $\beta = +0.8421 \implies \mathbf{Odds\ Ratio = 2.321\times}$ (Hợp đồng từng tháng làm **tăng 132% rủi ro Churn**).
  3. `PaymentMethod_Electronic check`: $\beta = +0.3837 \implies \mathbf{Odds\ Ratio = 1.468\times}$ (Thanh toán qua séc điện tử làm **tăng 46.8% rủi ro Churn** do ma sát thanh toán).
  4. `PaperlessBilling_Yes`: $\beta = +0.3341 \implies \mathbf{Odds\ Ratio = 1.397\times}$.
* **Top Yếu Tố Giúp Giữ Chân Khách Hàng Mạnh Nhất (Retention Anchors):**
  1. `Contract_Two year`: $\beta = -1.3242 \implies \mathbf{Odds\ Ratio = 0.266\times}$ (Cam kết 2 năm giúp **giảm 73.4% rủi ro rời mạng**).
  2. `tenure` (Thâm niên): $\beta = -1.2405 \implies \mathbf{Odds\ Ratio = 0.289\times}$ (Thâm niên càng cao, rủi ro rời mạng **giảm 71.1%**).
  3. `Contract_One year`: $\beta = -0.6888 \implies \mathbf{Odds\ Ratio = 0.502\times}$ (Giảm 49.8% rủi ro rời mạng).
  4. `OnlineSecurity_Yes`: $\beta = -0.4778 \implies \mathbf{Odds\ Ratio = 0.620\times}$ (Có dịch vụ bảo mật giúp **giảm 38.0% rủi ro Churn**).
  5. `TechSupport_Yes`: $\beta = -0.3820 \implies \mathbf{Odds\ Ratio = 0.682\times}$ (Có hỗ trợ kỹ thuật giúp **giảm 31.8% rủi ro Churn**).

### 2.5 Ứng Dụng Thực Tiễn Trên Dashboard Tương Tác
* **Trình mô phỏng What-If Simulator (Tab 3):** Tích hợp trực tiếp `Pipeline` đã huấn luyện. Khi người dùng thay đổi 8 thông số đầu vào trên giao diện, mô hình lập tức suy luận xác suất Churn và hiển thị trên **Kim đồng hồ Gauge Chart 3 dải màu** (<35% An toàn, 35-60% Cảnh báo, >=60% Nguy hiểm).
* **Mô phỏng giảm rủi ro sau can thiệp:** Thử nghiệm đổi hợp đồng sang 1 năm hoặc tặng gói TechSupport/Security, kim đo xác suất Churn giảm lập tức từ vùng Đỏ (78%) xuống vùng Xanh (<25%), định lượng trực tiếp giá trị cứu vãn doanh thu hàng năm.

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

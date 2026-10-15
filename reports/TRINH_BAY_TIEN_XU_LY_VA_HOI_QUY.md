# 🎯 TÀI LIỆU THUYẾT MINH NHANH: TIỀN XỬ LÝ DỮ LIỆU & MÔ HÌNH HỒI QUY
## ĐỒ ÁN: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN (IDV) - ĐỀ TÀI 5 - NHÓM 22
> **Dành cho buổi báo cáo / Demo trực tiếp với Giảng viên**  
> *Mã nguồn tham chiếu:* [`src/data_pipeline.py`](file:///c:/Tương%20Tác%20dữ%20liệu%20trực%20quan/src/data_pipeline.py) & [`src/model_training.py`](file:///c:/Tương%20Tác%20dữ%20liệu%20trực%20quan/src/model_training.py)

---

## 📌 PHẦN 1: QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING)

### 1. Sơ đồ Pipeline ETL 4 bước
```text
[4 Bảng Thô RDBMS] 
       │
       ▼ (1. Inner Join theo customerID - Khớp 100% 7,043 bản ghi)
[Bảng Dữ Liệu Hợp Nhất] 
       │
       ▼ (2. Làm sạch: Strip chuỗi, Xử lý missing TotalCharges = 0, Parse ngày tháng)
[Kiểm Định Ngoại Lai IQR] 
       │
       ▼ (3. Outlier check: MonthlyCharges, TotalCharges, tenure - Không có dị biệt phi lý)
[Feature Engineering] 
       │
       ▼ (4. Tạo 6 đặc trưng mới: TenureGroup, TotalServices, HasProtection, Deviation, CLV, ChurnNumeric)
[telco_churn_clean.csv] (Đưa vào Dashboard & Model)
```

---

### 2. Các công việc đã làm & Giải thích lý do (Chuẩn bị trả lời thầy)

| Công việc thực hiện | Cách xử lý cụ thể | Tại sao lại xử lý như vậy? (Lý do nghiệp vụ & kỹ thuật) |
| :--- | :--- | :--- |
| **1. Phân rã & Nối 4 bảng quan hệ** | Tách dữ liệu thành 4 bảng CSV (`demographics`, `services`, `contracts`, `churn_status`) và `Inner Join` qua khóa chính `customerID`. | • Chuẩn hóa theo thiết kế **RDBMS (3NF)** thực tế trong doanh nghiệp viễn thông.<br>• Đảm bảo tính toàn vẹn 100% (7,043 dòng), không mất mát hay trùng lặp bản ghi.<br>• Bổ sung tọa độ và mã 50 tiểu bang Hoa Kỳ để vẽ **Địa cầu 3D & Bản đồ 2D US**. |
| **2. Làm sạch chuỗi (String Strip)** | Dùng `.str.strip()` trên toàn bộ các cột văn bản. | Triệt tiêu khoảng trắng thừa vô hình ở đầu/cuối chuỗi, ngăn ngừa lỗi phân mảnh khi Group-by và lọc trên Dashboard. |
| **3. Xử lý Missing ở `TotalCharges`** | • `pd.to_numeric(errors='coerce')` ép 11 dòng rỗng thành `NaN`.<br>• Gán `TotalCharges = MonthlyCharges * tenure` (bằng **`0.0 USD`** vì `tenure == 0`). | • **Bản chất nghiệp vụ:** 11 khách này là **thuê bao mới ký hợp đồng trong tháng đầu tiên**, chưa kết thúc chu kỳ thanh toán nên tổng tiền tích lũy bằng 0.<br>• **Bảo toàn cỡ mẫu:** Không dùng `dropna()` vì sẽ làm mất 11 khách hàng mới này (vốn là đối tượng rủi ro cao nhất cần theo dõi). |
| **4. Chuẩn hóa Ngày tháng (Date Parsing)** | Sinh cột `ContractStartDate` dạng `YYYY-MM-DD` từ mốc hiện tại trừ đi `tenure * 30.4375` ngày. | Chuyển thâm niên từ dạng số nguyên (tháng) sang chuỗi thời gian thực (Time-Series) để Dashboard hỗ trợ phân tích Cohort và lọc theo ngày. |
| **5. Kiểm định ngoại lai (IQR)** | Tính $IQR = Q_3 - Q_1$, biên dưới $Q_1 - 1.5IQR$, biên trên $Q_3 + 1.5IQR$. | Kiểm tra tính chuẩn xác của dữ liệu định lượng; xác nhận dải cước ($18 - $118) và thâm niên (0 - 72 tháng) hoàn toàn hợp lệ, không có dữ liệu rác. |
| **6. Trích xuất 6 đặc trưng mới (Feature Engineering)** | • `TenureGroup`: Giỏ thâm niên 5 nhóm.<br>• `TotalServicesSubscribed`: Đếm tổng số dịch vụ đăng ký (0-7).<br>• `HasProtectionPackage`: Cờ bảo vệ an toàn mạng.<br>• `ChargeDeviation`: Độ lệch cước gần nhất so với TB.<br>• `CLV_Category`: Phân 4 hạng giá trị vòng đời.<br>• `ChurnNumeric`: Nhị phân 0/1. | • Phát hiện hiện tượng **First-Year Churn Trap**.<br>• Đo lường **Chi phí chuyển đổi (Switching Cost)**: Dùng càng nhiều dịch vụ càng ít rời mạng.<br>• Phát hiện hiện tượng **Sốc cước phí (Bill Shock)**.<br>• Phục vụ **Ma trận Giá trị vs Rủi ro** (Hero Chart 5). |

---

## 📌 PHẦN 2: MÔ HÌNH HỒI QUY DỰ BÁO (LOGISTIC REGRESSION)

### 1. Tại sao dùng Hồi quy Logistic (Mô hình Hồi quy Tuyến tính dạng Phân loại)?
* Dự báo Churn là bài toán **Phân loại nhị phân ($Y \in \{0, 1\}$)**.
* Nếu dùng Hồi quy tuyến tính thông thường (Ordinary Least Squares - OLS), giá trị dự báo có thể vượt ngoài đoạn $[0, 1]$ (ví dụ ra $-0.3$ hoặc $1.4$), vi phạm tiên đề xác suất.
* **Hồi quy Logistic** là mô hình tuyến tính tổng quát (GLM) đưa tổ hợp tuyến tính $z = \beta_0 + \sum \beta_j X_j$ qua **hàm Sigmoid** để ép giá trị về khoảng xác suất chuẩn xác $[0, 1]$:
  $$P(Y = 1 | X) = \frac{1}{1 + e^{-(\beta_0 + \sum \beta_j X_j)}}$$
* **Ưu điểm vượt trội:** Là **mô hình giải thích được (White-Box / Explainable AI)**. Nhà mạng không chỉ biết khách nào sắp rời mạng mà còn biết **chính xác lý do vì sao** thông qua Tỷ số chênh (**Odds Ratio**).

---

### 2. Tiền xử lý dữ liệu cho Mô hình (Scikit-Learn Pipeline)
* **Stratified Split 80/20:** Phân chia tập Train (5,634 mẫu) và Test (1,409 mẫu) có bảo toàn tỷ lệ nhãn Churn (~26.5%) ở cả 2 tập, chống lệch dữ liệu.
* **StandardScaler:** Chuẩn hóa $Z = (X - \mu) / \sigma$ trên các biến số (`tenure`, `MonthlyCharges`, `TotalCharges`...). Giúp thuật toán tối ưu `lbfgs` hội tụ nhanh và tránh biến tiền lớn áp đảo biến nhỏ.
* **One-Hot Encoding với `drop='first'`:** Bắt buộc dùng `drop='first'` để **triệt tiêu hiện tượng Đa cộng tuyến hoàn hảo (Multicollinearity / Dummy Variable Trap)**, giúp ma trận khả nghịch và hệ số hồi quy $\beta$ có ý nghĩa thống kê chuẩn mực.
* **Pipeline khép kín:** Đóng gói toàn bộ quá trình biến đổi để **tránh rò rỉ dữ liệu (Data Leakage)** và phục vụ tích hợp trực tiếp vào What-If Simulator trên web.

---

### 3. Hiệu năng mô hình (Tập Test độc lập 1,409 mẫu)

$$\mathbf{ROC\text{-}AUC = 0.8421} \quad | \quad \mathbf{Accuracy = 80.77\%} \quad | \quad \mathbf{Precision = 66.14\%} \quad | \quad \mathbf{Recall = 56.42\%}$$

* Chỉ số **ROC-AUC = 0.8421** chứng minh khả năng phân biệt giữa khách hàng ở lại và khách hàng rời mạng ở mức **Rất Tốt** (vượt chuẩn thông thường 0.80).

---

### 4. Kết quả định lượng: Đòn bẩy rủi ro & Yếu tố bảo vệ (Odds Ratio)

$$\text{Odds Ratio} = e^\beta$$

#### 🚨 Nhóm kích hoạt rủi ro rời mạng (Churn Drivers):
1. **Dùng cáp quang (`InternetService_Fiber optic`):** Odds Ratio = **3.25x** $\to$ Nguy cơ rời mạng **tăng 225%** so với DSL (do cước cao và thiếu gói bảo vệ đi kèm).
2. **Hợp đồng từng tháng (`Contract_Month-to-month`):** Odds Ratio = **2.32x** $\to$ Rủi ro rời mạng **tăng 132%** so với hợp đồng dài hạn.
3. **Thanh toán qua séc điện tử (`PaymentMethod_Electronic check`):** Odds Ratio = **1.47x** $\to$ Tăng **46.8% rủi ro** do tâm lý ma sát khi chi trả thủ công mỗi tháng.

#### 🛡️ Nhóm bảo vệ giữ chân khách hàng (Retention Anchors):
1. **Ký hợp đồng 2 năm (`Contract_Two year`):** Odds Ratio = **0.27x** $\to$ Giảm **73.4% rủi ro Churn**.
2. **Thâm niên (`tenure`):** Odds Ratio = **0.29x** $\to$ Càng gắn bó lâu, rủi ro Churn **giảm 71.1%**.
3. **Ký hợp đồng 1 năm (`Contract_One year`):** Odds Ratio = **0.50x** $\to$ Giảm **49.8% rủi ro Churn**.
4. **Có dịch vụ an toàn mạng (`OnlineSecurity`):** Odds Ratio = **0.62x** $\to$ Giảm **38.0% rủi ro Churn**.
5. **Có hỗ trợ kỹ thuật (`TechSupport`):** Odds Ratio = **0.68x** $\to$ Giảm **31.8% rủi ro Churn**.

---

## 💡 BỘ CÂU HỎI THƯỜNG GẶP CỦA GIẢNG VIÊN (FAQ PHẢN BIỆN)

> **Câu 1: Tại sao không dùng Random Forest hay XGBoost mà lại dùng Logistic Regression?**  
> **Trả lời:** Trong quản trị doanh nghiệp viễn thông (đặc biệt là báo cáo C-Level), tính **giải thích được (Explainability)** quan trọng không kém độ chính xác. Logistic Regression cung cấp chỉ số **Odds Ratio** trực tiếp giúp Giám đốc Kinh doanh biết chính xác chính sách nào (như ép chuyển sang Auto-Pay hay tặng TechSupport) sẽ giảm được bao nhiêu % rủi ro. Ngoài ra, mô hình đạt **ROC-AUC 0.8421** và **Accuracy 80.77%**, hoàn toàn đáp ứng tốt bài toán mà lại tính toán siêu nhanh (<5ms) trên Web Dashboard.

> **Câu 2: Tại sao 11 dòng TotalCharges bị khuyết thiếu không xóa đi mà lại gán bằng 0?**  
> **Trả lời:** Vì 11 dòng này đều có `tenure = 0` (khách hàng mới đăng ký trong tháng). Về mặt kế toán viễn thông, khách chưa qua kỳ lập hóa đơn đầu tiên nên cước lũy kế thực tế là 0.0 USD. Nếu xóa dòng thì sẽ làm mất đi phân khúc khách hàng mới tinh - vốn là phân khúc quan trọng nhất của bài toán Churn (*First-Year Churn Trap*).

> **Câu 3: Tại sao OneHotEncoder phải đặt `drop='first'`?**  
> **Trả lời:** Để tránh hiện tượng đa cộng tuyến hoàn hảo (*Dummy Variable Trap*). Nếu một biến có $k$ nhóm và ta giữ nguyên cả $k$ cột thì tổng các cột luôn bằng 1, làm cho ma trận $X^T X$ không khả nghịch, khiến việc ước lượng hệ số $\beta$ trong Hồi quy Logistic bị sai lệch.

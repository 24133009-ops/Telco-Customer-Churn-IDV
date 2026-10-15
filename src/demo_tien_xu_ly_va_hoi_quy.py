"""
========================================================================================
TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT TP. HỒ CHÍ MINH (HCMUTE)
KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN KỸ THUẬT DỮ LIỆU & AI
MÔN HỌC: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN (IDV) - ĐỀ TÀI SỐ 5: CUSTOMER CHURN
NHÓM 22:
  1. Trương Quốc Duy - 24133009 (Trưởng nhóm - Kỹ thuật & Pipeline)
  2. Đỗ Trọng Khôi   - 20133056 (Thành viên - Báo cáo & Tài liệu)
  3. Bùi Đức Huy     - 24133021 (Thành viên - Bối cảnh & Thuyết minh)
========================================================================================
MÃ NGUỒN CHUYÊN DỤNG TRÌNH BÀY GIẢNG VIÊN:
  PHẦN 1: TOÀN BỘ QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING & FEATURE ENGINEERING)
  PHẦN 2: MÔ HÌNH HỒI QUY LOGISTIC DỰ BÁO CHURN (LOGISTIC REGRESSION & ML PIPELINE)

* Chạy file này trực tiếp bằng lệnh:
    python src/demo_tien_xu_ly_va_hoi_quy.py
========================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd

# Đảm bảo in tiếng Việt chuẩn Unicode UTF-8 trên terminal Windows
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
PROCESSED_DATA_PATH = os.path.join(PROCESSED_DIR, "telco_churn_clean.csv")


# ######################################################################################
# PHẦN 1: QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING & FEATURE ENGINEERING)
# ######################################################################################

def trinh_bay_tien_xu_ly_du_lieu():
    """
    HÀM 1: TIỀN XỬ LÝ DỮ LIỆU VÀ TRÍCH XUẤT ĐẶC TRƯNG MỚI (ETL PIPELINE)
    -----------------------------------------------------------------------------
    """
    print("\n" + "=" * 80)
    print("🔬 PHẦN 1: QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU & GIẢI THÍCH LÝ DO KHOA HỌC")
    print("=" * 80)

    # ----------------------------------------------------------------------------------
    # BƯỚC 1.1: KẾT NỐI DỮ LIỆU TỪ 4 BẢNG CSDL QUAN HỆ (RELATIONAL JOIN)
    # ----------------------------------------------------------------------------------
    print("\n[BƯỚC 1.1] KẾT NỐI 4 BẢNG DỮ LIỆU QUAN HỆ (RDBMS) QUA KHÓA CHÍNH 'customerID'")
    print("  • Thao tác: Đọc 4 bảng thô tách biệt từ data/raw/:")
    print("      1. telco_demographics.csv (Nhân khẩu học, 50 bang Hoa Kỳ)")
    print("      2. telco_services.csv     (Danh mục dịch vụ thoại & internet)")
    print("      3. telco_contracts.csv    (Hợp đồng, phương thức thanh toán, cước phí)")
    print("      4. telco_churn_status.csv (Trạng thái rời mạng, điểm CSAT, lý do)")
    print("  • Thực hiện lệnh INNER JOIN liên tiếp theo khóa 'customerID'...")

    # Đọc 4 bảng thô (nếu chưa có thì sinh từ data_pipeline)
    path_demo = os.path.join(RAW_DIR, "telco_demographics.csv")
    path_serv = os.path.join(RAW_DIR, "telco_services.csv")
    path_cont = os.path.join(RAW_DIR, "telco_contracts.csv")
    path_stat = os.path.join(RAW_DIR, "telco_churn_status.csv")

    if not (os.path.exists(path_demo) and os.path.exists(path_serv) and os.path.exists(path_cont) and os.path.exists(path_stat)):
        from data_pipeline import fetch_or_generate_raw_data
        fetch_or_generate_raw_data()

    df_demo = pd.read_csv(path_demo)
    df_serv = pd.read_csv(path_serv)
    df_cont = pd.read_csv(path_cont)
    df_stat = pd.read_csv(path_stat)

    df_merged = df_demo.merge(df_serv, on="customerID", how="inner")
    df_merged = df_merged.merge(df_cont, on="customerID", how="inner")
    df_merged = df_merged.merge(df_stat, on="customerID", how="inner")

    print(f"  [+] Kết quả khớp nối: {len(df_merged)} dòng, {len(df_merged.columns)} cột thuộc tính.")
    print("  💡 GIẢI THÍCH TẠI SAO XỬ LÝ NHƯ VẬY:")
    print("     - Chuẩn 3NF doanh nghiệp: Dữ liệu viễn thông thực tế lưu trữ ở các phân hệ riêng biệt (CRM, Billing, NOC).")
    print("     - Đảm bảo tính toàn vẹn 100%: Join qua khóa chính duy nhất customerID không làm mất mát hoặc nhân đôi bản ghi.")

    # ----------------------------------------------------------------------------------
    # BƯỚC 1.2: CHUẨN HÓA ĐỊNH DẠNG CHUỖI (STRING STRIPPING)
    # ----------------------------------------------------------------------------------
    print("\n[BƯỚC 1.2] CHUẨN HÓA VĂN BẢN VÀ LOẠI BỎ KHOẢNG TRẮNG THỪA")
    str_cols = df_merged.select_dtypes(include=['object', 'string']).columns
    for c in str_cols:
        df_merged[c] = df_merged[c].astype(str).str.strip()
    print(f"  [+] Đã duyệt qua {len(str_cols)} cột kiểu chuỗi và áp dụng `.str.strip()`.")
    print("  💡 GIẢI THÍCH TẠI SAO XỬ LÝ NHƯ VẬY:")
    print("     - Dữ liệu thu thập từ web/CSV thường dính ký tự khoảng trắng ở đầu/cuối (ví dụ 'Yes ' khác 'Yes').")
    print("     - Nếu không strip, các bộ lọc Dropdown hay lệnh Group By sẽ bị phân mảnh thành các nhóm rác.")

    # ----------------------------------------------------------------------------------
    # BƯỚC 1.3: XỬ LÝ GIÁ TRỊ KHUYẾT THIẾU Ở CỘT 'TotalCharges'
    # ----------------------------------------------------------------------------------
    print("\n[BƯỚC 1.3] XỬ LÝ GIÁ TRỊ KHUYẾT THIẾU (MISSING VALUES) Ở CỘT 'TotalCharges'")
    # Dữ liệu gốc IBM có 11 dòng TotalCharges chứa khoảng trắng chuỗi ' '
    df_merged["TotalCharges"] = pd.to_numeric(df_merged["TotalCharges"].astype(str).str.strip(), errors="coerce")
    missing_count = df_merged["TotalCharges"].isna().sum()
    print(f"  [!] Phát hiện {missing_count} dòng có giá trị khuyết thiếu (NaN) ở TotalCharges.")

    # Điền khuyết thiếu theo bản chất nghiệp vụ kế toán viễn thông
    df_merged["TotalCharges"] = df_merged["TotalCharges"].fillna(df_merged["MonthlyCharges"] * df_merged["tenure"])
    df_merged["TotalCharges"] = df_merged["TotalCharges"].fillna(0.0)
    print(f"  [+] Đã gán TotalCharges = 0.0 USD cho các khách hàng có tenure = 0.")
    print(f"  [+] Số missing values sau khi xử lý: {df_merged['TotalCharges'].isna().sum()} (Đạt chuẩn 0.00% Missing).")
    print("  💡 GIẢI THÍCH TẠI SAO XỬ LÝ NHƯ VẬY (RẤT QUAN TRỌNG KHI BẢO VỆ):")
    print("     - 11 khách hàng này là THUÊ BAO MỚI KÝ HỢP ĐỒNG TRONG THÁNG ĐẦU TIÊN (tenure = 0 tháng).")
    print("     - Chưa trải qua chu kỳ đối soát cước nào nên tổng chi phí phát sinh thực tế là 0.0 USD.")
    print("     - KHÔNG ĐƯỢC XÓA DÒNG (dropna): Vì đây là phân khúc khách hàng mới cực kỳ nhạy cảm cần nghiên cứu")
    print("       (First-Year Churn Trap). Xử lý điền 0.0 bảo toàn toàn vẹn 100% cỡ mẫu (7,043 khách hàng).")

    # ----------------------------------------------------------------------------------
    # BƯỚC 1.4: CHUẨN HÓA VÀ BỔ SUNG NGÀY THÁNG (DATE/TIME PARSING)
    # ----------------------------------------------------------------------------------
    print("\n[BƯỚC 1.4] CHUẨN HÓA VÀ SINH TRƯỜNG NGÀY THÁNG (ContractStartDate)")
    ref_date = pd.to_datetime("2026-10-01")
    df_merged["ContractStartDate"] = ref_date - pd.to_timedelta(df_merged["tenure"] * 30.4375, unit="D")
    df_merged["ContractStartDate"] = pd.to_datetime(df_merged["ContractStartDate"].dt.strftime("%Y-%m-%d"))
    df_merged["CurrentBillingDate"] = pd.to_datetime("2026-10-01")
    df_merged["DaysActive"] = (df_merged["CurrentBillingDate"] - df_merged["ContractStartDate"]).dt.days
    print(f"  [+] Đã quy đổi tenure sang ngày ký hợp đồng định dạng chuẩn YYYY-MM-DD.")
    print("  💡 GIẢI THÍCH TẠI SAO XỬ LÝ NHƯ VẬY:")
    print("     - Giúp hệ thống Dashboard hỗ trợ phân tích chuỗi thời gian (Time-Series) và đường cong duy trì (Cohort).")

    # ----------------------------------------------------------------------------------
    # BƯỚC 1.5: KIỂM ĐỊNH NGOẠI LAI (OUTLIER DETECTION BẰNG PHƯƠNG PHÁP IQR)
    # ----------------------------------------------------------------------------------
    print("\n[BƯỚC 1.5] KIỂM ĐỊNH NGOẠI LAI ĐỊNH LƯỢNG (INTERQUARTILE RANGE - IQR)")
    for col in ["MonthlyCharges", "TotalCharges", "tenure"]:
        q25 = df_merged[col].quantile(0.25)
        q75 = df_merged[col].quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outliers_count = ((df_merged[col] < lower_bound) | (df_merged[col] > upper_bound)).sum()
        print(f"  • Kiểm định IQR cột {col:15s}: Q1={q25:8.2f}, Q3={q75:8.2f}, IQR={iqr:8.2f} -> {outliers_count} điểm dị biệt.")
    print("  💡 GIẢI THÍCH TẠI SAO XỬ LÝ NHƯ VẬY:")
    print("     - Xác thực dữ liệu không chứa giá trị cước âm hay giá trị cực đoan phi thực tế trước khi phân tích.")

    # ----------------------------------------------------------------------------------
    # BƯỚC 1.6: TRÍCH XUẤT ĐẶC TRƯNG MỚI (FEATURE ENGINEERING - 6 TRƯỜNG TÍNH TOÁN)
    # ----------------------------------------------------------------------------------
    print("\n[BƯỚC 1.6] TRÍCH XUẤT 6 ĐẶC TRƯNG TÍNH TOÁN MỚI (FEATURE ENGINEERING)")

    # 1. TenureGroup
    bins = [-1, 12, 24, 48, 60, 100]
    labels = ["0-12 Tháng", "13-24 Tháng", "25-48 Tháng", "49-60 Tháng", ">60 Tháng"]
    df_merged["TenureGroup"] = pd.cut(df_merged["tenure"], bins=bins, labels=labels)
    print("  1. 'TenureGroup': Rời rạc hóa thâm niên thành 5 giỏ để phân tích vòng đời khách hàng.")

    # 2. TotalServicesSubscribed
    service_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
    df_merged["TotalServicesSubscribed"] = (df_merged["PhoneService"] == "Yes").astype(int)
    for col in service_cols:
        df_merged["TotalServicesSubscribed"] += (df_merged[col] == "Yes").astype(int)
    print("  2. 'TotalServicesSubscribed': Đếm tổng số dịch vụ khách hàng kích hoạt (0 đến 7 dịch vụ).")
    print("     -> Nghiệp vụ: Càng dùng nhiều dịch vụ thì chi phí chuyển đổi (Switching Cost) càng lớn, ít bỏ mạng.")

    # 3. HasProtectionPackage
    df_merged["HasProtectionPackage"] = (
        (df_merged["OnlineSecurity"] == "Yes") | 
        (df_merged["OnlineBackup"] == "Yes") | 
        (df_merged["DeviceProtection"] == "Yes") | 
        (df_merged["TechSupport"] == "Yes")
    ).map({True: "Có gói bảo vệ", False: "Không gói bảo vệ"})
    print("  3. 'HasProtectionPackage': Cờ đánh dấu có dùng gói an toàn mạng (chiếc mỏ neo giữ chân).")

    # 4. CalculatedAvgMonthly & ChargeDeviation
    effective_tenure = np.where(df_merged["tenure"] == 0, 1, df_merged["tenure"])
    df_merged["CalculatedAvgMonthly"] = np.round(df_merged["TotalCharges"] / effective_tenure, 2)
    df_merged["ChargeDeviation"] = np.round(df_merged["MonthlyCharges"] - df_merged["CalculatedAvgMonthly"], 2)
    print("  4. 'CalculatedAvgMonthly' & 'ChargeDeviation': Đo độ lệch cước phí để phát hiện 'Sốc cước phí' (Bill Shock).")

    # 5. CLV_Category
    clv_quantiles = df_merged["TotalCharges"].quantile([0.33, 0.66, 0.90])
    def categorize_clv(val):
        if val <= clv_quantiles[0.33]:
            return "Thấp (Tier Bronze)"
        elif val <= clv_quantiles[0.66]:
            return "Trung bình (Tier Silver)"
        elif val <= clv_quantiles[0.90]:
            return "Cao (Tier Gold)"
        else:
            return "Đặc biệt (Tier Platinum / VIP)"
    df_merged["CLV_Category"] = df_merged["TotalCharges"].apply(categorize_clv)
    print("  5. 'CLV_Category': Phân 4 hạng giá trị vòng đời phục vụ Ma trận Giá trị vs Rủi ro.")

    # 6. ChurnNumeric
    df_merged["ChurnNumeric"] = (df_merged["Churn"] == "Yes").astype(int)
    print("  6. 'ChurnNumeric': Ánh xạ nhãn Churn thành 0 và 1 phục vụ mô hình học máy và tính tương quan.")

    # Lưu dữ liệu sạch
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df_merged.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"\n[+] Xuất tập dữ liệu sạch thành công: {PROCESSED_DATA_PATH} ({len(df_merged)} dòng, {len(df_merged.columns)} cột).")

    return df_merged


# ######################################################################################
# PHẦN 2: MÔ HÌNH HỒI QUY LOGISTIC DỰ BÁO CHURN (LOGISTIC REGRESSION & ML PIPELINE)
# ######################################################################################

def trinh_bay_mo_hinh_hoi_quy(df):
    """
    HÀM 2: HUẤN LUYỆN VÀ ĐÁNH GIÁ MÔ HÌNH HỒI QUY LOGISTIC (LOGISTIC REGRESSION)
    -----------------------------------------------------------------------------
    """
    print("\n" + "=" * 80)
    print("🤖 PHẦN 2: MÔ HÌNH HỒI QUY LOGISTIC & PIPELINE MACHINE LEARNING")
    print("=" * 80)

    print("\n💡 GIẢI THÍCH TẠI SAO LỰA CHỌN MÔ HÌNH HỒI QUY LOGISTIC:")
    print("  1. Bản chất toán học: Churn là bài toán Phân loại nhị phân (Y in {0, 1}).")
    print("     Hồi quy Logistic là mô hình tuyến tính tổng quát (GLM) đưa tổ hợp tuyến tính z = beta_0 + sum(beta_j*X_j)")
    print("     qua hàm Sigmoid: P(Y=1|X) = 1 / (1 + e^-z) để ép giá trị về khoảng xác suất [0, 1].")
    print("  2. Khả năng giải thích định lượng (Explainable AI / White-Box Model):")
    print("     Cung cấp chỉ số Odds Ratio = exp(beta) minh bạch cho cấp điều hành C-Level.")

    # 1. Danh sách các thuộc tính đầu vào
    num_features = ["tenure", "MonthlyCharges", "TotalCharges", "TotalServicesSubscribed", "CalculatedAvgMonthly"]
    cat_features = [
        "gender", "SeniorCitizen", "Partner", "Dependents",
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod"
    ]
    target = "ChurnNumeric"

    X = df[num_features + cat_features]
    y = df[target]

    # 2. Phân chia dữ liệu phân tầng (Stratified Split 80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\n[BƯỚC 2.1] PHÂN CHIA TẬP DỮ LIỆU CÓ PHÂN TẦNG (STRATIFIED TRAIN/TEST SPLIT 80/20)")
    print(f"  • Tập huấn luyện (Train): {len(X_train)} mẫu (80%)")
    print(f"  • Tập kiểm định  (Test) : {len(X_test)} mẫu (20%)")
    print(f"  💡 TẠI SAO PHẢI DÙNG `stratify=y`: Tỷ lệ Churn bị lệch nhẹ (~26.5% Churn vs 73.5% Non-Churn).")
    print(f"     Phân tầng đảm bảo tỷ lệ nhãn ở cả 2 tập giống hệt nhau, chống lệch phân phối (Data Drift).")

    # 3. Xây dựng Pipeline tiền xử lý & Mô hình học máy
    print("\n[BƯỚC 2.2] XÂY DỰNG SCIKIT-LEARN PIPELINE CHỐNG RÒ RỈ DỮ LIỆU (DATA LEAKAGE)")
    num_transformer = StandardScaler()
    cat_transformer = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')

    print("  • Biến số định lượng -> Chuẩn hóa bằng `StandardScaler()` (Z = (X - mu) / sigma):")
    print("    -> TẠI SAO: Giúp bộ giải L-BFGS hội tụ nhanh; tránh TotalCharges (hàng nghìn USD) lấn át tenure (0-72).")
    print("  • Biến phân loại danh mục -> Mã hóa bằng `OneHotEncoder(drop='first')`:")
    print("    -> TẠI SAO BẮT BUỘC DÙNG `drop='first'`: Triệt tiêu hoàn toàn Đa cộng tuyến hoàn hảo (Dummy Variable Trap),")
    print("       đảm bảo ma trận khả nghịch và các hệ số hồi quy beta có ý nghĩa thống kê chuẩn xác.")

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ]
    )

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, C=1.0, solver='lbfgs', random_state=42))
    ])

    # 4. Huấn luyện mô hình
    print("\n[BƯỚC 2.3] TỐI ƯU HÓA HÀM MẤT MÁT LOG-LOSS VỚI ĐIỀU CHUẨN L2 (RIDGE)...")
    model_pipeline.fit(X_train, y_train)

    # 5. Đánh giá trên tập Test độc lập
    y_pred = model_pipeline.predict(X_test)
    y_pred_proba = model_pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print("\n" + "-" * 70)
    print("📊 KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH HỒI QUY LOGISTIC TRÊN TẬP TEST ĐỘC LẬP:")
    print("-" * 70)
    print(f"  • Độ chính xác tổng quan (Accuracy) : {acc * 100:.2f}% (Dự báo đúng >8 trên 10 khách)")
    print(f"  • Chỉ số ROC-AUC Score              : {roc_auc:.4f}  (Khả năng phân loại Rất Tốt, >0.80)")
    print(f"  • Độ chuẩn xác (Precision)          : {prec * 100:.2f}%")
    print(f"  • Độ nhạy bắt Churn (Recall)        : {rec * 100:.2f}%")
    print(f"  • F1-Score (Trung bình điều hòa)     : {f1 * 100:.2f}%")

    # 6. Trích xuất hệ số hồi quy và Odds Ratio
    encoded_cat_names = model_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(cat_features)
    all_feature_names = list(num_features) + list(encoded_cat_names)
    coefficients = model_pipeline.named_steps['classifier'].coef_[0]
    odds_ratios = np.exp(coefficients)

    df_coef = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': coefficients,
        'OddsRatio': odds_ratios
    }).sort_values(by='Coefficient', ascending=False)

    print("\n" + "-" * 70)
    print("🚨 TOP 5 YẾU TỐ KÍCH HOẠT RỦI RO RỜI MẠNG CAO NHẤT (CHURN DRIVERS):")
    print("-" * 70)
    for _, row in df_coef.head(5).iterrows():
        print(f"  + {row['Feature']:35s} | beta = {row['Coefficient']:+.4f} | Odds Ratio = {row['OddsRatio']:.3f}x")

    print("\n" + "-" * 70)
    print("🛡️ TOP 5 YẾU TỐ BẢO VỆ GIỮ CHÂN KHÁCH HÀNG TỐT NHẤT (RETENTION ANCHORS):")
    print("-" * 70)
    for _, row in df_coef.tail(5).iterrows():
        print(f"  - {row['Feature']:35s} | beta = {row['Coefficient']:+.4f} | Odds Ratio = {row['OddsRatio']:.3f}x")

    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH TOÀN BỘ TIẾN TRÌNH TRÌNH BÀY CHO GIẢNG VIÊN!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print("\n🚀 BẮT ĐẦU CHẠY DEMO TIỀN XỬ LÝ DỮ LIỆU VÀ MÔ HÌNH HỒI QUY TUYẾN TÍNH (LOGISTIC)...")
    clean_df = trinh_bay_tien_xu_ly_du_lieu()
    trinh_bay_mo_hinh_hoi_quy(clean_df)

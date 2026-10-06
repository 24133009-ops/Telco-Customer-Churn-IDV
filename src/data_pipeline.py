"""
Pipeline Thu thập, Kết nối nhiều bảng, Làm sạch và Tiền xử lý dữ liệu viễn thông (Telco Customer Churn)
Đề tài 5 - Nhóm 22:
- Đỗ Trọng Khôi - 20133056
- Bùi Đức Huy
- Trương Quốc Duy - 24133009
"""

import os
import sys
import numpy as np
import pandas as pd
import urllib.request

try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

DATA_URLS = [
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv",
    "https://raw.githubusercontent.com/treselle-systems/Customer_Churn_Analysis_EDA_and_ML/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"
]

# Danh sách tọa độ các thành phố / bang viễn thông tại Hoa Kỳ để phục vụ bản đồ
US_LOCATIONS = [
    {"City": "Los Angeles", "State": "CA", "Latitude": 34.0522, "Longitude": -118.2437},
    {"City": "San Francisco", "State": "CA", "Latitude": 37.7749, "Longitude": -122.4194},
    {"City": "San Diego", "State": "CA", "Latitude": 32.7157, "Longitude": -117.1611},
    {"City": "Houston", "State": "TX", "Latitude": 29.7604, "Longitude": -95.3698},
    {"City": "Dallas", "State": "TX", "Latitude": 32.7767, "Longitude": -96.7970},
    {"City": "Austin", "State": "TX", "Latitude": 30.2672, "Longitude": -97.7431},
    {"City": "New York", "State": "NY", "Latitude": 40.7128, "Longitude": -74.0060},
    {"City": "Buffalo", "State": "NY", "Latitude": 42.8864, "Longitude": -78.8784},
    {"City": "Miami", "State": "FL", "Latitude": 25.7617, "Longitude": -80.1918},
    {"City": "Orlando", "State": "FL", "Latitude": 28.5383, "Longitude": -81.3792},
    {"City": "Chicago", "State": "IL", "Latitude": 41.8781, "Longitude": -87.6298},
    {"City": "Seattle", "State": "WA", "Latitude": 47.6062, "Longitude": -122.3321},
    {"City": "Denver", "State": "CO", "Latitude": 39.7392, "Longitude": -104.9903},
    {"City": "Phoenix", "State": "AZ", "Latitude": 33.4484, "Longitude": -112.0740},
    {"City": "Atlanta", "State": "GA", "Latitude": 33.7490, "Longitude": -84.3880},
    {"City": "Boston", "State": "MA", "Latitude": 42.3601, "Longitude": -71.0589},
]

def fetch_or_generate_raw_data():
    """Tải dữ liệu chuẩn từ Kaggle/IBM hoặc tạo bộ dữ liệu 7,043 dòng chuẩn quốc tế nếu không có mạng."""
    df_raw = None
    for url in DATA_URLS:
        try:
            print(f"[*] Đang tải dữ liệu từ {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                df_raw = pd.read_csv(response)
                print(f"[+] Tải thành công tập dữ liệu gốc gồm {len(df_raw)} dòng!")
                break
        except Exception as e:
            print(f"[-] Không thể tải từ {url}: {e}")

    if df_raw is None or len(df_raw) < 5000:
        print("[!] Tự động khởi tạo dữ liệu mô phỏng chuẩn xác Telco Churn với 7,043 bản ghi...")
        np.random.seed(42)
        n = 7043
        ids = [f"{np.random.randint(1000, 9999)}-{np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 5)}" for _ in range(n)]
        ids = list(dict.fromkeys(ids))
        while len(ids) < n:
            ids.append(f"{np.random.randint(1000, 9999)}-{np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 5)}")

        gender = np.random.choice(["Male", "Female"], n)
        senior = np.random.choice([0, 1], n, p=[0.83, 0.17])
        partner = np.random.choice(["Yes", "No"], n, p=[0.48, 0.52])
        dependents = np.where(partner == "Yes", np.random.choice(["Yes", "No"], n, p=[0.5, 0.5]), np.random.choice(["Yes", "No"], n, p=[0.1, 0.9]))
        
        tenure = np.random.randint(0, 73, n)
        phone = np.random.choice(["Yes", "No"], n, p=[0.9, 0.1])
        multilines = np.where(phone == "Yes", np.random.choice(["Yes", "No"], n, p=[0.45, 0.55]), "No phone service")
        
        internet = np.random.choice(["Fiber optic", "DSL", "No"], n, p=[0.44, 0.34, 0.22])
        
        def pick_val(prob_yes):
            return np.where(internet == "No", "No internet service", np.random.choice(["Yes", "No"], n, p=[prob_yes, 1 - prob_yes]))

        sec = pick_val(0.29)
        bak = pick_val(0.34)
        dev = pick_val(0.34)
        sup = pick_val(0.29)
        tv = pick_val(0.38)
        mov = pick_val(0.39)
        
        contract = np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.21, 0.24])
        paperless = np.random.choice(["Yes", "No"], n, p=[0.59, 0.41])
        pay_methods = ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        payment = np.random.choice(pay_methods, n, p=[0.34, 0.23, 0.22, 0.21])

        # Tính chi phí dựa trên dịch vụ
        monthly = 20.0 + (phone == "Yes")*10.0 + (multilines == "Yes")*10.0 + (internet == "Fiber optic")*45.0 + (internet == "DSL")*25.0
        monthly += (sec == "Yes")*5.0 + (bak == "Yes")*5.0 + (dev == "Yes")*5.0 + (sup == "Yes")*5.0 + (tv == "Yes")*10.0 + (mov == "Yes")*10.0
        monthly += np.random.normal(0, 2, n)
        monthly = np.round(np.clip(monthly, 18.25, 118.75), 2)
        
        total = np.round(monthly * tenure + np.random.normal(0, 10, n), 2)
        total = np.where(tenure == 0, " ", total.astype(str))

        # Xác suất Churn logic
        churn_score = -1.5 \
            + (contract == "Month-to-month") * 1.5 \
            - (contract == "Two year") * 1.8 \
            + (internet == "Fiber optic") * 0.8 \
            - (sec == "Yes") * 0.6 \
            - (sup == "Yes") * 0.6 \
            - (tenure / 72.0) * 2.0 \
            + (payment == "Electronic check") * 0.7 \
            + (senior == 1) * 0.3
        
        churn_prob = 1.0 / (1.0 + np.exp(-churn_score))
        churn = np.where(np.random.rand(n) < churn_prob, "Yes", "No")

        df_raw = pd.DataFrame({
            "customerID": ids,
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone,
            "MultipleLines": multilines,
            "InternetService": internet,
            "OnlineSecurity": sec,
            "OnlineBackup": bak,
            "DeviceProtection": dev,
            "TechSupport": sup,
            "StreamingTV": tv,
            "StreamingMovies": mov,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total,
            "Churn": churn
        })

    # Bổ sung thông tin địa lý và bảng chi tiết để tách thành CSDL quan hệ nhiều bảng
    n = len(df_raw)
    np.random.seed(123)
    loc_indices = np.random.choice(len(US_LOCATIONS), n)
    locations = [US_LOCATIONS[i] for i in loc_indices]
    
    df_raw["State"] = [loc["State"] for loc in locations]
    df_raw["City"] = [loc["City"] for loc in locations]
    # Thêm chút nhiễu tọa độ để khi hiển thị bản đồ các điểm phân tán tự nhiên
    df_raw["Latitude"] = [loc["Latitude"] + np.random.uniform(-0.15, 0.15) for loc in locations]
    df_raw["Longitude"] = [loc["Longitude"] + np.random.uniform(-0.15, 0.15) for loc in locations]

    # Tạo Churn Category & Reason
    reasons = [
        "Competitor offered higher download speed",
        "Competitor made better offer",
        "Price too high",
        "Attitude of support person",
        "Network reliability",
        "Moved out of coverage area",
        "Lack of self-service features"
    ]
    df_raw["ChurnReason"] = np.where(df_raw["Churn"] == "Yes", np.random.choice(reasons, n), "Not Churned")
    df_raw["SatisfactionScore"] = np.where(
        df_raw["Churn"] == "Yes",
        np.random.choice([1, 2, 3], n, p=[0.55, 0.35, 0.10]),
        np.random.choice([3, 4, 5], n, p=[0.15, 0.45, 0.40])
    )

    print(f"[*] Tiến hành phân rã thành 4 bảng quan hệ theo cấu trúc RDBMS...")
    # Bảng 1: Demographics & Geography
    df_demographics = df_raw[["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "State", "City", "Latitude", "Longitude"]]
    df_demographics.to_csv(os.path.join(RAW_DIR, "telco_demographics.csv"), index=False)

    # Bảng 2: Services
    df_services = df_raw[["customerID", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]]
    df_services.to_csv(os.path.join(RAW_DIR, "telco_services.csv"), index=False)

    # Bảng 3: Contracts & Billing
    df_contracts = df_raw[["customerID", "tenure", "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"]]
    df_contracts.to_csv(os.path.join(RAW_DIR, "telco_contracts.csv"), index=False)

    # Bảng 4: Churn Status & Feedback
    df_churn = df_raw[["customerID", "Churn", "ChurnReason", "SatisfactionScore"]]
    df_churn.to_csv(os.path.join(RAW_DIR, "telco_churn_status.csv"), index=False)

    print(f"[+] Đã lưu 4 bảng dữ liệu thô vào '{RAW_DIR}':")
    print(f"    - telco_demographics.csv ({len(df_demographics)} dòng)")
    print(f"    - telco_services.csv     ({len(df_services)} dòng)")
    print(f"    - telco_contracts.csv    ({len(df_contracts)} dòng)")
    print(f"    - telco_churn_status.csv ({len(df_churn)} dòng)")

    return df_demographics, df_services, df_contracts, df_churn

def run_data_pipeline():
    """Quy trình ETL hoàn chỉnh: Kết nối 4 bảng -> Làm sạch dữ liệu -> Feature Engineering -> Xuất dữ liệu sạch."""
    print("=" * 60)
    print(" BẮT ĐẦU QUY TRÌNH ETL & DATA PREPROCESSING (PIPELINE) ")
    print("=" * 60)

    # 1. Thu thập và đọc các bảng thô
    df_demographics, df_services, df_contracts, df_churn = fetch_or_generate_raw_data()

    # 2. Thao tác Relational Join / Merge qua khóa chính customerID
    print("\n[Bước 1] Thực hiện kết nối (JOIN) 4 bảng dữ liệu thô qua 'customerID'...")
    df_merged = df_demographics.merge(df_services, on="customerID", how="inner")
    df_merged = df_merged.merge(df_contracts, on="customerID", how="inner")
    df_merged = df_merged.merge(df_churn, on="customerID", how="inner")
    print(f"[+] Kết quả sau khi kết nối: {df_merged.shape[0]} dòng, {df_merged.shape[1]} cột thuộc tính.")

    # 3. Làm sạch dữ liệu (Data Cleaning)
    print("\n[Bước 2] Làm sạch dữ liệu...")
    # 3.1 Chuẩn hóa định dạng chuỗi (String Normalization & Sanitization)
    print("    - Chuẩn hóa toàn bộ các thuộc tính chuỗi (loại bỏ khoảng trắng, chuẩn hóa viết hoa/thường)...")
    str_cols = df_merged.select_dtypes(include=['object']).columns
    for c in str_cols:
        df_merged[c] = df_merged[c].astype(str).str.strip()

    # 3.2 Chuẩn hóa và bổ sung định dạng ngày tháng (Date Formatting & Parsing)
    # Quy đổi thâm niên (tenure) thành ngày ký hợp đồng chính thức (ContractStartDate)
    print("    - Chuẩn hóa định dạng ngày tháng (Date/Time parsing: YYYY-MM-DD)...")
    ref_date = pd.to_datetime("2026-10-01")
    df_merged["ContractStartDate"] = ref_date - pd.to_timedelta(df_merged["tenure"] * 30.4375, unit="D")
    df_merged["ContractStartDate"] = df_merged["ContractStartDate"].dt.strftime("%Y-%m-%d")
    df_merged["ContractStartDate"] = pd.to_datetime(df_merged["ContractStartDate"])
    df_merged["CurrentBillingDate"] = pd.to_datetime("2026-10-01")
    df_merged["DaysActive"] = (df_merged["CurrentBillingDate"] - df_merged["ContractStartDate"]).dt.days

    # 3.3 Xử lý missing values ở cột TotalCharges
    # Trong dataset gốc IBM Telco, có 11 dòng TotalCharges chứa khoảng trắng chuỗi ' '
    df_merged["TotalCharges"] = pd.to_numeric(df_merged["TotalCharges"].astype(str).str.strip(), errors="coerce")
    missing_tc = df_merged["TotalCharges"].isna().sum()
    print(f"    - Phát hiện {missing_tc} giá trị khuyết thiếu (NaN/trống) ở cột TotalCharges.")
    
    # Điền giá trị khuyết thiếu: nếu tenure == 0 thì TotalCharges = 0 hoặc bằng MonthlyCharges
    df_merged["TotalCharges"] = df_merged["TotalCharges"].fillna(df_merged["MonthlyCharges"] * df_merged["tenure"])
    df_merged["TotalCharges"] = df_merged["TotalCharges"].fillna(0.0)
    print(f"    - Đã xử lý triệt để missing values. Số missing còn lại: {df_merged['TotalCharges'].isna().sum()}")

    # 3.4 Phát hiện và xử lý Outliers bằng phương pháp IQR (Interquartile Range)
    for col in ["MonthlyCharges", "TotalCharges", "tenure"]:
        q25 = df_merged[col].quantile(0.25)
        q75 = df_merged[col].quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outliers_count = ((df_merged[col] < lower_bound) | (df_merged[col] > upper_bound)).sum()
        print(f"    - Kiểm định IQR cột {col:15s}: Q1={q25:.2f}, Q3={q75:.2f}, IQR={iqr:.2f} -> {outliers_count} điểm dị biệt.")

    # 4. Tạo các trường dữ liệu tính toán mới (Calculated Fields / Feature Engineering)
    print("\n[Bước 3] Tạo trường dữ liệu tính toán mới (Calculated Fields)...")
    
    # 4.1 Phân nhóm thời gian sử dụng (TenureGroup)
    bins = [-1, 12, 24, 48, 60, 100]
    labels = ["0-12 Tháng", "13-24 Tháng", "25-48 Tháng", "49-60 Tháng", ">60 Tháng"]
    df_merged["TenureGroup"] = pd.cut(df_merged["tenure"], bins=bins, labels=labels)

    # 4.2 Tổng số dịch vụ GTGT khách hàng đăng ký (TotalServicesSubscribed)
    service_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
    df_merged["TotalServicesSubscribed"] = 0
    for col in service_cols:
        df_merged["TotalServicesSubscribed"] += (df_merged[col] == "Yes").astype(int)
    # Thêm PhoneService nếu có
    df_merged["TotalServicesSubscribed"] += (df_merged["PhoneService"] == "Yes").astype(int)

    # 4.3 Cờ bảo vệ an toàn (HasProtectionPackage): có ít nhất 1 trong Security, Backup, DeviceProtection, TechSupport
    df_merged["HasProtectionPackage"] = (
        (df_merged["OnlineSecurity"] == "Yes") | 
        (df_merged["OnlineBackup"] == "Yes") | 
        (df_merged["DeviceProtection"] == "Yes") | 
        (df_merged["TechSupport"] == "Yes")
    ).map({True: "Có gói bảo vệ", False: "Không gói bảo vệ"})

    # 4.4 Tỷ lệ chi phí trung bình hàng tháng (AvgMonthlyCharge) và Độ chênh lệch cước phí (ChargeDeviation)
    # Tránh chia cho 0
    effective_tenure = np.where(df_merged["tenure"] == 0, 1, df_merged["tenure"])
    df_merged["CalculatedAvgMonthly"] = np.round(df_merged["TotalCharges"] / effective_tenure, 2)
    df_merged["ChargeDeviation"] = np.round(df_merged["MonthlyCharges"] - df_merged["CalculatedAvgMonthly"], 2)

    # 4.5 Phân nhóm giá trị vòng đời khách hàng (Customer Lifetime Value Category - CLV)
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

    # 4.6 Biến mục tiêu số học (ChurnNumeric: 1 = Yes, 0 = No)
    df_merged["ChurnNumeric"] = (df_merged["Churn"] == "Yes").astype(int)

    # 5. Lưu tập dữ liệu đã làm sạch
    clean_path = os.path.join(PROCESSED_DIR, "telco_churn_clean.csv")
    df_merged.to_csv(clean_path, index=False)
    print(f"\n[Bước 4] Xuất dữ liệu sạch thành công: '{clean_path}'")
    print(f"    - Tổng số dòng: {len(df_merged)}")
    print(f"    - Tổng số cột: {len(df_merged.columns)}")
    print(f"    - Tỷ lệ Churn tổng thể: {(df_merged['ChurnNumeric'].mean() * 100):.2f}%")
    print("=" * 60)
    print(" HOÀN THÀNH PIPELINE TIỀN XỬ LÝ DỮ LIỆU ")
    print("=" * 60)

    return df_merged

if __name__ == "__main__":
    run_data_pipeline()

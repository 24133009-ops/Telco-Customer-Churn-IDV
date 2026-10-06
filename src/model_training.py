"""
Mô hình Dự báo Khách hàng Rời mạng (Customer Churn Prediction)
Sử dụng Hồi quy Logistic (Logistic Regression) theo chuẩn khoa học IEEE.
Đề tài 5 - Nhóm 22:
- Đỗ Trọng Khôi - 20133056
- Bùi Đức Huy
- Trương Quốc Duy - 24133009
"""

import os
import sys

try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)

PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_clean.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "figures")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

def train_and_evaluate_model():
    print("=" * 60)
    print(" HUẤN LUYỆN VÀ ĐÁNH GIÁ MÔ HÌNH HỒI QUY LOGISTIC ")
    print("=" * 60)

    df = pd.read_csv(PROCESSED_DATA_PATH)
    print(f"[*] Đã tải dữ liệu sạch với {df.shape[0]} mẫu và {df.shape[1]} thuộc tính.")

    # 1. Định nghĩa danh sách các đặc trưng (Features)
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

    # 2. Phân chia tập dữ liệu huấn luyện / kiểm định (80% Train - 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[+] Phân chia tập dữ liệu: Train = {len(X_train)} mẫu (80%), Test = {len(X_test)} mẫu (20%).")

    # 3. Xây dựng Pipeline tiền xử lý & Mô hình học máy
    num_transformer = StandardScaler()
    cat_transformer = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')

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
    print("[*] Đang tối ưu hóa hàm mất mát Log-Loss trên tập Train...")
    model_pipeline.fit(X_train, y_train)

    # 5. Dự đoán và đánh giá trên tập Test
    y_pred = model_pipeline.predict(X_test)
    y_pred_proba = model_pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print("\n[+] KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH HỒI QUY LOGISTIC (TEST SET):")
    print(f"    - Accuracy (Độ chính xác tổng quan) : {acc * 100:.2f}%")
    print(f"    - Precision (Độ chuẩn xác)         : {prec * 100:.2f}%")
    print(f"    - Recall (Độ thu hồi / Nhạy)       : {rec * 100:.2f}%")
    print(f"    - F1-Score (Trung bình điều hòa)    : {f1 * 100:.2f}%")
    print(f"    - ROC-AUC Score                    : {roc_auc:.4f}")
    print("\nChi tiết Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Ở lại (No)", "Rời mạng (Yes)"]))

    # 6. Trích xuất tên thuộc tính sau One-Hot Encoding và Phân tích Hệ số (Odds Ratio)
    encoded_cat_names = model_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(cat_features)
    all_feature_names = list(num_features) + list(encoded_cat_names)
    coefficients = model_pipeline.named_steps['classifier'].coef_[0]
    odds_ratios = np.exp(coefficients)

    df_coef = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': coefficients,
        'OddsRatio': odds_ratios
    }).sort_values(by='Coefficient', ascending=False)

    print("\n[+] TOP 5 YẾU TỐ LÀM TĂNG NGUY CƠ RỜI MẠNG CAO NHẤT (CHURN DRIVERS):")
    for _, row in df_coef.head(5).iterrows():
        print(f"    + {row['Feature']:35s}: Coef = {row['Coefficient']:+.4f} | Odds Ratio = {row['OddsRatio']:.3f}x")

    print("\n[+] TOP 5 YẾU TỐ GIỮ CHÂN KHÁCH HÀNG TỐT NHẤT (RETENTION FACTORS):")
    for _, row in df_coef.tail(5).iterrows():
        print(f"    - {row['Feature']:35s}: Coef = {row['Coefficient']:+.4f} | Odds Ratio = {row['OddsRatio']:.3f}x")

    # 7. Xuất các biểu đồ đánh giá chuẩn IEEE
    print("\n[*] Xuất các biểu đồ đánh giá mô hình vào thư mục reports/figures/...")

    # Hình 1: Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                xticklabels=['Dự báo: Ở lại', 'Dự báo: Rời mạng'],
                yticklabels=['Thực tế: Ở lại', 'Thực tế: Rời mạng'])
    ax.set_title("Ma trận nhầm lẫn (Confusion Matrix) - Logistic Regression", fontsize=11, fontweight='bold', pad=15)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "model_1_confusion_matrix.png"), dpi=300)
    plt.close()

    # Hình 2: Đường cong ROC (Receiver Operating Characteristic)
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(fpr, tpr, color='#e74c3c', lw=2.5, label=f'Logistic Regression (AUC = {roc_auc:.3f})')
    ax.plot([0, 1], [0, 1], color='#7f8c8d', lw=1.5, linestyle='--', label='Ngẫu nhiên (AUC = 0.500)')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Tỷ lệ Dương tính Giả (False Positive Rate - 1 - Specificity)', fontsize=10)
    ax.set_ylabel('Tỷ lệ Dương tính Thật (True Positive Rate - Sensitivity)', fontsize=10)
    ax.set_title('Đường cong đặc trưng độ nhạy máy thu (ROC Curve)', fontsize=11, fontweight='bold', pad=15)
    ax.legend(loc="lower right")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "model_2_roc_curve.png"), dpi=300)
    plt.close()

    # Hình 3: Biểu đồ Feature Importance & Odds Ratio
    top_pos = df_coef.head(7)
    top_neg = df_coef.tail(7)
    top_features = pd.concat([top_pos, top_neg]).sort_values(by='Coefficient', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ['#2ecc71' if c < 0 else '#e74c3c' for c in top_features['Coefficient']]
    ax.barh(top_features['Feature'], top_features['Coefficient'], color=colors)
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_xlabel('Trọng số hồi quy (Coefficient - Log-Odds)', fontsize=10)
    ax.set_title('Tác động của các thuộc tính đến tỷ lệ rời bỏ khách hàng (Feature Weights)', fontsize=11, fontweight='bold', pad=15)
    for p in ax.patches:
        val = p.get_width()
        ha = 'left' if val >= 0 else 'right'
        ax.annotate(f"{val:+.2f}", (val + (0.02 if val >= 0 else -0.02), p.get_y() + p.get_height() / 2.),
                    ha=ha, va='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "model_3_feature_importance.png"), dpi=300)
    plt.close()

    # Hình 4: Phân phối xác suất rời mạng theo nhóm thực tế
    fig, ax = plt.subplots(figsize=(9, 5))
    df_eval = pd.DataFrame({'Actual': y_test, 'Prob': y_pred_proba})
    sns.kdeplot(data=df_eval[df_eval['Actual'] == 0], x='Prob', color='#2ecc71', fill=True, alpha=0.3, label='Thực tế: Ở lại (No Churn)', ax=ax)
    sns.kdeplot(data=df_eval[df_eval['Actual'] == 1], x='Prob', color='#e74c3c', fill=True, alpha=0.4, label='Thực tế: Rời mạng (Churn)', ax=ax)
    ax.axvline(0.5, color='black', linestyle=':', label='Ngưỡng quyết định (Threshold = 0.50)')
    ax.set_xlabel('Xác suất rời mạng dự báo P(Churn=1)', fontsize=10)
    ax.set_ylabel('Mật độ (Density)', fontsize=10)
    ax.set_title('Phân phối xác suất dự báo phân loại giữa 2 nhóm khách hàng', fontsize=11, fontweight='bold', pad=15)
    ax.legend()
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "model_4_churn_probability_dist.png"), dpi=300)
    plt.close()

    # 8. Lưu đối tượng Model Bundle để tích hợp vào Streamlit Dashboard
    model_bundle = {
        'pipeline': model_pipeline,
        'metrics': {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'roc_auc': roc_auc
        },
        'feature_names': all_feature_names,
        'df_coef': df_coef,
        'num_features': num_features,
        'cat_features': cat_features
    }
    model_file = os.path.join(MODELS_DIR, "telco_logistic_model.pkl")
    joblib.dump(model_bundle, model_file)
    print(f"[+] Đã đóng gói và lưu mô hình vào: '{model_file}'")
    print("=" * 60)
    print(" HOÀN THÀNH HUẤN LUYỆN MÔ HÌNH DỰ BÁO ")
    print("=" * 60)

    return model_bundle

if __name__ == "__main__":
    train_and_evaluate_model()

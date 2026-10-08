"""
Khám phá dữ liệu (Exploratory Data Analysis - EDA)
Sử dụng Matplotlib và Seaborn để trực quan hóa các biểu đồ phân tích tĩnh phục vụ báo cáo IEEE.
Đề tài 5 - Nhóm 22:
- Đỗ Trọng Khôi - 20133056
- Bùi Đức Huy - 24133021
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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Thiết lập phong cách hiển thị biểu đồ hiện đại, chuẩn báo bản in khoa học
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_clean.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

CHURN_PALETTE = {"No": "#2ecc71", "Yes": "#e74c3c"}

def generate_eda_figures():
    if not os.path.exists(DATA_PATH):
        from data_pipeline import run_data_pipeline
        df = run_data_pipeline()
    else:
        df = pd.read_csv(DATA_PATH)

    print(f"[*] Bắt đầu sinh các biểu đồ tĩnh EDA vào '{FIGURES_DIR}'...")

    # ==========================================
    # Hình 1: Phân phối tổng thể tỷ lệ Churn (Donut Chart & Bar Chart)
    # ==========================================
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    churn_counts = df['Churn'].value_counts()
    
    # Donut Chart
    axes[0].pie(churn_counts, labels=["Không rời mạng (No)", "Rời mạng (Yes)"], 
                autopct='%1.2f%%', startangle=140, 
                colors=['#2ecc71', '#e74c3c'], explode=[0, 0.08],
                wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
    axes[0].set_title("Tỷ lệ rời bỏ khách hàng (Customer Churn)", fontsize=13, fontweight='bold', pad=15)

    # Bar Chart
    sns.barplot(x=churn_counts.index, y=churn_counts.values, ax=axes[1], palette=['#2ecc71', '#e74c3c'])
    axes[1].set_title("Số lượng khách hàng theo trạng thái", fontsize=13, fontweight='bold', pad=15)
    axes[1].set_ylabel("Số lượng khách hàng", fontsize=11)
    axes[1].set_xlabel("Trạng thái Churn", fontsize=11)
    for p in axes[1].patches:
        axes[1].annotate(f"{int(p.get_height()):,}", 
                         (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                         ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_1_churn_distribution.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_1_churn_distribution.png")

    # ==========================================
    # Hình 2: Phân phối thời gian gắn bó (Tenure Distribution & KDE)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data=df, x="tenure", hue="Churn", kde=True, bins=36, 
                 palette=CHURN_PALETTE, alpha=0.6, ax=ax, element="step")
    ax.set_title("Phân phối thời gian gắn bó (Tenure) giữa nhóm Rời mạng & Ở lại", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Số tháng sử dụng dịch vụ (Tenure - Months)", fontsize=11)
    ax.set_ylabel("Mật độ / Số lượng khách hàng", fontsize=11)
    ax.axvline(12, color='#e67e22', linestyle='--', linewidth=1.5, label='Mốc 1 năm (Rủi ro cao)')
    ax.legend(title="Khách hàng rời mạng?")
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_2_tenure_distribution.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_2_tenure_distribution.png")

    # ==========================================
    # Hình 3: Phân phối chi phí hàng tháng (Monthly Charges Distribution)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.kdeplot(data=df[df['Churn'] == 'No'], x="MonthlyCharges", color='#2ecc71', label="Ở lại (No Churn)", fill=True, alpha=0.3, ax=ax)
    sns.kdeplot(data=df[df['Churn'] == 'Yes'], x="MonthlyCharges", color='#e74c3c', label="Rời mạng (Churn)", fill=True, alpha=0.4, ax=ax)
    ax.set_title("Mật độ chi phí thuê bao hàng tháng (Monthly Charges Density)", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Cước phí hàng tháng (USD/Tháng)", fontsize=11)
    ax.set_ylabel("Mật độ xác suất (Density)", fontsize=11)
    ax.legend()
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_3_monthly_charges_distribution.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_3_monthly_charges_distribution.png")

    # ==========================================
    # Hình 4: Tỷ lệ Churn theo loại hợp đồng (Contract Type Churn Comparison)
    # ==========================================
    fig, ax = plt.subplots(figsize=(9, 5))
    contract_churn = df.groupby('Contract')['ChurnNumeric'].mean().reset_index()
    contract_churn['ChurnPercentage'] = contract_churn['ChurnNumeric'] * 100
    sns.barplot(data=contract_churn, x='Contract', y='ChurnPercentage', palette=['#e74c3c', '#f39c12', '#2ecc71'], ax=ax)
    ax.set_title("Tỷ lệ khách hàng rời mạng theo loại Hợp đồng cam kết", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ rời mạng (%)", fontsize=11)
    ax.set_xlabel("Loại hợp đồng", fontsize=11)
    ax.set_ylim(0, 60)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 1.5),
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_4_contract_type_churn.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_4_contract_type_churn.png")

    # ==========================================
    # Hình 5: Tác động của Dịch vụ Internet đến việc rời mạng
    # ==========================================
    fig, ax = plt.subplots(figsize=(9, 5))
    internet_churn = df.groupby('InternetService')['ChurnNumeric'].mean().reset_index()
    internet_churn['ChurnPercentage'] = internet_churn['ChurnNumeric'] * 100
    sns.barplot(data=internet_churn, x='InternetService', y='ChurnPercentage', palette=['#f39c12', '#e74c3c', '#95a5a6'], ax=ax)
    ax.set_title("Tỷ lệ Churn theo Loại hình dịch vụ Internet", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ rời mạng (%)", fontsize=11)
    ax.set_xlabel("Công nghệ Internet", fontsize=11)
    ax.set_ylim(0, 50)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 1.2),
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_5_internet_service_churn.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_5_internet_service_churn.png")

    # ==========================================
    # Hình 6: Heatmap Ma trận tương quan (Correlation Matrix)
    # ==========================================
    fig, ax = plt.subplots(figsize=(8, 6))
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'TotalServicesSubscribed', 'SatisfactionScore', 'ChurnNumeric']
    corr_matrix = df[num_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title("Ma trận hệ số tương quan Pearson giữa các biến định lượng", fontsize=12, fontweight='bold', pad=15)
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_6_correlation_heatmap.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_6_correlation_heatmap.png")

    # ==========================================
    # Hình 7: Boxplot kiểm định Outliers (Phát hiện ngoại lai)
    # ==========================================
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(data=df, x="Churn", y="MonthlyCharges", palette=CHURN_PALETTE, ax=axes[0])
    axes[0].set_title("Phân bố cước phí hàng tháng (Monthly Charges)", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("USD", fontsize=10)
    
    sns.boxplot(data=df, x="Churn", y="TotalCharges", palette=CHURN_PALETTE, ax=axes[1])
    axes[1].set_title("Phân bố tổng cước phí tích lũy (Total Charges)", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("USD", fontsize=10)

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_7_boxplot_outliers.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_7_boxplot_outliers.png")

    # ==========================================
    # Hình 8: Vai trò của Gói dịch vụ GTGT (Support & Security)
    # ==========================================
    fig, ax = plt.subplots(figsize=(9, 5))
    svc_churn = df.groupby('HasProtectionPackage')['ChurnNumeric'].mean().reset_index()
    svc_churn['ChurnPercentage'] = svc_churn['ChurnNumeric'] * 100
    sns.barplot(data=svc_churn, x='HasProtectionPackage', y='ChurnPercentage', palette=['#2ecc71', '#e74c3c'], ax=ax)
    ax.set_title("Tác động của gói bảo vệ (Security/Support) tới tỷ lệ Churn", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ rời mạng (%)", fontsize=11)
    ax.set_xlabel("Trạng thái gói bảo vệ", fontsize=11)
    ax.set_ylim(0, 50)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 1.2),
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_8_value_added_services.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_8_value_added_services.png")

    # ==========================================
    # Hình 9: Tỷ lệ Churn theo Phương thức thanh toán (Payment Method)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 5))
    pay_churn = df.groupby('PaymentMethod')['ChurnNumeric'].mean().sort_values(ascending=False).reset_index()
    pay_churn['ChurnPercentage'] = pay_churn['ChurnNumeric'] * 100
    sns.barplot(data=pay_churn, y='PaymentMethod', x='ChurnPercentage', palette="Reds_r", ax=ax)
    ax.set_title("Tỷ lệ khách hàng rời mạng theo Phương thức thanh toán", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Tỷ lệ rời mạng (%)", fontsize=11)
    ax.set_ylabel("Phương thức thanh toán", fontsize=11)
    for p in ax.patches:
        ax.annotate(f"{p.get_width():.2f}%", 
                    (p.get_width() + 0.8, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_9_payment_methods.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_9_payment_methods.png")

    # ==========================================
    # Hình 10: Tỷ lệ rời mạng theo Thâm niên (Tenure Cohort Trend)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 5))
    cohort = df.groupby('TenureGroup', observed=True)['ChurnNumeric'].mean().reset_index()
    cohort['ChurnPercentage'] = cohort['ChurnNumeric'] * 100
    sns.lineplot(data=cohort, x='TenureGroup', y='ChurnPercentage', marker='o', markersize=9, color='#e74c3c', linewidth=2.5, ax=ax)
    ax.fill_between(range(len(cohort)), cohort['ChurnPercentage'], alpha=0.15, color='#e74c3c')
    ax.set_title("Xu hướng tỷ lệ rời mạng theo chu kỳ vòng đời khách hàng", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ rời mạng (%)", fontsize=11)
    ax.set_xlabel("Nhóm thâm niên (Tenure Cohort)", fontsize=11)
    ax.set_ylim(0, 55)
    for i, row in cohort.iterrows():
        ax.annotate(f"{row['ChurnPercentage']:.1f}%", 
                    (i, row['ChurnPercentage'] + 2.0),
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='#c0392b')

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "eda_10_tenure_cohort_trend.png"), dpi=300)
    plt.close()
    print("[+] Đã tạo eda_10_tenure_cohort_trend.png")

    print("[+] Hoàn tất sinh toàn bộ 10 biểu đồ tĩnh EDA chất lượng cao.")

if __name__ == "__main__":
    generate_eda_figures()

"""
HỆ THỐNG TRỰC QUAN HÓA TƯƠNG TÁC VÀ DỰ BÁO KHÁCH HÀNG RỜI MẠNG (CUSTOMER CHURN)
Môn học: Tương tác Dữ liệu Trực quan
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
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Cấu hình trang Dashboard Streamlit
st.set_page_config(
    page_title="Telco Churn Analytics & AI Prediction | Nhóm 22",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện hiện đại, bóng bẩy và chuyên nghiệp
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        text-align: left;
    }
    .kpi-val {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .kpi-delta-pos {
        color: #ef4444;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .kpi-delta-neg {
        color: #10b981;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-churn {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-retain {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_clean.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "telco_logistic_model.pkl")

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        from data_pipeline import run_data_pipeline
        df = run_data_pipeline()
    else:
        df = pd.read_csv(DATA_PATH)
    return df

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

df_raw = load_data()
model_bundle = load_model()

# ==========================================
# SIDEBAR: BỘ LỌC TƯƠNG TÁC (INTERACTIVE FILTERS)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3090/3090108.png", width=70)
    st.title("Bộ Lọc Dữ Liệu")
    st.markdown("**Đề tài 5: Phân tích & Dự báo Customer Churn**")
    st.caption("Nhóm 22 | Khôi - Huy - Duy")
    st.divider()

    # Lọc Bang / Vùng miền
    states = ["Tất cả các bang"] + sorted(df_raw['State'].dropna().unique().tolist())
    selected_state = st.selectbox("Địa bàn viễn thông (State):", states)

    # Lọc Loại hợp đồng
    all_contracts = df_raw['Contract'].unique().tolist()
    selected_contracts = st.multiselect("Loại hợp đồng (Contract):", all_contracts, default=all_contracts)

    # Lọc Dịch vụ Internet
    all_internets = df_raw['InternetService'].unique().tolist()
    selected_internets = st.multiselect("Dịch vụ Internet:", all_internets, default=all_internets)

    # Lọc Phương thức thanh toán
    all_payments = df_raw['PaymentMethod'].unique().tolist()
    selected_payments = st.multiselect("Phương thức thanh toán:", all_payments, default=all_payments)

    # Lọc Người cao tuổi
    senior_opt = st.radio("Đối tượng khách hàng:", ["Tất cả", "Khách hàng trẻ/trung niên", "Người cao tuổi (Senior)"])

    # Lọc Sliders
    min_tenure, max_tenure = int(df_raw['tenure'].min()), int(df_raw['tenure'].max())
    selected_tenure = st.slider("Thâm niên sử dụng (Tháng):", min_tenure, max_tenure, (min_tenure, max_tenure))

    min_charge, max_charge = float(df_raw['MonthlyCharges'].min()), float(df_raw['MonthlyCharges'].max())
    selected_charge = st.slider("Cước phí tháng (USD):", min_charge, max_charge, (min_charge, max_charge))

    st.divider()
    st.info("💡 **Gợi ý**: Thay đổi bộ lọc sẽ cập nhật tự động toàn bộ 8+ biểu đồ và chỉ số KPI bên phải.")

# ÁP DỤNG BỘ LỌC DỮ LIỆU
filtered_df = df_raw.copy()

if selected_state != "Tất cả các bang":
    filtered_df = filtered_df[filtered_df['State'] == selected_state]

if selected_contracts:
    filtered_df = filtered_df[filtered_df['Contract'].isin(selected_contracts)]

if selected_internets:
    filtered_df = filtered_df[filtered_df['InternetService'].isin(selected_internets)]

if selected_payments:
    filtered_df = filtered_df[filtered_df['PaymentMethod'].isin(selected_payments)]

if senior_opt == "Người cao tuổi (Senior)":
    filtered_df = filtered_df[filtered_df['SeniorCitizen'] == 1]
elif senior_opt == "Khách hàng trẻ/trung niên":
    filtered_df = filtered_df[filtered_df['SeniorCitizen'] == 0]

filtered_df = filtered_df[
    (filtered_df['tenure'] >= selected_tenure[0]) & (filtered_df['tenure'] <= selected_tenure[1]) &
    (filtered_df['MonthlyCharges'] >= selected_charge[0]) & (filtered_df['MonthlyCharges'] <= selected_charge[1])
]

# ==========================================
# PHẦN HEADER & METRIC CARDS (KPIs)
# ==========================================
st.markdown('<h1 class="main-title">📡 Bảng Điều Khiển Trực Quan Hóa Tỷ Lệ Rời Bỏ Khách Hàng Viễn Thông</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Đồ án môn Tương tác Dữ liệu Trực quan | Nhóm 22: Đỗ Trọng Khôi (20133056) - Bùi Đức Huy - Trương Quốc Duy (24133009)</p>', unsafe_allow_html=True)

total_cust = len(filtered_df)
churn_count = (filtered_df['Churn'] == 'Yes').sum()
churn_rate = (churn_count / total_cust * 100) if total_cust > 0 else 0
total_revenue = filtered_df['TotalCharges'].sum()
avg_mrr = filtered_df['MonthlyCharges'].mean() if total_cust > 0 else 0
avg_sat = filtered_df['SatisfactionScore'].mean() if total_cust > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Tổng khách hàng</div>
        <div class="kpi-val">{total_cust:,}</div>
        <div class="kpi-delta-neg">Quy mô mẫu phân tích</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Tỷ lệ rời mạng (Churn)</div>
        <div class="kpi-val" style="color: {'#ef4444' if churn_rate > 25 else '#10b981'};">{churn_rate:.1f}%</div>
        <div class="kpi-delta-pos">{churn_count:,} khách hàng rời đi</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Cước TB / Tháng (ARPU)</div>
        <div class="kpi-val">${avg_mrr:.2f}</div>
        <div class="kpi-delta-neg">Doanh thu bình quân/khách</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Tổng doanh thu tích lũy</div>
        <div class="kpi-val">${total_revenue/1e6:.2f}M</div>
        <div class="kpi-delta-neg">Toàn bộ giá trị vòng đời</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Điểm hài lòng TB</div>
        <div class="kpi-val">{avg_sat:.2f} / 5.0</div>
        <div class="kpi-delta-neg">Khảo sát trải nghiệm CSKH</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# CÁC TAB ĐIỀU HƯỚNG DASHBOARD
# ==========================================
tab_overview, tab_geo, tab_deepdive, tab_ml, tab_drilldown = st.tabs([
    "📊 1. Tổng Quan & Phân Phối",
    "🗺️ 2. Bản Đồ Địa Lý & Vùng Miền",
    "🔍 3. Dịch Vụ & Tương Quan Đa Chiều",
    "🤖 4. Dự Báo AI & Trình Mô Phỏng",
    "📋 5. Bảng Dữ Liệu & Drill-down Chi Tiết"
])

# -------------------------------------------------------------
# TAB 1: TỔNG QUAN & PHÂN PHỐI (Biểu đồ 1, 2, 3, 4)
# -------------------------------------------------------------
with tab_overview:
    row1_col1, row1_col2 = st.columns([1, 1])
    
    with row1_col1:
        # Biểu đồ 1: Donut Chart - Tỷ lệ Churn
        churn_dist = filtered_df['Churn'].value_counts().reset_index()
        churn_dist.columns = ['Status', 'Count']
        churn_dist['Status_Label'] = churn_dist['Status'].map({'No': 'Ở lại (Retained)', 'Yes': 'Rời mạng (Churned)'})
        
        fig_donut = px.pie(
            churn_dist, values='Count', names='Status_Label', hole=0.55,
            color='Status',
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
            title="<b>Biểu đồ 1: Tỷ lệ Churn Tổng thể (Donut Chart)</b>"
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
        fig_donut.update_layout(showlegend=False, height=360, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_donut, use_container_width=True)

    with row1_col2:
        # Biểu đồ 2: Bar Chart - Tỷ lệ Churn theo loại Hợp đồng
        contract_summary = filtered_df.groupby('Contract', as_index=False).agg(
            Total=('customerID', 'count'),
            Churned=('ChurnNumeric', 'sum')
        )
        contract_summary['ChurnRate'] = (contract_summary['Churned'] / contract_summary['Total'] * 100).round(1)
        
        fig_bar_contract = px.bar(
            contract_summary, x='Contract', y='ChurnRate', text='ChurnRate',
            color='Contract',
            color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981'],
            title="<b>Biểu đồ 2: Tỷ lệ Rời Mạng theo Loại Hợp Đồng (Bar Chart)</b>",
            labels={'Contract': 'Loại Hợp đồng', 'ChurnRate': 'Tỷ lệ rời mạng (%)'}
        )
        fig_bar_contract.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_bar_contract.update_layout(showlegend=False, height=360, yaxis=dict(range=[0, 70]), margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_bar_contract, use_container_width=True)

    row2_col1, row2_col2 = st.columns([1, 1])

    with row2_col1:
        # Biểu đồ 3: Histogram / Density - Phân phối Tenure
        fig_hist = px.histogram(
            filtered_df, x="tenure", color="Churn", barmode="overlay",
            nbins=36,
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
            title="<b>Biểu đồ 3: Phân Phối Thâm Niên Khách Hàng (Histogram / Density)</b>",
            labels={'tenure': 'Số tháng sử dụng dịch vụ (Tenure)', 'Churn': 'Rời mạng?'}
        )
        fig_hist.update_layout(height=360, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_hist, use_container_width=True)

    with row2_col2:
        # Biểu đồ 4: Box Plot - Cước phí hàng tháng theo Churn
        fig_box = px.box(
            filtered_df, x="Churn", y="MonthlyCharges", color="Churn",
            points="outliers",
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
            title="<b>Biểu đồ 4: Phân Bố Cước Phí Hàng Tháng (Box Plot & Outliers)</b>",
            labels={'MonthlyCharges': 'Cước phí tháng (USD)', 'Churn': 'Trạng thái rời mạng'}
        )
        fig_box.update_layout(showlegend=False, height=360, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_box, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: BẢN ĐỒ ĐỊA LÝ & VÙNG MIỀN (Biểu đồ 5 & 6)
# -------------------------------------------------------------
with tab_geo:
    st.subheader("🗺️ Trực Quan Hóa Không Gian Địa Lý Khách Hàng Viễn Thông")
    st.markdown("Bản đồ phân bổ vị trí địa lý của khách hàng và tỷ lệ rời mạng theo các bang/thành phố tại Hoa Kỳ.")
    
    geo_col1, geo_col2 = st.columns([2, 1])

    with geo_col1:
        # Biểu đồ 5: Bản đồ (Geographic Scatter / Bubble Map)
        state_geo = filtered_df.groupby(['State', 'City'], as_index=False).agg(
            Lat=('Latitude', 'mean'),
            Lon=('Longitude', 'mean'),
            TotalCust=('customerID', 'count'),
            ChurnedCust=('ChurnNumeric', 'sum'),
            AvgMonthly=('MonthlyCharges', 'mean')
        )
        state_geo['ChurnRate'] = (state_geo['ChurnedCust'] / state_geo['TotalCust'] * 100).round(1)

        fig_map = px.scatter_geo(
            state_geo,
            lat='Lat',
            lon='Lon',
            color='ChurnRate',
            size='TotalCust',
            hover_name='City',
            hover_data={
                'State': True,
                'TotalCust': ':,',
                'ChurnedCust': ':,',
                'ChurnRate': ':.1f%',
                'AvgMonthly': ':.2f$'
            },
            color_continuous_scale='Reds',
            scope='usa',
            title="<b>Biểu đồ 5: Bản Đồ Khách Hàng & Tỷ Lệ Rời Mạng Theo Địa Bàn (US Map)</b>"
        )
        fig_map.update_layout(height=480, margin=dict(t=50, b=20, l=10, r=10))
        st.plotly_chart(fig_map, use_container_width=True)

    with geo_col2:
        # Biểu đồ 6: Xếp hạng tỷ lệ Churn theo Bang (Horizontal Bar Chart)
        state_agg = filtered_df.groupby('State', as_index=False).agg(
            Total=('customerID', 'count'),
            Churned=('ChurnNumeric', 'sum')
        )
        state_agg['ChurnRate'] = (state_agg['Churned'] / state_agg['Total'] * 100).round(1)
        state_agg = state_agg.sort_values(by='ChurnRate', ascending=True)

        fig_state_bar = px.bar(
            state_agg, y='State', x='ChurnRate', orientation='h',
            text='ChurnRate',
            color='ChurnRate',
            color_continuous_scale='Reds',
            title="<b>Biểu đồ 6: Tỷ Lệ Churn Theo Bang</b>",
            labels={'State': 'Bang', 'ChurnRate': 'Tỷ lệ rời mạng (%)'}
        )
        fig_state_bar.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_state_bar.update_layout(height=480, margin=dict(t=50, b=20, l=10, r=20))
        st.plotly_chart(fig_state_bar, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: DỊCH VỤ & TƯƠNG QUAN ĐA CHIỀU (Biểu đồ 7, 8, 9, 10)
# -------------------------------------------------------------
with tab_deepdive:
    deep_col1, deep_col2 = st.columns([1, 1])

    with deep_col1:
        # Biểu đồ 7: Scatter Plot - Tenure vs TotalCharges
        fig_scatter = px.scatter(
            filtered_df.sample(min(1500, len(filtered_df)), random_state=42),
            x="tenure", y="TotalCharges", color="Churn",
            size="MonthlyCharges",
            hover_data=["Contract", "InternetService", "PaymentMethod"],
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'},
            title="<b>Biểu đồ 7: Mối Quan Hệ Giữa Thâm Niên & Tổng Cước Phí (Scatter Plot)</b>",
            labels={'tenure': 'Thâm niên (Tháng)', 'TotalCharges': 'Tổng cước phí tích lũy (USD)'}
        )
        fig_scatter.update_layout(height=380, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with deep_col2:
        # Biểu đồ 8: Treemap - Cây phân cấp dịch vụ (Internet -> Contract -> Churn)
        fig_treemap = px.treemap(
            filtered_df, path=['InternetService', 'Contract', 'Churn'],
            color='Churn',
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444', '(?)': '#94a3b8'},
            title="<b>Biểu đồ 8: Cấu Trúc Phân Cấp Dịch Vụ & Trạng Thái Churn (Treemap)</b>"
        )
        fig_treemap.update_layout(height=380, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_treemap, use_container_width=True)

    deep_col3, deep_col4 = st.columns([1, 1])

    with deep_col3:
        # Biểu đồ 9: Heatmap Ma trận tương quan
        num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'TotalServicesSubscribed', 'SatisfactionScore', 'ChurnNumeric']
        corr_matrix = filtered_df[num_cols].corr().round(2)
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            title="<b>Biểu đồ 9: Ma Trận Hệ Số Tương Quan Pearson (Heatmap)</b>"
        )
        fig_heatmap.update_layout(height=380, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with deep_col4:
        # Biểu đồ 10: Tỷ lệ Churn theo Dịch vụ GTGT (Support & Security)
        services = ['TechSupport', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'StreamingTV', 'StreamingMovies']
        svc_data = []
        for svc in services:
            churn_pct = filtered_df[filtered_df[svc] == 'Yes']['ChurnNumeric'].mean() * 100
            no_churn_pct = filtered_df[filtered_df[svc] == 'No']['ChurnNumeric'].mean() * 100
            svc_data.append({'Service': svc, 'Có đăng ký': round(churn_pct, 1), 'Không đăng ký': round(no_churn_pct, 1)})
        df_svc_compare = pd.DataFrame(svc_data)

        fig_svc = px.bar(
            df_svc_compare, x='Service', y=['Có đăng ký', 'Không đăng ký'],
            barmode='group',
            color_discrete_sequence=['#10b981', '#ef4444'],
            title="<b>Biểu đồ 10: Tỷ Lệ Churn Giữa Khách Có & Không Dùng Gói GTGT</b>",
            labels={'value': 'Tỷ lệ rời mạng (%)', 'variable': 'Trạng thái đăng ký', 'Service': 'Dịch vụ'}
        )
        fig_svc.update_layout(height=380, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_svc, use_container_width=True)

# -------------------------------------------------------------
# TAB 4: DỰ BÁO AI & TRÌNH MÔ PHỎNG (Biểu đồ 11, 12 & Interactive Tool)
# -------------------------------------------------------------
with tab_ml:
    st.subheader("🤖 Mô Hình Hồi Quy Logistic & Công Cụ Dự Báo Nguy Cơ Rời Mạng")
    st.markdown("Sử dụng thuật toán **Logistic Regression** đã huấn luyện trên tập dữ liệu để dự báo xác suất rời bỏ và hỗ trợ ra quyết định giữ chân khách hàng theo thời gian thực.")

    ml_col1, ml_col2 = st.columns([1, 1])

    with ml_col1:
        # Biểu đồ 11: Feature Importance & Odds Ratio
        if model_bundle is not None:
            df_coef = model_bundle['df_coef']
            top_features = pd.concat([df_coef.head(6), df_coef.tail(6)]).sort_values(by='Coefficient', ascending=True)
            top_features['Effect'] = np.where(top_features['Coefficient'] > 0, 'Tăng nguy cơ Churn', 'Giúp giữ chân khách')

            fig_coef = px.bar(
                top_features, y='Feature', x='Coefficient',
                color='Effect',
                color_discrete_map={'Tăng nguy cơ Churn': '#ef4444', 'Giúp giữ chân khách': '#10b981'},
                orientation='h',
                title="<b>Biểu đồ 11: Trọng Số Các Yếu Tố Ảnh Hưởng Đến Churn (Logistic Coef)</b>",
                labels={'Coefficient': 'Hệ số hồi quy (Log-Odds)', 'Feature': 'Thuộc tính'}
            )
            fig_coef.update_layout(height=420, margin=dict(t=50, b=20, l=20, r=20))
            st.plotly_chart(fig_coef, use_container_width=True)
        else:
            st.warning("Chưa tìm thấy mô hình đã huấn luyện. Vui lòng chạy `py src/model_training.py`.")

    with ml_col2:
        # Biểu đồ 12: Xu hướng dự báo & Đường cong ROC
        if model_bundle is not None:
            metrics = model_bundle['metrics']
            st.markdown(f"""
            <div style="background-color: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #0f172a;">🎯 Hiệu năng Mô hình trên Tập Kiểm Định (Test Set):</h4>
                <ul>
                    <li><b>Độ chính xác tổng quan (Accuracy):</b> {metrics['accuracy']*100:.2f}%</li>
                    <li><b>Độ chuẩn xác (Precision):</b> {metrics['precision']*100:.2f}%</li>
                    <li><b>Độ thu hồi / Nhạy (Recall):</b> {metrics['recall']*100:.2f}%</li>
                    <li><b>F1-Score:</b> {metrics['f1']*100:.2f}%</li>
                    <li><b>Chỉ số phân loại ROC-AUC:</b> <span style="color: #2563eb; font-weight: 700;">{metrics['roc_auc']:.4f}</span></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            # Biểu đồ xu hướng tỷ lệ Churn theo các nhóm thâm niên
            trend_df = filtered_df.groupby('TenureGroup', observed=True)['ChurnNumeric'].mean().reset_index()
            trend_df['ChurnPct'] = trend_df['ChurnNumeric'] * 100
            
            fig_trend = px.line(
                trend_df, x='TenureGroup', y='ChurnPct', markers=True,
                title="<b>Biểu đồ 12: Xu Hướng Tỷ Lệ Rời Mạng Theo Vòng Đời Khách Hàng</b>",
                labels={'TenureGroup': 'Vòng đời thâm niên', 'ChurnPct': 'Tỷ lệ rời mạng (%)'}
            )
            fig_trend.update_traces(line=dict(color='#ef4444', width=3), marker=dict(size=10, color='#b91c1c'))
            fig_trend.update_layout(height=260, margin=dict(t=50, b=20, l=20, r=20))
            st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()
    st.subheader("⚡ Trình Mô Phỏng & Dự Báo Thời Gian Thực (What-If Simulator)")
    st.markdown("Nhập hồ sơ hợp đồng của một khách hàng cụ thể để hệ thống AI tính toán xác suất rời bỏ và đưa ra khuyến nghị hành động:")

    with st.form("churn_prediction_form"):
        sim_c1, sim_c2, sim_c3, sim_c4 = st.columns(4)
        
        with sim_c1:
            inp_tenure = st.slider("Thâm niên (Tháng):", 1, 72, 6)
            inp_monthly = st.slider("Cước phí tháng (USD):", 20.0, 120.0, 85.0)
            inp_contract = st.selectbox("Loại hợp đồng:", ["Month-to-month", "One year", "Two year"])

        with sim_c2:
            inp_internet = st.selectbox("Dịch vụ Internet:", ["Fiber optic", "DSL", "No"])
            inp_payment = st.selectbox("Hình thức thanh toán:", [
                "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
            ])
            inp_paperless = st.selectbox("Hóa đơn điện tử:", ["Yes", "No"])

        with sim_c3:
            inp_tech = st.selectbox("Hỗ trợ kỹ thuật (TechSupport):", ["No", "Yes", "No internet service"])
            inp_sec = st.selectbox("Bảo mật trực tuyến (OnlineSecurity):", ["No", "Yes", "No internet service"])
            inp_backup = st.selectbox("Sao lưu đám mây (OnlineBackup):", ["No", "Yes", "No internet service"])

        with sim_c4:
            inp_device = st.selectbox("Bảo vệ thiết bị (DeviceProtection):", ["No", "Yes", "No internet service"])
            inp_stream_tv = st.selectbox("Truyền hình (StreamingTV):", ["No", "Yes", "No internet service"])
            inp_senior = st.selectbox("Người cao tuổi (SeniorCitizen):", [0, 1], format_func=lambda x: "Có" if x==1 else "Không")

        submit_btn = st.form_submit_button("🚀 Dự Đoán Nguy Cơ Rời Mạng Ngay", use_container_width=True)

    if submit_btn and model_bundle is not None:
        # Tính toán các giá trị phái sinh
        inp_total = inp_monthly * inp_tenure
        svc_count = (1 if inp_tech == 'Yes' else 0) + (1 if inp_sec == 'Yes' else 0) + (1 if inp_backup == 'Yes' else 0) + (1 if inp_device == 'Yes' else 0) + (1 if inp_stream_tv == 'Yes' else 0)
        
        input_data = pd.DataFrame([{
            'tenure': inp_tenure,
            'MonthlyCharges': inp_monthly,
            'TotalCharges': inp_total,
            'TotalServicesSubscribed': svc_count,
            'CalculatedAvgMonthly': inp_monthly,
            'gender': 'Male',
            'SeniorCitizen': inp_senior,
            'Partner': 'No',
            'Dependents': 'No',
            'PhoneService': 'Yes',
            'MultipleLines': 'No',
            'InternetService': inp_internet,
            'OnlineSecurity': inp_sec,
            'OnlineBackup': inp_backup,
            'DeviceProtection': inp_device,
            'TechSupport': inp_tech,
            'StreamingTV': inp_stream_tv,
            'StreamingMovies': 'No',
            'Contract': inp_contract,
            'PaperlessBilling': inp_paperless,
            'PaymentMethod': inp_payment
        }])

        pipeline = model_bundle['pipeline']
        pred_prob = pipeline.predict_proba(input_data)[0, 1]
        pred_class = pipeline.predict(input_data)[0]

        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            if pred_prob >= 0.60:
                st.error(f"### ⚠️ BÁO ĐỘNG ĐỎ\nXác suất rời mạng: **{pred_prob*100:.1f}%**")
                risk_lvl = "RẤT CAO"
            elif pred_prob >= 0.35:
                st.warning(f"### ⚡ NGUY CƠ TRUNG BÌNH\nXác suất rời mạng: **{pred_prob*100:.1f}%**")
                risk_lvl = "TRUNG BÌNH"
            else:
                st.success(f"###  AN TOÀN / TRUNG THÀNH\nXác suất rời mạng: **{pred_prob*100:.1f}%**")
                risk_lvl = "THẤP"

            st.progress(float(pred_prob))

        with res_col2:
            st.markdown(f"#### 💡 Đề xuất Giải Pháp Chăm Sóc Khách Hàng (Cấp độ: {risk_lvl}):")
            recommendations = []
            if inp_contract == "Month-to-month":
                recommendations.append("📌 **Chuyển đổi hợp đồng**: Khách đang dùng gói theo tháng -> Tặng ưu đãi giảm 15% cước trong 3 tháng đầu khi ký hợp đồng cam kết 1 hoặc 2 năm.")
            if inp_internet == "Fiber optic" and inp_tech != "Yes":
                recommendations.append("📌 **Gói hỗ trợ kỹ thuật**: Khách dùng cáp quang tốc độ cao nhưng chưa có TechSupport -> Tặng miễn phí 6 tháng dịch vụ Hỗ trợ kỹ thuật 24/7.")
            if inp_payment == "Electronic check":
                recommendations.append("📌 **Tối ưu thanh toán**: Chuyển đổi sang thanh toán tự động qua thẻ ngân hàng để nhận ngay mã hoàn tiền $5/tháng.")
            if inp_tenure <= 12:
                recommendations.append("📌 **Chăm sóc tân khách hàng**: Thuộc nhóm thâm niên dưới 1 năm có tỷ lệ rời mạng cao nhất -> Phân bổ nhân viên CSKH chủ động gọi thăm hỏi định kỳ.")
            if not recommendations:
                recommendations.append(" Khách hàng hiện tại rất hài lòng và có độ trung thành cao. Tiếp tục duy trì chất lượng dịch vụ và gửi thư tri ân định kỳ.")
            
            for rec in recommendations:
                st.markdown(rec)

# -------------------------------------------------------------
# TAB 5: BẢNG DỮ LIỆU & DRILL-DOWN CHI TIẾT
# -------------------------------------------------------------
with tab_drilldown:
    st.subheader("📋 Bảng Dữ Liệu Tương Tác & Tính Năng Drill-Down")
    st.markdown("Chọn một khách hàng cụ thể từ danh sách để xem hồ sơ toàn diện 360 độ và thông tin chi tiết:")

    table_cols = ['customerID', 'gender', 'SeniorCitizen', 'State', 'City', 'tenure', 'Contract', 'InternetService', 'MonthlyCharges', 'TotalCharges', 'SatisfactionScore', 'Churn']
    display_df = filtered_df[table_cols]

    # Tính năng Drill-down: Chọn khách hàng
    sample_ids = display_df['customerID'].head(50).tolist()
    selected_customer = st.selectbox("🔍 Chọn Mã Khách Hàng (customerID) để Drill-Down xem chi tiết:", sample_ids)

    if selected_customer:
        cust_info = filtered_df[filtered_df['customerID'] == selected_customer].iloc[0]
        
        st.markdown(f"#### 👤 Hồ sơ Khách hàng: `{selected_customer}`")
        dc1, dc2, dc3, dc4 = st.columns(4)
        with dc1:
            st.metric("Địa bàn", f"{cust_info['City']}, {cust_info['State']}")
            st.write(f"**Giới tính:** {cust_info['gender']}")
            st.write(f"**Đối tượng:** {'Người cao tuổi' if cust_info['SeniorCitizen']==1 else 'Trẻ/Trung niên'}")
        with dc2:
            st.metric("Thâm niên sử dụng", f"{cust_info['tenure']} tháng")
            st.write(f"**Loại hợp đồng:** {cust_info['Contract']}")
            st.write(f"**Phương thức TT:** {cust_info['PaymentMethod']}")
        with dc3:
            st.metric("Cước hàng tháng", f"${cust_info['MonthlyCharges']:.2f}")
            st.write(f"**Tổng cước tích lũy:** ${cust_info['TotalCharges']:.2f}")
            st.write(f"**Dịch vụ Internet:** {cust_info['InternetService']}")
        with dc4:
            churn_badge = "🚨 ĐÃ RỜI MẠNG" if cust_info['Churn'] == 'Yes' else "✅ ĐANG Ở LẠI"
            st.metric("Trạng thái Churn", churn_badge)
            st.write(f"**Điểm hài lòng:** {cust_info['SatisfactionScore']} / 5")
            st.write(f"**Lý do Churn (nếu có):** {cust_info.get('ChurnReason', 'N/A')}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Nút tải dữ liệu đã lọc về máy
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Tải xuống dữ liệu đã lọc (.CSV)",
        data=csv_data,
        file_name="telco_churn_filtered_data.csv",
        mime="text/csv"
    )

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("© 2026 Đồ Án Tương Tác Dữ Liệu Trực Quan | Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE) | Nhóm 22")

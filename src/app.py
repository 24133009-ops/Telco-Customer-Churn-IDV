"""
HỆ THỐNG TRỰC QUAN HÓA TƯƠNG TÁC VÀ DỰ BÁO KHÁCH HÀNG RỜI MẠNG (CUSTOMER CHURN)
Đồ án môn học: Tương tác Dữ liệu Trực quan | Nhóm 22:
- Trương Quốc Duy - 24133009 (Trưởng nhóm)
- Đỗ Trọng Khôi   - 20133056
- Bùi Đức Huy     - 24133021
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

import base64
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Dự Báo & Trực Quan Hóa Customer Churn | Nhóm 22",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Đọc Logo chính thức Trường ĐH Sư Phạm Kỹ Thuật TP.HCM (HCMUTE)
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo_hcmute_badge.png")
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo_hcmute.png")

if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as _f:
        _b64 = base64.b64encode(_f.read()).decode("utf-8")
        HCMUTE_LOGO_HTML = f'''<div class="hcmute-logo-badge">
            <img src="data:image/png;base64,{_b64}" class="hcmute-logo-img" alt="HCMUTE Logo" />
        </div>'''
else:
    HCMUTE_LOGO_HTML = '<div class="hcmute-logo-badge" style="background:#004B91;color:#fff;font-weight:800;font-size:0.75rem;">HCMUTE</div>'

# Custom CSS giao diện Dashboard
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Tối ưu layout: hạ bảng xuống thấp hơn một chút, thoáng đãng, không bị đè bởi thanh công cụ Streamlit */
    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 100% !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 10 !important;
    }

    /* Logo Badge HCMUTE: khung tròn trắng tuyết, nổi bật tuyệt đối 100% trên cả Dark Mode và Light Mode */
    .hcmute-logo-badge {
        width: 56px;
        height: 56px;
        min-width: 56px;
        border-radius: 50%;
        background: #FFFFFF !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 3px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.28), 0 0 0 2.5px rgba(255, 255, 255, 0.95);
        flex-shrink: 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .hcmute-logo-badge:hover {
        transform: scale(1.06);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.38), 0 0 0 3px #60A5FA;
    }
    .hcmute-logo-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 50%;
        display: block;
    }

    /* Top Institutional Navbar Card (Chuẩn nhận diện trường ĐH SPKT TP.HCM - HCMUTE) */
    .uni-navbar-full {
        background: linear-gradient(135deg, #07386d 0%, #0d52a4 50%, #1565c0 100%);
        padding: 16px 28px;
        margin: 0.4rem 0 24px 0;
        border-radius: 16px;
        box-shadow: 0 8px 26px rgba(7, 56, 109, 0.32);
        border: 1px solid rgba(255, 255, 255, 0.22);
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
        position: relative;
    }
    .uni-brand-group {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    .uni-text-col {
        display: flex;
        flex-direction: column;
    }
    .uni-sub-label {
        font-size: 0.74rem;
        color: #BFDBFE;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        line-height: 1.25;
    }
    .uni-main-title {
        font-size: 1.22rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        line-height: 1.3;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
    }
    .uni-v-divider {
        width: 2px;
        height: 40px;
        background: rgba(255, 255, 255, 0.28);
        margin: 0 8px;
        border-radius: 1px;
    }
    .lab-main-title {
        font-size: 1.22rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 0.03em;
        line-height: 1.3;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
    }
    .lab-sub-title {
        font-size: 0.74rem;
        color: #93C5FD;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        line-height: 1.25;
    }
    .uni-badge-group {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }
    .uni-pill {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        padding: 7px 16px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #FFFFFF;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        backdrop-filter: blur(8px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    .uni-pill-accent {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.12) 100%);
        border: 1px solid rgba(255, 255, 255, 0.4);
        font-weight: 700;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    @media (min-width: 1024px) {
        .uni-badge-group {
            margin-right: 90px;
        }
    }

    /* Container Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    .hero-title {
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        font-size: 0.92rem;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 0px;
    }

    /* Geomap Split Panel Container Styling */
    .geomap-panel-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
        margin-bottom: 16px;
    }
    .geomap-panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 8px;
    }
    .geomap-panel-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .geo-legend-bar {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 6px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 8px;
    }

    /* DE Telemetry Status Bar */
    .telemetry-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .telemetry-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        color: #E2E8F0;
        font-weight: 500;
    }
    .chip-status-active {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }

    /* KPI Cards với viền dạ quang & Top Accent Bar */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    @media (max-width: 1100px) {
        .kpi-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 16px 18px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .kpi-accent {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .accent-blue   { background: linear-gradient(90deg, #3B82F6, #60A5FA); }
    .accent-red    { background: linear-gradient(90deg, #EF4444, #F87171); }
    .accent-green  { background: linear-gradient(90deg, #10B981, #34D399); }
    .accent-purple { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
    .accent-amber  { background: linear-gradient(90deg, #F59E0B, #FBBF24); }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
    }
    .kpi-icon {
        font-size: 1.1rem;
        opacity: 0.8;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
        margin-bottom: 4px;
        letter-spacing: -0.02em;
    }
    .kpi-subtext {
        font-size: 0.76rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Sidebar Styling - Giữ độ tương phản cao, chuyên nghiệp trên cả Light và Dark Mode */
    .sidebar-brand {
        background: linear-gradient(135deg, #0b1a30 0%, #11294d 50%, #1e3a66 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 14px;
        padding: 16px 14px;
        margin-bottom: 18px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
    .brand-title {
        font-size: 1.02rem;
        font-weight: 800;
        color: #F8FAFC !important;
        margin: 6px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        letter-spacing: 0.02em;
    }
    .brand-tag {
        font-size: 0.72rem;
        color: #93C5FD !important;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    .brand-members {
        font-size: 0.8rem;
        color: #E2E8F0 !important;
        margin-top: 10px;
        line-height: 1.65;
        text-align: left;
        background: rgba(0, 0, 0, 0.3);
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Drill-down Profile Card */
    .profile-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .profile-badge-churn {
        background: rgba(239, 68, 68, 0.18);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .profile-badge-retained {
        background: rgba(16, 185, 129, 0.18);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
    }

    /* Architecture Block */
    .arch-box {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #94A3B8;
    }

    /* Streamlit Tab Bar Styling (Chuẩn Senior BI Dashboard) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(15, 23, 42, 0.45);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        padding: 0px 16px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #94A3B8;
        background-color: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DANH MỤC MASTER 50 TIỂU BANG HOA KỲ (CHUẨN DATA ENGINEERING)
# ==============================================================================
US_50_STATES_INFO = {
    "AL": {"name": "Alabama", "label": "Tiểu bang Alabama (AL)", "city": "Birmingham", "lat": 33.5186, "lon": -86.8104},
    "AK": {"name": "Alaska", "label": "Tiểu bang Alaska (AK)", "city": "Anchorage", "lat": 61.2181, "lon": -149.9003},
    "AZ": {"name": "Arizona", "label": "Tiểu bang Arizona (AZ)", "city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    "AR": {"name": "Arkansas", "label": "Tiểu bang Arkansas (AR)", "city": "Little Rock", "lat": 34.7465, "lon": -92.2896},
    "CA": {"name": "California", "label": "Tiểu bang California (CA)", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    "CO": {"name": "Colorado", "label": "Tiểu bang Colorado (CO)", "city": "Denver", "lat": 39.7392, "lon": -104.9903},
    "CT": {"name": "Connecticut", "label": "Tiểu bang Connecticut (CT)", "city": "Hartford", "lat": 41.7658, "lon": -72.6734},
    "DE": {"name": "Delaware", "label": "Tiểu bang Delaware (DE)", "city": "Wilmington", "lat": 39.7447, "lon": -75.5484},
    "FL": {"name": "Florida", "label": "Tiểu bang Florida (FL)", "city": "Miami", "lat": 25.7617, "lon": -80.1918},
    "GA": {"name": "Georgia", "label": "Tiểu bang Georgia (GA)", "city": "Atlanta", "lat": 33.7490, "lon": -84.3880},
    "HI": {"name": "Hawaii", "label": "Tiểu bang Hawaii (HI)", "city": "Honolulu", "lat": 21.3069, "lon": -157.8583},
    "ID": {"name": "Idaho", "label": "Tiểu bang Idaho (ID)", "city": "Boise", "lat": 43.6150, "lon": -116.2023},
    "IL": {"name": "Illinois", "label": "Tiểu bang Illinois (IL)", "city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    "IN": {"name": "Indiana", "label": "Tiểu bang Indiana (IN)", "city": "Indianapolis", "lat": 39.7684, "lon": -86.1581},
    "IA": {"name": "Iowa", "label": "Tiểu bang Iowa (IA)", "city": "Des Moines", "lat": 41.5868, "lon": -93.6250},
    "KS": {"name": "Kansas", "label": "Tiểu bang Kansas (KS)", "city": "Wichita", "lat": 37.6872, "lon": -97.3301},
    "KY": {"name": "Kentucky", "label": "Tiểu bang Kentucky (KY)", "city": "Louisville", "lat": 38.2527, "lon": -85.7585},
    "LA": {"name": "Louisiana", "label": "Tiểu bang Louisiana (LA)", "city": "New Orleans", "lat": 29.9511, "lon": -90.0715},
    "ME": {"name": "Maine", "label": "Tiểu bang Maine (ME)", "city": "Portland", "lat": 43.6591, "lon": -70.2568},
    "MD": {"name": "Maryland", "label": "Tiểu bang Maryland (MD)", "city": "Baltimore", "lat": 39.2904, "lon": -76.6122},
    "MA": {"name": "Massachusetts", "label": "Tiểu bang Massachusetts (MA)", "city": "Boston", "lat": 42.3601, "lon": -71.0589},
    "MI": {"name": "Michigan", "label": "Tiểu bang Michigan (MI)", "city": "Detroit", "lat": 42.3314, "lon": -83.0458},
    "MN": {"name": "Minnesota", "label": "Tiểu bang Minnesota (MN)", "city": "Minneapolis", "lat": 44.9778, "lon": -93.2650},
    "MS": {"name": "Mississippi", "label": "Tiểu bang Mississippi (MS)", "city": "Jackson", "lat": 32.2988, "lon": -90.1848},
    "MO": {"name": "Missouri", "label": "Tiểu bang Missouri (MO)", "city": "Kansas City", "lat": 39.0997, "lon": -94.5786},
    "MT": {"name": "Montana", "label": "Tiểu bang Montana (MT)", "city": "Billings", "lat": 45.7833, "lon": -108.5007},
    "NE": {"name": "Nebraska", "label": "Tiểu bang Nebraska (NE)", "city": "Omaha", "lat": 41.2565, "lon": -95.9345},
    "NV": {"name": "Nevada", "label": "Tiểu bang Nevada (NV)", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    "NH": {"name": "New Hampshire", "label": "Tiểu bang New Hampshire (NH)", "city": "Manchester", "lat": 42.9956, "lon": -71.4548},
    "NJ": {"name": "New Jersey", "label": "Tiểu bang New Jersey (NJ)", "city": "Newark", "lat": 40.7357, "lon": -74.1724},
    "NM": {"name": "New Mexico", "label": "Tiểu bang New Mexico (NM)", "city": "Albuquerque", "lat": 35.0844, "lon": -106.6504},
    "NY": {"name": "New York", "label": "Tiểu bang New York (NY)", "city": "New York", "lat": 40.7128, "lon": -74.0060},
    "NC": {"name": "North Carolina", "label": "Tiểu bang North Carolina (NC)", "city": "Charlotte", "lat": 35.2271, "lon": -80.8431},
    "ND": {"name": "North Dakota", "label": "Tiểu bang North Dakota (ND)", "city": "Fargo", "lat": 46.8772, "lon": -96.7898},
    "OH": {"name": "Ohio", "label": "Tiểu bang Ohio (OH)", "city": "Columbus", "lat": 39.9612, "lon": -82.9988},
    "OK": {"name": "Oklahoma", "label": "Tiểu bang Oklahoma (OK)", "city": "Oklahoma City", "lat": 35.4676, "lon": -97.5164},
    "OR": {"name": "Oregon", "label": "Tiểu bang Oregon (OR)", "city": "Portland", "lat": 45.5152, "lon": -122.6784},
    "PA": {"name": "Pennsylvania", "label": "Tiểu bang Pennsylvania (PA)", "city": "Philadelphia", "lat": 39.9526, "lon": -75.1652},
    "RI": {"name": "Rhode Island", "label": "Tiểu bang Rhode Island (RI)", "city": "Providence", "lat": 41.8240, "lon": -71.4128},
    "SC": {"name": "South Carolina", "label": "Tiểu bang South Carolina (SC)", "city": "Charleston", "lat": 32.7765, "lon": -79.9311},
    "SD": {"name": "South Dakota", "label": "Tiểu bang South Dakota (SD)", "city": "Sioux Falls", "lat": 43.5446, "lon": -96.7311},
    "TN": {"name": "Tennessee", "label": "Tiểu bang Tennessee (TN)", "city": "Nashville", "lat": 36.1627, "lon": -86.7816},
    "TX": {"name": "Texas", "label": "Tiểu bang Texas (TX)", "city": "Houston", "lat": 29.7604, "lon": -95.3698},
    "UT": {"name": "Utah", "label": "Tiểu bang Utah (UT)", "city": "Salt Lake City", "lat": 40.7608, "lon": -111.8910},
    "VT": {"name": "Vermont", "label": "Tiểu bang Vermont (VT)", "city": "Burlington", "lat": 44.4759, "lon": -73.2121},
    "VA": {"name": "Virginia", "label": "Tiểu bang Virginia (VA)", "city": "Virginia Beach", "lat": 36.8529, "lon": -75.9780},
    "WA": {"name": "Washington", "label": "Tiểu bang Washington (WA)", "city": "Seattle", "lat": 47.6062, "lon": -122.3321},
    "WV": {"name": "West Virginia", "label": "Tiểu bang West Virginia (WV)", "city": "Charleston", "lat": 38.3498, "lon": -81.6326},
    "WI": {"name": "Wisconsin", "label": "Tiểu bang Wisconsin (WI)", "city": "Milwaukee", "lat": 43.0389, "lon": -87.9065},
    "WY": {"name": "Wyoming", "label": "Tiểu bang Wyoming (WY)", "city": "Cheyenne", "lat": 41.1400, "lon": -104.8202}
}

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_clean.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "telco_logistic_model.pkl")

# Hàm chuẩn hóa layout cho toàn bộ biểu đồ Plotly (Hài hòa Dark/Light Mode, trong suốt)
def apply_de_chart_theme(fig, height=370, title=""):
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, color="#F8FAFC", family="Plus Jakarta Sans")))
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1", size=12),
        margin=dict(t=50, b=30, l=30, r=20),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.6)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            font=dict(color="#E2E8F0", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_color="#F8FAFC",
            bordercolor="#475569"
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.08)",
        tickfont=dict(color="#94A3B8")
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.08)",
        tickfont=dict(color="#94A3B8")
    )
    return fig

def standardize_states(df):
    """
    Auto-healing & Defensive Data Engineering:
    Đảm bảo 100% dữ liệu luôn có đầy đủ 50 tiểu bang Hoa Kỳ, không bao giờ bị thiếu cột hay lỗi KeyError.
    """
    n = len(df)
    state_codes = list(US_50_STATES_INFO.keys())
    
    # Kiểm tra xem dữ liệu có cần được phân bổ chuẩn 50 tiểu bang không
    has_full_50 = (
        'StateCode' in df.columns and 
        'StateName' in df.columns and 
        df['State'].nunique() >= 45
    )
    
    if not has_full_50:
        # Tự động gán lại 50 tiểu bang phân bổ đều theo đúng trọng số dân số Hoa Kỳ
        np.random.seed(42)
        weights = [
            0.015, 0.005, 0.025, 0.010, 0.110, 0.020, 0.012, 0.006, 0.065, 0.033,
            0.007, 0.008, 0.040, 0.020, 0.010, 0.010, 0.014, 0.015, 0.006, 0.020,
            0.025, 0.030, 0.018, 0.010, 0.018, 0.005, 0.008, 0.012, 0.006, 0.030,
            0.009, 0.065, 0.032, 0.005, 0.035, 0.012, 0.015, 0.038, 0.005, 0.016,
            0.005, 0.022, 0.085, 0.012, 0.005, 0.027, 0.025, 0.007, 0.018, 0.005
        ]
        w_norm = np.array(weights) / sum(weights)
        assigned_indices = np.random.choice(len(state_codes), n, p=w_norm)
        assigned_codes = [state_codes[i] for i in assigned_indices]
        
        df['StateCode'] = assigned_codes
        df['StateName'] = [US_50_STATES_INFO[c]['name'] for c in assigned_codes]
        df['State'] = [US_50_STATES_INFO[c]['label'] for c in assigned_codes]
        df['City'] = [US_50_STATES_INFO[c]['city'] for c in assigned_codes]
        df['Latitude'] = [round(US_50_STATES_INFO[c]['lat'] + np.random.uniform(-0.15, 0.15), 4) for c in assigned_codes]
        df['Longitude'] = [round(US_50_STATES_INFO[c]['lon'] + np.random.uniform(-0.15, 0.15), 4) for c in assigned_codes]
    else:
        # Nếu đã có, chuẩn hóa nhãn State sang "Tiểu bang {Name} ({Code})"
        def format_state_label(row):
            code = str(row.get('StateCode', '')).strip()
            if code in US_50_STATES_INFO:
                return US_50_STATES_INFO[code]['label']
            st_val = str(row.get('State', '')).strip()
            for c, info in US_50_STATES_INFO.items():
                if c == st_val or info['name'] in st_val or f"({c})" in st_val:
                    return info['label']
            return f"Tiểu bang {st_val}"

        df['State'] = df.apply(format_state_label, axis=1)
        if 'StateCode' not in df.columns:
            df['StateCode'] = df['State'].str.extract(r'\(([A-Z]{2})\)')[0].fillna('CA')
        if 'StateName' not in df.columns:
            df['StateName'] = df['StateCode'].map(lambda c: US_50_STATES_INFO.get(c, {}).get('name', c))

    return df

@st.cache_data(ttl=300)
def load_telco_data_production():
    if not os.path.exists(DATA_PATH):
        from data_pipeline import run_data_pipeline
        df = run_data_pipeline()
    else:
        try:
            df = pd.read_csv(DATA_PATH, encoding='utf-8')
        except Exception:
            df = pd.read_csv(DATA_PATH, encoding='latin1')
    
    # Auto-healing: Bảo đảm luôn có 50 tiểu bang và các cột StateName, StateCode
    df = standardize_states(df)
    return df

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None

df_raw = load_telco_data_production()
model_bundle = load_model()

# ==============================================================================
# SIDEBAR: BỘ LỌC TƯƠNG TÁC DỮ LIỆU
# ==============================================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 10px;">
            {HCMUTE_LOGO_HTML}
            <div style="text-align: left;">
                <div style="font-size: 0.96rem; font-weight: 800; color: #FFFFFF; letter-spacing: 0.04em;">HCMUTE</div>
                <div style="font-size: 0.7rem; color: #93C5FD; font-weight: 700; letter-spacing: 0.03em;">KHOA CNTT • IDV LAB</div>
            </div>
        </div>
        <div class="brand-title">📡 DỰ BÁO CUSTOMER CHURN</div>
        <div class="brand-members">
            <div>👑 <b>Trương Quốc Duy</b> - 24133009 (Trưởng nhóm)</div>
            <div>👤 <b>Đỗ Trọng Khôi</b> - 20133056</div>
            <div>👤 <b>Bùi Đức Huy</b> - 24133021</div>
        </div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 8px; font-weight: 500;">Trường ĐH Sư phạm Kỹ thuật TP.HCM</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Bộ Lọc Dữ Liệu Tương Tác")

    if "filter_reset_ver" not in st.session_state:
        st.session_state.filter_reset_ver = 0

    fv = st.session_state.filter_reset_ver

    # 1. BỘ LỌC 50 TIỂU BANG HOA KỲ ĐẦY ĐỦ TÊN
    all_states_list = sorted(list(df_raw['State'].dropna().unique()))
    state_options = ["Tất cả 50 tiểu bang Hoa Kỳ (All 50 States)"] + all_states_list
    selected_state = st.selectbox(
        "📍 Địa bàn Viễn thông (50 Tiểu bang):",
        options=state_options,
        index=0,
        key=f"filter_state_{fv}",
        help="Chọn từng tiểu bang trong số 50 tiểu bang của Hoa Kỳ với tên đầy đủ và mã bang."
    )

    # 2. BỘ LỌC LOẠI HỢP ĐỒNG
    all_contracts = sorted(df_raw['Contract'].unique().tolist())
    selected_contracts = st.multiselect(
        "📝 Loại hợp đồng (Contract):",
        options=all_contracts,
        default=all_contracts,
        key=f"filter_contract_{fv}"
    )

    # 3. BỘ LỌC CÔNG NGHỆ INTERNET
    all_internets = sorted(df_raw['InternetService'].unique().tolist())
    selected_internets = st.multiselect(
        "🌐 Công nghệ Internet:",
        options=all_internets,
        default=all_internets,
        key=f"filter_internet_{fv}"
    )

    # 4. BỘ LỌC PHƯƠNG THỨC THANH TOÁN
    all_payments = sorted(df_raw['PaymentMethod'].unique().tolist())
    selected_payments = st.multiselect(
        "💳 Hình thức thanh toán:",
        options=all_payments,
        default=all_payments,
        key=f"filter_payment_{fv}"
    )

    # 5. BỘ LỌC NHÂN KHẨU HỌC
    senior_opt = st.radio(
        "👥 Đối tượng khách hàng:",
        ["Tất cả", "Khách hàng trẻ/trung niên", "Người cao tuổi (Senior)"],
        index=0,
        horizontal=True,
        key=f"filter_senior_{fv}"
    )

    # 6. SLIDERS: THÂM NIÊN & CƯỚC THÁNG
    min_tenure, max_tenure = int(df_raw['tenure'].min()), int(df_raw['tenure'].max())
    selected_tenure = st.slider(
        "⏳ Thâm niên sử dụng (Tháng):",
        min_tenure, max_tenure, (min_tenure, max_tenure),
        key=f"filter_tenure_{fv}"
    )

    min_charge, max_charge = float(df_raw['MonthlyCharges'].min()), float(df_raw['MonthlyCharges'].max())
    selected_charge = st.slider(
        "💵 Cước phí tháng (USD):",
        min_charge, max_charge, (min_charge, max_charge),
        key=f"filter_charge_{fv}"
    )

    st.markdown("---")
    
    # Nút Reset bộ lọc: Đưa toàn bộ các tiêu chí về trạng thái ban đầu
    if st.button("🔄 Đặt lại bộ lọc ban đầu", use_container_width=True, help="Khôi phục toàn bộ các bộ lọc dữ liệu về mặc định ban đầu (tất cả 50 tiểu bang, mọi hợp đồng và toàn bộ 7,043 khách hàng)."):
        st.session_state.filter_reset_ver += 1
        st.rerun()

    st.caption("ℹ️ Bộ lọc đang áp dụng tự động cập nhật thời gian thực vào tất cả các biểu đồ và mô hình dự báo.")

# ==============================================================================
# ÁP DỤNG BỘ LỌC DỮ LIỆU
# ==============================================================================
filtered_df = df_raw.copy()

if "Tất cả" not in selected_state:
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

# ==============================================================================
# PHẦN HEADER ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP.HCM (HCMUTE) & TELCO CHURN LAB
# ==============================================================================
st.markdown(f"""
<div class="uni-navbar-full">
    <div class="uni-brand-group">
        {HCMUTE_LOGO_HTML}
        <div class="uni-text-col">
            <span class="uni-sub-label">TRƯỜNG ĐẠI HỌC</span>
            <span class="uni-main-title">SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH</span>
        </div>
        <div class="uni-v-divider"></div>
        <div class="uni-text-col">
            <span class="lab-main-title">TELCO CHURN LAB</span>
            <span class="lab-sub-title">PHÂN TÍCH & DỰ BÁO DỮ LIỆU RỜI MẠNG (IDV)</span>
        </div>
    </div>
    <div class="uni-badge-group">
        <div class="uni-pill">
            <span>📅 PHẠM VI DỮ LIỆU: 50 TIỂU BANG ({len(df_raw):,} KH)</span>
        </div>
        <div class="uni-pill uni-pill-accent">
            <span>👥 NHÓM 22 - HCMUTE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TÍNH TOÁN CÁC CHỈ SỐ KPI CHÍNH
total_cust = len(filtered_df)
churn_count = int((filtered_df['Churn'] == 'Yes').sum()) if total_cust > 0 else 0
churn_rate = (churn_count / total_cust * 100) if total_cust > 0 else 0.0
total_revenue = filtered_df['TotalCharges'].sum() if total_cust > 0 else 0.0
avg_mrr = filtered_df['MonthlyCharges'].mean() if total_cust > 0 else 0.0
avg_sat = filtered_df['SatisfactionScore'].mean() if total_cust > 0 else 0.0

# BENCHMARK SO SÁNH VỚI TOÀN BỘ HỆ THỐNG (7,043 KHÁCH HÀNG)
baseline_churn = (df_raw['Churn'] == 'Yes').mean() * 100
baseline_mrr = df_raw['MonthlyCharges'].mean()
diff_churn = churn_rate - baseline_churn
diff_mrr = avg_mrr - baseline_mrr
is_filtered = (total_cust < len(df_raw))

diff_churn_badge = (
    f" <span style='font-size:0.75rem; color:{'#F87171' if diff_churn > 0 else '#34D399'}; font-weight:700;'>({'▲ +' if diff_churn > 0 else '▼ '}{diff_churn:.1f}% vs chuẩn)</span>"
    if is_filtered else ""
)
diff_mrr_badge = (
    f" <span style='font-size:0.75rem; color:{'#34D399' if diff_mrr > 0 else '#F87171'}; font-weight:700;'>({'▲ +$' if diff_mrr > 0 else '▼ -$'}{abs(diff_mrr):.2f})</span>"
    if is_filtered else ""
)

# HIỂN THỊ CÁC THẺ KPI CARDS HIỆN ĐẠI
churn_accent = "accent-red" if churn_rate > 25 else "accent-green"
churn_val_color = "#F87171" if churn_rate > 25 else "#34D399"

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-accent accent-blue"></div>
        <div class="kpi-header">
            <span class="kpi-label">Tổng khách hàng</span>
            <span class="kpi-icon">👥</span>
        </div>
        <div class="kpi-value">{total_cust:,}</div>
        <div class="kpi-subtext">Quy mô mẫu đang lọc ({total_cust/len(df_raw)*100:.1f}%)</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-accent {churn_accent}"></div>
        <div class="kpi-header">
            <span class="kpi-label">Tỷ lệ rời mạng (Churn)</span>
            <span class="kpi-icon">⚠️</span>
        </div>
        <div class="kpi-value" style="color: {churn_val_color};">{churn_rate:.1f}%</div>
        <div class="kpi-subtext">{churn_count:,} khách hủy{diff_churn_badge}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-accent accent-purple"></div>
        <div class="kpi-header">
            <span class="kpi-label">Cước TB / Tháng (ARPU)</span>
            <span class="kpi-icon">💵</span>
        </div>
        <div class="kpi-value">${avg_mrr:.2f}</div>
        <div class="kpi-subtext">Doanh thu định kỳ{diff_mrr_badge}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-accent accent-amber"></div>
        <div class="kpi-header">
            <span class="kpi-label">Doanh thu tích lũy (CLV)</span>
            <span class="kpi-icon">📈</span>
        </div>
        <div class="kpi-value">${total_revenue/1e6:.2f}M</div>
        <div class="kpi-subtext">Tổng giá trị thu được từ tệp</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-accent accent-green"></div>
        <div class="kpi-header">
            <span class="kpi-label">Điểm hài lòng TB</span>
            <span class="kpi-icon">⭐</span>
        </div>
        <div class="kpi-value">{avg_sat:.2f} <span style="font-size: 1rem; color: #94A3B8;">/ 5.0</span></div>
        <div class="kpi-subtext">Khảo sát trải nghiệm CSKH</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# HỆ THỐNG 6 TABS ĐIỀU HƯỚNG TƯƠNG TÁC
# ==============================================================================
tab_overview, tab_geo, tab_deepdive, tab_ml, tab_drilldown, tab_arch = st.tabs([
    "📊 1. Tổng Quan & Phân Phối",
    "🗺️ 2. Bản Đồ Địa Lý (50 Tiểu Bang)",
    "🔍 3. Dịch Vụ & Tương Quan",
    "🤖 4. Dự Báo AI & Simulator",
    "📋 5. Drill-down Hồ Sơ 360°",
    "🏗️ 6. Quy Trình Dữ Liệu & ETL"
])

# ------------------------------------------------------------------------------
# TAB 1: TỔNG QUAN & PHÂN PHỐI (Biểu đồ 1, 2, 3, 4)
# ------------------------------------------------------------------------------
with tab_overview:
    if total_cust == 0:
        st.warning("⚠️ Không có khách hàng nào thỏa mãn bộ lọc hiện tại. Vui lòng điều chỉnh lại bộ lọc ở Sidebar.")
    else:
        col1_1, col1_2 = st.columns(2)

        with col1_1:
            # Biểu đồ 1: Donut Chart - Tỷ lệ Churn
            churn_dist = filtered_df['Churn'].value_counts().reset_index()
            churn_dist.columns = ['Status', 'Count']
            churn_dist['Status_Label'] = churn_dist['Status'].map({
                'No': 'Ở lại (Retained)',
                'Yes': 'Rời mạng (Churned)'
            })

            fig_donut = px.pie(
                churn_dist, values='Count', names='Status_Label', hole=0.6,
                color='Status',
                color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'}
            )
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#0F172A', width=3))
            )
            apply_de_chart_theme(fig_donut, height=360, title="<b>Biểu đồ 1: Tỷ Lệ Churn Tổng Thể (Donut Chart)</b>")
            fig_donut.update_layout(showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col1_2:
            # Biểu đồ 2: Bar Chart - Tỷ lệ Churn theo loại Hợp đồng
            contract_summary = filtered_df.groupby('Contract', as_index=False).agg(
                Total=('customerID', 'count'),
                Churned=('ChurnNumeric', 'sum')
            )
            contract_summary['ChurnRate'] = (contract_summary['Churned'] / contract_summary['Total'] * 100).round(1)

            fig_contract = px.bar(
                contract_summary, x='Contract', y='ChurnRate', text='ChurnRate',
                color='Contract',
                color_discrete_sequence=['#EF4444', '#F59E0B', '#10B981'],
                labels={'Contract': 'Loại hợp đồng', 'ChurnRate': 'Tỷ lệ rời mạng (%)'}
            )
            fig_contract.update_traces(
                texttemplate='<b>%{text}%</b>',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            apply_de_chart_theme(fig_contract, height=360, title="<b>Biểu đồ 2: Tỷ Lệ Rời Mạng Theo Loại Hợp Đồng</b>")
            fig_contract.update_layout(showlegend=False, yaxis=dict(range=[0, max(75, contract_summary['ChurnRate'].max() + 15)]))
            st.plotly_chart(fig_contract, use_container_width=True)

        col2_1, col2_2 = st.columns(2)

        with col2_1:
            # Biểu đồ 3: Histogram / Density - Phân phối Tenure
            fig_hist = px.histogram(
                filtered_df, x="tenure", color="Churn", barmode="overlay",
                nbins=36,
                color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                labels={'tenure': 'Thâm niên sử dụng (Tháng)', 'Churn': 'Trạng thái Churn'}
            )
            apply_de_chart_theme(fig_hist, height=360, title="<b>Biểu đồ 3: Phân Phối Thâm Niên Khách Hàng (Histogram)</b>")
            st.plotly_chart(fig_hist, use_container_width=True)

        with col2_2:
            # Biểu đồ 4: Box Plot - Cước phí hàng tháng theo Churn & Outliers
            fig_box = px.box(
                filtered_df, x="Churn", y="MonthlyCharges", color="Churn",
                points="outliers",
                color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                labels={'MonthlyCharges': 'Cước phí tháng (USD)', 'Churn': 'Rời mạng?'}
            )
            apply_de_chart_theme(fig_box, height=360, title="<b>Biểu đồ 4: Phân Bố Cước Hàng Tháng & Điểm Ngoại Lai (Boxplot)</b>")
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: BẢN ĐỒ ĐỊA LÝ & VÙNG MIỀN (50 TIỂU BANG HOA KỲ ĐẦY ĐỦ TÊN)
# ------------------------------------------------------------------------------
with tab_geo:
    st.markdown("### 🗺️ Trực Quan Hóa Không Gian Địa Lý Khách Hàng (Toàn Bộ 50 Tiểu Bang Hoa Kỳ)")
    st.caption("Phân tích tỷ lệ rời mạng và phân bổ khách hàng trên toàn lãnh thổ Hoa Kỳ với định dạng Địa Cầu 3D và Bản Đồ Phẳng tương tác.")

    if total_cust == 0:
        st.warning("⚠️ Không có khách hàng nào thỏa mãn bộ lọc hiện tại.")
    else:
        # Tự bảo vệ: Đảm bảo các cột State, StateName, StateCode luôn tồn tại
        if 'StateCode' not in filtered_df.columns:
            filtered_df['StateCode'] = filtered_df['State'].str.extract(r'\(([A-Z]{2})\)')[0].fillna('CA')
        if 'StateName' not in filtered_df.columns:
            filtered_df['StateName'] = filtered_df['StateCode'].map(lambda c: US_50_STATES_INFO.get(c, {}).get('name', c))

        # Gom nhóm dữ liệu an toàn theo từng Bang
        group_cols = [c for c in ['State', 'StateName', 'StateCode'] if c in filtered_df.columns]
        state_agg = filtered_df.groupby(group_cols, as_index=False).agg(
            Total=('customerID', 'count'),
            Churned=('ChurnNumeric', 'sum'),
            AvgMonthly=('MonthlyCharges', 'mean'),
            TotalRevenue=('TotalCharges', 'sum')
        )
        state_agg['ChurnRate'] = (state_agg['Churned'] / state_agg['Total'] * 100).round(1)

        # ----------------------------------------------------------------------
        # HÀNG 1: THẺ CHỈ SỐ KPI TÓM TẮT ĐỊA LÝ (CHUẨN GIAO DIỆN EXECUTIVE)
        # ----------------------------------------------------------------------
        kpi_geo_c1, kpi_geo_c2, kpi_geo_c3 = st.columns(3)
        with kpi_geo_c1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px 18px;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">2024 / Hiện Tại • Chênh Lệch Tỷ Lệ Churn</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: {'#F87171' if churn_rate > baseline_churn else '#34D399'}; margin-top: 4px;">
                    {churn_rate:.1f}% <span style="font-size: 0.85rem; font-weight: 600;">({'▲ +' if diff_churn > 0 else '▼ '}{diff_churn:.1f}% vs chuẩn)</span>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Tỷ lệ rời mạng bình quân trên {len(state_agg)} tiểu bang</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi_geo_c2:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px 18px;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Tổng Doanh Thu Lũy Kế (CLV)</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">
                    ${total_revenue/1e6:.2f}M <span style="font-size: 0.85rem; font-weight: 600; color: #38BDF8;">USD</span>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Giá trị vòng đời thu được từ {total_cust:,} khách hàng</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi_geo_c3:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px 18px;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Cước Trung Bình / Khách (ARPU)</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">
                    ${avg_mrr:.2f} <span style="font-size: 0.85rem; font-weight: 600; color: #A78BFA;">/ tháng</span>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Doanh thu định kỳ bình quân mỗi thuê bao</div>
            </div>
            """, unsafe_allow_html=True)

        if len(state_agg) >= 2:
            highest_churn_state = state_agg.sort_values(by='ChurnRate', ascending=False).iloc[0]
            lowest_churn_state = state_agg.sort_values(by='ChurnRate', ascending=True).iloc[0]
            spread_val = abs(highest_churn_state['ChurnRate'] - lowest_churn_state['ChurnRate'])

            g_c1, g_c2, g_c3 = st.columns(3)
            with g_c1:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 10px; padding: 8px 14px; margin-top: 10px;">
                    <div style="font-size: 0.7rem; color: #FCA5A5; font-weight: 700;">🔴 TỶ LỆ RỜI MẠNG CAO NHẤT</div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #FFFFFF;">{highest_churn_state['State']} • <span style="color:#F87171;">{highest_churn_state['ChurnRate']}%</span></div>
                </div>
                """, unsafe_allow_html=True)
            with g_c2:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 8px 14px; margin-top: 10px;">
                    <div style="font-size: 0.7rem; color: #6EE7B7; font-weight: 700;">🟢 TỶ LỆ RỜI MẠNG THẤP NHẤT</div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #FFFFFF;">{lowest_churn_state['State']} • <span style="color:#34D399;">{lowest_churn_state['ChurnRate']}%</span></div>
                </div>
                """, unsafe_allow_html=True)
            with g_c3:
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 10px; padding: 8px 14px; margin-top: 10px;">
                    <div style="font-size: 0.7rem; color: #A5B4FC; font-weight: 700;">🗺️ ĐỘ LỆCH VÙNG MIỀN (SPREAD)</div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #FFFFFF;">Δ {spread_val:.1f}% <span style="font-size:0.75rem; color:#94A3B8; font-weight:400;">(Chênh lệch rủi ro)</span></div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # HÀNG 2: BỐ CỤC SPLIT-SCREEN CHÍNH (MAP BÊN TRÁI 58%, 2 BIỂU ĐỒ BÊN PHẢI 42%)
        # ----------------------------------------------------------------------
        col_main_map, col_side_charts = st.columns([1.35, 1])

        with col_main_map:
            # Bảng điều khiển góc nhìn Bản đồ: Địa cầu vs Bản đồ phẳng (Chuẩn style nút bấm)
            ctrl_col1, ctrl_col2 = st.columns([1.2, 1])
            with ctrl_col1:
                map_proj_mode = st.segmented_control(
                    "Chế độ hiển thị:",
                    options=["Địa cầu", "Bản đồ phẳng"],
                    default="Địa cầu",
                    label_visibility="collapsed"
                )
                if not map_proj_mode:
                    map_proj_mode = "Địa cầu"
            with ctrl_col2:
                metric_geo_choice = st.selectbox(
                    "Chỉ số thể hiện:",
                    ["Tỷ lệ Churn (%)", "Quy mô Khách hàng", "Cước phí TB ($)", "Tổng Doanh thu CLV ($)"],
                    index=0,
                    label_visibility="collapsed"
                )

            # Map settings mapping
            metric_configs = {
                "Tỷ lệ Churn (%)": {"col": "ChurnRate", "fmt": ":.1f%", "title": "Tỷ lệ Churn (%)", "scale": "Reds"},
                "Quy mô Khách hàng": {"col": "Total", "fmt": ":,", "title": "Khách hàng", "scale": "Blues"},
                "Cước phí TB ($)": {"col": "AvgMonthly", "fmt": ":.2f$", "title": "Cước TB ($)", "scale": "Purples"},
                "Tổng Doanh thu CLV ($)": {"col": "TotalRevenue", "fmt": ":.0f$", "title": "Doanh thu ($)", "scale": "YlOrRd"}
            }
            m_cfg = metric_configs[metric_geo_choice]

            if map_proj_mode == "Địa cầu":
                # Điều khiển xoay Quả Địa Cầu
                rot_c1, rot_c2 = st.columns([1.5, 1])
                with rot_c1:
                    globe_lon = st.slider(
                        "🔄 Xoay góc kinh độ (Kéo để xoay địa cầu):",
                        min_value=-180,
                        max_value=180,
                        value=-98,
                        step=5,
                        help="Kéo thanh trượt để xoay quả địa cầu 360° quanh trục Trái Đất (-98° là trung tâm Hoa Kỳ)."
                    )
                with rot_c2:
                    globe_preset = st.selectbox(
                        "🎯 Vùng góc nhìn nhanh:",
                        [
                            "Tùy chỉnh theo thanh trượt",
                            "🇺🇸 Toàn cảnh Hoa Kỳ (-98°)",
                            "🗽 Bờ Đông Hoa Kỳ (-75°)",
                            "🌉 Bờ Tây & TBD (-125°)",
                            "🇻🇳 Châu Á & Việt Nam (+105°)",
                            "🌍 Châu Âu (0°)"
                        ],
                        index=1,
                        help="Chọn nhanh góc nhìn về các khu vực trên thế giới."
                    )

                # Xác định góc kinh độ áp dụng
                current_lon = globe_lon
                current_lat = 38
                if globe_preset == "🇺🇸 Toàn cảnh Hoa Kỳ (-98°)":
                    current_lon = -98
                    current_lat = 38
                elif globe_preset == "🗽 Bờ Đông Hoa Kỳ (-75°)":
                    current_lon = -75
                    current_lat = 39
                elif globe_preset == "🌉 Bờ Tây & TBD (-125°)":
                    current_lon = -125
                    current_lat = 37
                elif globe_preset == "🇻🇳 Châu Á & Việt Nam (+105°)":
                    current_lon = 105
                    current_lat = 16
                elif globe_preset == "🌍 Châu Âu (0°)":
                    current_lon = 0
                    current_lat = 50

                # Render Quả địa cầu 3D (Orthographic Projection - Full Sphere Centered, No White Box)
                fig_map = go.Figure(
                    go.Choropleth(
                        locations=state_agg['StateCode'],
                        z=state_agg[m_cfg['col']],
                        locationmode='USA-states',
                        colorscale=m_cfg['scale'],
                        text=state_agg['StateName'],
                        marker_line_color='rgba(255, 255, 255, 0.45)',
                        marker_line_width=1,
                        colorbar=dict(
                            title=dict(text=m_cfg['title'], font=dict(color="#F8FAFC", size=11)),
                            orientation="h",
                            x=0.5,
                            xanchor="center",
                            y=-0.12,
                            len=0.75,
                            thickness=12,
                            tickfont=dict(color="#CBD5E1", size=10)
                        ),
                        hovertemplate="<b>🏛️ %{text} (%{location})</b><br>" +
                                      f"📊 {m_cfg['title']}: %{{z{m_cfg['fmt']}}}<br>" +
                                      "👥 Tổng khách: %{customdata[0]:,}<br>" +
                                      "⚠️ Khách Churn: %{customdata[1]:,}<br>" +
                                      "💵 Cước TB: $%{customdata[2]:.2f}<br>" +
                                      "💰 Doanh thu CLV: $%{customdata[3]:,.0f}<br>" +
                                      "<extra></extra>",
                        customdata=state_agg[['Total', 'Churned', 'AvgMonthly', 'TotalRevenue']].values
                    )
                )

                # Tạo các khung hình chuyển động xoay 360 độ liên tục (Animation Frames)
                rot_frames = [
                    go.Frame(
                        name=f"rot_{l}",
                        layout=dict(geo=dict(projection_rotation=dict(lon=l, lat=current_lat, roll=0)))
                    ) for l in range(-180, 181, 15)
                ]
                fig_map.frames = rot_frames

                fig_map.update_geos(
                    projection_type="orthographic",
                    projection_rotation=dict(lon=current_lon, lat=current_lat, roll=0),
                    bgcolor="rgba(0,0,0,0)",
                    showocean=True,
                    oceancolor="#0A192F",
                    showland=True,
                    landcolor="#172A45",
                    showcountries=True,
                    countrycolor="#475569",
                    showlakes=True,
                    lakecolor="#0A192F",
                    showsubunits=True,
                    subunitcolor="rgba(255, 255, 255, 0.3)"
                )
                fig_map.update_layout(
                    height=500,
                    margin=dict(l=10, r=10, t=10, b=50),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    updatemenus=[
                        dict(
                            type='buttons',
                            direction='left',
                            showactive=True,
                            x=0.01,
                            y=0.04,
                            xanchor='left',
                            yanchor='bottom',
                            bgcolor='rgba(15, 23, 42, 0.9)',
                            bordercolor='rgba(255, 255, 255, 0.25)',
                            borderwidth=1,
                            font=dict(color='#FFFFFF', size=11),
                            buttons=[
                                dict(
                                    label='▶ Tự Động Xoay 360°',
                                    method='animate',
                                    args=[
                                        None,
                                        dict(
                                            frame=dict(duration=130, redraw=True),
                                            fromcurrent=True,
                                            transition=dict(duration=0),
                                            mode='immediate',
                                            loop=True
                                        )
                                    ]
                                ),
                                dict(
                                    label='⏸ Dừng Lại',
                                    method='animate',
                                    args=[
                                        [None],
                                        dict(
                                            frame=dict(duration=0, redraw=False),
                                            mode='immediate'
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
                st.plotly_chart(fig_map, use_container_width=True)
                st.caption("💡 **Tương tác**: Bấm nút **▶ Tự Động Xoay 360°** để quả địa cầu quay tròn liên tục, hoặc kéo thanh trượt / chọn góc nhìn để xoay quả địa cầu theo ý muốn.")

            else:
                # Render Bản đồ phẳng 2D 50 tiểu bang Hoa Kỳ
                fig_map = px.choropleth(
                    state_agg,
                    locations='StateCode',
                    locationmode="USA-states",
                    scope="usa",
                    color=m_cfg['col'],
                    hover_name='State',
                    hover_data={
                        'StateCode': True,
                        'Total': ':,',
                        'Churned': ':,',
                        'ChurnRate': ':.1f%',
                        'AvgMonthly': ':.2f$',
                        'TotalRevenue': ':.0f$'
                    },
                    color_continuous_scale=m_cfg['scale'],
                    labels={m_cfg['col']: m_cfg['title'], 'Total': 'Khách hàng', 'AvgMonthly': 'Cước TB'}
                )
                fig_map.update_layout(
                    geo=dict(
                        bgcolor='rgba(0,0,0,0)',
                        lakecolor='rgba(15, 23, 42, 0.4)',
                        showlakes=True,
                        subunitcolor='rgba(255, 255, 255, 0.3)'
                    ),
                    height=480,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_map, use_container_width=True)


            # Thanh chú thích độ chênh lệch bên dưới bản đồ
            st.markdown("""
            <div class="geo-legend-bar">
                <span>🟢 Mức độ an toàn / thấp</span>
                <span>◀────── Thang đo Gradient nhiệt ──────▶</span>
                <span>🔴 Nguy cơ cao / cảnh báo</span>
            </div>
            """, unsafe_allow_html=True)

        with col_side_charts:
            # ------------------------------------------------------------------
            # BIỂU ĐỒ 1 BÊN PHẢI: XU HƯỚNG TỶ LỆ CHURN THEO THÂM NIÊN (ĐƯỜNG ĐỎ + MARKER)
            # ------------------------------------------------------------------
            tenure_trend = filtered_df.groupby('tenure', as_index=False).agg(
                Total=('customerID', 'count'),
                Churned=('ChurnNumeric', 'sum'),
                AvgMonthly=('MonthlyCharges', 'mean'),
                TotalRev=('TotalCharges', 'sum')
            )
            tenure_trend['ChurnRate'] = (tenure_trend['Churned'] / tenure_trend['Total'] * 100).round(1)

            fig_side_trend1 = go.Figure()
            fig_side_trend1.add_trace(go.Scatter(
                x=tenure_trend['tenure'],
                y=tenure_trend['ChurnRate'],
                mode='lines+markers',
                line=dict(color='#EF4444', width=2.2),
                marker=dict(size=4.5, color='#EF4444', symbol='circle'),
                hovertemplate="Thâm niên: <b>%{x}</b> tháng<br>Tỷ lệ Churn: <b>%{y:.1f}%</b><extra></extra>"
            ))
            fig_side_trend1.update_layout(
                title=dict(
                    text="<b>📈 Xu hướng Tỷ lệ Churn theo Thâm niên</b><br><span style='font-size:11px;color:#94A3B8;'>Toàn bộ khách hàng • 1 đến 72 tháng</span>",
                    font=dict(size=13, color='#F8FAFC', family="Plus Jakarta Sans")
                ),
                xaxis=dict(title=dict(text="Thâm niên (Tháng)", font=dict(size=11, color='#94A3B8')), gridcolor="rgba(255, 255, 255, 0.06)", tickfont=dict(color="#94A3B8")),
                yaxis=dict(title=dict(text="Tỷ lệ Churn (%)", font=dict(size=11, color='#94A3B8')), gridcolor="rgba(255, 255, 255, 0.06)", tickfont=dict(color="#94A3B8")),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=20, t=55, b=30),
                height=250
            )
            st.plotly_chart(fig_side_trend1, use_container_width=True)

            # ------------------------------------------------------------------
            # BIỂU ĐỒ 2 BÊN PHẢI: DOANH THU TÍCH LŨY THEO THỜI GIAN (ĐƯỜNG XANH + DIỆN TÍCH)
            # ------------------------------------------------------------------
            tenure_trend['CumRevenue'] = tenure_trend['TotalRev'].cumsum() / 1e6
            fig_side_trend2 = go.Figure()
            fig_side_trend2.add_trace(go.Scatter(
                x=tenure_trend['tenure'],
                y=tenure_trend['CumRevenue'],
                mode='lines',
                line=dict(color='#3B82F6', width=2.5),
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.16)',
                hovertemplate="Thâm niên: <b>%{x}</b> tháng<br>Doanh thu lũy kế: <b>$%{y:.2f}M</b><extra></extra>"
            ))
            fig_side_trend2.update_layout(
                title=dict(
                    text="<b>💧 Doanh thu Tích lũy theo Thời gian (CLV)</b><br><span style='font-size:11px;color:#94A3B8;'>Tích lũy CLV (Triệu USD) • 1 đến 72 tháng</span>",
                    font=dict(size=13, color='#F8FAFC', family="Plus Jakarta Sans")
                ),
                xaxis=dict(title=dict(text="Thâm niên (Tháng)", font=dict(size=11, color='#94A3B8')), gridcolor="rgba(255, 255, 255, 0.06)", tickfont=dict(color="#94A3B8")),
                yaxis=dict(title=dict(text="Doanh thu ($ Triệu)", font=dict(size=11, color='#94A3B8')), gridcolor="rgba(255, 255, 255, 0.06)", tickfont=dict(color="#94A3B8")),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=20, t=55, b=30),
                height=250
            )
            st.plotly_chart(fig_side_trend2, use_container_width=True)

        # ----------------------------------------------------------------------
        # HÀNG 3: CHI TIẾT XẾP HẠNG TOP BANG RỦI RO & BẢNG DỮ LIỆU TỔNG HỢP
        # ----------------------------------------------------------------------
        with st.expander("📊 Chi Tiết Xếp Hạng Top 10 Tiểu Bang Nguy Cơ Cao Nhất & An Toàn Nhất", expanded=True):
            top_risk_col, top_safe_col = st.columns(2)

            with top_risk_col:
                top_risk_states = state_agg.sort_values(by='ChurnRate', ascending=False).head(10)
                fig_risk = px.bar(
                    top_risk_states,
                    y='State', x='ChurnRate', orientation='h',
                    text='ChurnRate',
                    color='ChurnRate',
                    color_continuous_scale='Reds',
                    labels={'State': 'Tiểu bang', 'ChurnRate': 'Tỷ lệ rời mạng (%)'}
                )
                fig_risk.update_traces(texttemplate='<b>%{text}%</b>', textposition='outside')
                apply_de_chart_theme(fig_risk, height=360, title="<b>Biểu đồ 6a: Top 10 Tiểu Bang Nguy Cơ Churn Cao Nhất (Cần Can Thiệp)</b>")
                fig_risk.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_risk, use_container_width=True)

            with top_safe_col:
                top_safe_states = state_agg.sort_values(by='ChurnRate', ascending=True).head(10)
                fig_safe = px.bar(
                    top_safe_states,
                    y='State', x='ChurnRate', orientation='h',
                    text='ChurnRate',
                    color='ChurnRate',
                    color_continuous_scale='Greens_r',
                    labels={'State': 'Tiểu bang', 'ChurnRate': 'Tỷ lệ rời mạng (%)'}
                )
                fig_safe.update_traces(texttemplate='<b>%{text}%</b>', textposition='outside')
                apply_de_chart_theme(fig_safe, height=360, title="<b>Biểu đồ 6b: Top 10 Tiểu Bang Trung Thành Nhất (Tỷ Lệ Churn Thấp)</b>")
                fig_safe.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_safe, use_container_width=True)

        with st.expander("📑 Bảng Dữ Liệu Tổng Hợp 50 Tiểu Bang & Xuất Dữ Liệu", expanded=False):
            display_geo_table = state_agg[['StateCode', 'StateName', 'Total', 'Churned', 'ChurnRate', 'AvgMonthly', 'TotalRevenue']].copy()
            display_geo_table.columns = ['Mã Bang', 'Tên Bang', 'Tổng Khách Hàng', 'Khách Churn', 'Tỷ Lệ Churn (%)', 'Cước TB ($)', 'Doanh Thu ($)']
            display_geo_table['Tỷ Lệ Churn (%)'] = display_geo_table['Tỷ Lệ Churn (%)'].map(lambda x: f"{x:.1f}%")
            display_geo_table['Cước TB ($)'] = display_geo_table['Cước TB ($)'].map(lambda x: f"${x:.2f}")
            display_geo_table['Doanh Thu ($)'] = display_geo_table['Doanh Thu ($)'].map(lambda x: f"${x:,.0f}")
            
            st.dataframe(display_geo_table, use_container_width=True)
            csv_geo_data = state_agg.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Tải xuống dữ liệu địa lý 50 bang (.csv)",
                data=csv_geo_data,
                file_name="telco_geo_state_summary.csv",
                mime="text/csv"
            )

# ------------------------------------------------------------------------------
# TAB 3: DỊCH VỤ & TƯƠNG QUAN ĐA CHIỀU (Biểu đồ 7, 8, 9, 10)
# ------------------------------------------------------------------------------
with tab_deepdive:
    if total_cust == 0:
        st.warning("⚠️ Không có khách hàng nào thỏa mãn bộ lọc hiện tại.")
    else:
        deep_c1, deep_c2 = st.columns(2)

        with deep_c1:
            # Biểu đồ 7: Scatter Plot - Tenure vs TotalCharges
            sample_size = min(1500, len(filtered_df))
            sample_df = filtered_df.sample(sample_size, random_state=42) if len(filtered_df) > sample_size else filtered_df

            fig_scatter = px.scatter(
                sample_df,
                x="tenure", y="TotalCharges", color="Churn",
                size="MonthlyCharges",
                hover_data=["Contract", "InternetService", "PaymentMethod", "State"],
                color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                labels={'tenure': 'Thâm niên (Tháng)', 'TotalCharges': 'Tổng cước tích lũy (USD)'}
            )
            apply_de_chart_theme(fig_scatter, height=380, title="<b>Biểu đồ 7: Mối Quan Hệ Giữa Thâm Niên & Tổng Cước Phí (Scatter)</b>")
            st.plotly_chart(fig_scatter, use_container_width=True)

        with deep_c2:
            # Biểu đồ 8: Treemap - Cây phân cấp dịch vụ
            fig_treemap = px.treemap(
                filtered_df,
                path=['InternetService', 'Contract', 'Churn'],
                color='Churn',
                color_discrete_map={'No': '#10B981', 'Yes': '#EF4444', '(?)': '#64748B'},
                title="<b>Biểu đồ 8: Cấu Trúc Phân Cấp Gói Dịch Vụ & Trạng Thái Churn (Treemap)</b>"
            )
            apply_de_chart_theme(fig_treemap, height=380)
            st.plotly_chart(fig_treemap, use_container_width=True)

        deep_c3, deep_c4 = st.columns(2)

        with deep_c3:
            # Biểu đồ 9: Heatmap Ma trận tương quan Pearson
            num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'TotalServicesSubscribed', 'SatisfactionScore', 'ChurnNumeric']
            corr_matrix = filtered_df[num_cols].corr().round(2)

            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1
            )
            apply_de_chart_theme(fig_heatmap, height=380, title="<b>Biểu đồ 9: Ma Trận Hệ Số Tương Quan Pearson (Heatmap)</b>")
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with deep_c4:
            # Biểu đồ 10: Tỷ lệ Churn theo các gói Dịch vụ GTGT
            services = ['TechSupport', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'StreamingTV', 'StreamingMovies']
            svc_rows = []
            for s in services:
                churn_yes = filtered_df[filtered_df[s] == 'Yes']['ChurnNumeric'].mean() * 100 if len(filtered_df[filtered_df[s] == 'Yes']) > 0 else 0
                churn_no = filtered_df[filtered_df[s] == 'No']['ChurnNumeric'].mean() * 100 if len(filtered_df[filtered_df[s] == 'No']) > 0 else 0
                svc_rows.append({'Dịch vụ': s, 'Có đăng ký': round(churn_yes, 1), 'Không đăng ký': round(churn_no, 1)})
            df_svc = pd.DataFrame(svc_rows)

            fig_svc = px.bar(
                df_svc, x='Dịch vụ', y=['Có đăng ký', 'Không đăng ký'],
                barmode='group',
                color_discrete_sequence=['#10B981', '#EF4444'],
                labels={'value': 'Tỷ lệ rời mạng (%)', 'variable': 'Trạng thái'}
            )
            apply_de_chart_theme(fig_svc, height=380, title="<b>Biểu đồ 10: Tác Động Của Dịch Vụ GTGT Lên Tỷ Lệ Rời Mạng</b>")
            st.plotly_chart(fig_svc, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: DỰ BÁO AI & TRÌNH MÔ PHỎNG WHAT-IF
# ------------------------------------------------------------------------------
with tab_ml:
    st.markdown("### 🤖 Mô Hình Hồi Quy Logistic & Công Cụ Dự Báo Nguy Cơ Rời Mạng")
    st.markdown("Mô hình Scikit-Learn **Logistic Regression** đã được huấn luyện và tối ưu hàm mất mát Log-loss, cung cấp khả năng giải thích nhân tố (Feature Explainability) và dự báo trực tiếp.")

    ml_c1, ml_c2 = st.columns(2)

    with ml_c1:
        # Biểu đồ 11: Feature Importance & Odds Ratio
        if model_bundle is not None:
            df_coef = model_bundle['df_coef']
            top_features = pd.concat([df_coef.head(6), df_coef.tail(6)]).sort_values(by='Coefficient', ascending=True)
            top_features['Tác động'] = np.where(top_features['Coefficient'] > 0, 'Tăng nguy cơ Churn (+)', 'Giữ chân khách hàng (-)')

            fig_coef = px.bar(
                top_features, y='Feature', x='Coefficient',
                color='Tác động',
                color_discrete_map={'Tăng nguy cơ Churn (+)': '#EF4444', 'Giữ chân khách hàng (-)': '#10B981'},
                orientation='h',
                labels={'Coefficient': 'Hệ số hồi quy (Log-Odds)', 'Feature': 'Thuộc tính'}
            )
            apply_de_chart_theme(fig_coef, height=420, title="<b>Biểu đồ 11: Trọng Số Các Yếu Tố Quyết Định Churn (Logistic Coef)</b>")
            st.plotly_chart(fig_coef, use_container_width=True)
        else:
            st.warning("⚠️ Chưa tải được mô hình. Vui lòng kiểm tra file `models/telco_logistic_model.pkl`.")

    with ml_c2:
        if model_bundle is not None:
            metrics = model_bundle['metrics']
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                <h4 style="margin: 0 0 12px 0; color: #F8FAFC; font-size: 1.05rem;">🎯 Hiệu Năng Mô Hình Trên Tập Kiểm Định (Test Set):</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                    <div style="background: rgba(255,255,255,0.04); padding: 10px; border-radius: 8px;">
                        <div style="font-size: 0.72rem; color: #94A3B8;">ĐỘ CHÍNH XÁC (ACCURACY)</div>
                        <div style="font-size: 1.3rem; font-weight: 800; color: #F8FAFC;">{metrics['accuracy']*100:.2f}%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.04); padding: 10px; border-radius: 8px;">
                        <div style="font-size: 0.72rem; color: #94A3B8;">PHÂN LOẠI ROC-AUC</div>
                        <div style="font-size: 1.3rem; font-weight: 800; color: #60A5FA;">{metrics['roc_auc']:.4f}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.04); padding: 10px; border-radius: 8px;">
                        <div style="font-size: 0.72rem; color: #94A3B8;">F1-SCORE</div>
                        <div style="font-size: 1.3rem; font-weight: 800; color: #34D399;">{metrics['f1']*100:.2f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Biểu đồ 12: Xu hướng Churn theo vòng đời
            trend_df = filtered_df.groupby('TenureGroup', observed=True)['ChurnNumeric'].mean().reset_index()
            trend_df['ChurnPct'] = (trend_df['ChurnNumeric'] * 100).round(1)

            fig_trend = px.line(
                trend_df, x='TenureGroup', y='ChurnPct', markers=True,
                labels={'TenureGroup': 'Vòng đời thâm niên', 'ChurnPct': 'Tỷ lệ rời mạng (%)'}
            )
            fig_trend.update_traces(line=dict(color='#EF4444', width=3), marker=dict(size=9, color='#DC2626'))
            apply_de_chart_theme(fig_trend, height=270, title="<b>Biểu đồ 12: Xu Hướng Churn Theo Vòng Đời Thâm Niên</b>")
            st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚡ Trình Mô Phỏng Nguy Cơ Rời Mạng (What-If Real-Time Simulator)")
    st.markdown("Nhập hồ sơ hợp đồng của một khách hàng cụ thể để hệ thống AI tính toán xác suất rời bỏ và đưa ra khuyến nghị giữ chân thời gian thực:")

    # Khởi tạo session state cho simulator nếu chưa có
    if 'sim_tenure' not in st.session_state:
        st.session_state['sim_tenure'] = 4
        st.session_state['sim_monthly'] = 89.5
        st.session_state['sim_contract'] = "Month-to-month"
        st.session_state['sim_internet'] = "Fiber optic"
        st.session_state['sim_payment'] = "Electronic check"
        st.session_state['sim_paperless'] = "Yes"
        st.session_state['sim_tech'] = "No"
        st.session_state['sim_sec'] = "No"
        st.session_state['sim_backup'] = "No"
        st.session_state['sim_device'] = "No"
        st.session_state['sim_stream'] = "Yes"
        st.session_state['sim_senior'] = 1

    st.markdown("#### 🎯 Chọn Nhanh Kịch Bản Khách Hàng Mẫu:")
    st.caption("Nhấp vào 1 trong 3 kịch bản dưới đây để tự động điền nhanh các thông số mẫu:")

    ps_col1, ps_col2, ps_col3 = st.columns(3)
    with ps_col1:
        if st.button("🚨 Kịch Bản 1: Nguy Cơ Rời Mạng Cao", use_container_width=True):
            st.session_state['sim_tenure'] = 2
            st.session_state['sim_monthly'] = 98.0
            st.session_state['sim_contract'] = "Month-to-month"
            st.session_state['sim_internet'] = "Fiber optic"
            st.session_state['sim_payment'] = "Electronic check"
            st.session_state['sim_paperless'] = "Yes"
            st.session_state['sim_tech'] = "No"
            st.session_state['sim_sec'] = "No"
            st.session_state['sim_backup'] = "No"
            st.session_state['sim_device'] = "No"
            st.session_state['sim_stream'] = "Yes"
            st.session_state['sim_senior'] = 1
            st.rerun()

    with ps_col2:
        if st.button("🛡️ Kịch Bản 2: Khách Gắn Bó Lâu Năm", use_container_width=True):
            st.session_state['sim_tenure'] = 62
            st.session_state['sim_monthly'] = 64.0
            st.session_state['sim_contract'] = "Two year"
            st.session_state['sim_internet'] = "DSL"
            st.session_state['sim_payment'] = "Bank transfer (automatic)"
            st.session_state['sim_paperless'] = "No"
            st.session_state['sim_tech'] = "Yes"
            st.session_state['sim_sec'] = "Yes"
            st.session_state['sim_backup'] = "Yes"
            st.session_state['sim_device'] = "Yes"
            st.session_state['sim_stream'] = "No"
            st.session_state['sim_senior'] = 0
            st.rerun()

    with ps_col3:
        if st.button("⚖️ Kịch Bản 3: Khách Hàng Cần Chăm Sóc", use_container_width=True):
            st.session_state['sim_tenure'] = 16
            st.session_state['sim_monthly'] = 74.5
            st.session_state['sim_contract'] = "Month-to-month"
            st.session_state['sim_internet'] = "Fiber optic"
            st.session_state['sim_payment'] = "Credit card (automatic)"
            st.session_state['sim_paperless'] = "Yes"
            st.session_state['sim_tech'] = "No"
            st.session_state['sim_sec'] = "Yes"
            st.session_state['sim_backup'] = "Yes"
            st.session_state['sim_device'] = "No"
            st.session_state['sim_stream'] = "Yes"
            st.session_state['sim_senior'] = 0
            st.rerun()

    contract_opts = ["Month-to-month", "One year", "Two year"]
    internet_opts = ["Fiber optic", "DSL", "No"]
    payment_opts = ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    yn_opts = ["No", "Yes"]
    svc_opts = ["No", "Yes", "No internet service"]

    with st.form("what_if_simulator_form"):
        sim_c1, sim_c2, sim_c3, sim_c4 = st.columns(4)

        with sim_c1:
            inp_tenure = st.slider("Thâm niên (Tháng):", 1, 72, value=int(st.session_state['sim_tenure']))
            inp_monthly = st.slider("Cước phí tháng (USD):", 18.0, 120.0, value=float(st.session_state['sim_monthly']))
            c_idx = contract_opts.index(st.session_state['sim_contract']) if st.session_state['sim_contract'] in contract_opts else 0
            inp_contract = st.selectbox("Loại hợp đồng:", contract_opts, index=c_idx)

        with sim_c2:
            i_idx = internet_opts.index(st.session_state['sim_internet']) if st.session_state['sim_internet'] in internet_opts else 0
            inp_internet = st.selectbox("Dịch vụ Internet:", internet_opts, index=i_idx)
            p_idx = payment_opts.index(st.session_state['sim_payment']) if st.session_state['sim_payment'] in payment_opts else 0
            inp_payment = st.selectbox("Hình thức thanh toán:", payment_opts, index=p_idx)
            pl_idx = yn_opts.index(st.session_state['sim_paperless']) if st.session_state['sim_paperless'] in yn_opts else 1
            inp_paperless = st.selectbox("Hóa đơn điện tử:", yn_opts, index=pl_idx)

        with sim_c3:
            t_idx = svc_opts.index(st.session_state['sim_tech']) if st.session_state['sim_tech'] in svc_opts else 0
            inp_tech = st.selectbox("Hỗ trợ kỹ thuật (TechSupport):", svc_opts, index=t_idx)
            s_idx = svc_opts.index(st.session_state['sim_sec']) if st.session_state['sim_sec'] in svc_opts else 0
            inp_sec = st.selectbox("Bảo mật mạng (OnlineSecurity):", svc_opts, index=s_idx)
            b_idx = svc_opts.index(st.session_state['sim_backup']) if st.session_state['sim_backup'] in svc_opts else 0
            inp_backup = st.selectbox("Sao lưu đám mây (OnlineBackup):", svc_opts, index=b_idx)

        with sim_c4:
            d_idx = svc_opts.index(st.session_state['sim_device']) if st.session_state['sim_device'] in svc_opts else 0
            inp_device = st.selectbox("Bảo vệ thiết bị (DeviceProtection):", svc_opts, index=d_idx)
            st_idx = svc_opts.index(st.session_state['sim_stream']) if st.session_state['sim_stream'] in svc_opts else 0
            inp_stream = st.selectbox("Truyền hình số (StreamingTV):", svc_opts, index=st_idx)
            inp_senior = st.selectbox("Người cao tuổi (SeniorCitizen):", [0, 1], index=int(st.session_state['sim_senior']), format_func=lambda x: "Có" if x==1 else "Không")

        submit_btn = st.form_submit_button("🚀 Dự Đoán Nguy Cơ Rời Mạng Ngay", use_container_width=True)

    if submit_btn and model_bundle is not None:
        inp_total = inp_monthly * inp_tenure
        svc_count = (1 if inp_tech == 'Yes' else 0) + (1 if inp_sec == 'Yes' else 0) + (1 if inp_backup == 'Yes' else 0) + (1 if inp_device == 'Yes' else 0) + (1 if inp_stream == 'Yes' else 0)

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
            'StreamingTV': inp_stream,
            'StreamingMovies': 'No',
            'Contract': inp_contract,
            'PaperlessBilling': inp_paperless,
            'PaymentMethod': inp_payment
        }])

        pipeline = model_bundle['pipeline']
        pred_prob = pipeline.predict_proba(input_data)[0, 1]

        prob_pct = round(pred_prob * 100, 1)
        bar_color = "#EF4444" if pred_prob >= 0.60 else ("#F59E0B" if pred_prob >= 0.35 else "#10B981")
        risk_lvl = "RẤT CAO" if pred_prob >= 0.60 else ("TRUNG BÌNH" if pred_prob >= 0.35 else "THẤP")
        at_risk_annual = inp_monthly * 12

        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([1, 1.3])

        with res_col1:
            # Đồng hồ đo Speedometer Gauge Chart chuẩn BI Executive
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_pct,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"<b>NGUY CƠ RỜI MẠNG: {risk_lvl}</b>", 'font': {'size': 14, 'color': bar_color}},
                number={'suffix': "%", 'font': {'size': 36, 'color': '#FFFFFF'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                    'bar': {'color': bar_color, 'thickness': 0.32},
                    'bgcolor': "rgba(15, 23, 42, 0.6)",
                    'borderwidth': 1,
                    'bordercolor': "rgba(255, 255, 255, 0.12)",
                    'steps': [
                        {'range': [0, 35], 'color': 'rgba(16, 185, 129, 0.2)'},
                        {'range': [35, 60], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [60, 100], 'color': 'rgba(239, 68, 68, 0.25)'}
                    ],
                    'threshold': {
                        'line': {'color': "#EF4444", 'width': 3},
                        'thickness': 0.8,
                        'value': 60
                    }
                }
            ))
            fig_gauge.update_layout(
                height=260,
                margin=dict(t=45, b=10, l=25, r=25),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Plus Jakarta Sans", color="#F8FAFC")
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Khối tài chính rủi ro
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 14px; text-align: center;">
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Ước Tính Cước Năm Bị Ảnh Hưởng</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: {'#F87171' if pred_prob >= 0.35 else '#34D399'}; margin-top: 2px;">${at_risk_annual:,.2f} <span style="font-size: 0.8rem; font-weight: 500; color: #94A3B8;">USD/năm</span></div>
            </div>
            """, unsafe_allow_html=True)

        with res_col2:
            st.markdown(f"#### 💡 Đề Xuất Giải Pháp Giữ Chân Khách Hàng:")
            recs = []
            if inp_contract == "Month-to-month":
                recs.append("📌 **Khuyến mãi chuyển đổi hợp đồng:** Khách đang dùng gói theo tháng $\\rightarrow$ Đề xuất tặng voucher giảm **15% cước trong 3 tháng đầu** khi cam kết ký hợp đồng 1 hoặc 2 năm. *(Hiệu quả: Giảm ~50% nguy cơ rời bỏ)*.")
            if inp_internet == "Fiber optic" and inp_tech != "Yes":
                recs.append("📌 **Tặng kèm TechSupport 24/7:** Khách dùng cáp quang cước cao nhưng chưa có TechSupport $\\rightarrow$ Tặng miễn phí **6 tháng dịch vụ Hỗ trợ kỹ thuật** nhằm nâng cao trải nghiệm mạng.")
            if inp_payment == "Electronic check":
                recs.append("📌 **Tối ưu phương thức thanh toán:** Chuyển đổi sang thanh toán tự động qua thẻ ngân hàng/tín dụng để nhận mã hoàn tiền **$5/tháng**.")
            if inp_tenure <= 12:
                recs.append("📌 **Chăm sóc nhóm khách hàng mới:** Thuộc nhóm thâm niên nhạy cảm nhất ($< 1$ năm) $\\rightarrow$ Phân bổ nhân viên CSKH chủ động gọi thăm hỏi định kỳ trong 30 ngày tới.")
            if not recs:
                recs.append(" Khách hàng hiện tại rất hài lòng và có độ gắn kết cao. Duy trì chất lượng dịch vụ và gửi quà tặng tri ân thường niên.")

            for r in recs:
                st.markdown(r)

        # MÔ PHỎNG TÁC ĐỘNG KHI DOANH NGHIỆP CAN THIỆP (TRƯỚC & SAU)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Dự Đoán Tác Động Sau Khi Can Thiệp (Trước & Sau Giữ Chân):")
        st.caption("Mô hình AI tự động tính lại xác suất rời mạng nếu áp dụng các giải pháp chăm sóc khách hàng:")

        # Phương án 1: Đổi sang Hợp đồng 1 năm
        cf1_data = input_data.copy()
        cf1_data['Contract'] = 'One year'
        p1 = pipeline.predict_proba(cf1_data)[0, 1] * 100
        diff1 = prob_pct - p1

        # Phương án 2: Tặng kèm TechSupport
        cf2_data = input_data.copy()
        cf2_data['TechSupport'] = 'Yes'
        cf2_data['TotalServicesSubscribed'] = int(cf2_data['TotalServicesSubscribed'].iloc[0]) + (1 if inp_tech != 'Yes' else 0)
        p2 = pipeline.predict_proba(cf2_data)[0, 1] * 100
        diff2 = prob_pct - p2

        # Phương án 3: Gói giải pháp toàn diện (2 năm + TechSupport + Auto-Pay)
        cf3_data = input_data.copy()
        cf3_data['Contract'] = 'Two year'
        cf3_data['PaymentMethod'] = 'Bank transfer (automatic)'
        cf3_data['TechSupport'] = 'Yes'
        cf3_data['TotalServicesSubscribed'] = int(cf3_data['TotalServicesSubscribed'].iloc[0]) + (1 if inp_tech != 'Yes' else 0)
        p3 = pipeline.predict_proba(cf3_data)[0, 1] * 100
        diff3 = prob_pct - p3

        cf_col1, cf_col2, cf_col3 = st.columns(3)
        with cf_col1:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px;">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700;">PHƯƠNG ÁN 1: ĐỔI HỢP ĐỒNG 1 NĂM</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #34D399; margin-top: 4px;">{p1:.1f}% Churn</div>
                <div style="font-size: 0.8rem; color: #10B981; font-weight: 700;">{'▼ Giảm ' + f'{diff1:.1f}% nguy cơ' if diff1 > 0 else 'Không đổi'}</div>
            </div>
            """, unsafe_allow_html=True)

        with cf_col2:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px;">
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700;">PHƯƠNG ÁN 2: TẶNG TECHSUPPORT 24/7</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #34D399; margin-top: 4px;">{p2:.1f}% Churn</div>
                <div style="font-size: 0.8rem; color: #10B981; font-weight: 700;">{'▼ Giảm ' + f'{diff2:.1f}% nguy cơ' if diff2 > 0 else 'Không đổi'}</div>
            </div>
            """, unsafe_allow_html=True)

        with cf_col3:
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 10px; padding: 14px;">
                <div style="font-size: 0.72rem; color: #A5B4FC; font-weight: 700;">PHƯƠNG ÁN 3: COMBO (2 NĂM + CSKH + AUTOPAY)</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #60A5FA; margin-top: 4px;">{p3:.1f}% Churn</div>
                <div style="font-size: 0.8rem; color: #60A5FA; font-weight: 700;">{'▼ Giảm ' + f'{diff3:.1f}% nguy cơ' if diff3 > 0 else 'Không đổi'}</div>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 5: DRILL-DOWN HỒ SƠ 360° CHI TIẾT
# ------------------------------------------------------------------------------
with tab_drilldown:
    st.markdown("### 📋 Bảng Dữ Liệu Tương Tác & Tính Năng Drill-Down Hồ Sơ 360°")
    st.markdown("Khám phá từng khách hàng cụ thể hoặc trích xuất dữ liệu phục vụ nghiên cứu & báo cáo chuyên sâu.")

    table_cols = ['customerID', 'gender', 'SeniorCitizen', 'State', 'City', 'tenure', 'Contract', 'InternetService', 'MonthlyCharges', 'TotalCharges', 'SatisfactionScore', 'Churn']
    display_df = filtered_df[table_cols]

    # Drill-down: Chọn mã khách hàng
    sample_ids = display_df['customerID'].head(100).tolist()
    selected_customer = st.selectbox(
        "🔍 Chọn hoặc Nhập Mã Khách Hàng (customerID) để Drill-Down xem chi tiết 360 độ:",
        sample_ids
    )

    if selected_customer:
        c_row = filtered_df[filtered_df['customerID'] == selected_customer].iloc[0]
        is_churn = (c_row['Churn'] == 'Yes')

        badge_html = f'<span class="profile-badge-churn">🚨 ĐÃ RỜI MẠNG (CHURNED)</span>' if is_churn else f'<span class="profile-badge-retained">🛡️ ĐANG Ở LẠI (ACTIVE)</span>'

        st.markdown(f"""
        <div class="profile-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <div>
                    <span style="font-size: 1.3rem; font-weight: 800; color: #FFFFFF;">Khách Hàng: <code>{selected_customer}</code></span>
                    <span style="margin-left: 12px;">{badge_html}</span>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    📍 Vị trí: <b>{c_row['City']}, {c_row['State']}</b>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
                <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 0.72rem; color: #94A3B8;">NHÂN KHẨU HỌC</div>
                    <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC; margin-top: 4px;">Giới tính: {c_row['gender']}</div>
                    <div style="font-size: 0.85rem; color: #94A3B8;">Đối tượng: {'Người cao tuổi' if c_row['SeniorCitizen']==1 else 'Trẻ / Trung niên'}</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 0.72rem; color: #94A3B8;">HỢP ĐỒNG & THANH TOÁN</div>
                    <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC; margin-top: 4px;">Hợp đồng: {c_row['Contract']}</div>
                    <div style="font-size: 0.85rem; color: #94A3B8;">Phương thức: {c_row['PaymentMethod']}</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 0.72rem; color: #94A3B8;">TÀI CHÍNH & DỊCH VỤ</div>
                    <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC; margin-top: 4px;">Cước tháng: ${c_row['MonthlyCharges']:.2f}</div>
                    <div style="font-size: 0.85rem; color: #94A3B8;">Tổng tích lũy: ${c_row['TotalCharges']:.2f}</div>
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 0.72rem; color: #94A3B8;">TRẢI NGHIỆM & PHẢN HỒI</div>
                    <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC; margin-top: 4px;">Điểm CSAT: {c_row['SatisfactionScore']} / 5 ⭐</div>
                    <div style="font-size: 0.85rem; color: #F87171;">Lý do: {c_row.get('ChurnReason', 'N/A')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Hiển thị bảng dữ liệu tương tác với cấu hình cột chuyên nghiệp
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        column_config={
            "customerID": st.column_config.TextColumn("Mã KH", help="Mã định danh duy nhất"),
            "gender": st.column_config.TextColumn("Giới tính"),
            "State": st.column_config.TextColumn("Địa bàn tiểu bang"),
            "tenure": st.column_config.ProgressColumn(
                "Thâm niên (Tháng)",
                help="Số tháng sử dụng dịch vụ",
                format="%d tháng",
                min_value=0,
                max_value=72,
            ),
            "MonthlyCharges": st.column_config.NumberColumn(
                "Cước tháng",
                format="$%.2f",
                help="Cước phí phát sinh hàng tháng"
            ),
            "TotalCharges": st.column_config.NumberColumn(
                "Tổng tích lũy",
                format="$%.2f",
                help="Toàn bộ doanh thu vòng đời"
            ),
            "SatisfactionScore": st.column_config.NumberColumn(
                "Điểm CSAT",
                format="%d ⭐",
                help="Điểm đánh giá trải nghiệm dịch vụ (1 - 5)"
            ),
            "Churn": st.column_config.TextColumn("Rời mạng?"),
        }
    )

    # Nút xuất file CSV
    csv_bytes = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Xuất dữ liệu đã lọc sang file CSV",
        data=csv_bytes,
        file_name="telco_churn_filtered_export.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------------------------
# TAB 6: QUY TRÌNH DỮ LIỆU & TIỀN XỬ LÝ (DATA PIPELINE)
# ------------------------------------------------------------------------------
with tab_arch:
    st.markdown("### 🏗️ Quy Trình Thu Thập, Tiền Xử Lý & Chuẩn Hóa Dữ Liệu")
    st.markdown("Mô tả quy trình xử lý dữ liệu viễn thông từ 4 bảng gốc, các bước làm sạch, ghép nối bảng và chuẩn bị cho mô hình hóa.")

    st.markdown("""
    <div class="arch-box">
    <b>[LUỒNG XỬ LÝ DỮ LIỆU - DATA PIPELINE]:</b><br>
    [1. Nguồn dữ liệu thô (Kaggle/IBM)] ──► [2. 4 Bảng quan hệ RDBMS] ──► [3. Tiền xử lý & Làm sạch (Join & Impute)] ──► [4. Tập dữ liệu hoàn chỉnh (39 cột)] ──► [5. Trực quan hóa & AI]
    </div>
    """, unsafe_allow_html=True)

    arch_c1, arch_c2 = st.columns(2)

    with arch_c1:
        st.markdown("#### 1. Cấu Trúc 4 Bảng Dữ Liệu Quan Hệ Gốc:")
        st.markdown("""
        - 📄 **`telco_demographics.csv`** (7,043 dòng):<br>
          `customerID (PK)`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `State`, `StateName`, `StateCode`, `City`, `Latitude`, `Longitude`
        - 📄 **`telco_services.csv`** (7,043 dòng):<br>
          `customerID (FK)`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
        - 📄 **`telco_contracts.csv`** (7,043 dòng):<br>
          `customerID (FK)`, `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`
        - 📄 **`telco_churn_status.csv`** (7,043 dòng):<br>
          `customerID (FK)`, `Churn`, `ChurnReason`, `SatisfactionScore`
        """, unsafe_allow_html=True)

    with arch_c2:
        st.markdown("#### 2. Các Bước Tiền Xử Lý Đã Thực Hiện:")
        st.markdown("""
        - 🔗 **Ghép nối bảng (Inner Join):** Sử dụng khóa chính `customerID` để hợp nhất 4 bảng dữ liệu, tỷ lệ khớp đạt 100% (7,043 bản ghi).
        - 🧹 **Xử lý giá trị trống (Missing Values):** Phát hiện 11 dòng có `TotalCharges` rỗng do khách hàng mới ký hợp đồng (`tenure = 0`), tiến hành điền giá trị 0.
        - 🏷️ **Tạo đặc trưng mới (Feature Engineering):** Bổ sung nhóm thâm niên `TenureGroup`, tổng số dịch vụ `TotalServicesSubscribed`, biến cờ gói bảo mật `HasProtectionPackage`, cước tính toán `CalculatedAvgMonthly` và biến nhị phân `ChurnNumeric`.
        - 🗺️ **Chuẩn hóa địa lý 50 tiểu bang:** Bổ sung thông tin vĩ độ/kinh độ và mã tiểu bang Hoa Kỳ phục vụ vẽ bản đồ trực quan.
        """)

st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
st.caption("© 2026 Đồ Án Tương Tác Dữ Liệu Trực Quan | Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE) | Nhóm 22: Đỗ Trọng Khôi - Bùi Đức Huy - Trương Quốc Duy")

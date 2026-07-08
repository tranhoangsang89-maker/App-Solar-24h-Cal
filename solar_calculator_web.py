import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page config
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tư Vấn Điện Mặt Trời Thông Minh",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to match Solar 24h Identity (Navy and Gold)
st.markdown("""
<style>
    :root {
        --primary-color: #003366;
        --secondary-color: #FFD700;
        --background-color: #F4F6F9;
    }
    .main-title {
        color: #003366;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #555;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        text-align: center;
        margin-bottom: 25px;
        font-size: 1.1rem;
    }
    .greeting-box {
        background-color: #E6F0FA;
        border-left: 5px solid #003366;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
        font-size: 1.05rem;
        color: #333;
    }
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-top: 4px solid #003366;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        font-weight: bold;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #003366;
        font-weight: bold;
    }
    .metric-desc {
        font-size: 0.85rem;
        color: #888;
    }
    .highlight-gold {
        color: #D4AF37;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F0F2F6;
        border-radius: 5px 5px 0px 0px;
        color: #003366;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Define packages and specifications
packages = {
    "SOLAR F1": {
        "power": 2.32, "storage": "2.5 kWh", "price": 47800000, 
        "inverter": "LUXPOWER SNA 5kW", "battery": "BSB Lithium 2.5 kWh", "panels": 4, 
        "desc": "Hóa đơn dưới 500k/tháng", "min_bill": 0, "max_bill": 500000
    },
    "SOLAR F2": {
        "power": 4.64, "storage": "5 kWh", "price": 68500000, 
        "inverter": "LUXPOWER SNA 5kW", "battery": "BSB Lithium 5 kWh", "panels": 8, 
        "desc": "Hóa đơn dưới 1.0 triệu/tháng", "min_bill": 500000, "max_bill": 1000000
    },
    "SOLAR F3": {
        "power": 5.80, "storage": "10 kWh", "price": 88000000, 
        "inverter": "SVE 6kW", "battery": "LS BATTERY 10 kWh", "panels": 10, 
        "desc": "Hóa đơn từ 1.0 đến 1.5 triệu/tháng", "min_bill": 1000000, "max_bill": 1500000
    },
    "SOLAR F4": {
        "power": 6.96, "storage": "16 kWh", "price": 104700000, 
        "inverter": "SVE 6kW", "battery": "EJOR Lithium 16 kWh", "panels": 12, 
        "desc": "Hóa đơn từ 1.5 đến 2.0 triệu/tháng", "min_bill": 1500000, "max_bill": 2000000
    },
    "SOLAR F5": {
        "power": 8.12, "storage": "16 kWh", "price": 114900000, 
        "inverter": "LUXPOWER PRO 6.5kW", "battery": "EJOR/LS Lithium 16 kWh", "panels": 14, 
        "desc": "Hóa đơn từ 2.0 đến 2.5 triệu/tháng", "min_bill": 2000000, "max_bill": 2500000
    },
    "SOLAR F6": {
        "power": 9.28, "storage": "16 kWh", "price": 123600000, 
        "inverter": "LUXPOWER 6.5 PRO", "battery": "EJOR/LS Lithium 16 kWh", "panels": 16, 
        "desc": "Hóa đơn từ 2.5 đến 3.0 triệu/tháng", "min_bill": 2500000, "max_bill": 3000000
    },
    "SOLAR F7": {
        "power": 11.60, "storage": "32 kWh", "price": 203000000, 
        "inverter": "LUXPOWER 6.5 PRO (x2)", "battery": "EJOR/LS Lithium 32 kWh", "panels": 20, 
        "desc": "Hóa đơn từ 3.0 đến 4.0 triệu/tháng", "min_bill": 3000000, "max_bill": 4000000
    },
    "SOLAR F8": {
        "power": 13.92, "storage": "32 kWh", "price": 217900000, 
        "inverter": "LUXPOWER 6.5 PRO (x2)", "battery": "EJOR/LS Lithium 32 kWh", "panels": 24, 
        "desc": "Hóa đơn từ 4.0 đến 5.0 triệu/tháng", "min_bill": 4000000, "max_bill": 5000000
    },
    "SOLAR F9": {
        "power": 17.40, "storage": "32 kWh", "price": 239000000, 
        "inverter": "LUXPOWER 6.5 PRO (x2)", "battery": "EJOR/LS Lithium 32 kWh", "panels": 30, 
        "desc": "Hóa đơn từ 5.0 đến 7.0 triệu/tháng", "min_bill": 5000000, "max_bill": 7000000
    },
    "SOLAR F10": {
        "power": 22.04, "storage": "48 kWh", "price": 329300000, 
        "inverter": "LUXPOWER 6.5 PRO (x3)", "battery": "EJOR/LS Lithium 48 kWh", "panels": 38, 
        "desc": "Hóa đơn từ 7.0 đến 10.0 triệu/tháng", "min_bill": 7000000, "max_bill": 10000000
    }
}

# 2026 Electricity Tariff 6-brackets calculation (excl. VAT)
# Bậc 1 (0-50 kWh): 1.984 | Bậc 2 (51-100 kWh): 2.050 | Bậc 3 (101-200 kWh): 2.380
# Bậc 4 (201-300): 2.998 | Bậc 5 (301-400): 3.350 | Bậc 6 (from 401): 3.460
tariff_prices = [1984, 2050, 2380, 2998, 3350, 3460]
tariff_steps = [50, 50, 100, 100, 100]

def calculate_kwh_from_bill(bill_amount, vat_rate):
    """Calculates kWh from bill amount based on 2026 tariff."""
    pre_vat = bill_amount / (1 + vat_rate / 100)
    remaining_money = pre_vat
    kwh = 0
    for i, step in enumerate(tariff_steps):
        cost = step * tariff_prices[i]
        if remaining_money > cost:
            remaining_money -= cost
            kwh += step
        else:
            kwh += remaining_money / tariff_prices[i]
            remaining_money = 0
            break
    if remaining_money > 0:
        kwh += remaining_money / tariff_prices[-1]
    return kwh

def calculate_bill_from_kwh(kwh, vat_rate):
    """Calculates bill amount from kWh based on 2026 tariff."""
    remaining = kwh
    cost = 0
    for i, step in enumerate(tariff_steps):
        if remaining > step:
            cost += step * tariff_prices[i]
            remaining -= step
        else:
            cost += remaining * tariff_prices[i]
            remaining = 0
            break
    if remaining > 0:
        cost += remaining * tariff_prices[-1]
    return cost * (1 + vat_rate / 100)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #003366;'>SOLAR 24H</h2>", unsafe_allow_html=True)
    
    # Image 1: Solar Girl Mascot in Sidebar (safe fallback)
    solar_girl_img_path = "images/solar_girl.jpg"
    if os.path.exists(solar_girl_img_path):
        st.image(solar_girl_img_path, use_column_width=True)
    else:
        st.info("💡 Solar Girl Mascot (images/solar_girl.jpg) chưa được tải lên GitHub. Sử dụng hình minh họa mặc định.")
        
    st.markdown("---")
    st.markdown("### 🏢 Liên hệ tư vấn:")
    st.markdown("**CÔNG TY TNHH TMDV SOLAR 24H**")
    st.markdown("📍 *Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh*")
    st.markdown("☎️ *Hotline:* **0909.363.579 - 0896.488.299**")
    st.markdown("📧 *Email:* Solar24h.tmdv@gmail.com")

# Header section
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.markdown("<h1 class='main-title'>SOLAR 24H - TƯ VẤN ĐIỆN MẶT TRỜI HYBRID</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Công cụ tính toán tự động dòng tiền và kế hoạch trả góp tối ưu</p>", unsafe_allow_html=True)

# Unified Welcome Message (Sách đào tạo / Master Approved)
st.markdown("""
<div class='greeting-box'>
    <strong>Solar Girl chào cả nhà! 👩‍💼</strong> Mọi người chỉ cần nhập hóa đơn và tùy chỉnh mức trả trước theo mong muốn. Hệ thống sẽ tự động tư vấn ạ!
</div>
""", unsafe_allow_html=True)

# Tabs definitions
tab_consult, tab_details, tab_shinhan = st.tabs([
    "📋 TƯ VẤN KHÁCH HÀNG", 
    "📦 CHI TIẾT GÓI LẮP ĐẶT", 
    "🏦 GÓI VAY SHINHAN BANK"
])

# Tab 1: Customer Consultation
with tab_consult:
    st.markdown("### 🔍 Nhập thông tin tiêu thụ điện của khách hàng")
    col1, col2 = st.columns(2)
    
    with col1:
        bill_input = st.number_input(
            "Nhập số tiền điện hàng tháng của khách (VNĐ):", 
            min_value=10000, max_value=50000000, value=2700000, step=50000
        )
    with col2:
        vat_rate = st.selectbox(
            "Thuế VAT áp dụng trên hóa đơn:", 
            options=[8, 10], index=0
        )
        
    # Process calculations
    kwh_monthly = calculate_kwh_from_bill(bill_input, vat_rate)
    kwh_daily = kwh_monthly / 30.0
    
    # Recommend optimal package based on bill ranges
    rec_pkg_name = "SOLAR F2" # default fallback
    for name, data in packages.items():
        if data["min_bill"] <= bill_input <= data["max_bill"]:
            rec_pkg_name = name
            break
            
    rec_pkg = packages[rec_pkg_name]
    
    # Prepayment slider input
    max_loan_limit = 100000000
    price_total = rec_pkg["price"]
    min_prepay = max(0, price_total - max_loan_limit)
    
    st.markdown("---")
    st.markdown(f"### 🌟 GỢI Ý GIẢI PHÁP TỐI ƯU CHO KHÁCH HÀNG")
    
    col_rec1, col_rec2 = st.columns([1, 1])
    with col_rec1:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Lượng Điện Tiêu Thụ Thực Tế</div>
            <div class='metric-value'>{kwh_monthly:,.2f} kWh <span style='font-size:1.2rem; color:#666;'>/ tháng</span></div>
            <div class='metric-desc'>Trung bình khoảng <strong>{kwh_daily:,.2f} kWh (số điện)</strong> mỗi ngày.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_rec2:
        st.markdown(f"""
        <div class='card' style='border-top: 4px solid #FFD700;'>
            <div class='metric-title'>🌟 Gói Đề Xuất Tối Ưu</div>
            <div class='metric-value' style='color:#D4AF37;'>{rec_pkg_name}</div>
            <div class='metric-desc'>Công suất: <strong>{rec_pkg['power']} kWp</strong> · Trọn gói: <strong>{rec_pkg['price']:,}đ</strong><br>{rec_pkg['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Input prepayment amount
    st.markdown("### 🏦 Cấu hình dòng tiền trả góp")
    prepay_input = st.number_input(
        f"Tiền khách trả trước (VNĐ) - Tối thiểu: {min_prepay:,} VNĐ cho gói này:", 
        min_value=int(min_prepay), max_value=int(price_total), 
        value=int(min_prepay), step=1000000
    )
    
    actual_loan = price_total - prepay_input
    
    # Economic Analysis (ROI)
    # Output production value per month
    # Daily production (kWh) = kWp * 4.3 (peak sun hours) * 0.82 (efficiency coefficient)
    daily_prod = rec_pkg["power"] * 4.3 * 0.82
    monthly_prod = daily_prod * 30
    
    # Calculate new bill (assume grid offset is monthly_prod)
    new_kwh = max(0.0, kwh_monthly - monthly_prod)
    new_bill = calculate_bill_from_kwh(new_kwh, vat_rate)
    monthly_savings = max(0.0, bill_input - new_bill)
    yearly_savings = monthly_savings * 12
    
    # Calculate ROI (years to payback based on actual prepay or total investment)
    roi_years = price_total / yearly_savings if yearly_savings > 0 else 0
    
    st.markdown("#### 💵 Phân Tích Hiệu Quả Đầu Tư (ROI) & Dự Kiến Phương Án Trả Góp")
    
    col_roi1, col_roi2, col_roi3 = st.columns(3)
    with col_roi1:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Hóa Đơn Điện Mới Dự Kiến</div>
            <div class='metric-value'>{new_bill:,.0f} đ</div>
            <div class='metric-desc'>Tiết kiệm <strong>{monthly_savings:,.0f} đ</strong> / tháng ({ (monthly_savings/bill_input*100):.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_roi2:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Tiết Kiệm Hàng Năm</div>
            <div class='metric-value'>{yearly_savings:,.0f} đ</div>
            <div class='metric-desc'>Tận hưởng điện xanh 20 - 30 năm tới</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_roi3:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Thời Gian Hòa Vốn (ROI)</div>
            <div class='metric-value'>{roi_years:.1f} Năm</div>
            <div class='metric-desc'>Bảo hành thiết bị lên tới 15 - 30 năm</div>
        </div>
        """, unsafe_allow_html=True)

    # Shinhan Repayment calculations for this dynamic loan
    if actual_loan > 0:
        st.markdown("#### 🏦 Phương Án Trả Góp Trắng Qua Shinhan Bank (Lãi phẳng 0.59%/tháng)")
        if prepay_input == min_prepay and min_prepay > 0:
            st.warning(f"⚠️ Do gói có giá trị lớn hơn hạn mức của Shinhan Bank (100 triệu), khách hàng cần thanh toán phí đối ứng chênh lệch ban đầu là: **{min_prepay:,}đ**.")
        elif prepay_input == 0:
            st.success("🎉 Khách hàng đủ điều kiện áp dụng chương trình **'Lắp Solar 0 đồng trả trước'** (Vay 100% không đối ứng)!")
            
        terms = [12, 24, 36, 48]
        repayment_data = []
        for t in terms:
            monthly_principal = actual_loan / t
            monthly_interest = actual_loan * 0.0059
            total_monthly_gop = monthly_principal + monthly_interest
            net_cashflow = monthly_savings - total_monthly_gop
            total_interest = monthly_interest * t
            
            cashflow_str = f"+{net_cashflow:,.0f}đ (Dư bỏ túi)" if net_cashflow >= 0 else f"-{abs(net_cashflow):,.0f}đ (Bù thêm)"
            
            repayment_data.append({
                "Kỳ hạn": f"{t} Tháng",
                "Khoản vay": f"{actual_loan:,.0f}đ",
                "Tiền gốc/tháng": f"{monthly_principal:,.0f}đ",
                "Tiền lãi/tháng (0.59%)": f"{monthly_interest:,.0f}đ",
                "Tổng Góp/tháng": f"{total_monthly_gop:,.0f}đ",
                "Dòng tiền thực tế": cashflow_str,
                "Tổng lãi trả ngân hàng": f"{total_interest:,.0f}đ"
            })
            
        df_repay = pd.DataFrame(repayment_data)
        st.table(df_repay)
    else:
        st.success("🎉 Khách hàng lựa chọn trả thẳng 100% bằng tiền mặt, tự chủ năng lượng không tốn một đồng lãi vay!")

# Tab 2: Package details & specs
with tab_details:
    st.markdown("### 📦 Bảng giá và Cấu hình thông số kỹ thuật 10 Gói Hybrid")
    
    # Image 2: Equipment photo in Package Details tab
    solar_equip_img_path = "images/solar_equipment.jpg"
    if os.path.exists(solar_equip_img_path):
        st.image(solar_equip_img_path, caption="Hệ thống trang thiết bị Hybrid tiêu chuẩn Đức của Solar 24h", use_column_width=True)
    else:
        st.info("💡 Hình ảnh thiết bị (images/solar_equipment.jpg) chưa được tải lên GitHub. Sử dụng bảng mô tả kỹ thuật bên dưới.")

    specs_list = []
    for name, data in packages.items():
        specs_list.append({
            "Mã Gói": name,
            "Công Suất": f"{data['power']} kWp",
            "Tấm Pin AE Solar 580W": f"{data['panels']} Tấm",
            "Inverter Hybrid": data["inverter"],
            "Pin Lưu Trữ Lithium": data["battery"],
            "Giá Trọn Gói": f"{data['price']:,}đ",
            "Dải Phù Hợp": data["desc"]
        })
    df_specs = pd.DataFrame(specs_list)
    st.dataframe(df_specs, use_container_width=True, hide_index=True)

# Tab 3: Shinhan Bank Reference details
with tab_consult: # Also embedded in consultation but adding reference here
    pass

with tab_shinhan:
    st.markdown("### 🏦 Chính sách liên kết tài chính Shinhan Bank & Solar 24h")
    st.markdown("""
    *   **Đối tượng áp dụng:** Các hộ gia đình, cá nhân có nhu cầu lắp đặt hệ thống điện mặt trời Hybrid tại Miền Tây.
    *   **Hạn mức hỗ trợ vay tối đa:** **100.000.000 VNĐ**.
    *   **Lãi suất ưu đãi cố định:** **0.59% / tháng** (Lãi suất phẳng cực kỳ hấp dẫn).
    *   **Kỳ hạn linh hoạt:** **12, 24, 36, 48 tháng**.
    *   **Thủ tục hồ sơ siêu đơn giản:** Chỉ cần **CCCD gắn chip** và **Hóa đơn tiền điện sinh hoạt** (không cần chứng minh thu nhập phức tạp).
    """)
    
    st.info("💡 **MẸO TƯ VẤN SALES:** Hãy nhấn mạnh thông điệp 'Lấy tiền điện trả tiền góp'. Với kỳ hạn 48 tháng cho các gói F1 - F3, dòng tiền khách hàng bù thêm thực tế mỗi tháng cực kỳ nhỏ (chỉ vài trăm ngàn) nhưng hóa đơn điện đã được triệt tiêu vĩnh viễn đến 25 năm!")

import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán & Tư Vấn Trả Góp",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand colors and custom CSS styles matching Solar 24h
st.markdown("""
<style>
    /* Navy and Gold brand palette */
    :root {
        --primary-color: #0F2C59;
        --secondary-color: #E6A15C;
        --accent-color: #F8F9FA;
    }
    
    /* Main container styling */
    .stApp {
        background-color: #f7f9fc;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #0A2540 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Card design */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1a365d;
        margin-bottom: 15px;
    }
    
    .gold-card {
        background-color: #fffbeb;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #d97706;
        margin-bottom: 15px;
    }
    
    /* Text colors and highlights */
    .highlight-gold {
        color: #d97706;
        font-weight: bold;
    }
    .highlight-navy {
        color: #0F2C59;
        font-weight: bold;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        color: #6c757d;
        font-size: 14px;
        border-top: 1px solid #e9ecef;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# Define packages and technical metadata
PACKAGES = [
    {
        "id": "F1",
        "name": "SOLAR F1",
        "kwp": 2.3,
        "panels": "4 Tấm AE SOLAR 580W",
        "panel_count": 4,
        "battery": "Lưu trữ BSB 2.5 kWh",
        "inverter": "Inverter LUXPOWER SNA 5kW",
        "price": 47800000,
        "min_bill": 0,
        "max_bill": 500000,
        "desc": "Phù hợp hộ gia đình nhỏ có hóa đơn dưới 500k/tháng.",
        "yield_min": 6,
        "yield_max": 10
    },
    {
        "id": "F2",
        "name": "SOLAR F2",
        "kwp": 4.6,
        "panels": "8 Tấm AE SOLAR 580W",
        "panel_count": 8,
        "battery": "Lưu trữ BSB 5 kWh",
        "inverter": "Inverter LUXPOWER SNA 5kW",
        "price": 68500000,
        "min_bill": 500000,
        "max_bill": 1000000,
        "desc": "Phù hợp hộ gia đình trung bình có hóa đơn 500k - 1 triệu/tháng.",
        "yield_min": 10,
        "yield_max": 18
    },
    {
        "id": "F3",
        "name": "SOLAR F3",
        "kwp": 5.8,
        "panels": "10 Tấm AE SOLAR 580W",
        "panel_count": 10,
        "battery": "Lưu trữ LS BATTERY 10 kWh",
        "inverter": "Inverter SVE 6kW",
        "price": 88000000,
        "min_bill": 1000000,
        "max_bill": 1500000,
        "desc": "Phù hợp hộ gia đình vừa có hóa đơn 1 triệu - 1.5 triệu/tháng.",
        "yield_min": 15,
        "yield_max": 28
    },
    {
        "id": "F4",
        "name": "SOLAR F4",
        "kwp": 6.9,
        "panels": "12 Tấm AE SOLAR 580W",
        "panel_count": 12,
        "battery": "Lưu trữ EJOR 16 kWh",
        "inverter": "Inverter SVE 6kW",
        "price": 104700000,
        "min_bill": 1500000,
        "max_bill": 2000000,
        "desc": "Phù hợp gia đình có hóa đơn từ 1.5 triệu - 2 triệu/tháng.",
        "yield_min": 20,
        "yield_max": 30
    },
    {
        "id": "F5",
        "name": "SOLAR F5",
        "kwp": 8.1,
        "panels": "14 Tấm AE SOLAR 580W",
        "panel_count": 14,
        "battery": "Lưu trữ EJOR hoặc LS 16 kWh",
        "inverter": "Inverter HYBRID LUXPOWER 6.5PRO",
        "price": 114900000,
        "min_bill": 2000000,
        "max_bill": 2500000,
        "desc": "Phù hợp gia đình vừa và lớn có hóa đơn từ 2 triệu - 2.5 triệu/tháng.",
        "yield_min": 20,
        "yield_max": 34
    },
    {
        "id": "F6",
        "name": "SOLAR F6",
        "kwp": 9.3, # 16 Tấm pin * 580W = 9.28 kWp -> 9.3 kWp
        "panels": "16 Tấm AE SOLAR 580W",
        "panel_count": 16,
        "battery": "Lưu trữ EJOR hoặc LS 16 kWh",
        "inverter": "Inverter HYBRID LUXPOWER 6.5PRO",
        "price": 123600000,
        "min_bill": 2500000,
        "max_bill": 3000000,
        "desc": "Phù hợp gia đình lớn, biệt thự có hóa đơn từ 2.5 triệu - 3 triệu/tháng.",
        "yield_min": 25,
        "yield_max": 40
    },
    {
        "id": "F7",
        "name": "SOLAR F7",
        "kwp": 11.6, # 20 Tấm pin * 580W = 11.6 kWp
        "panels": "20 Tấm AE SOLAR 580W",
        "panel_count": 20,
        "battery": "Lưu trữ EJOR hoặc LS 32 kWh (2 tủ)",
        "inverter": "Inverter HYBRID LUXPOWER 6.5PRO (x2)",
        "price": 203000000,
        "min_bill": 3000000,
        "max_bill": 4000000,
        "desc": "Phù hợp biệt thự, kinh doanh có hóa đơn từ 3 triệu - 4 triệu/tháng.",
        "yield_min": 35,
        "yield_max": 50
    },
    {
        "id": "F8",
        "name": "SOLAR F8",
        "kwp": 13.9, # 24 Tấm pin * 580W = 13.92 kWp
        "panels": "24 Tấm AE SOLAR 580W",
        "panel_count": 24,
        "battery": "Lưu trữ EJOR hoặc LS 32 kWh (2 tủ)",
        "inverter": "Inverter HYBRID LUXPOWER 6.5PRO (x2)",
        "price": 217900000,
        "min_bill": 4000000,
        "max_bill": 5000000,
        "desc": "Phù hợp biệt thự, nhà xưởng nhỏ, kho lạnh có hóa đơn từ 4 triệu - 5 triệu/tháng.",
        "yield_min": 40,
        "yield_max": 60
    },
    {
        "id": "F9",
        "name": "SOLAR F9",
        "kwp": 17.4, # 30 Tấm pin * 580W = 17.4 kWp
        "panels": "30 Tấm AE SOLAR 580W",
        "panel_count": 30,
        "battery": "Lưu trữ EJOR hoặc LS 32 kWh (2 tủ)",
        "inverter": "Inverter HYBRID LUXPOWER 6.5PRO (x2)",
        "price": 239000000,
        "min_bill": 5000000,
        "max_bill": 7000000,
        "desc": "Phù hợp nhà xưởng, kinh doanh vừa có hóa đơn từ 5 triệu - 7 triệu/tháng.",
        "yield_min": 50,
        "yield_max": 70
    },
    {
        "id": "F10",
        "name": "SOLAR F10",
        "kwp": 22.0, # 38 Tấm pin * 580W = 22.04 kWp
        "panels": "38 Tấm AE SOLAR 580W",
        "panel_count": 38,
        "battery": "Lưu trữ EJOR hoặc LS 48 kWh (3 tủ)",
        "inverter": "Inverter HYBRID LUXPOWER 6.5PRO (x3)",
        "price": 329300000,
        "min_bill": 7000000,
        "max_bill": 10000000,
        "desc": "Phù hợp cơ sở kinh doanh lớn, kho lạnh lớn có hóa đơn từ 7 triệu - 10 triệu/tháng.",
        "yield_min": 60,
        "yield_max": 90
    }
]

# 2026 progressive progressive tariff bands (QĐ 1279 & TT 60)
# Price per kWh before VAT
TARIFF_2026 = [
    {"limit": 50, "price": 1984},
    {"limit": 50, "price": 2050},
    {"limit": 100, "price": 2380},
    {"limit": 100, "price": 2998},
    {"limit": 100, "price": 3350},
    {"limit": float('inf'), "price": 3460}
]

def calculate_kwh_from_bill(bill_amount, vat_rate):
    """Calculates consumed kWh from total bill amount including VAT."""
    pre_vat_bill = bill_amount / (1 + vat_rate / 100)
    remaining = pre_vat_bill
    total_kwh = 0.0
    
    for band in TARIFF_2026:
        step_limit = band["limit"]
        step_price = band["price"]
        
        if step_limit == float('inf'):
            kwh_in_step = remaining / step_price
            total_kwh += kwh_in_step
            break
        else:
            max_step_cost = step_limit * step_price
            if remaining > max_step_cost:
                total_kwh += step_limit
                remaining -= max_step_cost
            else:
                kwh_in_step = remaining / step_price
                total_kwh += kwh_in_step
                break
                
    return total_kwh

def get_proposed_package(bill_amount):
    """Finds the best-matching package based on customer bill range."""
    # Find package where bill is in range
    for pkg in PACKAGES:
        if pkg["min_bill"] <= bill_amount < pkg["max_bill"]:
            return pkg
    # Fallback to F10 if extremely large bill
    return PACKAGES[-1]

# Header UI with Brand Info
col1, col2 = st.columns([1, 4])
with col1:
    import os
    if os.path.exists("images/solar_girl.jpg"):
        st.image("images/solar_girl.jpg", use_column_width=True)
    else:
        st.markdown("""
        <div style="background-color:#0F2C59; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">
            👩‍💼 Mascot<br>Solar Girl
        </div>
        """, unsafe_allow_html=True)
with col2:
    st.title("SOLAR 24H - NĂNG LƯỢNG MẶT TRỜI CHUYÊN NGHIỆP")
    st.markdown("""
    **Solar Girl chào cả nhà! 👩‍💼**  
    Mọi người chỉ cần nhập hóa đơn và tùy chỉnh mức trả trước theo mong muốn. Hệ thống sẽ tự động tư vấn ạ!
    
    *📍 Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh · 📞 Hotline: 0909.363.579 - 0896.488.299*
    """)

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Chi Tiết Gói Lắp Đặt", "🏦 Gói Vay Shinhan Bank"])

# Packages data mappings
packages_info = {
    "F1": {"kwp": 2.3, "area_min": 12, "area_max": 14, "price": 47800000},
    "F2": {"kwp": 4.6, "area_min": 23, "area_max": 28, "price": 68500000},
    "F3": {"kwp": 5.8, "area_min": 29, "area_max": 35, "price": 88000000},
    "F4": {"kwp": 6.9, "area_min": 35, "area_max": 42, "price": 104700000},
    "F5": {"kwp": 8.1, "area_min": 41, "area_max": 49, "price": 114900000},
    "F6": {"kwp": 9.3, "area_min": 47, "area_max": 56, "price": 123600000},
    "F7": {"kwp": 11.6, "area_min": 58, "area_max": 70, "price": 203000000},
    "F8": {"kwp": 13.9, "area_min": 70, "area_max": 84, "price": 217900000},
    "F9": {"kwp": 17.4, "area_min": 87, "area_max": 105, "price": 239000000},
    "F10": {"kwp": 22.0, "area_min": 110, "area_max": 132, "price": 329300000}
}

with tab1:
    st.subheader("Báo Cáo Tư Vấn Lắp Đặt Nhanh Cho Khách Hàng")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        bill_input = st.number_input(
            "Nhập số tiền điện hàng tháng của khách (VNĐ):",
            min_value=100000,
            max_value=50000000,
            value=2700000,
            step=100000,
            format="%d"
        )
    with col_input2:
        vat_input = st.selectbox(
            "Thuế VAT áp dụng trên hóa đơn (%):",
            [8, 10],
            index=0
        )
        
    # Process calculations
    kwh_consumed = calculate_kwh_from_bill(bill_input, vat_input)
    proposed_pkg = get_proposed_package(bill_input)
    
    pkg_id = proposed_pkg["id"]
    pkg_meta = packages_info[pkg_id]
    
    # Calculate savings
    saving_percentage = 1.0
    bill_saved = bill_input * saving_percentage
    bill_new = bill_input - bill_saved
    bill_saved_annual = bill_saved * 12
    
    # ROI calculation
    roi_years = pkg_meta["price"] / bill_saved_annual if bill_saved_annual > 0 else 0
    
    st.markdown("---")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>LƯỢNG ĐIỆN TIÊU THỤ THỰC TẾ</h4>
            <h2 class="highlight-navy">{kwh_consumed:,.2f} kWh / tháng</h2>
            <p>Trung bình khoảng <b>{kwh_consumed/30:,.2f} kWh (số điện)</b> mỗi ngày</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_res2:
        st.markdown(f"""
        <div class="gold-card">
            <h4>🌟 GÓI ĐỀ XUẤT TỐI ƯU</h4>
            <h2 class="highlight-gold">{proposed_pkg['name']}</h2>
            <p>Công suất: <b>{pkg_meta['kwp']} kWp</b> · Trọn gói: <b>{pkg_meta['price']:,.0f}đ</b></p>
            <p><b>Diện tích mái tối thiểu cần thiết:</b> <span class="highlight-gold">{pkg_meta['area_min']} - {pkg_meta['area_max']} m²</span> (không đổ bóng)</p>
            <p><i>{proposed_pkg['desc']}</i></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 💵 Phân Tích Hiệu Quả Đầu Tư (ROI) & Dự Kiến Phương Án Trả Góp")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="HÓA ĐƠN ĐIỆN MỚI DỰ KIẾN", value="0 đ", delta=f"-{bill_input:,.0f} đ/tháng", delta_color="inverse")
    with col_m2:
        st.metric(label="TIẾT KIỆM HÀNG NĂM", value=f"{bill_saved_annual:,.0f} đ", delta="Tận hưởng điện xanh 20 - 30 năm tới", delta_color="normal")
    with col_m3:
        st.metric(label="THỜI GIAN HOÀN VỐN (ROI)", value=f"{roi_years:.1f} Năm", delta="Bảo hành thiết bị lên tới 15-30 năm", delta_color="normal")
        
    st.markdown("---")
    
    st.markdown("### 🏦 Phương Án Trả Góp Qua Shinhan Bank (0đ Trả Trước)")
    
    price = pkg_meta["price"]
    
    # Default initial prepaid amount minimum (if package price > 100M, minimum prepayment is price - 100M)
    min_prepay = max(0.0, price - 100000000.0)
    
    st.markdown(f"**Thông tin gói:** Giá trọn gói là **{price:,.0f} VNĐ**. Hạn mức cho vay tối đa của Shinhan Bank là **100.000.000 VNĐ**.")
    
    prepay_input = st.number_input(
        "Tiền khách trả trước (VNĐ):",
        min_value=float(min_prepay),
        max_value=float(price),
        value=float(min_prepay),
        step=1000000.0,
        format="%.0f"
    )
    
    loan_amount = price - prepay_input
    
    if loan_amount <= 0:
        st.success("🎉 Khách hàng tự chi trả 100% bằng tiền mặt, không phát sinh nợ vay và lãi suất ngân hàng!")
    else:
        st.info(f"👉 **Số tiền vay ngân hàng thực tế:** **{loan_amount:,.0f} VNĐ** (Tiền trả trước: **{prepay_input:,.0f} VNĐ**).")
        
        # Calculate payment table
        periods = [12, 24, 36, 48]
        flat_rate = 0.0059 # 0.59% per month
        
        rows = []
        for period in periods:
            monthly_principal = loan_amount / period
            monthly_interest = loan_amount * flat_rate
            total_monthly = monthly_principal + monthly_interest
            total_interest = monthly_interest * period
            
            # Net monthly cashflow (Savings - Installment payment)
            net_cashflow = bill_saved - total_monthly
            if net_cashflow >= 0:
                cashflow_str = f"+{net_cashflow:,.0f}đ (Dư ra)"
            else:
                cashflow_str = f"-{abs(net_cashflow):,.0f}đ (Bù thêm)"
                
            rows.append({
                "Kỳ hạn": f"{period} Tháng",
                "Khoản vay": f"{loan_amount:,.0f}đ",
                "Tiền gốc/tháng": f"{monthly_principal:,.0f}đ",
                "Tiền lãi/tháng": f"{monthly_interest:,.0f}đ",
                "Tổng Góp/tháng": f"{total_monthly:,.0f}đ",
                "Dòng tiền thực tế": cashflow_str,
                "Tổng lãi trả ngân hàng": f"{total_interest:,.0f}đ"
            })
            
        df_loans = pd.DataFrame(rows)
        st.table(df_loans)
        
        st.markdown("""
        *   **Lãi suất áp dụng:** Cố định phẳng cực ưu đãi **0.59%/tháng** suốt thời hạn vay.
        *   **Thủ tục phê duyệt:** Siêu nhanh gọn, chỉ cần **Căn cước công dân gắn chip** và **Hóa đơn tiền điện sinh hoạt**. Không yêu cầu thế chấp hay chứng minh thu nhập phức tạp!
        """)

with tab2:
    st.subheader("Bảng Tra Cứu Danh Mục Thiết Bị & Khảo Sát Mái")
    
    # Custom input for arbitrary kWp to calculate required area and yield
    st.markdown("#### 🔍 Tính Toán Nhanh Diện Tích Mái & Sản Lượng Cho Công Suất Tùy Chọn")
    col_custom1, col_custom2 = st.columns(2)
    with col_custom1:
        kwp_custom = st.number_input(
            "Nhập công suất thiết kế tùy chỉnh (kWp):",
            min_value=1.0,
            max_value=500.0,
            value=5.0,
            step=0.5,
            format="%.1f"
        )
    with col_custom2:
        sun_hours = st.slider(
            "Số giờ nắng đỉnh trung bình (giờ/ngày):",
            min_value=3.5,
            max_value=5.5,
            value=4.3,
            step=0.1
        )
        
    # Calculate based on custom kwp
    custom_area_min = kwp_custom * 5
    custom_area_max = kwp_custom * 6
    # Yield = kWp * peak_hours * 30 days * 0.82 standard efficiency
    custom_yield = kwp_custom * sun_hours * 30 * 0.82
    
    st.markdown(f"""
    <div class="metric-card" style="border-left: 5px solid #d97706;">
        <p>📊 <b>Kết quả tính toán nhanh:</b></p>
        <ul>
            <li>Diện tích mái cần thiết: <b>{custom_area_min:.1f} - {custom_area_max:.1f} m²</b> (không bị đổ bóng)</li>
            <li>Hướng lắp đặt tối ưu: <b>Hướng Nam</b> hoặc <b>Hướng Đông Nam</b> tại khu vực miền Tây</li>
            <li>Sản lượng điện dự kiến sinh ra: <span class="highlight-gold"><b>{custom_yield:.1f} kWh/tháng</b></span> (trung bình ~<b>{custom_yield/30:.1f} kWh/ngày</b>)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📦 Bảng Quy Chuẩn 10 Gói Hybrid Hộ Gia Đình")
    
    # Format data for display table
    pkg_rows = []
    for p in PACKAGES:
        meta = packages_info[p["id"]]
        pkg_rows.append({
            "Tên Gói": p["name"],
            "Công Suất (kWp)": f"{meta['kwp']} kWp",
            "Số Tấm AE 580W": f"{p['panels']}",
            "Diện Tích Mái Cần (m²)": f"{meta['area_min']} - {meta['area_max']} m²",
            "Inverter Kèm": p["inverter"],
            "Dung Lượng Lưu Trữ": p["battery"],
            "Đơn Giá Trọn Gói": f"{p['price']:,.0f}đ",
            "Phân Khúc Phù Hợp": p["desc"]
        })
    df_pkgs = pd.DataFrame(pkg_rows)
    st.dataframe(df_pkgs, use_container_width=True)
    
    import os
    if os.path.exists("images/solar_equipment.jpg"):
        st.image("images/solar_equipment.jpg", caption="Hệ thống thiết bị Hybrid cao cấp Solar 24h", use_column_width=True)

with tab3:
    st.subheader("Chương Trình Trả Góp Liên Kết Shinhan Bank")
    st.markdown("""
    #### 🏦 Đôi nét về gói vay Xanh đặc quyền của Shinhan Bank:
    Công ty Solar 24h ký kết hợp tác chiến lược cùng Shinhan Bank để cung cấp dòng vốn vay tiêu dùng xanh cực kỳ ưu đãi dành riêng cho khách hàng lắp đặt điện năng lượng mặt trời:
    
    *   **Lãi suất cố định siêu phẳng:** **0.59%/tháng** cố định trong suốt vòng đời kỳ hạn vay (không bị biến động theo biên độ thị trường).
    *   **Hạn mức cho vay tối đa:** **100.000.000 VNĐ** (Thích hợp vay trắng 100% cho các dòng từ F1 đến F3, hỗ trợ tài chính cực lớn cho các dòng từ F4 trở lên).
    *   **Kỳ hạn linh hoạt:** Cho phép lựa chọn **12, 24, 36 hoặc 48 tháng**.
    *   **Điều kiện phê duyệt đơn giản:** 
        *   Căn cước công dân gắn chip của chủ hộ.
        *   Hóa đơn tiền điện sinh hoạt 3 tháng gần nhất tại địa điểm lắp đặt.
        *   Không cần tài sản bảo thế chấp, không cần chứng minh sao kê bảng lương!
    """)
    
    st.markdown("#### 📊 Bảng Quy Đổi Số Góp Cố Định Trên Các Hạn Mức Vay")
    
    # Display the static matrix of loans as reference
    loan_limits = [10000000, 20000000, 40000000, 60000000, 80000000, 100000000]
    matrix_rows = []
    flat_rate_val = 0.0059
    
    for l_val in loan_limits:
        for p_val in [12, 24, 36, 48]:
            p_monthly = l_val / p_val
            i_monthly = l_val * flat_rate_val
            total_gop = p_monthly + i_monthly
            total_pay = total_gop * p_val
            
            matrix_rows.append({
                "Hạn mức vay": f"{l_val:,.0f}đ",
                "Kỳ hạn": f"{p_val} Tháng",
                "Tiền gốc/tháng": f"{p_monthly:,.0f}đ",
                "Tiền lãi/tháng": f"{i_monthly:,.0f}đ",
                "Tổng Góp hàng tháng": f"{total_gop:,.0f}đ",
                "Tổng Gốc + Lãi": f"{total_pay:,.0f}đ"
            })
            
    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix, use_container_width=True)

# Shared Brand Footer
st.markdown("""
<div class="footer">
    <p>© 2026 Solar 24h. Tất cả các quyền được bảo lưu. Được vận hành bởi đội ngũ Solar Girl tận tâm ☀️</p>
    <p>Địa chỉ: Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh, Tỉnh Đồng Tháp</p>
</div>
""", unsafe_allow_html=True)

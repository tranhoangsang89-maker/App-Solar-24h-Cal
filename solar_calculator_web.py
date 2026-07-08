import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration to wide layout and set title & icon
st.set_page_config(
    page_title="Solar 24h - Công cụ tính toán điện mặt trời",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for branding colors (Navy Blue & Gold) and mobile optimization
st.markdown("""
<style>
    :root {
        --primary-color: #0F2C59;
        --secondary-color: #DAC0A3;
        --text-color: #1F2937;
        --bg-color: #F8F9FA;
    }
    .stApp {
        background-color: #F8F9FA;
        color: #1F2937;
    }
    .main-title {
        color: #0F2C59;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #F5A623;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
        border-left: 5px solid #0F2C59;
    }
    .card-gold {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
        border-left: 5px solid #F5A623;
    }
    .highlight-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F2C59;
    }
    .highlight-val-gold {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F5A623;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 0.8rem;
        color: #6B7280;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA DEFINITIONS -----------------
# 2026 Electricity Tariffs
TARIFFS = [
    {"limit": 50, "rate": 1984, "cumulative_cost": 99200},          # Bậc 1
    {"limit": 50, "rate": 2050, "cumulative_cost": 99200 + 102500},  # Bậc 2
    {"limit": 100, "rate": 2380, "cumulative_cost": 201700 + 238000}, # Bậc 3
    {"limit": 100, "rate": 2998, "cumulative_cost": 439700 + 299800}, # Bậc 4
    {"limit": 100, "rate": 3350, "cumulative_cost": 739500 + 335000}, # Bậc 5
    {"limit": float('inf'), "rate": 3460, "cumulative_cost": float('inf')} # Bậc 6
]

# Fixed pre-paid rate
PREPAID_RATE = 2909

# 10 Hybrid Solar Packages of Solar 24h
PACKAGES = [
    {
        "id": "SOLAR F1",
        "name": "SOLAR F1 (Hệ 2.3 kWp - Lưu trữ 2.5 kWh)",
        "capacity": 2.3,
        "storage": 2.5,
        "panels": 4,
        "inverter": "Luxpower SNA 5kW",
        "battery": "Lithium BSB 2.5 kWh",
        "price": 47800000,
        "description": "Phù hợp hộ gia đình nhỏ tiêu thụ dưới 500.000đ tiền điện/tháng"
    },
    {
        "id": "SOLAR F2",
        "name": "SOLAR F2 (Hệ 4.6 kWp - Lưu trữ 5 kWh)",
        "capacity": 4.6,
        "storage": 5.0,
        "panels": 8,
        "inverter": "Luxpower SNA 5kW",
        "battery": "Lithium BSB 5 kWh",
        "price": 68500000,
        "description": "Phù hợp hộ gia đình có hóa đơn dưới 1.000.000đ tiền điện/tháng"
    },
    {
        "id": "SOLAR F3",
        "name": "SOLAR F3 (Hệ 5.8 kWp - Lưu trữ 10 kWh)",
        "capacity": 5.8,
        "storage": 10.0,
        "panels": 10,
        "inverter": "SVE 6kW",
        "battery": "Lithium LS Battery 10 kWh",
        "price": 88000000,
        "description": "Phù hợp hộ gia đình tiêu thụ từ 1.000.000đ - 1.500.000đ tiền điện/tháng"
    },
    {
        "id": "SOLAR F4",
        "name": "SOLAR F4 (Hệ 6.9 kWp - Lưu trữ 16 kWh)",
        "capacity": 6.9,
        "storage": 16.0,
        "panels": 12,
        "inverter": "SVE 6kW",
        "battery": "Lithium EJOR 16 kWh",
        "price": 104700000,
        "description": "Phù hợp hộ gia đình tiêu thụ từ 1.500.000đ - 2.000.000đ tiền điện/tháng"
    },
    {
        "id": "SOLAR F5",
        "name": "SOLAR F5 (Hệ 8.1 kWp - Lưu trữ 16 kWh)",
        "capacity": 8.1,
        "storage": 16.0,
        "panels": 14,
        "inverter": "Luxpower Pro 6.5kW",
        "battery": "Lithium EJOR/LS 16 kWh",
        "price": 114900000,
        "description": "Phù hợp hộ gia đình tiêu thụ từ 2.000.000đ - 2.500.000đ tiền điện/tháng"
    },
    {
        "id": "SOLAR F6",
        "name": "SOLAR F6 (Hệ 9.28 kWp - Lưu trữ 16 kWh)",
        "capacity": 9.28,
        "storage": 16.0,
        "panels": 16,
        "inverter": "Luxpower 6.5 Pro",
        "battery": "Lithium EJOR/LS 16 kWh",
        "price": 123600000,
        "description": "Phù hợp hộ gia đình tiêu thụ từ 2.500.000đ - 3.000.000đ tiền điện/tháng"
    },
    {
        "id": "SOLAR F7",
        "name": "SOLAR F7 (Hệ 11.6 kWp - Lưu trữ 32 kWh)",
        "capacity": 11.6,
        "storage": 32.0,
        "panels": 20,
        "inverter": "2x Luxpower 6.5 Pro",
        "battery": "2x Lithium EJOR/LS 16 kWh (32kWh)",
        "price": 203000000,
        "description": "Phù hợp biệt thự, hộ kinh doanh tiêu thụ từ 3.000.000đ - 4.000.000đ/tháng"
    },
    {
        "id": "SOLAR F8",
        "name": "SOLAR F8 (Hệ 13.9 kWp - Lưu trữ 32 kWh)",
        "capacity": 13.9,
        "storage": 32.0,
        "panels": 24,
        "inverter": "2x Luxpower 6.5 Pro",
        "battery": "2x Lithium EJOR/LS 16 kWh (32kWh)",
        "price": 217900000,
        "description": "Phù hợp biệt thự, nhà xưởng nhỏ tiêu thụ từ 4.000.000đ - 5.000.000đ/tháng"
    },
    {
        "id": "SOLAR F9",
        "name": "SOLAR F9 (Hệ 17.4 kWp - Lưu trữ 32 kWh)",
        "capacity": 17.4,
        "storage": 32.0,
        "panels": 30,
        "inverter": "2x Luxpower 6.5 Pro",
        "battery": "2x Lithium EJOR/LS 16 kWh (32kWh)",
        "price": 239000000,
        "description": "Phù hợp nhà xưởng, hộ kinh doanh lớn tiêu thụ từ 5.000.000đ - 7.000.000đ/tháng"
    },
    {
        "id": "SOLAR F10",
        "name": "SOLAR F10 (Hệ 22.0 kWp - Lưu trữ 48 kWh)",
        "capacity": 22.0,
        "storage": 48.0,
        "panels": 38,
        "inverter": "3x Luxpower 6.5 Pro",
        "battery": "3x Lithium EJOR/LS 16 kWh (48kWh)",
        "price": 329300000,
        "description": "Phù hợp nhà xưởng lớn, cơ sở đông lạnh tiêu thụ từ 7.000.000đ - 10.000.000đ/tháng"
    }
]

# ----------------- HELPER FUNCTIONS -----------------
def calculate_kwh_from_bill(bill_with_vat, vat_rate=0.10):
    """Calculate consumed kWh from total bill with VAT based on 2026 progressive tariffs."""
    pre_vat_bill = bill_with_vat / (1 + vat_rate)
    
    if pre_vat_bill <= 99200:
        return pre_vat_bill / 1984
    elif pre_vat_bill <= 201700:
        return 50 + (pre_vat_bill - 99200) / 2050
    elif pre_vat <= 439700: # 1074500 is pre-vat for 300kWh? No, let's calculate:
        # B1: 50 * 1984 = 99200
        # B2: 50 * 2050 = 102500 -> Cum: 201700
        # B3: 100 * 2380 = 238000 -> Cum: 439700
        return 100 + (pre_vat_bill - 201700) / 2380
    elif pre_vat_bill <= 739500: # B4 limit
        # B4: 100 * 2998 = 299800 -> Cum: 739500
        return 200 + (pre_vat_bill - 439700) / 2998
    elif pre_vat_bill <= 1074500: # B5 limit
        # B5: 100 * 3350 = 335000 -> Cum: 1074500
        return 300 + (pre_vat_bill - 739500) / 3350
    else: # B6 limit
        return 400 + (pre_vat_bill - 1074500) / 3460

def calculate_bill_from_kwh(kwh, vat_rate=0.10):
    """Calculate total bill with VAT from consumed kWh based on 2026 progressive tariffs."""
    if kwh <= 0:
        return 0
    
    pre_vat = 0
    remaining_kwh = kwh
    
    # Bậc 1: 0 - 50 kWh
    b1_kwh = min(50, remaining_kwh)
    pre_vat += b1_kwh * 1984
    remaining_kwh -= b1_kwh
    
    # Bậc 2: 51 - 100 kWh
    if remaining_kwh > 0:
        b2_kwh = min(50, remaining_kwh)
        pre_vat += b2_kwh * 2050
        remaining_kwh -= b2_kwh
        
    # Bậc 3: 101 - 200 kWh
    if remaining_kwh > 0:
        b3_kwh = min(100, remaining_kwh)
        pre_vat += b3_kwh * 2380
        remaining_kwh -= b3_kwh
        
    # Bậc 4: 201 - 300 kWh
    if remaining_kwh > 0:
        b4_kwh = min(100, remaining_kwh)
        pre_vat += b4_kwh * 2998
        remaining_kwh -= b4_kwh
        
    # Bậc 5: 301 - 400 kWh
    if remaining_kwh > 0:
        b5_kwh = min(100, remaining_kwh)
        pre_vat += b5_kwh * 3350
        remaining_kwh -= b5_kwh
        
    # Bậc 6: trên 400 kWh
    if remaining_kwh > 0:
        pre_vat += remaining_kwh * 3460
        
    return pre_vat * (1 + vat_rate)

def calculate_monthly_generation(capacity_kwp):
    """Calculate expected monthly generation in Tiền Giang/Đồng Tháp."""
    # formula: kWp * 4.3 (sun hours) * 30 days * 0.82 (efficiency coefficient)
    return capacity_kwp * 4.3 * 30 * 0.82

def recommend_package(monthly_kwh):
    """Automatically recommend a suitable solar package based on monthly kWh usage."""
    # Estimate required capacity: required_monthly_gen = monthly_kwh
    # kWp = required_monthly_gen / (4.3 * 30 * 0.82)
    est_kwp = monthly_kwh / (4.3 * 30 * 0.82)
    
    # Find the closest package that has capacity >= est_kwp (or closest to it)
    recommended = PACKAGES[0]
    for pkg in PACKAGES:
        if pkg["capacity"] >= est_kwp:
            recommended = pkg
            break
    else:
        recommended = PACKAGES[-1] # if too large, suggest the biggest
    return recommended

# ----------------- HEADER -----------------
st.markdown("<h1 class='main-title'>SOLAR 24H ☀️</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>Công Cụ Tính Toán Năng Lượng & Trả Góp Shinhan Bank</h3>", unsafe_allow_html=True)

# Tabs definitions
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Chi Tiết Gói Lắp Đặt", "🏦 Gói Vay Shinhan Bank"])

# ----------------- TAB 1: NHẬP TIỀN ĐIỆN TƯ VẤN NHANH -----------------
with tab1:
    st.write("### Nhập dữ liệu khách hàng thực tế")
    col1, col2 = st.columns(2)
    with col1:
        monthly_bill_input = st.number_input("Hóa đơn tiền điện hàng tháng (VNĐ):", min_value=100000, max_value=50000000, value=3000000, step=50000)
    with col2:
        vat_rate_select = st.selectbox("Thuế suất VAT điện lực:", options=[0.10, 0.08], format_func=lambda x: f"{int(x*100)}%")

    # Calculate consumed kWh
    monthly_kwh = calculate_kwh_from_bill(monthly_bill_input, vat_rate_select)
    daily_kwh = monthly_kwh / 30
    
    st.markdown(f"""
    <div class='card'>
        <h4>Phân tích lượng điện tiêu thụ:</h4>
        • Số điện của bạn đang sử dụng mỗi tháng: <span class='highlight-val'>{monthly_kwh:,.1f} kWh</span><br>
        • Trung bình tiêu thụ mỗi ngày: <span class='highlight-val'>{daily_kwh:,.1f} kWh/ngày</span><br>
        <i>*Số liệu được tính toán dựa trên biểu giá lũy tiến sinh hoạt 2026 chính thức.*</i>
    </div>
    """, unsafe_allow_html=True)

    # Recommend suitable package
    pkg = recommend_package(monthly_kwh)
    st.write("### Gói giải pháp Solar 24h đề xuất:")
    
    # Calculate performance metrics
    pkg_generation = calculate_monthly_generation(pkg["capacity"])
    pkg_daily_generation = pkg_generation / 30
    
    new_kwh_needed = max(0.0, monthly_kwh - pkg_generation)
    new_bill = calculate_bill_from_kwh(new_kwh_needed, vat_rate_select)
    monthly_savings = monthly_bill_input - new_bill
    yearly_savings = monthly_savings * 12
    roi_years = pkg["price"] / yearly_savings if yearly_savings > 0 else float('inf')
    
    st.markdown(f"""
    <div class='card-gold'>
        <h3 style='color: #F5A623; margin-top: 0;'>🌟 {pkg['id']} - {pkg['name']}</h3>
        <p style='font-style: italic;'>{pkg['description']}</p>
        <table style='width: 100%; border-collapse: collapse; margin-top: 10px;'>
            <tr><td><b>Số tấm pin AE Solar 580W:</b></td><td>{pkg['panels']} tấm (Diện tích mái cần: {pkg['panels'] * 2.6:.1f} m²)</td></tr>
            <tr><td><b>Inverter Hybrid:</b></td><td>{pkg['inverter']}</td></tr>
            <tr><td><b>Bình lưu trữ Lithium:</b></td><td>{pkg['battery']}</td></tr>
            <tr><td><b>Sản lượng phát điện dự kiến:</b></td><td><span style='color: #0F2C59; font-weight:700;'>{pkg_generation:,.1f} kWh/tháng</span> (~{pkg_daily_generation:,.1f} kWh/ngày)</td></tr>
            <tr style='background-color: #F8F9FA;'><td style='padding: 8px 0;'><b>Đơn giá lắp đặt trọn gói:</b></td><td style='padding: 8px 0;'><span class='highlight-val'>{pkg['price']:,.0f} VNĐ</span></td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Hiệu quả tài chính dự kiến:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Tiền điện mới", f"{new_bill:,.0f} đ", delta=f"-{monthly_savings:,.0f} đ", delta_color="inverse")
    with col_b:
        st.metric("Tiết kiệm/Năm", f"{yearly_savings:,.0f} đ")
    with col_c:
        st.metric("Thời gian hoàn vốn", f"{roi_years:.1f} Năm")

# ----------------- TAB 2: CHI TIẾT 10 GÓI LẮP ĐẶT -----------------
with tab2:
    st.write("### Chọn gói lắp đặt để tra cứu cấu hình chi tiết")
    selected_pkg_name = st.selectbox("Chọn gói lắp đặt Hybrid:", options=[p["name"] for p in PACKAGES])
    selected_pkg = next(p for p in PACKAGES if p["name"] == selected_pkg_name)
    
    # Calculate performance for custom selected package
    custom_monthly_gen = calculate_monthly_generation(selected_pkg["capacity"])
    custom_daily_gen = custom_monthly_gen / 30
    roof_area = selected_pkg["panels"] * 2.6 # ~2.6m2 per 580W panel with spacing
    
    st.markdown(f"""
    <div class='card'>
        <h3 style='color: #0F2C59; margin-top: 0;'>📋 Thông Số Chi Tiết: {selected_pkg['id']}</h3>
        <table style='width: 100%; border-collapse: collapse;'>
            <tr><td style='padding: 8px 0; border-bottom: 1px solid #EEE;'><b>Công suất giàn pin:</b></td><td style='padding: 8px 0; border-bottom: 1px solid #EEE; text-align: right;'>{selected_pkg['capacity']} kWp</td></tr>
            <tr><td style='padding: 8px 0; border-bottom: 1px solid #EEE;'><b>Số tấm pin AE Solar 580W:</b></td><td style='padding: 8px 0; border-bottom: 1px solid #EEE; text-align: right;'>{selected_pkg['panels']} tấm</td></tr>
            <tr><td style='padding: 8px 0; border-bottom: 1px solid #EEE;'><b>Diện tích mái cần tối thiểu:</b></td><td style='padding: 8px 0; border-bottom: 1px solid #EEE; text-align: right;'>{roof_area:.1f} m²</td></tr>
            <tr><td style='padding: 8px 0; border-bottom: 1px solid #EEE;'><b>Biến tần Inverter Hybrid:</b></td><td style='padding: 8px 0; border-bottom: 1px solid #EEE; text-align: right;'>{selected_pkg['inverter']}</td></tr>
            <tr><td style='padding: 8px 0; border-bottom: 1px solid #EEE;'><b>Hệ lưu trữ Lithium:</b></td><td style='padding: 8px 0; border-bottom: 1px solid #EEE; text-align: right;'>{selected_pkg['battery']}</td></tr>
            <tr><td style='padding: 8px 0; border-bottom: 1px solid #EEE;'><b>Sản lượng phát trung bình:</b></td><td style='padding: 8px 0; border-bottom: 1px solid #EEE; text-align: right; color: #0F2C59; font-weight: bold;'>{custom_monthly_gen:,.1f} kWh/tháng ({custom_daily_gen:,.1f} kWh/ngày)</td></tr>
            <tr><td style='padding: 12px 0; color: #F5A623; font-size: 1.2rem;'><b>ĐƠN GIÁ TRỌN GÓI LẮP ĐẶT:</b></td><td style='padding: 12px 0; text-align: right; color: #0F2C59; font-size: 1.3rem; font-weight: bold;'>{selected_pkg['price']:,.0f} VNĐ</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Nhập công suất tùy chỉnh để ước tính sản lượng:")
    custom_capacity = st.number_input("Nhập số kWp mong muốn:", min_value=1.0, max_value=100.0, value=5.0, step=0.5)
    custom_gen = calculate_monthly_generation(custom_capacity)
    st.info(f"☀️ Hệ thống công suất {custom_capacity} kWp dự kiến tạo ra {custom_gen:,.1f} kWh (số điện) mỗi tháng tại miền Tây (lấy trung bình 4.3 giờ nắng đỉnh/ngày).")

# ----------------- TAB 3: TRẢ GÓP SHINHAN BANK 0 ĐỒNG -----------------
with tab3:
    st.write("### Tính toán bài toán trả góp 100% không đối ứng")
    st.write("Đối tác Shinhan Bank hỗ trợ cho vay tối đa **100.000.000 VNĐ** với mức lãi suất phẳng siêu ưu đãi cố định **0.59%/tháng**.")
    
    selected_loan_pkg_name = st.selectbox("Chọn gói muốn tính trả góp:", options=[p["name"] for p in PACKAGES], key="loan_pkg")
    loan_pkg = next(p for p in PACKAGES if p["name"] == selected_loan_pkg_name)
    
    # Calculate loan details
    package_price = loan_pkg["price"]
    # Maximum loan from Shinhan is 100M
    loan_amount = min(100000000, package_price)
    down_payment = max(0, package_price - 100000000)
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.write(f"• **Giá trị gói:** {package_price:,.0f} đ")
        if down_payment == 0:
            st.success("🎉 Gói này được duyệt hỗ trợ Vay Trắng 100%! Trả trước 0 đồng.")
        else:
            st.warning(f"⚠️ Do vượt hạn mức vay 100 triệu, quý khách cần tự thanh toán đối ứng: {down_payment:,.0f} đ")
    with col_y:
        st.write(f"• **Số tiền vay Shinhan Bank:** {loan_amount:,.0f} đ")
        st.write(f"• **Lãi suất phẳng/tháng:** 0.59% (cố định)")

    # Loan tenure comparison table
    tenures = [12, 24, 36, 48]
    loan_data = []
    
    # Estimated monthly savings for this package to compare cashflow
    pkg_savings = (calculate_monthly_generation(loan_pkg["capacity"])) * 3000 # average electricity savings with ~3000đ/kWh
    
    for t in tenures:
        goc = loan_amount / t
        lai = loan_amount * 0.0059
        tong_gop = goc + lai
        total_payment = tong_gop * t
        total_interest = lai * t
        cashflow = pkg_savings - tong_gop
        
        loan_data.append({
            "Kỳ hạn (Tháng)": f"{t} tháng",
            "Gốc hàng tháng (đ)": f"{goc:,.0f} đ",
            "Lãi hàng tháng (đ)": f"{lai:,.0f} đ",
            "Tổng góp/Tháng (đ)": f"{tong_gop:,.0f} đ",
            "Tổng tiền lãi (đ)": f"{total_interest:,.0f} đ",
            "Tổng Gốc + Lãi (đ)": f"{total_payment:,.0f} đ"
        })
        
    df_loan = pd.DataFrame(loan_data)
    st.write("### Bảng so sánh các kỳ hạn trả góp")
    st.table(df_loan.set_index("Kỳ hạn (Tháng)"))
    
    st.write("### 💡 Bài toán dòng tiền thực tế (\"Lấy tiền điện trả tiền góp\"):")
    st.info(f"Hệ thống **{loan_pkg['id']}** giúp tiết kiệm trung bình khoảng **{pkg_savings:,.0f}đ/tháng** tiền điện. Số tiền này sẽ tự động gánh vác phần lớn (hoặc dư thừa) tiền góp ngân hàng hàng tháng, giúp gia đình sở hữu nguồn điện sạch một cách nhàn hạ nhất!")

# ----------------- FOOTER -----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class='footer'>
    <b>CÔNG TY TNHH TMDV SOLAR 24H</b><br>
    🏢 Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh, Tỉnh Tiền Giang (kế bên Đồng Tháp)<br>
    ☎️ Hotline tư vấn & khảo sát miễn phí: 0909.363.579 - 0896.488.299<br>
    📧 Email: Solar24h.tmdv@gmail.com
</div>
""", unsafe_allow_html=True)

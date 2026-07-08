import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán Điện Mặt Trời",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand Color Palette (Navy Blue & Gold)
PRIMARY_COLOR = "#0F3057"
ACCENT_COLOR = "#FFD700"
BACKGROUND_COLOR = "#F4F6F9"

# Custom CSS for styling
st.markdown(f"""
    <style>
    .main {{
        background-color: {BACKGROUND_COLOR};
        color: #333333;
    }}
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}
    h1, h2, h3 {{
        color: {PRIMARY_COLOR};
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
    .brand-header {{
        background-color: {PRIMARY_COLOR};
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 5px solid {ACCENT_COLOR};
    }}
    .brand-header h1 {{
        color: {ACCENT_COLOR} !important;
        margin: 0;
        font-size: 2.2rem;
        font-weight: bold;
    }}
    .brand-header p {{
        margin: 5px 0 0 0;
        font-size: 1.1rem;
        font-style: italic;
    }}
    .card {{
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 5px solid {PRIMARY_COLOR};
    }}
    .highlight-card {{
        background-color: #EBF4FA;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 5px solid {ACCENT_COLOR};
    }}
    .metric-value {{
        font-size: 1.8rem;
        font-weight: bold;
        color: {PRIMARY_COLOR};
    }}
    .metric-label {{
        font-size: 0.9rem;
        color: #666666;
    }}
    </style>
""", unsafe_allow_html=True)

# 2026 Price List Sinh Hoạt (6 bậc lũy tiến)
BILL_STEPS_2026 = [
    {"limit": 50, "price": 1984},
    {"limit": 50, "price": 2050},
    {"limit": 100, "price": 2380},
    {"limit": 100, "price": 2998},
    {"limit": 100, "price": 3350},
    {"limit": float('inf'), "price": 3460}
]

# Package Data SOLAR F1 - F10
PACKAGES = [
    {
        "id": "F1",
        "name": "SOLAR F1",
        "desc": "Phù hợp hộ gia đình nhỏ, hóa đơn dưới 500k",
        "kwp": 2.3,
        "panels": 4,
        "storage": "2.5 kWh (BSB)",
        "inverter": "Luxpower SNA 5kW",
        "price": 47800000,
        "daily_min": 6,
        "daily_max": 10
    },
    {
        "id": "F2",
        "name": "SOLAR F2",
        "desc": "Phù hợp hộ gia đình trung bình khá, hóa đơn dưới 1 triệu",
        "kwp": 4.6,
        "panels": 8,
        "storage": "5 kWh (BSB)",
        "inverter": "Luxpower SNA 5kW",
        "price": 68500000,
        "daily_min": 10,
        "daily_max": 18
    },
    {
        "id": "F3",
        "name": "SOLAR F3",
        "desc": "Phù hợp hóa đơn từ 1.0 đến 1.5 triệu",
        "kwp": 5.8,
        "panels": 10,
        "storage": "10 kWh (LS Battery)",
        "inverter": "SVE 6kW",
        "price": 88000000,
        "daily_min": 15,
        "daily_max": 28
    },
    {
        "id": "F4",
        "name": "SOLAR F4",
        "desc": "Phù hợp hóa đơn từ 1.5 đến 2.0 triệu",
        "kwp": 6.9,
        "panels": 12,
        "storage": "16 kWh (EJOR)",
        "inverter": "SVE 6kW",
        "price": 104700000,
        "daily_min": 20,
        "daily_max": 30
    },
    {
        "id": "F5",
        "name": "SOLAR F5",
        "desc": "Phù hợp hóa đơn từ 2.0 đến 2.5 triệu",
        "kwp": 8.1,
        "panels": 14,
        "storage": "16 kWh (EJOR/LS)",
        "inverter": "Luxpower PRO 6.5kW",
        "price": 114900000,
        "daily_min": 20,
        "daily_max": 34
    },
    {
        "id": "F6",
        "name": "SOLAR F6",
        "desc": "Hệ cao cấp, nâng cấp số lượng tấm pin",
        "kwp": 8.1,
        "panels": 16,
        "storage": "16 kWh (EJOR/LS)",
        "inverter": "Luxpower 6.5 PRO",
        "price": 123600000,
        "daily_min": 25,
        "daily_max": 40
    },
    {
        "id": "F7",
        "name": "SOLAR F7",
        "desc": "Hệ cao cấp công suất lớn, lưu trữ khủng",
        "kwp": 11.4,
        "panels": 20,
        "storage": "32 kWh (EJOR/LS)",
        "inverter": "Luxpower 6.5 PRO (x2)",
        "price": 203000000,
        "daily_min": 35,
        "daily_max": 50
    },
    {
        "id": "F8",
        "name": "SOLAR F8",
        "desc": "Hệ cao cấp cho hộ biệt thự/kinh doanh lớn (4.0 - 5.0 triệu)",
        "kwp": 13.9,
        "panels": 24,
        "storage": "32 kWh (EJOR/LS)",
        "inverter": "Luxpower 6.5 PRO (x2)",
        "price": 217900000,
        "daily_min": 40,
        "daily_max": 60
    },
    {
        "id": "F9",
        "name": "SOLAR F9",
        "desc": "Hệ siêu khủng cho biệt thự, nhà xưởng vừa",
        "kwp": 17.4,
        "panels": 30,
        "storage": "32 kWh (EJOR/LS)",
        "inverter": "Luxpower 6.5 PRO (x2)",
        "price": 239000000,
        "daily_min": 50,
        "daily_max": 70
    },
    {
        "id": "F10",
        "name": "SOLAR F10",
        "desc": "Hệ đặc biệt công suất lớn nhất (7.0 - 10.0 triệu)",
        "kwp": 22.0,
        "panels": 38,
        "storage": "48 kWh (EJOR/LS)",
        "inverter": "Luxpower 6.5 PRO (x3)",
        "price": 329300000,
        "daily_min": 60,
        "daily_max": 90
    }
]

# Helper function to calculate consumed kWh from bill (2026 tariff)
def calculate_kwh_from_bill(bill_amount, vat_rate):
    # Pre-VAT amount
    pre_vat_bill = bill_amount / (1 + vat_rate / 100)
    
    remaining = pre_vat_bill
    kwh = 0
    
    # Track through the 6 step tariff
    for step in BILL_STEPS_2026:
        step_limit = step["limit"]
        step_price = step["price"]
        
        # Max money for this step
        if step_limit == float('inf'):
            # Bậc 6
            step_kwh = remaining / step_price
            kwh += step_kwh
            break
        else:
            max_step_cost = step_limit * step_price
            if remaining > max_step_cost:
                # Fill this step completely
                kwh += step_limit
                remaining -= max_step_cost
            else:
                # Partially fill this step
                kwh += remaining / step_price
                break
                
    return round(kwh, 2)

# Helper function to calculate monthly bill for a given kWh
def calculate_bill_from_kwh(kwh, vat_rate):
    pre_vat = 0
    remaining = kwh
    
    for step in BILL_STEPS_2026:
        step_limit = step["limit"]
        step_price = step["price"]
        
        if step_limit == float('inf') or remaining <= step_limit:
            pre_vat += remaining * step_price
            break
            
        pre_vat += step_limit * step_price
        remaining -= step_limit
        
    return round(pre_vat * (1 + vat_rate / 100), 2)

# Header
st.markdown("""
    <div class="brand-header">
        <h1>SOLAR 24H</h1>
        <p>Năng Lượng Sạch - Nâng Tầm Cuộc Sống</p>
    </div>
""", unsafe_allow_html=True)

# Tabs
tab_tuvandongtien, tab_thongsogoi, tab_shinhan_bank = st.tabs([
    "📋 TƯ VẤN KHÁCH HÀNG",
    "📦 CHI TIẾT GÓI HYBRID",
    "🏦 TRẢ GÓP SHINHAN BANK"
])

# SIDEBAR FOR CONSTANTS AND INFO
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: #0F3057;'>🤖 TRỢ LÝ SOLAR GIRL</h3>
            <p style='font-size: 0.9rem; font-style: italic; color: #666;'>Tư vấn năng lượng tận tâm 24/7</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **Thông số tính toán tại Miền Tây:**
    * **Giờ nắng trung bình:** 4.3 giờ nắng đỉnh/ngày
    * **Hiệu suất hệ thống:** 82% (Khấu hao thực tế)
    * **Lãi suất Shinhan Bank:** 0.59% / tháng (Lãi phẳng cố định)
    * **CCCD gắn chip + Hóa đơn điện** là duyệt vay ngay!
    """)
    
    st.markdown("---")
    st.markdown("📞 **Hotline:** 0909.363.579 - 0896.488.299")
    st.markdown("🏢 **Địa chỉ:** Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh, Mỹ Tho, Tiền Giang")

# TAB 1: TƯ VẤN KHÁCH HÀNG & ROI
with tab_tuvandongtien:
    st.subheader("💡 Phân Tích Dòng Tiền & Đề Xuất Giải Pháp")
    
    col_input_1, col_input_2 = st.columns(2)
    with col_input_1:
        bill_input = st.number_input("Nhập số tiền điện hàng tháng của khách (VNĐ):", min_value=100000, max_value=50000000, value=3000000, step=100000)
    with col_input_2:
        vat_select = st.selectbox("Thuế VAT áp dụng trên hóa đơn:", [10, 8], index=0)
        
    # Process inputs
    kwh_consumed = calculate_kwh_from_bill(bill_input, vat_select)
    daily_kwh = round(kwh_consumed / 30, 2)
    
    col_metric_1, col_metric_2 = st.columns(2)
    with col_metric_1:
        st.markdown(f"""
            <div class="card">
                <div class="metric-label">LƯỢNG ĐIỆN TIÊU THỤ THỰC TẾ</div>
                <div class="metric-value">{kwh_consumed:,.2f} kWh <span style='font-size: 1rem;'>/ tháng</span></div>
                <div style='font-size: 0.9rem; color:#666;'>Trung bình khoảng {daily_kwh} kWh (số điện) mỗi ngày</div>
            </div>
        """, unsafe_allow_html=True)
        
    # Auto-recommend package based on bill
    recommended_pkg = None
    for pkg in PACKAGES:
        # Expected monthly production
        pkg_monthly_prod = pkg["kwp"] * 4.3 * 30 * 0.82
        # We recommend the package that covers >= 85% of consumption
        if pkg_monthly_prod >= (kwh_consumed * 0.85):
            recommended_pkg = pkg
            break
            
    if not recommended_pkg:
        recommended_pkg = PACKAGES[-1] # Fallback to F10 if huge
        
    with col_metric_2:
        st.markdown(f"""
            <div class="highlight-card">
                <div class="metric-label">🌟 GÓI ĐỀ XUẤT TỐI ƯU</div>
                <div class="metric-value" style="color: #0F3057;">{recommended_pkg['name']}</div>
                <div style='font-weight: bold; color: #B8860B;'>Công suất: {recommended_pkg['kwp']} kWp · Trọn gói: {recommended_pkg['price']:,.0f}đ</div>
                <div style='font-size: 0.9rem; color:#555;'>{recommended_pkg['desc']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("💵 Phân Tích Hiệu Quả Đầu Tư (ROI) & Dự Kiến Phương Án Trả Góp")
    
    # Calculate performance for the recommended package
    kwp = recommended_pkg["kwp"]
    package_price = recommended_pkg["price"]
    
    # Production
    prod_daily = kwp * 4.3 * 0.82
    prod_monthly = prod_daily * 30
    
    # Saving analysis
    # Assuming solar covers up to 90% of household needs (or up to consumption limit)
    solar_utilized_kwh = min(kwh_consumed, prod_monthly)
    remaining_grid_kwh = max(0.0, kwh_consumed - solar_utilized_kwh)
    
    grid_bill_old = bill_input
    grid_bill_new = calculate_bill_from_kwh(remaining_grid_kwh, vat_select)
    monthly_saving = max(0.0, grid_bill_old - grid_bill_new)
    annual_saving = monthly_saving * 12
    
    payback_years = package_price / annual_saving if annual_saving > 0 else 0
    
    col_roi_1, col_roi_2, col_roi_3 = st.columns(3)
    with col_roi_1:
        st.markdown(f"""
            <div class="card">
                <div class="metric-label">HÓA ĐƠN ĐIỆN MỚI DỰ KIẾN</div>
                <div class="metric-value">{grid_bill_new:,.0f} đ</div>
                <div style='font-size: 0.9rem; color:green; font-weight: bold;'>Tiết kiệm {monthly_saving:,.0f} đ / tháng</div>
            </div>
        """, unsafe_allow_html=True)
    with col_roi_2:
        st.markdown(f"""
            <div class="card">
                <div class="metric-label">TIẾT KIỆM HÀNG NĂM</div>
                <div class="metric-value">{annual_saving:,.0f} đ</div>
                <div style='font-size: 0.9rem; color:#666;'>Tận hưởng điện xanh 20 - 30 năm tới</div>
            </div>
        """, unsafe_allow_html=True)
    with col_roi_3:
        st.markdown(f"""
            <div class="highlight-card">
                <div class="metric-label">THỜI GIAN HÒA VỐN (ROI)</div>
                <div class="metric-value" style="color: #0F3057;">{payback_years:.1f} Năm</div>
                <div style='font-size: 0.9rem; color:#555;'>Bảo hành thiết bị lên tới 15-30 năm</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 🏦 Phương Án Trả Góp Trắng 100% Qua Shinhan Bank (Không Phí Đối Ứng)")
    
    # Loan logic
    loan_limit = 100000000.0
    loan_amount = min(package_price, loan_limit)
    counter_payment = max(0.0, package_price - loan_amount)
    
    if counter_payment == 0:
        st.success(f"🎉 Gói {recommended_pkg['name']} có giá trị {package_price:,.0f}đ dưới 100 triệu, khách hàng được **VAY 100% không cần trả trước (0 đồng đối ứng)**!")
    else:
        st.warning(f"⚠️ Do gói có giá trị lớn hơn hạn mức của Shinhan Bank (100 triệu), khách hàng cần thanh toán phí đối ứng chênh lệch ban đầu là: **{counter_payment:,.0f}đ**.")
        
    # Table for loan periods
    periods = [12, 24, 36, 48]
    interest_rate_flat = 0.59 / 100
    
    repayment_data = []
    for m in periods:
        monthly_principal = loan_amount / m
        monthly_interest = loan_amount * interest_rate_flat
        total_monthly_installment = monthly_principal + monthly_interest
        total_repayment = total_monthly_installment * m
        total_interest = monthly_interest * m
        net_cashflow = monthly_saving - total_monthly_installment
        
        repayment_data.append({
            "Kỳ hạn": f"{m} Tháng",
            "Khoản vay": f"{loan_amount:,.0f}đ",
            "Tiền gốc/tháng": f"{monthly_principal:,.0f}đ",
            "Tiền lãi/tháng": f"{monthly_interest:,.0f}đ",
            "Tổng Góp/tháng": f"{total_monthly_installment:,.0f}đ",
            "Dòng tiền thực tế": f"+{net_cashflow:,.0f}đ (Dư dả)" if net_cashflow >= 0 else f"-{abs(net_cashflow):,.0f}đ (Bù thêm)",
            "Tổng lãi trả ngân hàng": f"{total_interest:,.0f}đ"
        })
        
    st.table(pd.DataFrame(repayment_data))
    
    st.markdown("""
    💡 **Lời khuyên cho Sales tư vấn:** 
    * Đối với hộ gia đình nhỏ chọn gói **SOLAR F2 (68.5 triệu)**, vay trắng 100% kỳ hạn **48 tháng** chỉ cần góp **1.83 triệu/tháng** (bù thêm tầm 600-800k so với tiền điện cũ). Khách hàng cực kỳ dễ chốt!
    * Sử dụng bài toán so sánh dòng tiền trên để khách thấy số tiền thực tế bù thêm hàng tháng chỉ bằng vài ly cafe, nhưng đổi lại sở hữu vĩnh viễn hệ thống cao cấp dùng vài chục năm!
    """)

# TAB 2: PACAKGES DIRECTORY
with tab_thongsogoi:
    st.subheader("📦 Tra Cứu Thông Số Vật Tư Các Gói Hybrid Solar 24h")
    
    package_list = []
    for pkg in PACKAGES:
        prod_monthly = pkg["kwp"] * 4.3 * 30 * 0.82
        package_list.append({
            "Gói": pkg["name"],
            "Công suất (kWp)": pkg["kwp"],
            "Số tấm pin 580W": f"{pkg['panels']} Tấm",
            "Diện tích mái cần": f"{pkg['panels'] * 5.5:.1f} m²",
            "Bộ Pin lưu trữ": pkg["storage"],
            "Biến tần Inverter": pkg["inverter"],
            "Sản lượng ngày (kWh)": f"{pkg['daily_min']} - {pkg['daily_max']}",
            "Sản lượng tháng (kWh)": f"{prod_monthly:.0f}",
            "Đơn giá trọn gói": f"{pkg['price']:,.0f}đ"
        })
        
    st.dataframe(pd.DataFrame(package_list), use_container_width=True)
    
    st.markdown("---")
    st.subheader("📐 Công Cụ Tự Tính Sản Lượng Cho Diện Tích Mái Tùy Chỉnh")
    
    col_calc_1, col_calc_2 = st.columns(2)
    with col_calc_1:
        custom_kwp = st.number_input("Nhập công suất pin mong muốn lắp đặt (kWp):", min_value=1.0, max_value=200.0, value=5.0, step=0.5)
        solar_hours = st.slider("Số giờ nắng đỉnh trung bình ngày:", min_value=3.5, max_value=5.5, value=4.3, step=0.1)
        system_efficiency = st.slider("Hệ số hiệu suất hệ thống (%):", min_value=70, max_value=90, value=82, step=1) / 100.0
    with col_calc_2:
        calc_daily = custom_kwp * solar_hours * system_efficiency
        calc_monthly = calc_daily * 30
        required_area = custom_kwp * 5.5
        
        st.markdown(f"""
            <div class="highlight-card">
                <h4 style="margin: 0 0 10px 0; color: {PRIMARY_COLOR};">KẾT QUẢ TÍNH SẢN LƯỢNG</h4>
                <p>⚡ <b>Sản lượng dự kiến ngày:</b> {calc_daily:.2f} kWh (số điện)</p>
                <p>⚡ <b>Sản lượng dự kiến tháng:</b> {calc_monthly:.2f} kWh (số điện)</p>
                <p>🏠 <b>Diện tích mái tối thiểu:</b> {required_area:.1f} - {custom_kwp * 6.0:.1f} m²</p>
                <p>☘️ <b>Giảm phát thải CO2:</b> {calc_monthly * 0.8 * 12 / 1000:.2f} Tấn CO2/Năm</p>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: TRẢ GÓP SHINHAN BANK
with tab_shinhan_bank:
    st.subheader("🏦 Bảng Tính Khoản Vay Trả Góp Shinhan Bank")
    st.write("Tra cứu nhanh số tiền trả góp hàng tháng cho mọi hạn mức vay và kỳ hạn (Lãi suất cố định phẳng 0.59%/tháng).")
    
    loan_amount_input = st.number_input("Nhập số tiền khách hàng muốn vay (Hạn mức 10M - 100M):", min_value=10000000, max_value=100000000, value=60000000, step=5000000)
    
    periods_table = [12, 24, 36, 48]
    bank_data = []
    
    for m in periods_table:
        goc = loan_amount_input / m
        lai = loan_amount_input * 0.59 / 100
        tong = goc + lai
        
        bank_data.append({
            "Kỳ hạn trả góp": f"{m} Tháng",
            "Tiền Gốc / Tháng": f"{goc:,.0f}đ",
            "Tiền Lãi / Tháng": f"{lai:,.0f}đ",
            "Tổng Góp / Tháng (Cả Gốc + Lãi)": f"{tong:,.0f}đ",
            "Tổng Số Tiền Lãi Phải Trả": f"{lai * m:,.0f}đ",
            "Tổng Gốc + Lãi Phải Trả": f"{tong * m:,.0f}đ"
        })
        
    st.table(pd.DataFrame(bank_data))
    
    st.markdown("""
    💡 **Quy trình chuẩn bị hồ sơ vay cực nhanh:**
    1. **CCCD gắn chip** của người đứng tên hóa đơn điện.
    2. **Hóa đơn tiền điện sinh hoạt** của 3 tháng gần nhất để ngân hàng thẩm định khả năng chi trả.
    *Không yêu cầu chứng minh thu nhập phức tạp, giải ngân thần tốc trong vòng 24h - 48h làm việc!*
    """)

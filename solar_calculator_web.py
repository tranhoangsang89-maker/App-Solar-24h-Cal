import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán Năng Lượng",
    page_icon="☀️",
    layout="wide"
)

# Custom Styling to match Solar 24h branding (Navy Blue #1A365D and Gold #D4AF37)
st.markdown("""
<style>
    .title-container {
        background-color: #1A365D;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align: center;
        border-bottom: 5px solid #D4AF37;
    }
    .main-title {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: bold;
        margin: 0;
    }
    .sub-title {
        color: #D4AF37 !important;
        font-size: 1.1rem;
        margin-top: 5px;
        margin-bottom: 0;
    }
    .section-header {
        color: #1A365D;
        border-left: 5px solid #D4AF37;
        padding-left: 12px;
        font-size: 1.4rem;
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .highlight-card {
        background-color: #FFF9E6;
        border-left: 5px solid #D4AF37;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #F0F4F8;
        border-left: 5px solid #1A365D;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Logo & Header Header Section
st.markdown("""
<div class="title-container">
    <h1 class="main-title">☀️ SOLAR 24H</h1>
    <p class="sub-title">Công Cụ Tính Toán Năng Lượng & Tư Vấn Trả Góp Shinhan Bank</p>
</div>
""", unsafe_allow_html=True)

# Packages specifications according to company manuals
packages = [
    {
        "id": "SOLAR F1",
        "name": "SOLAR F1 (2.3 kWp)",
        "kwp": 2.32,
        "plates": 4,
        "storage": "2.5 kWh",
        "inverter": "Inverter LUXPOWER SNA 5kW",
        "price": 47800000,
        "min_bill": 0,
        "max_bill": 500000,
        "desc": "Phù hợp hộ gia đình nhỏ có hóa đơn dưới 500k/tháng"
    },
    {
        "id": "SOLAR F2",
        "name": "SOLAR F2 (4.6 kWp)",
        "kwp": 4.64,
        "plates": 8,
        "storage": "5 kWh",
        "inverter": "Inverter LUXPOWER SNA 5kW",
        "price": 68500000,
        "min_bill": 500000,
        "max_bill": 1000000,
        "desc": "Phù hợp hộ gia đình nhỏ/trung bình, điện dưới 1 triệu/tháng"
    },
    {
        "id": "SOLAR F3",
        "name": "SOLAR F3 (5.8 kWp)",
        "kwp": 5.8,
        "plates": 10,
        "storage": "10 kWh (LS Battery)",
        "inverter": "Inverter SVE 6kW",
        "price": 88000000,
        "min_bill": 1000000,
        "max_bill": 1500000,
        "desc": "Phù hợp hóa đơn từ 1.0 đến 1.5 triệu"
    },
    {
        "id": "SOLAR F4",
        "name": "SOLAR F4 (6.9 kWp)",
        "kwp": 6.96,
        "plates": 12,
        "storage": "16 kWh (EJOR)",
        "inverter": "Inverter SVE 6kW",
        "price": 104700000,
        "min_bill": 1500000,
        "max_bill": 2000000,
        "desc": "Phù hợp hóa đơn từ 1.5 đến 2.0 triệu"
    },
    {
        "id": "SOLAR F5",
        "name": "SOLAR F5 (8.1 kWp)",
        "kwp": 8.12,
        "plates": 14,
        "storage": "16 kWh (EJOR/LS)",
        "inverter": "Inverter LUXPOWER PRO 6.5kW",
        "price": 114900000,
        "min_bill": 2000000,
        "max_bill": 2500000,
        "desc": "Phù hợp hóa đơn từ 2.0 đến 2.5 triệu"
    },
    {
        "id": "SOLAR F6",
        "name": "SOLAR F6 (9.3 kWp)",
        "kwp": 9.28,
        "plates": 16,
        "storage": "16 kWh (EJOR/LS)",
        "inverter": "Inverter LUXPOWER 6.5 PRO",
        "price": 123600000,
        "min_bill": 2500000,
        "max_bill": 3000000,
        "desc": "Phù hợp hóa đơn từ 2.5 đến 3.0 triệu"
    },
    {
        "id": "SOLAR F7",
        "name": "SOLAR F7 (11.6 kWp)",
        "kwp": 11.6,
        "plates": 20,
        "storage": "32 kWh (EJOR/LS x2)",
        "inverter": "Inverter LUXPOWER 6.5 PRO (x2)",
        "price": 203000000,
        "min_bill": 3000000,
        "max_bill": 4000000,
        "desc": "Phù hợp hóa đơn từ 3.0 đến 4.0 triệu"
    },
    {
        "id": "SOLAR F8",
        "name": "SOLAR F8 (13.9 kWp)",
        "kwp": 13.92,
        "plates": 24,
        "storage": "32 kWh (EJOR/LS)",
        "inverter": "Inverter LUXPOWER 6.5 PRO (x2)",
        "price": 217900000,
        "min_bill": 4000000,
        "max_bill": 5000000,
        "desc": "Phù hợp hóa đơn từ 4.0 đến 5.0 triệu"
    },
    {
        "id": "SOLAR F9",
        "name": "SOLAR F9 (17.4 kWp)",
        "kwp": 17.4,
        "plates": 30,
        "storage": "32 kWh",
        "inverter": "Inverter LUXPOWER 6.5 PRO (x2)",
        "price": 239000000,
        "min_bill": 5000000,
        "max_bill": 7000000,
        "desc": "Phù hợp hóa đơn từ 5.0 đến 7.0 triệu"
    },
    {
        "id": "SOLAR F10",
        "name": "SOLAR F10 (22.0 kWp)",
        "kwp": 22.04,
        "plates": 38,
        "storage": "48 kWh",
        "inverter": "Inverter LUXPOWER 6.5 PRO (x3)",
        "price": 329300000,
        "min_bill": 7000000,
        "max_bill": 10000000,
        "desc": "Phù hợp hóa đơn từ 7.0 đến 10.0 triệu"
    }
]

def calculate_kwh_from_bill(bill_amount, vat_rate):
    """
    Tính ngược số kWh từ tiền hóa đơn sinh hoạt đã gồm VAT dựa trên biểu giá lũy tiến 6 bậc mới nhất 2026.
    """
    vat_multiplier = 1 + (vat_rate / 100.0)
    pre_vat_bill = bill_amount / vat_multiplier
    
    steps = [
        (50, 1984),
        (50, 2050),
        (100, 2380),
        (100, 2998),
        (100, 3350),
        (float('inf'), 3460)
    ]
    
    kwh = 0.0
    remaining_money = pre_vat_bill
    for limit, price in steps:
        if remaining_money <= 0:
            break
        max_step_cost = limit * price
        if remaining_money > max_step_cost:
            kwh += limit
            remaining_money -= max_step_cost
        else:
            kwh += remaining_money / price
            remaining_money = 0.0
            break
    return kwh

def calculate_bill_from_kwh(kwh, vat_rate):
    """
    Tính tiền điện sinh hoạt từ số kWh dựa trên biểu giá lũy tiến 6 bậc mới nhất 2026.
    """
    if kwh <= 0:
        return 0.0
    
    steps = [
        (50, 1984),
        (50, 2050),
        (100, 2380),
        (100, 2998),
        (100, 3350),
        (float('inf'), 3460)
    ]
    
    pre_vat_bill = 0.0
    remaining_kwh = kwh
    for limit, price in steps:
        if remaining_kwh <= 0:
            break
        consumed = min(remaining_kwh, limit)
        pre_vat_bill += consumed * price
        remaining_kwh -= consumed
        
    vat_multiplier = 1 + (vat_rate / 100.0)
    return pre_vat_bill * vat_multiplier

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Chi Tiết Gói Lắp Đặt", "🏦 Trả Góp Shinhan Bank"])

with tab1:
    st.markdown('<div class="section-header">Nhập Thông Tin Tiêu Thụ Điện</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        bill_input = st.number_input(
            "Nhập số tiền điện hàng tháng của khách (VNĐ):",
            min_value=10000,
            value=2700000,
            step=50000,
            format="%d"
        )
    with col2:
        vat_input = st.selectbox(
            "Thuế VAT áp dụng trên hóa đơn (%):",
            options=[8, 10],
            index=0
        )
        
    # Process consumption
    kwh_monthly = calculate_kwh_from_bill(bill_input, vat_input)
    kwh_daily = kwh_monthly / 30.0
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💡 LƯỢNG ĐIỆN TIÊU THỤ THỰC TẾ</h4>
            <h2 style='color: #1A365D; margin: 0;'>{kwh_monthly:,.2f} kWh / tháng</h2>
            <p style='margin: 0; color: #555555;'>Trung bình khoảng <b>{kwh_daily:,.2f} kWh</b> (số điện) mỗi ngày.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # --- SMART PACKAGE MATCHING LOGIC ---
    # We select package based on either direct bill range matching (the official standard of the company)
    # OR we make sure production covers >= 95% of consumption so customer does not pay extra to EVN & bank.
    recommended_package = None
    for pkg in packages:
        if pkg["min_bill"] <= bill_input <= pkg["max_bill"]:
            recommended_package = pkg
            break
            
    # Fallback/Safety Check: Ensure the recommended package produces enough or nearly enough electricity to be realistic
    # Let's check production coverage of the direct range match
    if recommended_package:
        prod_monthly = recommended_package["kwp"] * 4.3 * 30 * 0.82
        # If the range matched package produces less than 85% of consumption (e.g. because of the new expensive tariffs of 2026),
        # we upgrade to the next package so the customer has a realistic ROI and positive cashflow!
        if prod_monthly < kwh_monthly * 0.85:
            current_idx = packages.index(recommended_package)
            if current_idx < len(packages) - 1:
                recommended_package = packages[current_idx + 1]
    else:
        # If out of range, default to F10
        recommended_package = packages[-1]

    with col_b:
        st.markdown(f"""
        <div class="highlight-card">
            <h4>🌟 GÓI ĐỀ XUẤT TỐI ƯU</h4>
            <h2 style='color: #D4AF37; margin: 0;'>{recommended_package["id"]}</h2>
            <p style='margin: 0; font-size: 1.1rem; font-weight: bold; color: #1A365D;'>{recommended_package["name"]}</p>
            <p style='margin: 3px 0 0 0;'>Giá Trọn Gói: <b>{recommended_package["price"]:,.0f} VNĐ</b></p>
            <p style='margin: 0; color: #666;'>{recommended_package["desc"]}</p>
        </div>
        """, unsafe_allow_html=True)

    # Calculate ROI & Post-Solar Bill
    prod_monthly = recommended_package["kwp"] * 4.3 * 30 * 0.82
    remaining_kwh = max(0.0, kwh_monthly - prod_monthly)
    new_bill = calculate_bill_from_kwh(remaining_kwh, vat_input)
    monthly_savings = max(0.0, bill_input - new_bill)
    yearly_savings = monthly_savings * 12.0
    
    # ROI calculation
    roi_years = recommended_package["price"] / yearly_savings if yearly_savings > 0 else 0
    
    st.markdown('<div class="section-header">💵 Phân Tích Hiệu Quả Đầu Tư (ROI) & Dự Kiến Phương Án Trả Góp</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-card" style='text-align: center;'>
            <p style='margin: 0; color: #555; font-weight: 600;'>HÓA ĐƠN ĐIỆN MỚI DỰ KIẾN</p>
            <h2 style='color: #E53E3E; margin: 5px 0;'>{new_bill:,.0f} đ</h2>
            <p style='margin: 0; color: #38A169; font-weight: bold;'>Tiết kiệm: {monthly_savings:,.0f} đ / tháng</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="metric-card" style='text-align: center;'>
            <p style='margin: 0; color: #555; font-weight: 600;'>TIẾT KIỆM HÀNG NĂM</p>
            <h2 style='color: #38A169; margin: 5px 0;'>{yearly_savings:,.0f} đ</h2>
            <p style='margin: 0; color: #666;'>Tận hưởng điện xanh 20 - 30 năm tới</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="highlight-card" style='text-align: center;'>
            <p style='margin: 0; color: #555; font-weight: 600;'>THỜI GIAN HÒA VỐN (ROI)</p>
            <h2 style='color: #D4AF37; margin: 5px 0;'>{roi_years:.1f} Năm</h2>
            <p style='margin: 0; color: #666;'>Bảo hành thiết bị lên tới 15 - 30 năm</p>
        </div>
        """, unsafe_allow_html=True)

    # Shinhan Bank Installation Calculator
    st.markdown('<div class="section-header">🏦 Phương Án Trả Góp Trắng 100% Qua Shinhan Bank (0đ Trả Trước)</div>', unsafe_allow_html=True)
    
    max_loan = 100000000.0  # Limit is 100M VND
    total_price = recommended_package["price"]
    
    # Calculate loan and downpayment
    if total_price <= max_loan:
        loan_amount = total_price
        downpayment = 0.0
    else:
        loan_amount = max_loan
        downpayment = total_price - max_loan
        
    if downpayment > 0:
        st.warning(f"⚠️ Do gói có giá trị lớn hơn hạn mức của Shinhan Bank (100 triệu), khách hàng cần thanh toán phí đối ứng chênh lệch ban đầu là: **{downpayment:,.0f}đ**.")
    else:
        st.info("🎉 Gói nằm trong hạn mức vay 100 triệu của Shinhan Bank! Khách hàng có thể áp dụng gói trả góp **0 đồng trả trước - vay trắng 100%**.")

    # Generate Installment Table
    terms = [12, 24, 36, 48]
    interest_rate_flat = 0.59 / 100.0  # 0.59% flat rate per month
    
    installment_data = []
    for term in terms:
        principal_monthly = loan_amount / term
        interest_monthly = loan_amount * interest_rate_flat
        total_monthly = principal_monthly + interest_monthly
        cash_flow = monthly_savings - total_monthly
        total_interest = interest_monthly * term
        
        flow_str = f"+{cash_flow:,.0f}đ (Dư ra!)" if cash_flow >= 0 else f"-{abs(cash_flow):,.0f}đ (Bù thêm)"
        
        installment_data.append({
            "Kỳ hạn": f"{term} Tháng",
            "Khoản vay": f"{loan_amount:,.0f}đ",
            "Tiền gốc/tháng": f"{principal_monthly:,.0f}đ",
            "Tiền lãi/tháng": f"{interest_monthly:,.0f}đ",
            "Tổng Góp/tháng": f"{total_monthly:,.0f}đ",
            "Dòng tiền thực tế": flow_str,
            "Tổng lãi trả ngân hàng": f"{total_interest:,.0f}đ"
        })
        
    df_installments = pd.DataFrame(installment_data)
    st.table(df_installments)

with tab2:
    st.markdown('<div class="section-header">Tra Cứu Chi Tiết 10 Gói Giải Pháp Hybrid</div>', unsafe_allow_html=True)
    
    # Simple search or custom kWp calculation
    custom_kwp = st.number_input("Tính sản lượng cho số kWp tùy chỉnh:", min_value=1.0, max_value=100.0, value=5.0, step=0.5)
    custom_prod_daily = custom_kwp * 4.3 * 0.82
    custom_prod_monthly = custom_prod_daily * 30
    
    st.markdown(f"👉 Hệ thống **{custom_kwp:.2f} kWp** dự kiến tạo ra khoảng **{custom_prod_daily:.2f} kWh/ngày** (Trung bình **{custom_prod_monthly:.2f} kWh/tháng** trong điều kiện thời tiết tốt).")
    
    # Create packages details table
    pkg_list = []
    for p in packages:
        pkg_prod = p["kwp"] * 4.3 * 30 * 0.82
        pkg_list.append({
            "Mã Gói": p["id"],
            "Công Suất (kWp)": f"{p['kwp']:.2f} kWp",
            "Số Tấm Pin (580W)": f"{p['plates']} Tấm",
            "Pin Lưu Trữ": p["storage"],
            "Biến Tần Inverter": p["inverter"],
            "Sản Lượng (kWh/tháng)": f"~{pkg_prod:,.0f} kWh",
            "Giá Trọn Gói": f"{p['price']:,.0f}đ"
        })
    df_packages = pd.DataFrame(pkg_list)
    st.dataframe(df_packages, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">Chính Sách & Thủ Tục Vay Trả Góp Shinhan Bank</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 🌟 Lợi Thế Vượt Trội Của Shinhan Bank so với Tài Chính Tiêu Dùng:
    * **Lãi suất phẳng cố định siêu thấp:** Chỉ **0.59%/tháng** (so với mức 2.8% - 3% của tài chính tiêu dùng).
    * **Tiết kiệm tối đa chi phí lãi vay:** Giúp khách hàng giảm tới **80 triệu tiền lãi** (cho khoản vay 100M trong 3 năm) so với gói vay cũ.
    * **Hỗ trợ thời gian trả góp linh hoạt:** Từ 12, 24, 36 cho đến 48 tháng.
    
    ### 📋 Thủ Tục Đơn Giản & Xét Duyệt Nhanh Chóng:
    * Khách hàng **không cần chứng minh thu nhập** phức tạp.
    * Hồ sơ chỉ cần cung cấp:
      1. **Căn cước công dân (CCCD) có gắn chip** hợp lệ.
      2. **Hóa đơn tiền điện sinh hoạt** 1-3 tháng gần nhất tại địa điểm lắp đặt.
    """)

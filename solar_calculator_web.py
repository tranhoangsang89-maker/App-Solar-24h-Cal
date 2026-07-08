import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán Điện Mặt Trời",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling with brand colors (Navy #0A3370 and Gold #FFC20E)
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }
    .stApp {
        color: #1e293b;
    }
    .brand-title {
        color: #0A3370;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2px;
        font-size: 2.5rem;
    }
    .brand-subtitle {
        color: #FFC20E;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 600;
        text-align: center;
        margin-bottom: 25px;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    .greeting-card {
        background: linear-gradient(135deg, #0A3370 0%, #1e40af 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border-left: 5px solid #0A3370;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0A3370;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
    }
    .highlight-gold {
        color: #FFC20E;
        font-weight: bold;
    }
    .package-box {
        background-color: #f0fdf4;
        border: 2px solid #22c55e;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .package-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #15803d;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Define packages and specifications
packages = {
    "SOLAR F1": {
        "kwp": 2.3,
        "pin_count": 4,
        "storage": "2.5 kWh BSB",
        "inverter": "LUXPOWER SNA 5kW",
        "price": 47800000,
        "min_bill": 0,
        "max_bill": 500000,
        "desc": "Phù hợp cho gia đình nhỏ có hóa đơn điện dưới 500.000đ/tháng"
    },
    "SOLAR F2": {
        "kwp": 4.6,
        "pin_count": 8,
        "storage": "5 kWh BSB",
        "inverter": "LUXPOWER SNA 5kW",
        "price": 68500000,
        "min_bill": 500001,
        "max_bill": 1000000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 500.000đ đến 1.000.000đ/tháng"
    },
    "SOLAR F3": {
        "kwp": 5.8,
        "pin_count": 10,
        "storage": "10 kWh LS",
        "inverter": "SVE 6kW",
        "price": 88000000,
        "min_bill": 1000001,
        "max_bill": 1500000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 1.000.000đ đến 1.500.000đ/tháng"
    },
    "SOLAR F4": {
        "kwp": 6.9,
        "pin_count": 12,
        "storage": "16 kWh EJOR",
        "inverter": "SVE 6kW",
        "price": 104700000,
        "min_bill": 1500001,
        "max_bill": 2000000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 1.500.000đ đến 2.000.000đ/tháng"
    },
    "SOLAR F5": {
        "kwp": 8.1,
        "pin_count": 14,
        "storage": "16 kWh EJOR/LS",
        "inverter": "LUXPOWER PRO 6.5kW",
        "price": 114900000,
        "min_bill": 2000001,
        "max_bill": 2500000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 2.000.000đ đến 2.500.000đ/tháng"
    },
    "SOLAR F6": {
        "kwp": 9.3,
        "pin_count": 16,
        "storage": "16 kWh EJOR/LS",
        "inverter": "LUXPOWER 6.5 PRO",
        "price": 123600000,
        "min_bill": 2500001,
        "max_bill": 3000000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 2.500.000đ đến 3.000.000đ/tháng"
    },
    "SOLAR F7": {
        "kwp": 11.4,
        "pin_count": 20,
        "storage": "32 kWh EJOR/LS",
        "inverter": "LUXPOWER 6.5 PRO (x2)",
        "price": 203000000,
        "min_bill": 3000001,
        "max_bill": 4000000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 3.000.000đ đến 4.000.000đ/tháng"
    },
    "SOLAR F8": {
        "kwp": 13.9,
        "pin_count": 24,
        "storage": "32 kWh EJOR/LS",
        "inverter": "LUXPOWER 6.5 PRO (x2)",
        "price": 217900000,
        "min_bill": 4000001,
        "max_bill": 5000000,
        "desc": "Phù hợp cho gia đình có hóa đơn điện từ 4.000.000đ đến 5.000.000đ/tháng"
    },
    "SOLAR F9": {
        "kwp": 17.4,
        "pin_count": 30,
        "storage": "32 kWh EJOR/LS",
        "inverter": "LUXPOWER 6.5 PRO (x2)",
        "price": 239000000,
        "min_bill": 5000001,
        "max_bill": 7000000,
        "desc": "Phù hợp cho biệt thự/hộ kinh doanh có hóa đơn điện từ 5.000.000đ đến 7.000.000đ/tháng"
    },
    "SOLAR F10": {
        "kwp": 22.0,
        "pin_count": 38,
        "storage": "48 kWh EJOR/LS",
        "inverter": "LUXPOWER 6.5 PRO (x3)",
        "price": 329300000,
        "min_bill": 7000001,
        "max_bill": 15000000,
        "desc": "Giải pháp toàn diện cho nhà xưởng/hộ kinh doanh lớn có hóa đơn điện từ 7.000.000đ đến 10.000.000đ/tháng"
    }
}

# 2026 Progressive Electricity Tariff
def calculate_kwh_from_bill(pre_tax_bill):
    # Progressive steps definition
    steps = [
        (50, 1984),
        (50, 2050),
        (100, 2380),
        (100, 2998),
        (100, 3350),
        (float('inf'), 3460)
    ]
    
    thresholds = [
        50 * 1984,
        50 * 1984 + 50 * 2050,
        50 * 1984 + 50 * 2050 + 100 * 2380,
        50 * 1984 + 50 * 2050 + 100 * 2380 + 100 * 2998,
        50 * 1984 + 50 * 2050 + 100 * 2380 + 100 * 2998 + 100 * 3350
    ]
    
    if pre_tax_bill <= thresholds[0]:
        return pre_tax_bill / steps[0][1]
    elif pre_tax_bill <= thresholds[1]:
        return 50 + (pre_tax_bill - thresholds[0]) / steps[1][1]
    elif pre_tax_bill <= thresholds[2]:
        return 100 + (pre_tax_bill - thresholds[1]) / steps[2][1]
    elif pre_tax_bill <= thresholds[3]:
        return 200 + (pre_tax_bill - thresholds[2]) / steps[3][1]
    elif pre_tax_bill <= thresholds[4]:
        return 300 + (pre_tax_bill - thresholds[3]) / steps[4][1]
    else:
        return 400 + (pre_tax_bill - thresholds[4]) / steps[5][1]

def calculate_bill_from_kwh(kwh, vat_rate):
    steps = [
        (50, 1984),
        (50, 2050),
        (100, 2380),
        (100, 2998),
        (100, 3350),
        (float('inf'), 3460)
    ]
    
    pre_tax_cost = 0
    remaining_kwh = kwh
    
    for limit, rate in steps:
        if remaining_kwh <= 0:
            break
        consumed = min(remaining_kwh, limit)
        pre_tax_cost += consumed * rate
        remaining_kwh -= consumed
        
    return pre_tax_cost * (1 + vat_rate / 100)

# Sidebar brand header
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color:#0A3370; margin-bottom:0px;'>SOLAR 24H</h2><small style='color:#64748b;'>NĂNG LƯỢNG SẠCH - NÂNG TẦM CUỘC SỐNG</small></div>", unsafe_allow_html=True)
    st.markdown("""
    **Thông Tin Liên Hệ:**
    - 🏢 **Địa chỉ:** Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh
    - ☎️ **Hotline:** 0909.363.579 - 0896.488.299
    - 📧 **Email:** Solar24h.tmdv@gmail.com
    """)
    st.image("https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?q=80&w=300&auto=format&fit=crop", use_container_width=True)

# Main layout header
st.markdown("<div class='brand-title'>SOLAR 24H</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-subtitle'>CÔNG CỤ HỖ TRỢ TƯ VẤN ĐIỆN MẶT TRỜI THÔNG MINH</div>", unsafe_allow_html=True)

# Interactive Welcome Message requested by user
st.markdown("""
<div class='greeting-card'>
    <h4>Solar Girl chào cả nhà! 👩‍💼</h4>
    <p style='margin-bottom:0px; font-size:1.05rem;'>
        Mọi người chỉ cần nhập hóa đơn và tùy chỉnh mức trả trước theo mong muốn. Hệ thống sẽ tự động tư vấn ạ!
    </p>
</div>
""", unsafe_allow_html=True)

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Chi Tiết Gói Lắp Đặt", "🏦 Gói Vay Shinhan Bank"])

# ================= TAB 1: TƯ VẤN KHÁCH HÀNG =================
with tab1:
    st.subheader("1. Nhập thông tin hóa đơn hiện tại")
    col1, col2 = st.columns(2)
    with col1:
        current_bill = st.number_input(
            "Số tiền điện hàng tháng của khách (VNĐ):",
            min_value=200000,
            max_value=30000000,
            value=2700000,
            step=100000,
            format="%d"
        )
    with col2:
        vat_rate = st.selectbox(
            "Thuế VAT áp dụng trên hóa đơn (%):",
            options=[10, 8, 0],
            index=1
        )
        
    pre_tax_bill = current_bill / (1 + vat_rate / 100)
    kwh_consumed = calculate_kwh_from_bill(pre_tax_bill)
    
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>LƯỢNG ĐIỆN TIÊU THỤ THỰC TẾ DỰA TRÊN BIỂU GIÁ 2026</div>
        <div class='metric-value'>{kwh_consumed:,.2f} kWh / tháng</div>
        <div style='color: #0A3370; font-weight:600; margin-top:5px;'>Trung bình khoảng {kwh_consumed/30:,.2f} kWh (số điện) mỗi ngày</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Identify the best package
    recommended_package_name = "SOLAR F1"
    for name, spec in packages.items():
        if spec["min_bill"] <= current_bill <= spec["max_bill"]:
            recommended_package_name = name
            break
    else:
        if current_bill > 15000000:
            recommended_package_name = "SOLAR F10"
            
    rec_spec = packages[recommended_package_name]
    
    st.subheader("2. Gói lắp đặt đề xuất & Tính toán tài chính")
    
    st.markdown(f"""
    <div class='package-box'>
        <div class='package-header'>🌟 GÓI ĐỀ XUẤT TỐI ƯU: {recommended_package_name}</div>
        <p><b>Công suất:</b> {rec_spec['kwp']} kWp | <b>Giá trọn gói:</b> {rec_spec['price']:,.0f}đ</p>
        <p><b>Cấu hình:</b> {rec_spec['pin_count']} tấm pin AE Solar 580W | Biến tần: {rec_spec['inverter']} | Lưu trữ: {rec_spec['storage']}</p>
        <p style='margin-bottom:0px; color:#166534;'><i>{rec_spec['desc']}</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Financial calculations
    solar_generation_monthly = rec_spec['kwp'] * 4.3 * 30 * 0.82
    new_kwh_consumed = max(0.0, kwh_consumed - solar_generation_monthly)
    new_bill = calculate_bill_from_kwh(new_kwh_consumed, vat_rate)
    monthly_saving = current_bill - new_bill
    annual_saving = monthly_saving * 12
    roi_years = rec_spec['price'] / annual_saving if annual_saving > 0 else 99
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>HÓA ĐƠN ĐIỆN MỚI DỰ KIẾN</div>
            <div class='metric-value'>{new_bill:,.0f} đ</div>
            <div style='color: #15803d; font-weight:600; margin-top:5px;'>Tiết kiệm {monthly_saving:,.0f} đ / tháng</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>TIẾT KIỆM HÀNG NĂM</div>
            <div class='metric-value'>{annual_saving:,.0f} đ</div>
            <div style='color: #0A3370; font-weight:600; margin-top:5px;'>Tận hưởng điện xanh 20 - 30 năm tới</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>THỜI GIAN HÒA VỐN (ROI)</div>
            <div class='metric-value'>{roi_years:,.1f} Năm</div>
            <div style='color: #0A3370; font-weight:600; margin-top:5px;'>Bảo hành thiết bị lên tới 15 - 30 năm</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Dynamic Prepayment and Loan Calculator
    st.subheader("3. Thiết lập phương án trả góp Shinhan Bank (Lãi phẳng 0.59%/tháng)")
    
    # Determine minimum prepayment required
    # Max loan from Shinhan is 100M
    max_loan_limit = 100000000
    min_prepay = max(0, rec_spec['price'] - max_loan_limit)
    
    prepay_col, loan_col = st.columns(2)
    with prepay_col:
        prepayment = st.number_input(
            "Tiền khách trả trước (VNĐ):",
            min_value=int(min_prepay),
            max_value=int(rec_spec['price']),
            value=int(min_prepay),
            step=1000000,
            format="%d"
        )
        if min_prepay > 0:
            st.info(f"⚠️ Do gói có giá trị lớn hơn hạn mức của Shinhan Bank (100 triệu), khách cần trả trước tối thiểu là {min_prepay:,.0f}đ.")
            
    with loan_col:
        actual_loan = rec_spec['price'] - prepayment
        st.markdown(f"""
        <div style='background-color:#eff6ff; padding:15px; border-radius:8px; border-left:5px solid #2563eb;'>
            <div style='font-size:0.85rem; color:#1e40af; font-weight:600;'>KHOẢN TIỀN CẦN VAY THỰC TẾ</div>
            <div style='font-size:1.6rem; font-weight:700; color:#1e40af;'>{actual_loan:,.0f} đ</div>
        </div>
        """, unsafe_allow_html=True)

    if actual_loan > 0:
        st.write("#### 📊 Bảng Tính Trả Góp Chi Tiết Cá Nhân Hóa:")
        
        durations = [12, 24, 36, 48]
        rows = []
        for dur in durations:
            principal_monthly = actual_loan / dur
            interest_monthly = actual_loan * 0.0059
            total_monthly = principal_monthly + interest_monthly
            net_cashflow = monthly_saving - total_monthly
            total_interest = interest_monthly * dur
            
            cashflow_text = f"+{net_cashflow:,.0f}đ (Dư ra)" if net_cashflow >= 0 else f"{net_cashflow:,.0f}đ (Bù thêm)"
            
            rows.append({
                "Kỳ hạn (Tháng)": f"{dur} tháng",
                "Khoản vay (đ)": f"{actual_loan:,.0f}đ",
                "Tiền gốc/tháng (đ)": f"{principal_monthly:,.0f}đ",
                "Tiền lãi/tháng (đ)": f"{interest_monthly:,.0f}đ",
                "Tổng Góp/tháng (đ)": f"{total_monthly:,.0f}đ",
                "Dòng tiền thực tế (đ)": cashflow_text,
                "Tổng lãi trả ngân hàng (đ)": f"{total_interest:,.0f}đ"
            })
            
        df_loan = pd.DataFrame(rows)
        st.dataframe(df_loan, use_container_width=True, hide_index=True)
        st.caption("(*) Lãi suất phẳng áp dụng cố định 0.59%/tháng theo gói hỗ trợ tín dụng xanh của Shinhan Bank.")
    else:
        st.success("🎉 Chúc mừng quý khách đã tự chủ năng lượng 100% bằng tiền mặt không lo trả góp và lãi vay!")

# ================= TAB 2: CHI TIẾT GÓI LẮP ĐẶT =================
with tab2:
    st.subheader("Tra cứu thông số kỹ thuật 10 gói Hybrid Solar 24h")
    
    # Custom kWp quick calculator
    with st.expander("➕ Công cụ tính nhanh sản lượng theo số kWp tùy chỉnh"):
        custom_kwp = st.number_input("Nhập số kWp mong muốn:", min_value=1.0, max_value=100.0, value=5.0, step=0.5)
        gen_day = custom_kwp * 4.3 * 0.82
        gen_month = gen_day * 30
        required_area = custom_kwp * 5.5
        
        col_c1, col_c2, col_c3 = st.columns(3)
        col_c1.metric("Sản lượng ngày dự kiến", f"{gen_day:.2f} kWh/ngày")
        col_c2.metric("Sản lượng tháng dự kiến", f"{gen_month:.0f} kWh/tháng")
        col_c3.metric("Diện tích mái tối thiểu", f"{required_area:.1f} m²")
        st.caption("(*) Tính toán dựa trên số giờ nắng đỉnh trung bình 4.3 giờ/ngày tại Tiền Giang/Đồng Tháp và hệ số hiệu suất 0.82.")

    # Package list table
    pkg_data = []
    for name, spec in packages.items():
        daily_gen = spec["kwp"] * 4.3 * 0.82
        monthly_gen = daily_gen * 30
        pkg_data.append({
            "Mã Gói": name,
            "Công Suất (kWp)": spec["kwp"],
            "Số Tấm Pin (580W)": spec["pin_count"],
            "Biến Tần": spec["inverter"],
            "Pin Lưu Trữ": spec["storage"],
            "Sản Lượng (kWh/tháng)": f"~{monthly_gen:,.0f}",
            "Đơn Giá (đ)": f"{spec['price']:,.0f}đ"
        })
        
    df_pkg = pd.DataFrame(pkg_data)
    st.dataframe(df_pkg, use_container_width=True, hide_index=True)

# ================= TAB 3: GÓI VAY SHINHAN BANK =================
with tab3:
    st.subheader("Thông tin chương trình vay tiêu dùng xanh Shinhan Bank")
    st.markdown("""
    **Solar 24h** liên kết chặt chẽ cùng đối tác tài chính nước ngoài **Shinhan Bank** mang đến giải pháp tín dụng xanh vô cùng ưu đãi phục vụ chuyển đổi năng lượng:
    
    *   **Lãi suất cố định phẳng cực thấp:** **0.59% / tháng** (Giảm thiểu hơn 80% áp lực lãi so với tài chính tiêu dùng thông thường).
    *   **Hạn mức hỗ trợ tối đa:** **100.000.000 VNĐ** (Hỗ trợ vay 100% không trả trước cho các gói F1, F2, F3).
    *   **Thời gian duyệt hồ sơ:** Siêu nhanh, nhận kết quả phê duyệt chỉ trong ngày.
    *   **Thủ tục hồ sơ cực kỳ tinh giản:**
        - 🪪 **Căn cước công dân gắn chip** (bản gốc để đối chiếu).
        - ⚡ **Hóa đơn tiền điện sinh hoạt** của 3 tháng gần nhất để đối chứng tiêu dùng.
        - 📄 Không yêu cầu sao kê lương hay chứng minh nguồn thu nhập phức tạp!
    """)
    
    st.info("💡 Mẹo tư vấn cho khách hàng: Hãy vẽ ra viễn cảnh 'Lấy tiền điện trả tiền góp'. Với lãi phẳng 0.59%/tháng, tổng số tiền góp định kỳ hàng tháng thường chỉ tương đương hoặc nhỉnh hơn một chút so với số tiền điện thực tế mà hệ thống đã giúp gia đình họ cắt giảm!")

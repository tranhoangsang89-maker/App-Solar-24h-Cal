import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page config
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán Điện Mặt Trời",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Brand Colors CSS
st.markdown("""
<style>
    :root {
        --navy-blue: #0F2942;
        --gold-yellow: #F4B41A;
        --soft-bg: #F4F6F9;
    }
    .main-title {
        color: #0F2942;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #555;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 25px;
    }
    .solar-girl-card {
        background-color: #EBF3F9;
        border-left: 5px solid #0F2942;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #EAEAEA;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0F2942;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F4F6F9;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-weight: 600;
        color: #0F2942;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F2942 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Define Solar Packages Data
PACKAGES = {
    "SOLAR F1": {"kwp": 2.3, "storage": "2.5 kWh", "inverter": "Luxpower SNA 5kW", "battery": "Lithium BSB", "price": 47800000, "min_bill": 0, "max_bill": 1000000, "panels": 4, "desc": "Phù hợp hóa đơn dưới 1 triệu/tháng. Giúp giảm gánh nặng giá điện lũy tiến bậc cao sinh hoạt."},
    "SOLAR F2": {"kwp": 4.6, "storage": "5 kWh", "inverter": "Luxpower SNA 5kW", "battery": "Lithium BSB", "price": 68500000, "min_bill": 1000000, "max_bill": 1500000, "panels": 8, "desc": "Phù hợp hóa đơn từ 1.0M đến 1.5 triệu. Dòng Hybrid bán chạy nhất cho hộ gia đình nhỏ lẻ."},
    "SOLAR F3": {"kwp": 5.8, "storage": "10 kWh", "inverter": "SVE 6kW", "battery": "Lithium LS", "price": 88000000, "min_bill": 1500000, "max_bill": 2000000, "panels": 10, "desc": "Phù hợp hóa đơn từ 1.5M đến 2.0 triệu. Sản lượng lưu trữ lớn thoải mái sử dụng ban đêm."},
    "SOLAR F4": {"kwp": 6.9, "storage": "16 kWh", "inverter": "SVE 6kW", "battery": "Lithium EJOR", "price": 104700000, "min_bill": 2000000, "max_bill": 2500000, "panels": 12, "desc": "Phù hợp hóa đơn từ 2.0M đến 2.5 triệu. Thừa hưởng cấu hình khủng và pin lưu trữ cực lớn."},
    "SOLAR F5": {"kwp": 8.1, "storage": "16 kWh", "inverter": "Luxpower PRO 6.5kW", "battery": "Lithium EJOR/LS", "price": 114900000, "min_bill": 2500000, "max_bill": 3000000, "panels": 14, "desc": "Phù hợp hóa đơn từ 2.5M đến 3.0 triệu. Sử dụng Inverter dòng Pro cao cấp thế hệ mới."},
    "SOLAR F6": {"kwp": 8.1, "storage": "16 kWh", "inverter": "Luxpower 6.5 PRO", "battery": "Lithium EJOR/LS", "price": 123600000, "min_bill": 3000000, "max_bill": 3500000, "panels": 16, "desc": "Phù hợp hóa đơn từ 3.0M đến 3.5 triệu. Giàn pin tối ưu diện tích cho hiệu quả gánh tải tối đa."},
    "SOLAR F7": {"kwp": 11.4, "storage": "32 kWh", "inverter": "Luxpower 6.5 PRO (x2)", "battery": "Lithium EJOR/LS", "price": 203000000, "min_bill": 3500000, "max_bill": 4000000, "panels": 20, "desc": "Phù hợp hóa đơn từ 3.5M đến 4.0 triệu. Cấu hình 2 Inverter chạy song song bảo đảm công suất kéo tải cực mạnh."},
    "SOLAR F8": {"kwp": 13.9, "storage": "32 kWh", "inverter": "Luxpower 6.5 PRO (x2)", "battery": "Lithium EJOR/LS", "price": 217900000, "min_bill": 4000000, "max_bill": 5000000, "panels": 24, "desc": "Phù hợp hóa đơn từ 4.0M đến 5.0 triệu. Triệt tiêu hoàn toàn hóa đơn điện bậc sinh hoạt cao nhất."},
    "SOLAR F9": {"kwp": 17.4, "storage": "32 kWh", "inverter": "Luxpower 6.5 PRO (x2)", "battery": "Lithium EJOR/LS", "price": 239000000, "min_bill": 5000000, "max_bill": 7000000, "panels": 30, "desc": "Phù hợp biệt thự hoặc hộ gia đình lớn kết hợp kinh doanh ban ngày công suất cực cao."},
    "SOLAR F10": {"kwp": 22.0, "storage": "48 kWh", "inverter": "Luxpower 6.5 PRO (x3)", "battery": "Lithium EJOR/LS", "price": 329300000, "min_bill": 7000000, "max_bill": 15000000, "panels": 38, "desc": "Cấu hình siêu khủng đỉnh chóp của hộ gia đình. Giải pháp tự chủ năng lượng 100% không lo cúp điện."}
}

# 2026 Progressive Electricity Tariff (EVN)
TARIF_2026 = [
    {"limit": 50, "rate": 1984},
    {"limit": 100, "rate": 2050},
    {"limit": 200, "rate": 2380},
    {"limit": 300, "rate": 2998},
    {"limit": 400, "rate": 3350},
    {"limit": float('inf'), "rate": 3460}
]

def calculate_kwh_from_bill(bill_vnd, vat_rate=8):
    """Calculate consumed kWh from total bill based on 2026 Tariff"""
    pre_vat_bill = bill_vnd / (1 + vat_rate/100.0)
    remaining = pre_vat_bill
    kwh = 0.0
    
    # We must calculate cumulative costs for each tier
    tier_costs = []
    prev_limit = 0
    for tier in TARIF_2026[:-1]:
        qty = tier["limit"] - prev_limit
        tier_costs.append(qty * tier["rate"])
        prev_limit = tier["limit"]
        
    prev_limit = 0
    for i, tier in enumerate(TARIF_2026):
        if tier["limit"] == float('inf'):
            kwh += remaining / tier["rate"]
            break
        
        step_max_cost = tier_costs[i]
        if remaining > step_max_cost:
            qty = tier["limit"] - prev_limit
            kwh += qty
            remaining -= step_max_cost
            prev_limit = tier["limit"]
        else:
            kwh += remaining / tier["rate"]
            break
            
    return kwh

def get_recommended_package(bill_vnd):
    """Recommend the optimal package based on company standards matching bill brackets"""
    for code, info in PACKAGES.items():
        if info["min_bill"] <= bill_vnd < info["max_bill"]:
            return code, info
    # Default to last package if exceeds max
    return "SOLAR F10", PACKAGES["SOLAR F10"]

# Header Row (Title & Logo)
st.markdown("<h1 class='main-title'>SOLAR 24H ☀️</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Năng lượng sạch - Nâng tầm cuộc sống</div>", unsafe_allow_html=True)

# Grid Layout for Top Panel (Mascot & Introduction)
col_left, col_right = st.columns([1, 3])

with col_left:
    # Safely load Solar Girl image if it exists in the user's GitHub images folder
    # Defaults to local fallback or nice custom styling if missing
    if os.path.exists("images/solar_girl.jpg"):
        st.image("images/solar_girl.jpg", use_column_width=True, caption="Solar Girl - Đại sứ Thương hiệu")
    elif os.path.exists("images/solar_girl.png"):
        st.image("images/solar_girl.png", use_column_width=True, caption="Solar Girl - Đại sứ Thương hiệu")
    else:
        # Show a stylish card if no image found yet
        st.markdown("""
        <div style='background-color:#0F2942; color:white; padding:15px; border-radius:10px; text-align:center;'>
            <span style='font-size:3rem;'>👩‍💼</span>
            <h4 style='margin:5px 0 0 0;'>Solar Girl</h4>
            <p style='font-size:0.8rem; margin:5px 0 0 0; color:#F4B41A;'>Sẵn sàng hỗ trợ tư vấn 24/7!</p>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class='solar-girl-card'>
        <strong>Solar Girl chào cả nhà! 👩‍💼</strong><br>
        Mọi người chỉ cần nhập hóa đơn và tùy chỉnh mức trả trước theo mong muốn. 
        Hệ thống sẽ tự động tư vấn ạ!
    </div>
    """, unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Chi Tiết Gói Lắp Đặt", "🏦 Gói Vay Shinhan Bank"])

with tab1:
    st.markdown("### Phân Tích Nhu Cầu & Đề Xuất Gói Tối Ưu")
    
    col_input1, col_input2, col_input3 = st.columns([2, 1, 2])
    with col_input1:
        bill_input = st.number_input("Nhập số tiền điện hàng tháng của khách (VNĐ):", min_value=100000, max_value=50000000, value=2500000, step=100000)
    with col_input2:
        vat_input = st.selectbox("Thuế VAT áp dụng:", [8, 10], index=0)
    
    consumed_kwh = calculate_kwh_from_bill(bill_input, vat_input)
    avg_daily_kwh = consumed_kwh / 30.0
    
    # Recommendation calculation
    pkg_code, pkg_info = get_recommended_package(bill_input)
    
    # Output metrics grid
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{consumed_kwh:.1f} kWh</div>
            <div class='metric-label'>LƯỢNG ĐIỆN TIÊU THỤ THỰC TẾ</div>
            <div style='font-size:0.8rem; color:#888;'>~ {avg_daily_kwh:.2f} kWh (số điện) / ngày</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class='metric-card' style='border-top: 4px solid #F4B41A;'>
            <div class='metric-value' style='color:#F4B41A;'>{pkg_code}</div>
            <div class='metric-label'>GÓI ĐỀ XUẤT TỐI ƯU</div>
            <div style='font-size:0.8rem; color:#888;'>Công suất {pkg_info["kwp"]} kWp · Trọn gói: {pkg_info["price"]:,}đ</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        # Savings Calculations
        expected_new_bill = 0.0 # Standard hybrid F-series wipes out bills completely
        monthly_saving = bill_input - expected_new_bill
        annual_saving = monthly_saving * 12
        roi_years = pkg_info["price"] / annual_saving if annual_saving > 0 else 0
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value' style='color:#28A745;'>{roi_years:.1f} Năm</div>
            <div class='metric-label'>THỜI GIAN HÒA VỐN (ROI)</div>
            <div style='font-size:0.8rem; color:#28A745;'>Tiết kiệm: {monthly_saving:,.0f}đ / tháng</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 💰 Thiết Lập Phương Án Tài Chính (Shinhan Bank - Lãi suất phẳng 0.59%/tháng)")
    
    # Set maximum loan limit based on Shinhan parameters
    max_loan_limit = min(float(pkg_info["price"]), 100000000.0)
    
    col_fin1, col_input_pre = st.columns([1, 1])
    with col_fin1:
        loan_selected = st.slider("Số tiền ngân hàng hỗ trợ trả góp (VNĐ):", min_value=0, max_value=int(max_loan_limit), value=int(max_loan_limit), step=10000000)
    with col_input_pre:
        custom_prepay = pkg_info["price"] - loan_selected
        st.write("") # vertical spacing align
        st.markdown(f"""
        <div style='background-color:#F4F6F9; padding: 12px; border-radius:6px; font-weight:600; text-align:center; border: 1px solid #DDD;'>
            Tiền khách tự thanh toán (Trả trước): <span style='color:#0F2942; font-size:1.1rem;'>{custom_prepay:,.0f} VNĐ</span>
        </div>
        """, unsafe_allow_html=True)
        
    if loan_selected > 0:
        st.markdown("#### Bảng dự toán nghĩa vụ trả góp hàng tháng")
        
        # Build live amortization comparison table
        terms = [12, 24, 36, 48]
        amort_data = []
        for term in terms:
            monthly_principal = loan_selected / term
            monthly_interest = loan_selected * 0.0059 # 0.59% Flat Rate
            total_monthly = monthly_principal + monthly_interest
            net_flow = monthly_saving - total_monthly
            total_interest = monthly_interest * term
            
            if net_flow >= 0:
                flow_desc = f"+{net_flow:,.0f}đ (Dư ra túi)"
                flow_color = "color:#28A745; font-weight:bold;"
            else:
                flow_desc = f"{net_flow:,.0f}đ (Bù thêm)"
                flow_color = "color:#DC3545; font-weight:bold;"
                
            amort_data.append({
                "Kỳ hạn": f"{term} Tháng",
                "Khoản vay": f"{loan_selected:,.0f}đ",
                "Gốc/tháng": f"{monthly_principal:,.0f}đ",
                "Lãi/tháng (0.59%)": f"{monthly_interest:,.0f}đ",
                "Tổng Góp/tháng": f"{total_monthly:,.0f}đ",
                "Dòng tiền thực tế": flow_desc,
                "Tổng lãi": f"{total_interest:,.0f}đ"
            })
            
        df_amort = pd.DataFrame(amort_data)
        st.table(df_amort.set_index("Kỳ hạn"))
        st.markdown("<p style='font-size:0.85rem; color:#666;'>*Ghi chú: <strong>Dòng tiền thực tế</strong> = Số tiền điện tiết kiệm hàng tháng - Tiền góp hàng tháng. Dòng tiền dương (+) nghĩa là khách hàng không cần bỏ thêm tiền túi mà còn tiết kiệm dôi dư thêm tiền hàng tháng.</p>", unsafe_allow_html=True)
    else:
        st.success("Khách hàng thanh toán trực tiếp 100% bằng tiền mặt. Hưởng trọn vẹn dòng tiền tiết kiệm điện mà không mất bất cứ khoản lãi vay nào!")

with tab2:
    st.markdown("### Danh Sách Toàn Bộ Hệ Thống Hybrid Cao Cấp Solar 24h")
    
    # Option to view equipment image if uploaded to GitHub images directory
    if os.path.exists("images/solar_equipment.jpg"):
        st.image("images/solar_equipment.jpg", use_column_width=True, caption="Hệ Thống Thiết Bị Điện Mặt Trời Hybrid Hiện Đại")
    elif os.path.exists("images/solar_equipment.png"):
        st.image("images/solar_equipment.png", use_column_width=True, caption="Hệ Thống Thiết Bị Điện Mặt Trời Hybrid Hiện Đại")
    
    st.markdown("Chọn một gói để xem chi tiết vật tư, cấu hình thiết bị chuyên sâu:")
    
    selected_code = st.selectbox("Chọn gói sản phẩm:", list(PACKAGES.keys()), index=1) # Default F2
    pkg_detail = PACKAGES[selected_code]
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(f"""
        <div style='background-color:#F8F9FA; padding:20px; border-radius:10px; border-left:5px solid #F4B41A;'>
            <h4 style='color:#0F2942; margin-top:0;'>📐 Cấu Hình {selected_code}</h4>
            <ul style='list-style-type: none; padding-left: 0; line-height:1.8;'>
                <li><strong>Tổng công suất giàn pin:</strong> {pkg_detail["kwp"]} kWp</li>
                <li><strong>Số lượng tấm pin (AE Solar 580W):</strong> {pkg_detail["panels"]} Tấm (Mono TOPCon)</li>
                <li><strong>Diện tích mái tối thiểu:</strong> {pkg_detail["kwp"] * 6:.1f} m²</li>
                <li><strong>Hệ thống Biến tần Inverter:</strong> {pkg_detail["inverter"]}</li>
                <li><strong>Hệ thống bình lưu trữ Lithium:</strong> {pkg_detail["storage"]} ({pkg_detail["battery"]})</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_d2:
        # Calculate standard generation
        daily_gen = pkg_detail["kwp"] * 4.3 * 0.82
        monthly_gen = daily_gen * 30
        
        st.markdown(f"""
        <div style='background-color:#F8F9FA; padding:20px; border-radius:10px; border-left:5px solid #0F2942;'>
            <h4 style='color:#0F2942; margin-top:0;'>📈 Sản Lượng & Tiết Kiệm Dự Kiến</h4>
            <ul style='list-style-type: none; padding-left: 0; line-height:1.8;'>
                <li><strong>Giá trọn gói lắp đặt:</strong> <span style='font-size:1.2rem; color:#0F2942; font-weight:bold;'>{pkg_detail["price"]:,} VNĐ</span></li>
                <li><strong>Sản lượng điện hàng ngày:</strong> {daily_gen:.1f} - {daily_gen*1.2:.1f} kWh / ngày</li>
                <li><strong>Sản lượng điện hàng tháng:</strong> ~ {monthly_gen:,.0f} kWh (số điện)</li>
                <li><strong>Khả năng chống dột & cách nhiệt:</strong> Giảm 3-5°C nhiệt độ mái, bảo hành 100% không thấm dột.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### Quy Trình Vay & Ưu Điểm Đối Tác Shinhan Bank")
    st.markdown("""
    <div style='background-color:#EBF3F9; padding:20px; border-radius:8px;'>
        <h4 style='color:#0F2942; margin-top:0;'>🎯 Ưu Điểm Tuyệt Đối Của Gói Vay Shinhan Bank</h4>
        <ul style='line-height:1.8;'>
            <li><strong>Lãi suất phẳng cực tốt:</strong> Chỉ <strong>0.59%/tháng</strong> cố định trọn đời.</li>
            <li><strong>Hạn mức cho vay:</strong> Hỗ trợ tối đa lên đến <strong>100.000.000 VNĐ</strong>.</li>
            <li><strong>Hồ sơ thủ tục siêu đơn giản:</strong> Chỉ cần <strong>CCCD có gắn chip</strong> và <strong>Hóa đơn tiền điện sinh hoạt</strong> của gia đình.</li>
            <li><strong>Không cần chứng minh thu nhập:</strong> Xét duyệt và phê duyệt khoản vay cực nhanh trực tuyến.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Quy trình 4 bước đơn giản để lắp đặt điện mặt trời 0 đồng:")
    st.markdown("""
    1. **Khảo sát & Tư vấn:** Nhân viên Solar 24h đo đạc thông số mái, lập sơ đồ 3D và lập bảng dự toán dòng tiền hoàn toàn miễn phí.
    2. **Lên hồ sơ vay:** Kỹ thuật viên hướng dẫn chụp ảnh CCCD và hóa đơn tiền điện gửi Shinhan Bank thẩm duyệt.
    3. **Phê duyệt & Giải ngân:** Shinhan Bank phê duyệt trong ngày, giải ngân trực tiếp cho dự án.
    4. **Thi công & Nghiệm thu:** Đội ngũ kỹ thuật Solar 24h hoàn thành thi công đúng kỹ thuật trong vòng 2-3 ngày, bàn giao app theo dõi năng lượng.
    """)

# Footer with corporate info
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.85rem;'>
    <strong>CÔNG TY TNHH TMDV SOLAR 24H</strong><br>
    Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh, Tỉnh Đồng Tháp<br>
    Hotline tư vấn & khảo sát miễn phí: 0909.363.579 - 0896.488.299<br>
    © 2026 Solar 24h. Bảo lưu mọi quyền.
</div>
""", unsafe_allow_html=True)

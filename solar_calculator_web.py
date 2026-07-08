import streamlit as st
import pandas as pd
import numpy as np

# Cấu hình trang
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán Dòng Tiền Trả Góp",
    page_icon="☀️",
    layout="centered"
)

# Áp dụng CSS tùy chỉnh theo nhận diện thương hiệu Solar 24h
st.markdown("""
<style>
.stApp {
    background-color: #F8F9FA;
}
.main-title {
    color: #0F2C59;
    font-size: 1.8rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.2rem;
}
.sub-title {
    color: #E2B616;
    font-size: 1.1rem;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1.5rem;
}
.section-card {
    background-color: #FFFFFF;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.2rem;
    border-left: 5px solid #0F2C59;
}
.highlight-card {
    background-color: #FFFDF0;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.2rem;
    border-left: 5px solid #E2B616;
}
.card-title {
    color: #0F2C59;
    font-size: 1.15rem;
    font-weight: bold;
    margin-bottom: 0.8rem;
}
.mascot-box {
    background-color: #E8F0FE;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1A73E8;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}
.metric-container {
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
}
.metric-box {
    flex: 1;
    text-align: center;
    padding: 0.5rem;
    background: #F1F3F4;
    border-radius: 6px;
    margin: 0 0.2rem;
}
.metric-num {
    font-size: 1.2rem;
    font-weight: bold;
    color: #0F2C59;
}
.metric-lbl {
    font-size: 0.8rem;
    color: #5F6368;
}
</style>
""", unsafe_allow_html=True)

# ----------------- DỮ LIỆU CỐ ĐỊNH -----------------
# Biểu giá điện sinh hoạt lũy tiến 6 bậc mới năm 2026
BAC_GIA = [
    {"limit": 50, "price": 1984},
    {"limit": 50, "price": 2050},
    {"limit": 100, "price": 2380},
    {"limit": 100, "price": 2998},
    {"limit": 100, "price": 3350},
    {"limit": float('inf'), "price": 3460}
]

# Danh mục 10 gói Hybrid Solar 24h
PACKAGES = {
    "SOLAR F1": {
        "price": 47800000, "capacity": 2.3, "panels": 4, "inverter": "Inverter LUXPOWER SNA 5kW",
        "storage": "Lưu trữ BSB: 2.5 kWh", "prod_min": 6, "prod_max": 10, "target": "Dưới 500.000đ"
    },
    "SOLAR F2": {
        "price": 68500000, "capacity": 4.6, "panels": 8, "inverter": "Inverter LUXPOWER SNA 5kW",
        "storage": "Lưu trữ BSB: 5 kWh", "prod_min": 10, "prod_max": 18, "target": "Dưới 1.000.000đ"
    },
    "SOLAR F3": {
        "price": 88000000, "capacity": 5.8, "panels": 10, "inverter": "Inverter SVE 6kW",
        "storage": "Lưu trữ LS Battery: 10 kWh", "prod_min": 15, "prod_max": 28, "target": "1.0 đến 1.5 triệu"
    },
    "SOLAR F4": {
        "price": 104700000, "capacity": 6.9, "panels": 12, "inverter": "Inverter SVE 6kW",
        "storage": "Lưu trữ EJOR: 16 kWh", "prod_min": 20, "prod_max": 30, "target": "1.5 đến 2.0 triệu"
    },
    "SOLAR F5": {
        "price": 114900000, "capacity": 8.1, "panels": 14, "inverter": "Inverter LUXPOWER PRO 6.5kW",
        "storage": "Lưu trữ EJOR/LS: 16 kWh", "prod_min": 20, "prod_max": 34, "target": "2.0 đến 2.5 triệu"
    },
    "SOLAR F6": {
        "price": 123600000, "capacity": 8.1, "panels": 16, "inverter": "Inverter LUXPOWER 6.5 PRO",
        "storage": "Lưu trữ EJOR/LS: 16 kWh", "prod_min": 25, "prod_max": 40, "target": "2.5 đến 3.0 triệu"
    },
    "SOLAR F7": {
        "price": 203000000, "capacity": 11.4, "panels": 20, "inverter": "Inverter LUXPOWER 6.5 PRO (x2)",
        "storage": "Lưu trữ EJOR/LS: 32 kWh", "prod_min": 35, "prod_max": 50, "target": "3.0 đến 4.0 triệu"
    },
    "SOLAR F8": {
        "price": 217900000, "capacity": 13.9, "panels": 24, "inverter": "Inverter LUXPOWER 6.5 PRO (x2)",
        "storage": "Lưu trữ EJOR/LS: 32 kWh", "prod_min": 40, "prod_max": 60, "target": "4.0 đến 5.0 triệu"
    },
    "SOLAR F9": {
        "price": 239000000, "capacity": 17.4, "panels": 30, "inverter": "Inverter LUXPOWER 6.5 PRO (x2)",
        "storage": "Lưu trữ EJOR/LS: 32 kWh", "prod_min": 50, "prod_max": 70, "target": "5.0 đến 7.0 triệu"
    },
    "SOLAR F10": {
        "price": 329300000, "capacity": 22.0, "panels": 38, "inverter": "Inverter LUXPOWER 6.5 PRO (x3)",
        "storage": "Lưu trữ EJOR/LS: 48 kWh", "prod_min": 60, "prod_max": 90, "target": "7.0 đến 10.0 triệu"
    }
}

# ----------------- CÁC HÀM XỬ LÝ TOÁN HỌC -----------------
def calculate_kwh_from_bill(bill, vat_rate):
    """Tính toán lượng điện tiêu thụ trước thuế từ hóa đơn sau thuế"""
    pre_vat = bill / (1 + vat_rate / 100)
    remaining = pre_vat
    kwh = 0
    for step in BAC_GIA:
        limit = step["limit"]
        price = step["price"]
        step_limit_cost = limit * price
        if remaining > step_limit_cost and limit != float('inf'):
            kwh += limit
            remaining -= step_limit_cost
        else:
            kwh += remaining / price
            break
    return kwh, pre_vat

def calculate_bill_from_kwh(kwh, vat_rate):
    """Tính toán hóa đơn sau thuế từ số điện sinh hoạt"""
    remaining = kwh
    pre_vat = 0
    for step in BAC_GIA:
        limit = step["limit"]
        price = step["price"]
        if remaining > limit:
            pre_vat += limit * price
            remaining -= limit
        else:
            pre_vat += remaining * price
            break
    return pre_vat * (1 + vat_rate / 100)

def recommend_package(bill):
    """Đề xuất đúng dải gói Hybrid dựa trên hóa đơn thực tế của công ty"""
    if bill <= 500000:
        return "SOLAR F1"
    elif bill <= 1000000:
        return "SOLAR F2"
    elif bill <= 1500000:
        return "SOLAR F3"
    elif bill <= 2000000:
        return "SOLAR F4"
    elif bill <= 2500000:
        return "SOLAR F5"
    elif bill <= 3000000:
        return "SOLAR F6"
    elif bill <= 4000000:
        return "SOLAR F7"
    elif bill <= 5000000:
        return "SOLAR F8"
    elif bill <= 7000000:
        return "SOLAR F9"
    else:
        return "SOLAR F10"

# ----------------- HEADER GIAO DIỆN -----------------
st.markdown('<div class="main-title">SOLAR 24H</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hệ Thống Phân Tích Dòng Tiền Trả Góp Shinhan Bank 2026</div>', unsafe_allow_html=True)

# Khởi tạo Tabs
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Danh Sách Gói Hybrid", "☀️ Công Cụ Tính Nhanh"])

# ================= TAB 1: TƯ VẤN KHÁCH HÀNG & TRẢ GÓP TÙY CHỈNH =================
with tab1:
    st.markdown('<div class="mascot-box"><b>Solar Girl chào anh Sang và cả nhà!</b> 👩‍💼 Để tư vấn cho khách, anh chỉ cần nhập hóa đơn và tùy chỉnh mức trả trước theo mong muốn của khách nhé. Hệ thống sẽ tự động xuất dòng tiền chi tiết nhất!</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        bill_input = st.number_input(
            "Hóa đơn tiền điện (VNĐ/Tháng):",
            min_value=100000,
            max_value=50000000,
            value=2700000,
            step=100000,
            format="%d"
        )
    with col2:
        vat_rate = st.selectbox("Thuế suất VAT (%) trên hóa đơn:", [8, 10], index=0)
        
    # Tính toán cơ sở dữ liệu của khách
    kwh, pre_vat = calculate_kwh_from_bill(bill_input, vat_rate)
    rec_package_id = recommend_package(bill_input)
    
    st.markdown(f"""
    <div class="section-card">
        <div class="card-title">🔍 LƯỢNG ĐIỆN TIÊU THỤ THỰC TẾ</div>
        <b>{kwh:,.2f} kWh / tháng</b> (Số điện)<br>
        Trung bình khoảng <b>{kwh/30:,.2f} kWh</b> mỗi ngày.<br>
        <i>*Tính toán dựa trên cơ sở biểu giá lũy tiến 6 bậc năm 2026.</i>
    </div>
    """, unsafe_allow_html=True)
    
    # Cho phép chọn gói lắp đặt (Mặc định là gói được đề xuất)
    st.markdown('<div class="card-title">🌟 THIẾT LẬP GÓI LẮP ĐẶT & SỐ TIỀN TRẢ TRƯỚC</div>', unsafe_allow_html=True)
    
    package_list = list(PACKAGES.keys())
    rec_index = package_list.index(rec_package_id)
    
    chosen_package_id = st.selectbox(
        "Lựa chọn Gói lắp đặt thực tế:",
        package_list,
        index=rec_index,
        help="Hệ thống tự động đề xuất gói tối ưu nhất dựa trên hóa đơn của khách, bạn có thể điều chỉnh thủ công."
    )
    
    pkg_data = PACKAGES[chosen_package_id]
    total_price = pkg_data["price"]
    
    # CÁCH TÍNH TOÁN KHOẢN VAY VÀ TIỀN TRẢ TRƯỚC
    # Hạn mức vay tối đa của Shinhan Bank là 100,000,000đ
    max_loan_limit = 100000000
    min_required_prepay = max(0, total_price - max_loan_limit)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"""
        <b>Thông số gói được chọn:</b><br>
        • Công suất: <b>{pkg_data['capacity']} kWp</b><br>
        • Trọn gói: <span style='color:#0F2C59; font-weight:bold;'>{total_price:,.0f}đ</span><br>
        • Tấm pin: {pkg_data['panels']} Tấm AE Solar 580W<br>
        • Lưu trữ: {pkg_data['storage']}
        """, unsafe_allow_html=True)
        
    with col_p2:
        # Nhập số tiền trả trước mong muốn (VNĐ)
        prepayment = st.number_input(
            "Tiền khách trả trước (VNĐ):",
            min_value=float(min_required_prepay),
            max_value=float(total_price),
            value=float(min_required_prepay),
            step=1000000.0,
            format="%.0f",
            help="Khách hàng cần trả trước ít nhất khoản chênh lệch vượt hạn mức 100M (nếu có). Có thể trả trước nhiều hơn để giảm nợ vay."
        )
        
    # Tính khoản vay thực tế
    loan_amount = total_price - prepayment
    
    # Hiển thị tóm tắt dòng tiền
    st.markdown(f"""
    <div class="highlight-card">
        <div class="card-title">💰 CƠ CẤU VỐN ĐẦU TƯ</div>
        • Tổng giá trị hệ thống: <b>{total_price:,.0f} VNĐ</b><br>
        • Tiền mặt trả trước: <span style='color:#E2B616; font-weight:bold;'>{prepayment:,.0f} VNĐ</span> (Chiếm {prepayment/total_price*100:.1f}%)<br>
        • Khoản vay trả góp ngân hàng: <span style='color:#0F2C59; font-weight:bold;'>{loan_amount:,.0f} VNĐ</span> (Lãi suất cố định <b>0.59%/tháng</b>)
    </div>
    """, unsafe_allow_html=True)
    
    # Tính toán hiệu quả tiết kiệm điện
    # Lấy sản lượng tháng trung bình theo giờ nắng miền Tây 4.3h
    monthly_gen = pkg_data["capacity"] * 4.3 * 30 * 0.82
    remaining_kwh = max(0.0, kwh - monthly_gen)
    new_bill = calculate_bill_from_kwh(remaining_kwh, vat_rate)
    monthly_saving = max(0.0, bill_input - new_bill)
    annual_saving = monthly_saving * 12
    roi_years = total_price / annual_saving if annual_saving > 0 else 0
    
    st.markdown(f"""
    <div class="section-card">
        <div class="card-title">💵 PHÂN TÍCH HIỆU QUẢ TIẾT KIỆM (ROI)</div>
        <div class="metric-container">
            <div class="metric-box">
                <div class="metric-num">{new_bill:,.0f}đ</div>
                <div class="metric-lbl">Hóa đơn điện mới</div>
            </div>
            <div class="metric-box">
                <div class="metric-num">+{monthly_saving:,.0f}đ</div>
                <div class="metric-lbl">Tiết kiệm / Tháng</div>
            </div>
            <div class="metric-box">
                <div class="metric-num">{roi_years:.1f} Năm</div>
                <div class="metric-lbl">Thời gian hòa vốn</div>
            </div>
        </div>
        <p style='margin-top:0.8rem; font-size:0.9rem; color:#5F6368;'>
        * Hệ thống sản sinh khoảng <b>{monthly_gen:,.1f} kWh/tháng</b>, bù đắp trực tiếp <b>{min(100.0, (monthly_gen/kwh)*100):.1f}%</b> lượng điện thực tế của khách hàng.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # PHƯƠNG ÁN TRẢ GÓP SHINHAN BANK DỰA TRÊN KHOẢN VAY THỰC TẾ
    st.markdown('<div class="card-title">🏦 BẢNG SO SÁNH KỲ HẠN VAY QUA SHINHAN BANK</div>', unsafe_allow_html=True)
    
    if loan_amount <= 0:
        st.success("Khách hàng thanh toán trả thẳng 100% bằng tiền mặt. Không phát sinh chi phí trả góp và lãi vay!")
    else:
        periods = [12, 24, 36, 48]
        repayment_data = []
        
        for m in periods:
            goc_thang = loan_amount / m
            # Lãi suất phẳng 0.59%/tháng
            lai_thang = loan_amount * 0.0059
            tong_gop_thang = goc_thang + lai_thang
            dong_tien = monthly_saving - tong_gop_thang
            tong_lai = lai_thang * m
            
            # Định dạng hiển thị dòng tiền thực tế
            if dong_tien >= 0:
                dong_tien_str = f"+{dong_tien:,.0f}đ (Dư ra)"
            else:
                dong_tien_str = f"-{abs(dong_tien):,.0f}đ (Bù thêm)"
                
            repayment_data.append({
                "Kỳ hạn": f"{m} Tháng",
                "Khoản vay": f"{loan_amount:,.0f}đ",
                "Tiền gốc/tháng": f"{goc_thang:,.0f}đ",
                "Tiền lãi/tháng": f"{lai_thang:,.0f}đ",
                "Tổng Góp/tháng": f"{tong_gop_thang:,.0f}đ",
                "Dòng tiền thực tế": dong_tien_str,
                "Tổng lãi trả ngân hàng": f"{tong_lai:,.0f}đ"
            })
            
        df_repayment = pd.DataFrame(repayment_data)
        st.table(df_repayment.set_index("Kỳ hạn"))
        
        st.info("💡 Mẹo tư vấn cho Sales: Hãy định hướng khách hàng chọn các kỳ hạn dài (36 - 48 tháng) để số tiền góp hàng tháng ở mức thấp nhất, giúp dòng tiền hàng tháng ở trạng thái dương hoặc chỉ bù thêm một khoản cực nhỏ, đúng theo tinh thần 'Lấy tiền điện trả tiền góp'!")

# ================= TAB 2: CHI TIẾT DANH SÁCH 10 GÓI HYBRID =================
with tab2:
    st.markdown('<div class="card-title">📦 BẢNG THÔNG SỐ VẬT TƯ & BÁO GIÁ CÁC GÓI HYBRID</div>', unsafe_allow_html=True)
    
    pkg_table_data = []
    for kid, kdata in PACKAGES.items():
        pkg_table_data.append({
            "Mã Gói": kid,
            "Công suất (kWp)": f"{kdata['capacity']} kWp",
            "Số tấm pin (580W)": f"{kdata['panels']} Tấm",
            "Biến tần (Inverter)": kdata['inverter'],
            "Pin lưu trữ Lithium": kdata['storage'],
            "Giá trọn gói": f"{kdata['price']:,.0f}đ",
            "Hóa đơn phù hợp": kdata['target']
        })
    df_pkgs = pd.DataFrame(pkg_table_data)
    st.dataframe(df_pkgs.set_index("Mã Gói"), use_container_width=True)

# ================= TAB 3: CÔNG CỤ TÍNH NHANH SẢN LƯỢNG MÁI =================
with tab3:
    st.markdown('<div class="card-title">☀️ TÍNH TOÁN SẢN LƯỢNG THEO CÔNG SUẤT TÙY CHỈNH</div>', unsafe_allow_html=True)
    
    custom_kwp = st.number_input(
        "Nhập tổng công suất giàn pin mong muốn (kWp):",
        min_value=1.0,
        max_value=500.0,
        value=5.0,
        step=0.5
    )
    
    # Tính toán diện tích mái & sản lượng dự kiến theo công thức chuẩn của Solar 24h
    roof_space_min = custom_kwp * 5
    roof_space_max = custom_kwp * 6
    daily_prod = custom_kwp * 4.3 * 0.82
    monthly_prod = daily_prod * 30
    
    st.markdown(f"""
    <div class="section-card">
        <div class="card-title">📊 KẾT QUẢ DỰ BÁO KỸ THUẬT</div>
        • Diện tích mái cần thiết: <b>{roof_space_min:.1f} - {roof_space_max:.1f} mét vuông</b> (thông thoáng, không đổ bóng).<br>
        • Sản lượng điện dự kiến hàng ngày: <b>{daily_prod:.1f} - {custom_kwp*4.5*0.82:.1f} kWh / ngày</b> (Điều kiện thời tiết tốt).<br>
        • Sản lượng điện trung bình hàng tháng: <span style='color:#0F2C59; font-weight:bold;'>{monthly_prod:,.1f} kWh / tháng</span>.<br>
        <i>*Hệ số tổn hao hiệu suất hệ thống tiêu chuẩn: 0.82. Số giờ nắng miền Tây trung bình: 4.3 giờ/ngày.</i>
    </div>
    """, unsafe_allow_html=True)

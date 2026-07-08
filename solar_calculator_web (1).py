import streamlit as st
import pandas as pd
import numpy as np
import os

# Cấu hình trang tối ưu cho điện thoại
st.set_page_config(
    page_title="Solar 24h - Công Cụ Tính Toán Điện Mặt Trời",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Thêm CSS để giao diện hiển thị đẹp mắt trên di động với tông màu Solar 24h (Navy Blue & Gold)
st.markdown("""
<style>
    .main-title {
        color: #0F2E59;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #D4AF37;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
        font-style: italic;
    }
    .section-header {
        color: #0F2E59;
        font-size: 18px;
        font-weight: bold;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #F0F4F8;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #D4AF37;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 13px;
        color: #555555;
    }
    .metric-value {
        font-size: 20px;
        font-weight: bold;
        color: #0F2E59;
    }
    .highlight-box {
        background-color: #FFFDF0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #D4AF37;
        margin-top: 15px;
    }
    /* Điều chỉnh cỡ chữ cho bảng biểu trên mobile */
    div[data-testid="stDataFrame"] {
        font-size: 12px;
    }
</style>
""", unsafe_allowed_html=True)

# Khai báo thông tin 10 gói Hybrid Solar 24h
GOI_SOLAR = {
    "SOLAR F1": {"kwp": 2.3, "tam_pin": 4, "pin_lt": "2.5 kWh", "inverter": "LUXPOWER SNA 5kW", "gia": 47800000, "phu_hop": "Dưới 500.000đ/tháng"},
    "SOLAR F2": {"kwp": 4.6, "tam_pin": 8, "pin_lt": "5 kWh", "inverter": "LUXPOWER SNA 5kW", "gia": 68500000, "phu_hop": "Dưới 1.000.000đ/tháng"},
    "SOLAR F3": {"kwp": 5.8, "tam_pin": 10, "pin_lt": "10 kWh (giao tiếp)", "inverter": "SVE 6KW", "gia": 88000000, "phu_hop": "Từ 1.000.000đ đến 1.500.000đ/tháng"},
    "SOLAR F4": {"kwp": 6.9, "tam_pin": 12, "pin_lt": "16 kWh (giao tiếp)", "inverter": "SVE 6KW", "gia": 104700000, "phu_hop": "Từ 1.500.000đ đến 2.000.000đ/tháng"},
    "SOLAR F5": {"kwp": 8.1, "tam_pin": 14, "pin_lt": "16 kWh (giao tiếp)", "inverter": "LUXPOWER PRO 6.5KW", "gia": 114900000, "phu_hop": "Từ 2.000.000đ đến 2.500.000đ/tháng"},
    "SOLAR F6": {"kwp": 8.1, "tam_pin": 16, "pin_lt": "16 kWh (giao tiếp)", "inverter": "LUXPOWER 6.5 PRO", "gia": 123600000, "phu_hop": "Từ 2.500.000đ đến 3.000.000đ/tháng"},
    "SOLAR F7": {"kwp": 11.4, "tam_pin": 20, "pin_lt": "32 kWh (giao tiếp)", "inverter": "LUXPOWER 6.5 PRO (x2)", "gia": 203000000, "phu_hop": "Từ 3.000.000đ đến 4.000.000đ/tháng"},
    "SOLAR F8": {"kwp": 13.9, "tam_pin": 24, "pin_lt": "32 kWh (giao tiếp)", "inverter": "LUXPOWER 6.5 PRO (x2)", "gia": 217900000, "phu_hop": "Từ 4.000.000đ đến 5.000.000đ/tháng"},
    "SOLAR F9": {"kwp": 17.4, "tam_pin": 30, "pin_lt": "32 kWh (giao tiếp)", "inverter": "LUXPOWER 6.5 PRO (x2)", "gia": 239000000, "phu_hop": "Từ 5.000.000đ đến 7.000.000đ/tháng"},
    "SOLAR F10": {"kwp": 22.0, "tam_pin": 38, "pin_lt": "48 kWh (giao tiếp)", "inverter": "LUXPOWER 6.5 PRO (x3)", "gia": 329300000, "phu_hop": "Từ 7.000.000đ đến 10.000.000đ/tháng"},
}

# Tiêu đề ứng dụng
st.markdown('<div class="main-title">SOLAR 24H</div>', unsafe_allowed_html=True)
st.markdown('<div class="sub-title">Trợ lý ảo tư vấn & tính toán sản lượng điện thông minh 2026</div>', unsafe_allowed_html=True)

# Khởi tạo các Tab
tab1, tab2, tab3 = st.tabs(["📋 Tư Vấn Khách Hàng", "📦 Các Gói Hybrid", "🏦 Trả Góp Shinhan"])

# --- TAB 1: TƯ VẤN KHÁCH HÀNG ---
with tab1:
    st.markdown('<div class="section-header">Tính toán lượng điện & Đề xuất giải pháp</div>', unsafe_allowed_html=True)
    
    # Input tiền điện
    bill_input = st.number_input("Nhập số tiền điện hàng tháng của khách (VNĐ):", min_value=0, value=1500000, step=50000)
    vat_rate = st.radio("Mức thuế VAT áp dụng:", [10, 8], horizontal=True)
    
    # Tính ngược ra số điện (kWh) dựa trên biểu giá lũy tiến 6 bậc mới 2026
    pre_vat_bill = bill_input / (1 + vat_rate/100)
    
    # Các mốc giá 2026 (chưa VAT)
    prices = [1984, 2050, 2380, 2998, 3350, 3460]
    steps = [50, 50, 100, 100, 100]  # bậc 1->5
    step_costs = [
        50 * 1984,                 # bậc 1 (0-50): 99,200đ
        50 * 2050,                 # bậc 2 (51-100): 102,500đ
        100 * 2380,                # bậc 3 (101-200): 238,000đ
        100 * 2998,                # bậc 4 (201-300): 299,800đ
        100 * 3350                 # bậc 5 (301-400): 335,000đ
    ]
    cum_costs = np.cumsum(step_costs)  # [99200, 201700, 439700, 739500, 1074500]
    
    kwh = 0.0
    if pre_vat_bill <= 0:
        kwh = 0.0
    elif pre_vat_bill <= cum_costs[0]:
        kwh = pre_vat_bill / prices[0]
    elif pre_vat_bill <= cum_costs[1]:
        kwh = 50 + (pre_vat_bill - cum_costs[0]) / prices[1]
    elif pre_vat_bill <= cum_costs[2]:
        kwh = 100 + (pre_vat_bill - cum_costs[1]) / prices[2]
    elif pre_vat_bill <= cum_costs[3]:
        kwh = 200 + (pre_vat_bill - cum_costs[2]) / prices[3]
    elif pre_vat_bill <= cum_costs[4]:
        kwh = 300 + (pre_vat_bill - cum_costs[3]) / prices[4]
    else:
        kwh = 400 + (pre_vat_bill - cum_costs[4]) / prices[5]
        
    kwh_day = kwh / 30
    
    # Hiển thị số liệu bóc tách
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tổng số điện tiêu thụ/tháng</div>
            <div class="metric-value">{kwh:.2f} kWh</div>
        </div>
        """, unsafe_allowed_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Lượng điện dùng trung bình/ngày</div>
            <div class="metric-value">{kwh_day:.2f} kWh</div>
        </div>
        """, unsafe_allowed_html=True)
        
    # Đề xuất gói lắp đặt dựa trên số điện và hóa đơn
    st.markdown('<div class="section-header">Gói lắp đặt đề xuất tối ưu</div>', unsafe_allowed_html=True)
    
    goi_de_xuat = "SOLAR F1"
    for name, data in GOI_SOLAR.items():
        # Tìm gói có sản lượng phát điện tháng (kwp * 4.3 * 30 * 0.82) vừa bao phủ hoặc mấp nghé nhu cầu
        san_luong_thang = data["kwp"] * 4.3 * 30 * 0.82
        if san_luong_thang >= kwh:
            goi_de_xuat = name
            break
    else:
        goi_de_xuat = "SOLAR F10"
        
    de_xuat_data = GOI_SOLAR[goi_de_xuat]
    sl_goi = de_xuat_data["kwp"] * 4.3 * 30 * 0.82
    sl_goi_ngay = de_xuat_data["kwp"] * 4.3 * 0.82
    tile_coverage = min(100.0, (sl_goi / kwh) * 100) if kwh > 0 else 100.0
    
    st.success(f"Khuyên dùng: **{goi_de_xuat}** ({de_xuat_data['kwp']} kWp)")
    
    st.markdown(f"""
    <div class="highlight-box">
        <b>📊 Thông tin chi tiết gói đề xuất:</b><br>
        • <b>Cấu hình:</b> {de_xuat_data['tam_pin']} Tấm pin AE Solar 580W | Lưu trữ {de_xuat_data['pin_lt']}<br>
        • <b>Biến tần:</b> {de_xuat_data['inverter']}<br>
        • <b>Giá trọn gói lắp đặt:</b> <span style="color:#0F2E59; font-weight:bold;">{de_xuat_data['gia']:,} VNĐ</span><br>
        • <b>Sản lượng dự kiến:</b> ~{sl_goi:.1f} kWh/tháng (gần {sl_goi_ngay:.1f} kWh/ngày)<br>
        • <b>Mức độ đáp ứng:</b> Hệ thống gánh khoảng <b>{tile_coverage:.1f}%</b> nhu cầu sử dụng điện thực tế của nhà khách hàng.
    </div>
    """, unsafe_allowed_html=True)
    
    # Tính thời gian hòa vốn (ROI)
    # Giả định tiết kiệm được tối đa (giảm về mốc tối thiểu)
    # Lượng điện mặt trời gánh bớt bậc cao nhất
    kwh_tiet_kiem = min(kwh, sl_goi)
    # Tính số tiền điện trước thuế được giảm từ việc bớt kwh_tiet_kiem số điện từ bậc cao nhất trở xuống
    remaining_kwh = kwh
    reduced_bill_pre_vat = 0.0
    
    # Tính lại hóa đơn mới sau khi trừ điện mặt trời
    new_kwh = max(0.0, kwh - kwh_tiet_kiem)
    new_pre_vat_bill = 0.0
    if new_kwh <= 50:
        new_pre_vat_bill = new_kwh * prices[0]
    elif new_kwh <= 100:
        new_pre_vat_bill = cum_costs[0] + (new_kwh - 50) * prices[1]
    elif new_kwh <= 200:
        new_pre_vat_bill = cum_costs[1] + (new_kwh - 100) * prices[2]
    elif new_kwh <= 300:
        new_pre_vat_bill = cum_costs[2] + (new_kwh - 200) * prices[3]
    elif new_kwh <= 400:
        new_pre_vat_bill = cum_costs[3] + (new_kwh - 300) * prices[4]
    else:
        new_pre_vat_bill = cum_costs[4] + (new_kwh - 400) * prices[5]
        
    tiet_kiem_thang_vat = bill_input - (new_pre_vat_bill * (1 + vat_rate/100))
    tiet_kiem_nam_vat = tiet_kiem_thang_vat * 12
    roi_years = de_xuat_data["gia"] / tiet_kiem_nam_vat if tiet_kiem_nam_vat > 0 else 99
    
    st.markdown(f"""
    <div class="metric-card" style="margin-top:15px; border-left-color: #0F2E59;">
        <div style="font-weight:bold; color:#0F2E59; margin-bottom:5px;">💵 BÀI TOÁN HOÀN VỐN (DỰ KIẾN)</div>
        • <b>Tiền tiết kiệm hàng tháng:</b> ~{tiet_kiem_thang_vat:,.0f} VNĐ<br>
        • <b>Tiền tiết kiệm hàng năm:</b> ~{tiet_kiem_nam_vat:,.0f} VNĐ<br>
        • <b>Thời gian hòa vốn thực tế:</b> ~<b>{roi_years:.1f} năm</b> (Sau thời gian này, khách hàng sử dụng điện MIỄN PHÍ suốt hơn 20 năm tiếp theo).
    </div>
    """, unsafe_allowed_html=True)

# --- TAB 2: CHI TIẾT GÓI LẮP ĐẶT ---
with tab2:
    st.markdown('<div class="section-header">Bảng tra cứu thông số vật tư & đơn giá</div>', unsafe_allowed_html=True)
    
    # Chuyển đổi dict sang DataFrame để hiển thị đẹp mắt
    df_goi = pd.DataFrame([
        {
            "Mã Gói": name,
            "Công Suất (kWp)": d["kwp"],
            "SL Tấm Pin (580W)": f"{d['tam_pin']} tấm",
            "Bình Lưu Trữ": d["pin_lt"],
            "Biến Tần (Inverter)": d["inverter"],
            "Phù hợp hóa đơn": d["phu_hop"],
            "Giá Trọn Gói (VNĐ)": f"{d['gia']:,}đ"
        }
        for name, d in GOI_SOLAR.items()
    ])
    st.dataframe(df_goi, use_container_width=True, hide_index=True)
    
    # Công cụ tính nhanh kWp tùy chỉnh
    st.markdown('<div class="section-header">Tính sản lượng theo kWp tùy chỉnh</div>', unsafe_allowed_html=True)
    custom_kwp = st.number_input("Nhập tổng công suất giàn pin mong muốn (kWp):", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
    
    c_day = custom_kwp * 4.3 * 0.82
    c_month = custom_kwp * 4.3 * 30 * 0.82
    c_area = custom_kwp * 5.5 # trung bình 5-6m2 cho mỗi kwp
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.metric("Sản lượng ngày (trung bình)", f"{c_day:.1f} kWh")
    with col_c2:
        st.metric("Sản lượng tháng (dự kiến)", f"{c_month:.0f} kWh")
    with col_c3:
        st.metric("Diện tích mái cần thiết", f"~{c_area:.1f} m²")

# --- TAB 3: GÓI VAY SHINHAN BANK ---
with tab3:
    st.markdown('<div class="section-header">Bài toán trả góp Shinhan Bank (0.59%/tháng)</div>', unsafe_allowed_html=True)
    
    # Chọn gói lắp đặt để chạy bài toán trả góp
    selected_goi_repay = st.selectbox("Chọn gói lắp đặt để tính toán dòng tiền:", list(GOI_SOLAR.keys()), index=1)
    goi_rep_data = GOI_SOLAR[selected_goi_repay]
    gia_tri_he_thong = goi_rep_data["gia"]
    
    # Tính khoản vay tối đa (Shinhan tài trợ max 100M, và không vượt quá giá trị hệ thống)
    max_loan = min(100000000, gia_tri_he_thong)
    
    st.info(f"Hệ thống: **{selected_goi_repay}** — Giá trọn gói: **{gia_tri_he_thong:,} VNĐ**")
    
    # Thanh trượt chọn số tiền vay
    loan_amount = st.slider(
        "Nhập số tiền đăng ký vay qua Shinhan Bank (VNĐ):",
        min_value=10000000,
        max_value=max_loan,
        value=max_loan,
        step=5000000
    )
    
    doi_ung = gia_tri_he_thong - loan_amount
    
    st.markdown(f"""
    <div class="highlight-box" style="margin-top:0px; margin-bottom:15px;">
        • <b>Số tiền khách hàng Trả Trước:</b> <span style="color:#D4AF37; font-weight:bold;">{doi_ung:,} VNĐ</span> {"(Đặc quyền: TRẢ TRƯỚC 0 ĐỒNG!)" if doi_ung == 0 else ""}<br>
        • <b>Số tiền Ngân hàng giải ngân:</b> <span style="color:#0F2E59; font-weight:bold;">{loan_amount:,} VNĐ</span>
    </div>
    """, unsafe_allowed_html=True)
    
    # Tính toán bảng trả góp chi tiết
    ki_han_list = [12, 24, 36, 48]
    lai_flat_thang = 0.59 / 100 # Lãi suất phẳng 0.59%/tháng
    
    records = []
    for m in ki_han_list:
        goc_hang_thang = loan_amount / m
        lai_hang_thang = loan_amount * lai_flat_thang
        tong_gop_thang = goc_hang_thang + lai_hang_thang
        tong_lai_suot_ky = lai_hang_thang * m
        tong_goc_lai = loan_amount + tong_lai_suot_ky
        
        records.append({
            "Kỳ hạn": f"{m} tháng",
            "Gốc hàng tháng": f"{goc_hang_thang:,.0f}đ",
            "Lãi hàng tháng": f"{lai_hang_thang:,.0f}đ",
            "Tổng góp/tháng": f"{tong_gop_thang:,.0f}đ",
            "Tổng tiền lãi": f"{tong_lai_suot_ky:,.0f}đ",
            "Tổng Gốc + Lãi": f"{tong_goc_lai:,.0f}đ"
        })
        
    df_repay = pd.DataFrame(records)
    st.dataframe(df_repay, use_container_width=True, hide_index=True)
    
    # Kịch bản so sánh dòng tiền
    st.markdown('<div class="section-header">Kịch bản tư vấn: Lấy tiền điện trả tiền góp</div>', unsafe_allowed_html=True)
    
    # Ước tính số tiền điện tiết kiệm được của gói này
    c_month_rep = goi_rep_data["kwp"] * 4.3 * 30 * 0.82
    # Tính số tiền điện trước thuế được giảm từ lượng c_month_rep kWh này (giả định giảm toàn ở bậc cao 3,350đ hoặc 3,460đ)
    avg_price_2026 = 3350 # Lấy bậc 5 làm trung bình tính nhanh
    money_saved_rep = c_month_rep * avg_price_2026 * 1.1 # gồm VAT 10%
    
    st.write(f"👉 Ước tính hệ thống giúp gia đình tiết kiệm khoảng: **{money_saved_rep:,.0f} VNĐ/tháng** tiền điện.")
    
    # Chọn một kỳ hạn để làm ví dụ thực tế cho khách
    kihan_select = st.selectbox("Chọn kỳ hạn để đối chiếu dòng tiền thực tế:", [24, 36, 48], index=2)
    
    g_thang = loan_amount / kihan_select
    l_thang = loan_amount * lai_flat_thang
    total_gop = g_thang + l_thang
    chenh_lech = money_saved_rep - total_gop
    
    if chenh_lech >= 0:
        st.markdown(f"""
        <div class="highlight-box" style="background-color: #E6F4EA; border-color: #34A853;">
            <span style="color:#137333; font-weight:bold;">🎉 PHƯƠNG ÁN DÒNG TIỀN DƯ (THẶNG DƯ TÀI CHÍNH!)</span><br>
            • Khách hàng góp ngân hàng: <b>{total_gop:,.0f} VNĐ/tháng</b><br>
            • Số tiền điện tiết kiệm được: <b>{money_saved_rep:,.0f} VNĐ/tháng</b><br>
            👉 <b>Kết luận:</b> Khách hàng không cần bù thêm tiền túi, ngược lại mỗi tháng còn <b>dư ra {chenh_lech:,.0f} VNĐ</b> bỏ túi!
        </div>
        """, unsafe_allowed_html=True)
    else:
        st.markdown(f"""
        <div class="highlight-box" style="background-color: #FFFDF0; border-color: #D4AF37;">
            <span style="color:#B06000; font-weight:bold;">⚖️ PHƯƠNG ÁN BÙ CHÊNH LỆCH NHỎ</span><br>
            • Khách hàng góp ngân hàng: <b>{total_gop:,.0f} VNĐ/tháng</b><br>
            • Số tiền điện tiết kiệm được: <b>{money_saved_rep:,.0f} VNĐ/tháng</b><br>
            👉 <b>Kết luận:</b> Mỗi tháng khách chỉ cần bù thêm khoảng <b>{abs(chenh_lech):,.0f} VNĐ</b> tiền túi (bằng vài ly cà phê) để sở hữu trọn bộ hệ thống Hybrid trị giá trăm triệu!
        </div>
        """, unsafe_allowed_html=True)

# Footer chân trang chuyên nghiệp
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #555555; font-size: 11px;">
    <b>CÔNG TY TNHH TMDV SOLAR 24H</b><br>
    🏢 Vòng xoay Quảng Trường Mỹ Tho, Phường Đạo Thạnh, Tỉnh Đồng Tháp / Mỹ Tho<br>
    📞 Hotline hỗ trợ kỹ thuật & tư vấn: 0909.363.579 - 0896.488.299<br>
    💻 <i>Cung cấp giải pháp năng lượng sạch tối ưu, chuyên nghiệp và tận tâm.</i>
</div>
""", unsafe_allowed_html=True)

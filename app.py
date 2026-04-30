import streamlit as st
import datetime
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="AyamKu 2026",
    layout="wide"
)

# =========================
# STYLE (CREME + ANIMATION)
# =========================
st.markdown("""
<style>
body {
    background-color: #fdf6e3;
}

.stApp {
    background: linear-gradient(135deg, #fdf6e3, #fceabb);
}

/* animasi fade */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

.block-container {
    animation: fadeIn 0.7s ease-in-out;
}

/* card style */
.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# USER SYSTEM
# =========================
USERS = {
    "admin": {"password": "4dm1n", "role": "admin"},
    "krwn": {"password": "k4ry4w4n", "role": "karyawan"}
}

# =========================
# SESSION INIT
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.kandang = []
    st.session_state.kirim = []

# =========================
# LOGIN
# =========================
def login():
    st.markdown("<h1 style='text-align:center;'>🐔 AyamKu 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Sistem Manajemen Peternakan Modern</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.button("Masuk", use_container_width=True):
            data = USERS.get(user)
            if data and data["password"] == pw:
                st.session_state.login = True
                st.session_state.user = user
                st.session_state.role = data["role"]
                st.rerun()
            else:
                st.error("Login gagal")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
def sidebar():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user}")
        st.caption(st.session_state.role.upper())

        if st.session_state.role == "admin":
            menu = st.radio("Menu", ["Dashboard"])
        else:
            menu = st.radio("Menu", ["Input Kandang", "Input Pengiriman"])

        if st.button("Logout"):
            st.session_state.login = False
            st.rerun()

    return menu

# =========================
# ADMIN DASHBOARD
# =========================
def admin_dashboard():
    st.title("📊 Dashboard Admin")

    df_kandang = pd.DataFrame(st.session_state.kandang)
    df_kirim = pd.DataFrame(st.session_state.kirim)

    # ===== METRIC =====
    col1, col2, col3 = st.columns(3)

    hidup = df_kandang["hidup"].iloc[-1] if not df_kandang.empty else 0
    mati = df_kandang["mati"].sum() if not df_kandang.empty else 0
    kirim = df_kirim["jumlah"].sum() if not df_kirim.empty else 0

    col1.metric("🐔 Hidup", hidup)
    col2.metric("💀 Mati", mati)
    col3.metric("🚚 Kirim", kirim)

    st.divider()

    # ===== PIE CHART =====
    st.subheader("📊 Distribusi Ayam")

    if not df_kandang.empty:
        data = pd.DataFrame({
            "Kategori": ["Hidup", "Mati"],
            "Jumlah": [hidup, mati]
        })

        st.plotly_chart({
            "data": [{
                "labels": data["Kategori"],
                "values": data["Jumlah"],
                "type": "pie",
                "hole": 0.4
            }],
            "layout": {"title": "Komposisi Ayam"}
        })
    else:
        st.info("Belum ada data")

    # ===== TABLE =====
    st.subheader("📋 Data Kandang")
    if not df_kandang.empty:
        st.dataframe(df_kandang, use_container_width=True)
    else:
        st.info("Kosong")

    st.subheader("🚚 Data Pengiriman")
    if not df_kirim.empty:
        st.dataframe(df_kirim, use_container_width=True)
    else:
        st.info("Kosong")

# =========================
# INPUT KANDANG
# =========================
def input_kandang():
    st.title("🏠 Input Kandang")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        hidup = st.number_input("Jumlah Hidup", 0)
        mati = st.number_input("Jumlah Mati", 0)
        kondisi = st.selectbox("Kondisi", ["Baik", "Cukup", "Buruk"])

        if st.button("Simpan"):
            st.session_state.kandang.append({
                "tgl": str(datetime.date.today()),
                "hidup": hidup,
                "mati": mati,
                "kondisi": kondisi,
                "user": st.session_state.user
            })
            st.success("Data tersimpan!")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# INPUT PENGIRIMAN
# =========================
def input_pengiriman():
    st.title("🚚 Input Pengiriman")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        jumlah = st.number_input("Jumlah Ayam", 0)

        if st.button("Simpan"):
            st.session_state.kirim.append({
                "tgl": str(datetime.date.today()),
                "jumlah": jumlah,
                "user": st.session_state.user
            })
            st.success("Data tersimpan!")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MAIN
# =========================
if not st.session_state.login:
    login()
else:
    menu = sidebar()

    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        if menu == "Input Kandang":
            input_kandang()
        elif menu == "Input Pengiriman":
            input_pengiriman()

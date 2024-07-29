import streamlit as st
import login_app
import main

# Mengatur layout halaman menjadi lebar
st.set_page_config(layout="wide")

# Mengakses file CSS untuk styling page
with open("css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Memastikan bahwa session_state sudah ada
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Memilih halaman yang akan ditampilkan berdasarkan status login
if st.session_state.logged_in:
    # Jika pengguna sudah login, tampilkan halaman utama
    main.main()
else:
    # Jika pengguna belum login, tampilkan halaman login
    login_app.login_section()

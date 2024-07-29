import streamlit as st
import mysql.connector
from datetime import datetime

# Fungsi untuk membuat koneksi ke database MySQL
def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="uas_bp",
        )
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        st.stop()


# Fungsi untuk mengecek kredensial login
def check_login(name, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM tb_account WHERE name = %s", (name,))
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Database query error: {err}")
        result = None
    finally:
        cursor.close()
        conn.close()
    return result and password == result[0]


# Fungsi untuk menampilkan halaman login
def login_section():
    """
    Menampilkan halaman login dengan batas percobaan login.
    """
    st.title("Halaman Login")

    # Inisialisasi jumlah percobaan login
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0

    # Memeriksa apakah batas percobaan login sudah tercapai
    if st.session_state.login_attempts >= 3:
        st.error("Anda telah mencapai batas percobaan login.")
        return

    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        name = st.text_input("Nama Lengkap")
        password = st.text_input("Password", type="password")

    # Validasi panjang password dan menentukan semester
    if len(password) >= 4 and password[:4].isdigit():
        start_year = int(password[:4])
        current_semester = get_current_semester(start_year)
    else:
        start_year = None
        current_semester = None

    if st.button("Log in"):
        if start_year is None:
            st.error("Password harus terdiri dari setidaknya 11 digit yang valid.")
        elif check_login(name, password):
            st.session_state.logged_in = True
            st.session_state.login_attempts = 0
            st.session_state.user_name = name  # Simpan nama pengguna di session state
            st.session_state.current_semester = (
                current_semester  # Simpan current_semester di session state
            )
            st.experimental_rerun()  # Refresh untuk menerapkan perubahan
        else:
            st.session_state.login_attempts += 1
            st.error(
                f"Login gagal! Percobaan ke-{st.session_state.login_attempts} dari 3"
            )

# Fungsi untuk menghitung semester saat ini
def get_current_semester(start_year):
    current_year = datetime.now().year
    current_month = datetime.now().month
    years_passed = current_year - start_year
    if current_month < 7:  # Semester genap
        return years_passed * 2 + 2
    else:  # Semester ganjil
        return years_passed * 2 + 1


if __name__ == "__main__":
    login_section()

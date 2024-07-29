import streamlit as st
import pandas as pd
import main
import login_app

# Mengakses file CSS untuk styling page
with open("css/pages.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Memeriksa login pengguna dan menampilkan sidebar
main.check_login()
main.sidebar()

# Mendapatkan semester saat ini dari session state
current_semester = st.session_state.get("current_semester", "Tidak diketahui")

# Mendapatkan koneksi ke database dan cursor
conn = login_app.get_connection()
cursor = conn.cursor(dictionary=True)

# Mengambil jadwal kuliah untuk semester saat ini
cursor.execute(
    "SELECT mata_kuliah, hari, jam, kelas FROM tb_jadwal_kuliah WHERE semester = %s",
    (current_semester,),
)
jadwal = cursor.fetchall()

# Mengambil informasi kelas pengganti
cursor.execute("SELECT hari, tanggal, mata_kuliah FROM tb_info_kelas_pengganti")
kelas_pengganti = cursor.fetchall()

# Menampilkan tombol untuk kembali ke halaman utama
if st.button("Kembali"):
    st.switch_page("Beranda.py")

# Menampilkan subjudul
st.subheader(f"Jadwal Perkuliahan di Semester {current_semester}")

# Mengonversi hasil query menjadi DataFrame
jadwal_df = pd.DataFrame(jadwal)
kelas_pengganti_df = pd.DataFrame(kelas_pengganti)

# Mengganti nama header pada tabel
jadwal_df.columns = ["Mata Kuliah", "Hari", "Jam", "Kelas"]
kelas_pengganti_df.columns = ["Hari", "Tanggal", "Mata Kuliah"]

# Menampilkan tabel jadwal kuliah dan informasi kelas pengganti
with st.container(border=True):
    jadwal_column, kelasPengganti_column = st.columns(2)
    with jadwal_column:
        st.write("Tabel Jadwal Perkuliahan")
        st.dataframe(jadwal_df, hide_index=True)

    with kelasPengganti_column:
        st.write("Informasi tentang Kelas Pengganti")
        with st.expander("Klik disini"):
            st.dataframe(kelas_pengganti_df, hide_index=True)

# Menutup koneksi ke database
cursor.close()
conn.close()

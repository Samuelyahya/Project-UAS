import streamlit as st
import plotly.express as px
import pandas as pd
import main
import login_app

# Mengakses file CSS untuk styling page
with open("css/pages.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Memeriksa login user dan menampilkan sidebar
main.check_login()
main.sidebar()

# Mendapatkan username dari session state
username = st.session_state.user_name

# Mendapatkan semester saat ini dari session state
current_semester = st.session_state.get("current_semester", "Tidak diketahui")

# Mendapatkan koneksi ke database dan cursor
conn = login_app.get_connection()
cursor = conn.cursor(dictionary=True)


# Fungsi untuk mendapatkan SKS yang diambil di setiap semester hingga current_semester
def get_sks_per_semester(current_semester):
    # Mengambil nama tabel berdasarkan username yang diinput
    table_name = f"tb_nilai_{username.lower().replace(' ', '_')}"
    query = f"""
    SELECT semester, SUM(sks) as total_sks 
    FROM {table_name} 
    WHERE semester <= %s 
    GROUP BY semester 
    ORDER BY semester
    """
    cursor.execute(query, (current_semester,))
    return cursor.fetchall()


# Mengambil mata kuliah kuliah untuk semester saat ini
cursor.execute(
    "SELECT nama, sks, semester FROM tb_mata_kuliah WHERE semester = %s",
    (current_semester,),
)
mata_kuliah = cursor.fetchall()

# Mengambil SKS per semester hingga semester saat ini
sks_per_semester = get_sks_per_semester(current_semester)

# Menampilkan tombol untuk kembali ke halaman utama
if st.button("Kembali"):
    st.switch_page("Beranda.py")

# Menampilkan subjudul dan tabel mata kuliah
st.subheader(f"Daftar Mata Kuliah di Semester {current_semester}")
with st.container(border=True):
    col1, col2 = st.columns([4, 6])

    with col1:
        st.write(f"Tabel Mata Kuliah di Semester {current_semester}")
        matkul_df = pd.DataFrame(mata_kuliah)
        matkul_df.columns = ["Mata Kuliah", "SKS", "Semester"]
        st.dataframe(matkul_df, hide_index=True)

    with col2:
        # Membuat grafik SKS per semester menggunakan Plotly
        semesters = [int(record["semester"]) for record in sks_per_semester]
        sks = [record["total_sks"] for record in sks_per_semester]

        fig = px.line(
            x=semesters,
            y=sks,
            labels={"x": "Semester", "y": "Total SKS"},
            title="Grafik SKS per Semester",
        )
        st.plotly_chart(fig)

# Menutup koneksi ke database
cursor.close()
conn.close()

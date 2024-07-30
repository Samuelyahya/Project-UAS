import streamlit as st
import plotly.express as px
import pandas as pd
import main
import login_app

# Mengakses file CSS untuk styling page
with open("css/pages.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Memeriksa login dan menampilkan sidebar
main.check_login()
main.sidebar()

# Mendapatkan username dari session state
username = st.session_state.user_name

# Mendapatkan semester saat ini dari session state
current_semester = st.session_state.get("current_semester", "Tidak diketahui")

# Membuat daftar semester dari 1 hingga current_semester
available_semesters = [str(i) for i in range(1, int(current_semester) + 1)]

# Membuka koneksi ke database
conn = login_app.get_connection()
cursor = conn.cursor(dictionary=True)


# Fungsi untuk menghitung IPK berdasarkan nilai yang ada
def calculate_ipk(matkul):
    total_nilai = 0
    for mk in matkul:
        if mk["nilai"] == "A":
            total_nilai += 4.00
        elif mk["nilai"] == "A-":
            total_nilai += 3.67
        elif mk["nilai"] == "B+":
            total_nilai += 3.33
        elif mk["nilai"] == "B":
            total_nilai += 3.00
        elif mk["nilai"] == "B-":
            total_nilai += 2.67
        elif mk["nilai"] == "C+":
            total_nilai += 2.33
        elif mk["nilai"] == "C":
            total_nilai += 2.00
        elif mk["nilai"] == "C-":
            total_nilai += 1.67
        elif mk["nilai"] == "D":
            total_nilai += 1.00
        elif mk["nilai"] == "E":
            total_nilai += 0.00
    return total_nilai / len(matkul) if matkul else 0


# Fungsi untuk menghitung IPK berdasarkan nilai yang ada
def cumulative_IPK(matkul):
    total_nilai = 0
    total_sks = 0
    nilai_to_sks = {
        "A": 4.00,
        "A-": 3.67,
        "B+": 3.33,
        "B": 3.00,
        "B-": 2.67,
        "C+": 2.33,
        "C": 2.00,
        "C-": 1.67,
        "D": 1.00,
        "E": 0.00,
    }
    for mk in matkul:
        nilai = mk["nilai"]
        sks = mk.get("sks", 3)  # Misalkan default SKS adalah 3 jika tidak tersedia
        total_nilai += nilai_to_sks.get(nilai, 0) * sks
        total_sks += sks
    return total_nilai / total_sks if total_sks > 0 else 0


# Fungsi untuk mendapatkan mata kuliah dan nilai untuk semester tertentu
def get_matkul_with_grades(semester):
    table_name = f"tb_nilai_{username.lower().replace(' ', '_')}"
    query = f"SELECT mata_kuliah, nilai FROM {table_name} WHERE semester = %s"
    cursor.execute(query, (semester,))
    return cursor.fetchall()


# Menghitung IPK untuk setiap semester
ipk_per_semester = []
for semester in available_semesters:
    matkul = get_matkul_with_grades(semester)
    ipk = calculate_ipk(matkul)
    ipk_per_semester.append((semester, ipk))

# Menghitung IPK untuk setiap semester dan mengumpulkan data untuk IPK kumulatif
matkul_all_semesters = []
for semester in available_semesters:
    matkul = get_matkul_with_grades(semester)
    matkul_all_semesters.extend(matkul)

ipk_cumulative = cumulative_IPK(matkul_all_semesters)


if st.button("Kembali"):
    st.switch_page("Beranda.py")

# Menggunakan selectbox untuk memilih semester
selected_semester = st.selectbox(
    "Pilih Semester", available_semesters, index=len(available_semesters) - 1
)

matkul = get_matkul_with_grades(selected_semester)
# Menampilkan IPK untuk semester yang dipilih
ipk = calculate_ipk(matkul)

# Menampilkan daftar mata kuliah dengan nilai sesuai aturan
st.subheader(f"Daftar Nilai di Semester {selected_semester}")
with st.container(border=True):
    col1, col2 = st.columns([4, 8], gap="small")
    with col1:
        st.write(f"Tabel Nilai Perkuliahan")
        matkul_df = pd.DataFrame(matkul)
        matkul_df.columns = ["Mata Kuliah", "Nilai"]
        st.dataframe(matkul_df, hide_index=True)
        st.write(f"IP kamu di semester {selected_semester} adalah: {ipk:.2f}")
        st.write(f"IPK kamu adalah: {ipk_cumulative:.2f}")

    with col2:
        # Membuat chart IPK per semester menggunakan plotly
        semesters = [int(s[0]) for s in ipk_per_semester]
        ipks = [s[1] for s in ipk_per_semester]

        fig = px.line(
            x=semesters,
            y=ipks,
            labels={"x": "Semester", "y": "IPS"},
            title="Grafik IPS Mahasiswa",
        )
        st.plotly_chart(fig)

# Menutup koneksi ke database
cursor.close()
conn.close()

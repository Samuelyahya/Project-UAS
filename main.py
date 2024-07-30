import streamlit as st

# Mengecek apakah pengguna sudah login
def check_login():
    """
    Memeriksa status login pengguna. Jika pengguna belum login, tampilkan pesan error dan hentikan eksekusi.
    """
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Mohon untuk log in terlebih dahulu.")
        st.stop()

# Fungsi utama untuk menampilkan konten halaman setelah login
def main():
    # Tampilkan pesan selamat datang dengan nama pengguna
    user_name = st.session_state.get("user_name", "Pengguna")
    st.subheader(f"Selamat datang, {user_name}!")

    # Menampilkan semester saat ini
    current_semester = st.session_state.get("current_semester", "Tidak diketahui")
    st.write(f"Semester saat ini: {current_semester}")

    # Menyusun layout dengan 3 kolom
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True, height=None):
            st.subheader("Daftar Mata Kuliah")
            st.image('img/subject.png')
            if st.button("Lihat Mata Kuliah"):
                st.switch_page("pages/1_Daftar_Mata_Kuliah.py")

    with col2:
        with st.container(border=True, height=None):
            st.subheader("Jadwal Kuliah")
            st.image("img/schedule.png")
            if st.button("Lihat Jadwal Perkuliahan"):
                st.switch_page("pages/2_Jadwal_Perkuliahan.py")

    with col3:
        with st.container(border=True, height=None):
            st.subheader("Daftar Nilai")
            st.image("img/grade.png")
            if st.button("Lihat Daftar Nilai"):
                st.switch_page("pages/3_Daftar_Nilai_dan_IPK.py")

    # Menampilkan sidebar
    sidebar()


def sidebar():
    """
    Menampilkan sidebar dengan tombol logout.
    """
    with st.sidebar:
        if st.button("Log out"):
            st.session_state.logged_in = False  # Set status login menjadi False
            st.session_state.user_name = ""  # Hapus nama pengguna dari session state
            st.experimental_rerun()  # Refresh untuk menerapkan perubahan


if __name__ == "__main__":
    check_login()  # Memastikan pengguna sudah login sebelum menampilkan halaman utama
    main()

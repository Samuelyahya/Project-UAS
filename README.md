# Aplikasi Login dan Dashboard Perkuliahan dengan Streamlit

Aplikasi ini adalah sebuah sistem login dan dashboard perkuliahan yang dibangun menggunakan Streamlit dan MySQL. Aplikasi ini memungkinkan pengguna untuk masuk dengan kredensial mereka, melihat mata kuliah yang terdaftar, jadwal kuliah, dan daftar nilai mereka.

## Struktur Proyek

Proyek ini terdiri dari beberapa file Python yang saling berinteraksi. Berikut adalah struktur file dan deskripsi singkatnya:

### 1. `login_app.py`
File ini berisi logika untuk menghubungkan ke database MySQL, memeriksa kredensial login, dan menampilkan halaman login. 

**Fungsi Utama:**
- `get_connection()`: Membuat koneksi ke database MySQL.
- `check_login(name, password)`: Memeriksa kredensial login pengguna.
- `login_section()`: Menampilkan halaman login.

### 2. `main.py`
File ini menampilkan halaman utama setelah pengguna login. Halaman ini menyediakan akses ke berbagai bagian seperti daftar mata kuliah, jadwal kuliah, dan daftar nilai.

**Fungsi Utama:**
- `check_login()`: Memeriksa status login pengguna.
- `main()`: Menampilkan konten utama halaman setelah login.
- `sidebar()`: Menampilkan sidebar dengan tombol logout.

### 3. `1_Daftar_Mata_Kuliah.py`
Menampilkan daftar mata kuliah untuk semester saat ini dan grafik SKS per semester.

**Fungsi Utama:**
- Menampilkan tabel mata kuliah.
- Menampilkan grafik SKS per semester.

### 4. `2_Jadwal_Perkuliahan.py`
Menampilkan jadwal kuliah dan informasi tentang kelas pengganti untuk semester saat ini.

**Fungsi Utama:**
- Menampilkan jadwal kuliah.
- Menampilkan informasi tentang kelas pengganti.

### 5. `3_Daftar_Nilai_dan_IPK.py`
Menampilkan daftar nilai dan IPK untuk setiap semester. Menggunakan grafik untuk menampilkan IPK per semester.

**Fungsi Utama:**
- Menampilkan tabel nilai perkuliahan.
- Menampilkan grafik IPK per semester.

### 6. `Beranda.py`
File utama yang menentukan halaman mana yang akan ditampilkan berdasarkan status login. Jika pengguna sudah login, halaman utama akan ditampilkan; jika belum, halaman login akan ditampilkan.

## Instalasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/Samuelyahya/Project-UAS.git
   ```

2. Masuk ke direktori proyek:
   ```bash
   cd repository
   ```

3. Instal dependensi yang diperlukan:
    ```bash
   pip install -r requirements.txt
    ```

4. Pastikan MySQL server sedang berjalan dan telah mengonfigurasi database dengan tabel yang sesuai.

## Penggunaan

1. Jalankan aplikasi dengan perintah:
   ```bash
   streamlit run Beranda.py
   ```

2. Akses aplikasi di browser melalui URL yang ditampilkan di terminal.

## Struktur Database
Database MySQL yang digunakan harus memiliki tabel berikut:

- **tb_account**: Tabel untuk kredensial login.
- **tb_mata_kuliah**: Tabel untuk daftar mata kuliah.
- **tb_jadwal_kuliah**: Tabel untuk jadwal kuliah.
- **tb_nilai_{username}**: Tabel untuk nilai perkuliahan pengguna.
- **tb_info_kelas_pengganti**: Tabel untuk informasi kelas pengganti.

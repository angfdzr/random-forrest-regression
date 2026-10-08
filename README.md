# 🐟 Prediksi Harga Rata-Rata Ikan di Provinsi Banten dengan Random Forest Regression

Proyek Data Mining untuk memprediksi **Harga Rata-Rata Tertimbang ikan (Rp/kg)** di wilayah Provinsi Banten menggunakan algoritma **Random Forest Regression**, lengkap dengan antarmuka web sederhana berbasis **Flask** agar model dapat dicoba langsung.

Sumber data: **Kementerian Kelautan dan Perikanan (KKP)**.

---

## 📌 Latar Belakang

Harga ikan dipengaruhi banyak faktor, seperti jenis ikan, wilayah, volume produksi, dan nilai produksi. Proyek ini membangun model regresi yang mempelajari pola dari data produksi perikanan tahun 2019–2023 untuk memperkirakan harga rata-rata ikan per kilogram.

## 📊 Dataset

| Keterangan | Detail |
|---|---|
| Sumber | KKP (Kementerian Kelautan dan Perikanan) |
| Wilayah | Provinsi Banten |
| Periode | 2019 – 2023 |
| Format | 5 file CSV yang digabung menjadi satu DataFrame |
| Target | `Harga Rata-Rata Tertimbang (Rp/kg)` |

**Wilayah yang tercakup:** Kota Cilegon, Kota Serang, Lebak, Pandeglang, Serang (Kabupaten), dan Tangerang.

**Fitur yang digunakan model:**

| Fitur | Keterangan |
|---|---|
| `Tahun` | Tahun data produksi |
| `Kabupaten Kota` | Kabupaten/kota (hasil label encoding) |
| `Jenis Ikan (kode)` | Jenis ikan (hasil label encoding) |
| `Volume (ton)` | Volume produksi dalam ton |
| `Nilai (Rp. Juta)` | Nilai produksi dalam jutaan rupiah |

## ⚙️ Alur Pengerjaan

1. **Pengumpulan data**: menggabungkan 5 file CSV hasil permintaan data dari KKP.
2. **Pembersihan data**: menghapus karakter `;` dan mengubah koma desimal menjadi titik, mengonversi kolom ke numerik, lalu membuang baris yang bernilai kosong (*missing values*).
3. **Encoding**: mengubah `Kabupaten/Kota` dan `Jenis Ikan` menjadi kode numerik (label encoding).
4. **Eksplorasi data (EDA)**: distribusi data per kabupaten, jenis ikan, dan tahun; visualisasi *missing values*; boxplot untuk melihat outlier; perbandingan distribusi sebelum dan sesudah standarisasi.
5. **Pembagian data**: 80% data latih dan 20% data uji (`random_state=42`).
6. **Pemodelan**: `RandomForestRegressor` dengan *hyperparameter tuning* menggunakan `GridSearchCV` (5-fold cross validation, skor `R²`).
7. **Evaluasi**: `R²` dan `RMSE` pada data uji, plot aktual vs prediksi, serta *feature importance*.
8. **Deployment**: model dan mapping disimpan dengan `joblib`, lalu dipakai oleh aplikasi web Flask.

### Hyperparameter Tuning

| Parameter | Nilai yang Dicoba |
|---|---|
| `n_estimators` | 50, 100, 200 |
| `max_depth` | 5, 10, 15 |
| `min_samples_split` | 2, 5 |
| `min_samples_leaf` | 1, 2, 4 |

**Parameter terbaik:** `n_estimators=50`, `max_depth=15`, `min_samples_split=2`, `min_samples_leaf=1`

## 📈 Hasil Evaluasi

| Metrik | Nilai |
|---|---|
| **R² Score** | **0,9194** |
| **RMSE** | **≈ 11.925,54 Rp/kg** |

Model mampu menjelaskan sekitar **91,9%** variasi harga ikan pada data uji.

## 🖥️ Aplikasi Web

Aplikasi dibuat dengan Flask. Pengguna mengisi:

- Tahun
- Kabupaten/Kota
- Jenis Ikan
- Volume (ton)
- Nilai (Rp. Juta)

lalu menekan tombol **Prediksi** untuk melihat estimasi harga rata-rata ikan dalam Rp/kg.

## 📁 Struktur Proyek

```
random-forrest-regression/
├── RFR_Ikan_91.ipynb      # Notebook: preprocessing, EDA, training, evaluasi
├── app.py                 # Aplikasi web Flask
├── model_rfr.pkl          # Model Random Forest terlatih
├── mappings.pkl           # Mapping kode jenis ikan & kabupaten/kota
├── templates/
│   └── index.html         # Tampilan form prediksi
└── static/
    └── KKP.jpg            # Logo KKP
```

> **Catatan:** Flask membaca `index.html` dari folder `templates/`, dan gambar dari folder `static/`.

## 🚀 Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/angfdzr/random-forrest-regression.git
cd random-forrest-regression
```

### 2. (Opsional) Buat virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependensi

```bash
pip install flask pandas numpy scikit-learn joblib matplotlib seaborn
```

### 4. Jalankan aplikasi

```bash
python app.py
```

Buka browser dan akses **http://127.0.0.1:5000**.

### Menjalankan ulang notebook

Buka `RFR_Ikan_91.ipynb` dengan Jupyter Notebook / VS Code, lalu sesuaikan path file CSV pada sel pertama dengan lokasi dataset di komputer Anda. Pastikan nama file model hasil `joblib.dump` sama dengan yang dimuat di `app.py` (`model_rfr.pkl`).

## 🛠️ Teknologi yang Digunakan

- **Python 3.11**
- **pandas** & **NumPy**: pengolahan data
- **scikit-learn**: Random Forest Regressor, GridSearchCV, metrik evaluasi
- **matplotlib** & **seaborn**: visualisasi
- **joblib**: menyimpan model dan mapping
- **Flask**: aplikasi web
- **HTML & CSS**: antarmuka pengguna

## ⚠️ Keterbatasan

- Data hanya mencakup **Provinsi Banten** periode **2019–2023**, sehingga prediksi di luar cakupan ini kurang andal.
- Model memakai `Nilai (Rp. Juta)` sebagai salah satu fitur. Nilai produksi berkaitan langsung dengan harga (nilai ÷ volume), sehingga fitur ini sangat berpengaruh terhadap hasil prediksi.
- Label encoding memberi urutan angka pada kategori yang sebenarnya tidak berurutan; pengembangan lanjutan dapat mencoba *one-hot encoding* atau model lain.

## 👤 Penulis

**Angga Fadzar**
Mahasiswa, Tugas UAS Mata Kuliah Data Mining (Semester 4)

---

*Sumber data: Kementerian Kelautan dan Perikanan (KKP).*

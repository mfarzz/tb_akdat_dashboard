# Analisis Segmentasi Konten Hoaks di Indonesia

Dashboard interaktif untuk menganalisis dan memvisualisasikan konten hoaks di Indonesia dengan fokus pada segmentasi topik, persebaran geografis, platform media, dan pola temporal.

## 📊 Storytelling Dashboard

### Alur Cerita Visualisasi

Dashboard ini dirancang dengan pendekatan **data storytelling** yang menghubungkan berbagai dimensi analisis hoaks melalui visualisasi interaktif. Setiap visualisasi saling terhubung dan mempengaruhi satu sama lain, menciptakan narasi yang kohesif tentang karakteristik hoaks di Indonesia.

#### 1. **Executive Overview (KPI Cards)**
Dashboard dimulai dengan **6 KPI cards** yang memberikan gambaran umum:
- **Total Hoaks Terdeteksi**: Jumlah keseluruhan hoaks dalam database
- **Hoaks dengan Publikasi**: Hoaks yang memiliki tanggal publikasi
- **Hoaks tanpa Publikasi**: Hoaks tanpa informasi tanggal
- **Total Sumber Unik**: Jumlah platform/media unik yang menyebarkan hoaks
- **Rata-rata / hari**: Rata-rata hoaks per hari
- **Total Referensi**: Jumlah total referensi/klarifikasi yang tersedia

**Narasi**: KPI cards ini memberikan konteks awal tentang skala masalah hoaks di Indonesia.

#### 2. **DeepHoaxID Detector (Real-time Analysis)**
Sistem deteksi hoaks real-time yang terintegrasi dengan dashboard:
- User dapat memasukkan teks untuk dianalisis
- Sistem mengklasifikasikan teks sebagai HOAX, SUSPICIOUS, CLEAN, atau UNKNOWN
- **Hasil klasifikasi otomatis memfilter semua visualisasi** di dashboard
- Menampilkan artikel serupa dari database

**Narasi**: Detector ini menghubungkan analisis real-time dengan data historis, memungkinkan user melihat pola hoaks serupa yang pernah terjadi.

#### 3. **Tab 1: Segmentasi Topik**
**Pertanyaan yang dijawab**: "Apa tema-tema hoaks yang paling dominan?"

**Visualisasi**:
- **Top 10 Kategori**: Bar chart horizontal menunjukkan kategori hoaks terbanyak
- **Distribusi Top 10 Kategori**: Pie chart menunjukkan proporsi kategori
- **Top 10 Klasifikasi**: Bar chart vertikal untuk klasifikasi hoaks
- **Word Cloud**: Visualisasi kata kunci paling sering muncul dengan filtering stopwords yang komprehensif

**Koneksi dengan Visualisasi Lain**:
- Filter kategori/klasifikasi di sini → mempengaruhi **Persebaran Geografis** (tab 2)
- Filter kategori → mempengaruhi **Platform dan Media** (tab 3)
- Filter kategori → mempengaruhi **Pola dan Timeline** (tab 4)
- Word cloud mengungkapkan tema-tema utama yang dapat dikaitkan dengan lokasi dan platform tertentu

**Narasi**: Segmentasi topik adalah titik awal analisis. Setelah mengidentifikasi kategori dominan, user dapat mengeksplorasi di mana (lokasi) dan melalui apa (platform) kategori tersebut tersebar.

#### 4. **Tab 2: Persebaran Geografis**
**Pertanyaan yang dijawab**: "Di mana hoaks tersebar secara geografis?"

**Visualisasi**:
- **Top 15 Lokasi**: Bar chart horizontal lokasi dengan hoaks terbanyak
- **Distribusi Top 10 Lokasi**: Pie chart proporsi lokasi
- **Statistik Lokasi**: Metrics untuk total lokasi unik, lokasi teratas, dan jumlah hoaks
- **Tabel Detail**: Daftar lengkap persebaran lokasi

**Koneksi dengan Visualisasi Lain**:
- Filter lokasi di sini → mempengaruhi **Segmentasi Topik** (tab 1) - menunjukkan kategori hoaks dominan di lokasi tertentu
- Filter lokasi → mempengaruhi **Platform dan Media** (tab 3) - platform apa yang digunakan di lokasi tertentu
- Filter lokasi → mempengaruhi **Pola dan Timeline** (tab 4) - pola temporal hoaks di lokasi tertentu
- **Filter dari tab Segmentasi Topik** → mempengaruhi data di sini - menunjukkan di mana kategori hoaks tertentu dominan

**Narasi**: Setelah mengidentifikasi topik hoaks, analisis geografis mengungkapkan di mana hoaks tersebut paling aktif. Ini membantu memahami apakah ada pola regional dalam penyebaran hoaks tertentu.

#### 5. **Tab 3: Platform dan Media**
**Pertanyaan yang dijawab**: "Platform apa yang paling banyak digunakan untuk menyebarkan hoaks?"

**Visualisasi**:
- **Distribusi Platform**: Bar chart vertikal dengan color scale berdasarkan jumlah
- **Proporsi Platform**: Pie chart menunjukkan persentase setiap platform

**Koneksi dengan Visualisasi Lain**:
- Filter platform di sini → mempengaruhi **Segmentasi Topik** (tab 1) - kategori hoaks apa yang dominan di platform tertentu
- Filter platform → mempengaruhi **Persebaran Geografis** (tab 2) - lokasi mana yang aktif di platform tertentu
- Filter platform → mempengaruhi **Pola dan Timeline** (tab 4) - pola temporal penyebaran hoaks di platform tertentu
- **Filter dari tab sebelumnya** → mempengaruhi distribusi platform - mengungkapkan platform mana yang digunakan untuk kategori/lokasi tertentu

**Narasi**: Analisis platform mengidentifikasi saluran distribusi hoaks. Kombinasi dengan filter topik dan lokasi mengungkapkan pola penyebaran yang lebih kompleks, seperti platform tertentu yang lebih banyak menyebarkan kategori hoaks tertentu di lokasi tertentu.

#### 6. **Tab 4: Pola dan Timeline**
**Pertanyaan yang dijawab**: "Kapan hoaks terjadi dan bagaimana polanya?"

**Visualisasi**:
- **Perbandingan Timeline**: Line chart membandingkan tanggal publish artikel vs tanggal relevan hoax
  - Menunjukkan delay dalam pelaporan hoaks
  - Statistik: rata-rata delay, median delay, maksimum delay
  - Distribusi delay dalam histogram
- **Perbandingan Bulanan**: Bar chart grouped membandingkan distribusi bulanan berdasarkan publish date vs relevant date
- **Timeline Harian**: Line chart dengan markers menunjukkan tren harian
- **Distribusi Bulanan**: Bar chart distribusi hoaks per bulan
- **Pola Harian**: Bar chart menunjukkan hari dalam minggu dengan hoaks terbanyak

**Koneksi dengan Visualisasi Lain**:
- **Semua filter dari tab sebelumnya** → mempengaruhi timeline
  - Filter kategori → menunjukkan kapan kategori hoaks tertentu paling aktif
  - Filter lokasi → menunjukkan pola temporal hoaks di lokasi tertentu
  - Filter platform → menunjukkan waktu puncak penyebaran hoaks di platform tertentu
- Timeline mengungkapkan **waktu-waktu kritis** ketika hoaks paling banyak terjadi
- Delay analysis menunjukkan **efektivitas sistem klarifikasi** - semakin besar delay, semakin lama hoaks beredar sebelum ada klarifikasi

**Narasi**: Analisis temporal adalah puncak dari storytelling dashboard. Setelah memahami apa (topik), di mana (lokasi), dan melalui apa (platform), analisis waktu mengungkapkan kapan hoaks paling aktif dan seberapa cepat sistem merespons.

### Hubungan Antar Dimensi

Dashboard ini menghubungkan 4 dimensi utama:

1. **Topik → Lokasi**: Kategori hoaks tertentu lebih dominan di lokasi tertentu
2. **Topik → Platform**: Platform tertentu lebih banyak menyebarkan kategori hoaks tertentu
3. **Lokasi → Timeline**: Lokasi tertentu memiliki pola temporal yang berbeda
4. **Platform → Timeline**: Platform tertentu memiliki waktu puncak penyebaran yang berbeda
5. **Topik → Lokasi → Platform → Timeline**: Kombinasi semua dimensi mengungkapkan pola kompleks penyebaran hoaks

### Cross-Filtering Mechanism

Semua visualisasi menggunakan **satu dataframe terfilter** (`filtered_df`) yang sama, mirip dengan pola di `contoh.py`:
- Filter diterapkan sekali di awal
- Semua visualisasi menggunakan `filtered_df` yang sama
- Ketika user mengklik/drag pada chart, filter diupdate di `st.session_state.active_filters`
- Streamlit rerun, `filtered_df` dihitung ulang, semua visualisasi otomatis terupdate

## 🏗️ Overview Kodingan

### Struktur File

```
tb_dashboard/
├── app.py                          # Main dashboard application
├── README.md                       # Dokumentasi (file ini)
├── requirements.txt                # Dependencies
├── loaders/
│   └── article_loader.py           # Data loading dan enrichment
├── helpers/
│   ├── deephoaxid_wrapper.py      # Wrapper untuk DeepHoaxID system
│   ├── postgres_db_adapter.py     # PostgreSQL database adapter
│   ├── date_extractor.py          # Ekstraksi tanggal dari konten
│   └── location_extractor.py      # Ekstraksi lokasi dari konten
├── models/
│   ├── base.py                    # SQLAlchemy base
│   ├── entities.py                # Database models (Article, Category, dll)
│   └── reflect.py                 # Model reflection utilities
└── db/
    └── connection.py              # Database connection management
```

### Komponen Utama

#### 1. **app.py** - Main Dashboard Application

**Fungsi Utama**:
- `get_data()`: Load dan enrich data dari database dengan caching
- `extract_platform(url)`: Ekstrak platform dari URL
- Auto-initialization DeepHoaxID system
- Session state management untuk filters dan hoax system

**Struktur Aplikasi**:
1. **Setup & Initialization** (baris 1-58)
   - Import dependencies
   - Setup path untuk DeepHoaxID
   - Initialize session state
   - Auto-initialize DeepHoaxID system

2. **Data Loading** (baris 60-72)
   - Load data dari PostgreSQL
   - Enrich dengan dates dan locations
   - Convert datetime columns

3. **Date Range Filter** (baris 81-106)
   - Date input widget
   - Filter data berdasarkan tanggal
   - Gabungkan data dengan dan tanpa tanggal

4. **KPI Cards** (baris 108-172)
   - 6 KPI metrics
   - Helper functions untuk menghitung metrics
   - Custom CSS styling

5. **DeepHoaxID Detector** (baris 174-295)
   - Input text area
   - Analyze button
   - Display hasil analisis
   - Simpan hasil ke session state untuk filtering

6. **Filter Management** (baris 332-485)
   - Initialize `active_filters` di session state
   - Handle chart selections (box select/drag dan click)
   - Apply filters ke dataframe
   - Display filter summary dan clear button

7. **Visualizations** (baris 487-1270)
   - **Tab 1: Segmentasi Topik**
     - Categories bar chart dan pie chart
     - Classifications bar chart
     - Word cloud dengan filtering stopwords
   - **Tab 2: Persebaran Geografis**
     - Location bar chart dan pie chart
     - Location statistics
     - Location detail table
   - **Tab 3: Platform dan Media**
     - Platform bar chart dan pie chart
   - **Tab 4: Pola dan Timeline**
     - Timeline comparison (published_at vs relevant_date)
     - Daily timeline
     - Monthly distribution
     - Day of week pattern

**Pola Cross-Filtering**:
```python
# 1. Filter diterapkan sekali
filtered_df = shown_df.copy()
if st.session_state.active_filters.get('categories'):
    filtered_df = filtered_df[filtered_df["categories"].isin(...)]

# 2. Semua visualisasi menggunakan filtered_df yang sama
cat_counts = filtered_df["categories"].value_counts()
location_counts = filtered_df["relevant_location"].value_counts()
# ... dst

# 3. Chart selection update filter
if selected_data and "selection" in selected_data:
    st.session_state.active_filters['categories'] = selected_values
    st.rerun()  # Rerun → filtered_df dihitung ulang → semua chart terupdate
```

#### 2. **loaders/article_loader.py** - Data Loading

**Fungsi**:
- `load_articles_df()`: Load artikel dari PostgreSQL menggunakan adapter
- `enrich_with_dates(df)`: Tambahkan kolom `relevant_date` dengan ekstraksi tanggal
- `enrich_with_locations(df)`: Tambahkan kolom `relevant_location` dengan ekstraksi lokasi

**Alur Data**:
1. Load raw data dari PostgreSQL
2. Enrich dengan dates (ekstraksi tanggal dari konten)
3. Enrich dengan locations (ekstraksi lokasi dari konten)
4. Return enriched dataframe

#### 3. **helpers/deephoaxid_wrapper.py** - DeepHoaxID Integration

**Class**: `DeepHoaxIDPostgreSQLWrapper`

**Fungsi**:
- Wrapper untuk DeepHoaxID system yang menggunakan PostgreSQL
- `initialize()`: Initialize similarity engine dan load models
- `analyze_message(message)`: Analisis teks dan klasifikasi hoaks
- Handle database operations untuk similarity search

**Integrasi dengan Dashboard**:
- Auto-initialize saat aplikasi start
- Hasil analisis disimpan ke `st.session_state.last_hoax_result`
- Kategori hasil otomatis memfilter visualisasi

#### 4. **helpers/postgres_db_adapter.py** - Database Adapter

**Class**: `PostgreSQLDatabaseAdapter`

**Fungsi**:
- `load_hoax_articles()`: Load artikel dari PostgreSQL
- Convert SQLAlchemy models ke pandas DataFrame
- Handle relationships (categories, classifications, references)

#### 5. **helpers/date_extractor.py** - Date Extraction

**Fungsi**:
- `extract_dates_from_text(text)`: Ekstrak tanggal dari teks menggunakan regex
- Support berbagai format tanggal Indonesia
- Return tanggal yang paling relevan

#### 6. **helpers/location_extractor.py** - Location Extraction

**Fungsi**:
- `extract_locations_from_text(text)`: Ekstrak lokasi dari teks
- Pattern matching untuk provinsi dan kota di Indonesia
- Return lokasi yang paling relevan

#### 7. **models/entities.py** - Database Models

**Models**:
- `Article`: Model utama untuk artikel hoaks
- `Category`: Kategori hoaks
- `Classification`: Klasifikasi hoaks
- `ArticleReference`: Referensi/klarifikasi artikel

**Relationships**:
- Article ↔ Category (many-to-many)
- Article ↔ Classification (many-to-many)
- Article → ArticleReference (one-to-many)

### Alur Data

```
PostgreSQL Database
    ↓
PostgreSQLDatabaseAdapter (load_hoax_articles)
    ↓
pandas DataFrame (raw data)
    ↓
enrich_with_dates (extract dates from content)
    ↓
enrich_with_locations (extract locations from content)
    ↓
get_data() [cached]
    ↓
Date Range Filter
    ↓
shown_df (filtered by date)
    ↓
Active Filters (from chart selections + DeepHoaxID)
    ↓
filtered_df (applied all filters)
    ↓
All Visualizations (use filtered_df)
```

### Teknologi yang Digunakan

- **Streamlit**: Framework untuk dashboard web
- **Plotly Express**: Library untuk visualisasi interaktif
- **Pandas**: Data manipulation dan analysis
- **SQLAlchemy**: ORM untuk database operations
- **PostgreSQL**: Database untuk menyimpan data hoaks
- **Matplotlib**: Word cloud visualization
- **Sentence-BERT + FAISS**: Similarity search untuk DeepHoaxID
- **WordCloud**: Library untuk word cloud generation

### Fitur Utama

1. **Interactive Cross-Filtering**
   - Klik/drag pada chart untuk filter
   - Semua visualisasi terupdate otomatis
   - Filter dapat dikombinasikan

2. **Real-time Hoax Detection**
   - DeepHoaxID detector terintegrasi
   - Hasil analisis mempengaruhi visualisasi
   - Menampilkan artikel serupa

3. **Comprehensive Data Enrichment**
   - Ekstraksi tanggal dari konten
   - Ekstraksi lokasi dari konten
   - Platform extraction dari URL

4. **Advanced Word Cloud**
   - Filtering stopwords yang komprehensif
   - Filtering kata-kata tidak bermakna
   - Regex-based cleaning

5. **Timeline Analysis**
   - Perbandingan publish date vs relevant date
   - Delay analysis
   - Pola temporal (harian, bulanan, hari dalam minggu)

### Best Practices yang Diterapkan

1. **Caching**: `@st.cache_data` untuk data loading
2. **Session State**: Untuk maintain state across reruns
3. **Error Handling**: Try-except untuk semua operasi kritis
4. **Lazy Loading**: DeepHoaxID hanya di-load jika tersedia
5. **Single Source of Truth**: Satu `filtered_df` untuk semua visualisasi
6. **Modular Code**: Helper functions untuk reusability
7. **Type Safety**: Pandas operations dengan proper error handling

## 🚀 Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**:
   - Pastikan PostgreSQL sudah running
   - Update connection string di `db/connection.py`
   - Database schema sudah ada (lihat `models/entities.py`)

3. **Run Dashboard**:
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

1. **Pilih Rentang Tanggal**: Gunakan date input di kanan atas
2. **Analisis Teks**: Masukkan teks di DeepHoaxID Detector untuk analisis real-time
3. **Filter Interaktif**: Klik/drag pada chart untuk memfilter data
4. **Eksplorasi Tab**: Navigasi antar tab untuk melihat berbagai dimensi analisis
5. **Hapus Filter**: Gunakan tombol "Hapus Semua Filter" untuk reset

## 🔗 Dependencies

Lihat `requirements.txt` untuk daftar lengkap dependencies. Dependencies utama:
- streamlit
- pandas
- plotly
- sqlalchemy
- psycopg2
- wordcloud
- matplotlib
- sentence-transformers (untuk DeepHoaxID)
- faiss-cpu (untuk DeepHoaxID)

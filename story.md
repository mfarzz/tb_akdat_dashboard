# Storytelling Dashboard: Analisis Segmentasi Konten Hoaks di Indonesia

## 🎯 Opening: Masalah yang Kita Hadapi

**Pertanyaan Pembuka:**
"Berapa banyak hoaks yang beredar di Indonesia setiap harinya? Dan yang lebih penting, bagaimana kita bisa memahami pola penyebarannya untuk melawannya dengan lebih efektif?"

Hoaks bukan sekadar informasi salah. Hoaks adalah **fenomena kompleks** yang memiliki pola, karakteristik, dan dampak yang dapat dianalisis. Dashboard ini hadir untuk menjawab pertanyaan-pertanyaan kritis tentang hoaks di Indonesia melalui pendekatan data-driven.

---

## 📊 Act 1: Gambaran Besar (Executive Overview)

### KPI Cards: Skala Masalah

Mari kita mulai dengan **6 KPI cards** yang memberikan konteks awal:

1. **Total Hoaks Terdeteksi**: Ini adalah jumlah keseluruhan hoaks dalam database kita. Angka ini menunjukkan skala masalah yang kita hadapi.

2. **Hoaks dengan Publikasi vs Tanpa Publikasi**: Perbandingan ini mengungkapkan seberapa banyak hoaks yang memiliki metadata lengkap. Hoaks tanpa tanggal publikasi mungkin lebih sulit dilacak dan dianalisis.

3. **Total Sumber Unik**: Berapa banyak platform atau media yang terlibat dalam penyebaran hoaks? Angka ini menunjukkan diversitas saluran distribusi.

4. **Rata-rata per Hari**: Ini memberikan perspektif temporal - seberapa intensif masalah hoaks terjadi.

5. **Total Referensi**: Berapa banyak klarifikasi atau referensi yang tersedia? Ini menunjukkan upaya counter-narrative yang sudah dilakukan.

**Narasi Kunci:**
> "Angka-angka ini bukan sekadar statistik. Mereka adalah cerminan dari ekosistem informasi di Indonesia. Setiap hoaks yang terdeteksi adalah satu langkah menuju pemahaman yang lebih baik."

---

## 🔍 Act 2: Deteksi Real-time (DeepHoaxID Detector)

### Sistem Deteksi Cerdas

Dashboard ini dilengkapi dengan **DeepHoaxID Detector** - sistem deteksi hoaks real-time yang menggunakan teknologi AI canggih.

**Cara Kerja:**
- User memasukkan teks untuk dianalisis
- Sistem mengklasifikasikan teks sebagai:
  - **HOAX**: Konten yang teridentifikasi sebagai hoaks
  - **SUSPICIOUS**: Konten yang mencurigakan
  - **CLEAN**: Konten yang bersih
  - **UNKNOWN**: Tidak dapat diklasifikasikan

**Keunikan:**
Yang membuat sistem ini istimewa adalah **hasil klasifikasi otomatis memfilter semua visualisasi** di dashboard. Ini berarti:
- Jika kita mendeteksi hoaks tentang topik tertentu, kita langsung bisa melihat pola historis hoaks serupa
- Sistem menampilkan artikel-artikel serupa dari database
- Kita bisa melihat bagaimana hoaks serupa pernah tersebar sebelumnya

**Narasi Kunci:**
> "Ini bukan sekadar deteksi. Ini adalah koneksi antara masa kini dan masa lalu. Setiap hoaks baru yang terdeteksi langsung terhubung dengan pola historis, membantu kita memahami apakah ini adalah hoaks baru atau variasi dari hoaks yang sudah pernah terjadi."

---

## 📈 Act 3: Segmentasi Topik - "Apa yang Diserang?"

### Pertanyaan Utama:
**"Apa tema-tema hoaks yang paling dominan di Indonesia?"**

### Visualisasi yang Menjawab:

#### 1. Top 10 Kategori
Bar chart horizontal menunjukkan kategori hoaks terbanyak. Ini adalah **entry point** analisis kita.

**Insight yang Bisa Ditemukan:**
- Kategori mana yang paling banyak?
- Apakah ada dominasi kategori tertentu?
- Bagaimana distribusinya?

#### 2. Distribusi Top 10 Kategori
Pie chart memberikan perspektif proporsional. Kita bisa melihat seberapa besar porsi setiap kategori.

#### 3. Top 10 Klasifikasi
Bar chart vertikal untuk klasifikasi hoaks. Ini membantu memahami bagaimana hoaks dikategorikan secara teknis.

#### 4. Word Cloud
Visualisasi kata kunci paling sering muncul dengan filtering stopwords yang komprehensif. Word cloud ini **mengungkapkan tema-tema utama** yang mungkin tidak terlihat di kategori formal.

**Narasi Kunci:**
> "Segmentasi topik adalah titik awal analisis. Setelah kita mengidentifikasi kategori dominan - misalnya, hoaks tentang kesehatan, politik, atau ekonomi - kita bisa mulai bertanya: 'Di mana hoaks ini tersebar?' dan 'Melalui platform apa?'"

**Koneksi dengan Visualisasi Lain:**
- Filter kategori di sini → mempengaruhi **Persebaran Geografis** (tab 2)
- Filter kategori → mempengaruhi **Platform dan Media** (tab 3)
- Filter kategori → mempengaruhi **Pola dan Timeline** (tab 4)

---

## 🗺️ Act 4: Persebaran Geografis - "Di Mana Hoaks Tersebar?"

### Pertanyaan Utama:
**"Di mana hoaks tersebar secara geografis? Apakah ada pola regional?"**

### Visualisasi yang Menjawab:

#### 1. Peta Bubble Interaktif
Peta Indonesia dengan bubble yang menunjukkan jumlah hoaks per provinsi. Setiap provinsi memiliki **warna unik**, memudahkan identifikasi. Ukuran bubble menunjukkan jumlah hoaks.

**Fitur Interaktif:**
- Klik legend untuk toggle provinsi tertentu
- Hover untuk melihat detail jumlah hoaks
- Zoom dan pan untuk eksplorasi lebih detail

#### 2. Top 15 Provinsi
Bar chart horizontal menunjukkan provinsi dengan hoaks terbanyak. Ini memberikan ranking yang jelas.

#### 3. Distribusi Top 10 Provinsi
Pie chart menunjukkan proporsi hoaks per provinsi.

#### 4. Statistik Lokasi
Metrics untuk:
- Total provinsi unik yang terdeteksi
- Provinsi teratas
- Jumlah hoaks dari provinsi teratas

**Narasi Kunci:**
> "Setelah kita tahu **apa** topik hoaks yang dominan, sekarang kita bertanya **di mana**. Analisis geografis mengungkapkan apakah ada pola regional dalam penyebaran hoaks tertentu. Misalnya, apakah hoaks tentang bencana alam lebih banyak di daerah tertentu? Atau apakah hoaks politik tersebar merata di seluruh Indonesia?"

**Koneksi dengan Visualisasi Lain:**
- Filter lokasi di sini → mempengaruhi **Segmentasi Topik** (tab 1) - menunjukkan kategori hoaks dominan di lokasi tertentu
- Filter lokasi → mempengaruhi **Platform dan Media** (tab 3) - platform apa yang digunakan di lokasi tertentu
- Filter lokasi → mempengaruhi **Pola dan Timeline** (tab 4) - pola temporal hoaks di lokasi tertentu

**Contoh Insight:**
> "Ketika kita filter untuk provinsi tertentu, kita bisa melihat kategori hoaks apa yang dominan di sana. Ini membantu memahami karakteristik hoaks lokal dan mungkin mengidentifikasi isu-isu spesifik daerah."

---

## 📱 Act 5: Platform dan Media - "Melalui Apa Hoaks Tersebar?"

### Pertanyaan Utama:
**"Platform apa yang paling banyak digunakan untuk menyebarkan hoaks? Apakah ada platform tertentu yang lebih 'berbahaya'?"**

### Visualisasi yang Menjawab:

#### 1. Distribusi Platform
Bar chart vertikal dengan color scale berdasarkan jumlah. Platform dengan hoaks terbanyak akan terlihat lebih menonjol.

#### 2. Proporsi Platform
Pie chart menunjukkan persentase setiap platform. Ini membantu memahami **market share** platform dalam ekosistem hoaks.

**Narasi Kunci:**
> "Analisis platform mengidentifikasi saluran distribusi hoaks. Ini penting karena setiap platform memiliki karakteristik berbeda - ada yang lebih viral, ada yang lebih terpercaya, ada yang lebih mudah di-share. Kombinasi dengan filter topik dan lokasi mengungkapkan pola penyebaran yang lebih kompleks."

**Koneksi dengan Visualisasi Lain:**
- Filter platform di sini → mempengaruhi **Segmentasi Topik** (tab 1) - kategori hoaks apa yang dominan di platform tertentu
- Filter platform → mempengaruhi **Persebaran Geografis** (tab 2) - lokasi mana yang aktif di platform tertentu
- Filter platform → mempengaruhi **Pola dan Timeline** (tab 4) - pola temporal penyebaran hoaks di platform tertentu

**Contoh Insight:**
> "Ketika kita filter untuk platform tertentu, kita bisa melihat apakah platform tersebut cenderung menyebarkan kategori hoaks tertentu. Misalnya, apakah platform A lebih banyak menyebarkan hoaks kesehatan, sementara platform B lebih banyak hoaks politik?"

---

## ⏰ Act 6: Pola dan Timeline - "Kapan Hoaks Terjadi?"

### Pertanyaan Utama:
**"Kapan hoaks terjadi? Bagaimana polanya? Seberapa cepat sistem merespons?"**

### Visualisasi yang Menjawab:

#### 1. Perbandingan Timeline: Publish vs Relevan
Line chart membandingkan **tanggal publish artikel** vs **tanggal relevan hoax**. Ini adalah analisis yang sangat penting!

**Apa yang Dilihat:**
- **Delay Analysis**: Berapa lama selisih antara kapan hoaks terjadi (relevant_date) dan kapan artikel klarifikasi dipublish (published_at)?
- **Statistik Delay**:
  - Rata-rata delay
  - Median delay
  - Maksimum delay
- **Distribusi Delay**: Histogram menunjukkan sebaran delay

**Insight Kunci:**
> "Delay yang besar berarti hoaks beredar lebih lama sebelum ada klarifikasi. Ini menunjukkan urgensi untuk mempercepat respons sistem counter-narrative."

#### 2. Perbandingan Bulanan
Bar chart grouped membandingkan distribusi bulanan berdasarkan publish date vs relevant date. Ini membantu melihat pola musiman.

#### 3. Timeline Harian
Line chart dengan markers menunjukkan tren harian. Apakah ada hari-hari tertentu yang lebih banyak hoaks?

#### 4. Distribusi Bulanan
Bar chart distribusi hoaks per bulan. Apakah ada bulan-bulan tertentu yang lebih intensif?

#### 5. Pola Harian (Hari dalam Minggu)
Bar chart menunjukkan hari dalam minggu dengan hoaks terbanyak. Apakah ada pola hari kerja vs akhir pekan?

**Narasi Kunci:**
> "Analisis temporal adalah puncak dari storytelling dashboard. Setelah kita memahami **apa** (topik), **di mana** (lokasi), dan **melalui apa** (platform), analisis waktu mengungkapkan **kapan** hoaks paling aktif dan seberapa cepat sistem merespons."

**Koneksi dengan Visualisasi Lain:**
- **Semua filter dari tab sebelumnya** → mempengaruhi timeline
  - Filter kategori → menunjukkan kapan kategori hoaks tertentu paling aktif
  - Filter lokasi → menunjukkan pola temporal hoaks di lokasi tertentu
  - Filter platform → menunjukkan waktu puncak penyebaran hoaks di platform tertentu

**Contoh Insight:**
> "Ketika kita filter untuk kategori hoaks tertentu, kita bisa melihat kapan kategori tersebut paling aktif. Misalnya, apakah hoaks tentang bencana alam lebih banyak terjadi pada musim tertentu? Atau apakah hoaks politik lebih intensif menjelang pemilu?"

---

## 🧩 Act 7: Clustering Konten - "Bagaimana Hoaks Dikelompokkan?"

### Pertanyaan Utama:
**"Apakah ada pola tersembunyi dalam konten hoaks? Bagaimana hoaks yang serupa dikelompokkan?"**

### Teknologi yang Digunakan:

Dashboard ini menggunakan **teknik data mining clustering** untuk mengelompokkan artikel hoaks berdasarkan kesamaan konten. Teknologi yang digunakan:

- **Sentence-BERT Embeddings**: Menggunakan model bahasa multibahasa untuk mengubah teks menjadi vektor numerik yang merepresentasikan makna semantik
- **KMeans Clustering**: Algoritma unsupervised learning untuk mengelompokkan artikel berdasarkan kesamaan embeddings
- **PCA / t-SNE**: Reduksi dimensi untuk visualisasi cluster dalam ruang 2D

### Visualisasi yang Menjawab:

#### 1. Visualisasi Cluster 2D
Scatter plot yang menunjukkan posisi setiap artikel dalam ruang 2D setelah reduksi dimensi. Artikel-artikel yang berada dalam cluster yang sama memiliki warna yang sama.

**Apa yang Dilihat:**
- **Kedekatan Artikel**: Artikel yang berdekatan memiliki konten yang serupa
- **Pemisahan Cluster**: Cluster yang terpisah jelas menunjukkan kelompok hoaks yang berbeda
- **Density**: Area dengan banyak titik menunjukkan tema hoaks yang dominan

#### 2. Statistik per Cluster
Informasi detail tentang setiap cluster:
- **Jumlah Artikel**: Berapa banyak artikel dalam setiap cluster
- **Persentase**: Proporsi cluster terhadap total artikel
- **Kategori Teratas**: Kategori hoaks yang paling dominan di cluster tersebut
- **Provinsi Teratas**: Lokasi geografis yang paling banyak muncul
- **Platform Teratas**: Platform media yang paling banyak digunakan

#### 3. Distribusi Cluster
Bar chart menunjukkan distribusi artikel per cluster. Ini membantu memahami apakah ada cluster yang dominan atau distribusinya merata.

#### 4. Kata Kunci per Cluster
Daftar kata kunci yang paling sering muncul di setiap cluster. Ini membantu memahami tema utama setiap cluster.

#### 5. Sample Artikel per Cluster
Contoh artikel dari setiap cluster untuk memberikan konteks lebih detail tentang karakteristik cluster.

### Fitur Interaktif:

1. **Penentuan Jumlah Cluster**
   - User dapat menentukan jumlah cluster secara manual (2-20)
   - Atau menggunakan opsi "Gunakan Jumlah Optimal" untuk menghitung secara otomatis menggunakan Elbow Method dan Silhouette Score

2. **Metode Reduksi Dimensi**
   - **PCA**: Lebih cepat, cocok untuk dataset besar
   - **t-SNE**: Lebih baik untuk visualisasi, mengungkapkan struktur non-linear

3. **Sampling Otomatis**
   - Untuk dataset besar (>1000 artikel), sistem otomatis melakukan sampling untuk menjaga performa
   - Tetap mempertahankan representasi data yang baik

### Narasi Kunci:
> "Clustering adalah teknik data mining yang powerful untuk menemukan pola tersembunyi. Dengan mengelompokkan artikel berdasarkan kesamaan konten, kita bisa menemukan tema-tema hoaks yang mungkin tidak terlihat dari kategori formal. Misalnya, cluster tertentu mungkin berisi hoaks tentang vaksin yang menggunakan narasi serupa, meskipun mereka dikategorikan berbeda."

### Insight yang Bisa Ditemukan:

1. **Pola Tersembunyi**
   - Apakah ada kelompok hoaks yang menggunakan narasi serupa?
   - Apakah ada variasi hoaks yang sebenarnya berasal dari sumber yang sama?

2. **Koneksi Antar Hoaks**
   - Hoaks yang terlihat berbeda mungkin sebenarnya memiliki pola narasi yang sama
   - Cluster mengungkapkan hubungan semantik antar artikel

3. **Karakteristik Cluster**
   - Setiap cluster memiliki karakteristik unik (kategori, lokasi, platform)
   - Ini membantu memahami strategi penyebaran hoaks

4. **Targeted Response**
   - Dengan memahami cluster, kita bisa merancang counter-narrative yang lebih spesifik
   - Setiap cluster mungkin memerlukan pendekatan yang berbeda

### Koneksi dengan Visualisasi Lain:

- **Clustering menggunakan data yang sudah difilter** dari tab sebelumnya
  - Filter kategori → clustering hanya pada kategori tertentu
  - Filter lokasi → clustering hanya pada lokasi tertentu
  - Filter platform → clustering hanya pada platform tertentu
- **Hasil clustering dapat digunakan untuk analisis lebih lanjut**
  - Cluster tertentu mungkin memiliki pola geografis yang unik
  - Cluster tertentu mungkin lebih aktif pada waktu-waktu tertentu

### Contoh Insight:
> "Ketika kita melakukan clustering pada hoaks tentang kesehatan, kita menemukan 5 cluster utama. Cluster 1 berisi hoaks tentang vaksin dengan narasi 'bahan berbahaya', Cluster 2 tentang 'efek samping', dan Cluster 3 tentang 'konspirasi'. Setiap cluster memiliki karakteristik geografis dan platform yang berbeda, menunjukkan strategi penyebaran yang berbeda pula."

---

## 🔗 Act 8: Hubungan Antar Dimensi - "The Big Picture"

### Koneksi yang Mencerahkan

Dashboard ini tidak hanya menampilkan data secara terpisah. Setiap visualisasi **saling terhubung** dan mempengaruhi satu sama lain melalui sistem cross-filtering yang canggih.

### Pola Hubungan:

1. **Topik → Lokasi**
   - Kategori hoaks tertentu lebih dominan di lokasi tertentu
   - Contoh: Hoaks tentang gempa mungkin lebih banyak di daerah rawan gempa

2. **Topik → Platform**
   - Platform tertentu lebih banyak menyebarkan kategori hoaks tertentu
   - Contoh: Platform A mungkin lebih banyak hoaks kesehatan, Platform B lebih banyak hoaks politik

3. **Lokasi → Timeline**
   - Lokasi tertentu memiliki pola temporal yang berbeda
   - Contoh: Daerah tertentu mungkin lebih aktif pada waktu-waktu tertentu

4. **Platform → Timeline**
   - Platform tertentu memiliki waktu puncak penyebaran yang berbeda
   - Contoh: Platform media sosial mungkin lebih aktif di malam hari

5. **Topik → Lokasi → Platform → Timeline**
   - Kombinasi semua dimensi mengungkapkan pola kompleks penyebaran hoaks
   - Contoh: Hoaks kesehatan di Jakarta melalui platform tertentu lebih banyak terjadi pada bulan tertentu

**Narasi Kunci:**
> "Ini bukan sekadar dashboard. Ini adalah **jaringan pengetahuan** yang saling terhubung. Setiap klik, setiap filter, setiap eksplorasi membuka wawasan baru tentang ekosistem hoaks di Indonesia."

---

## 💡 Act 9: Insight dan Rekomendasi

### Insight yang Bisa Ditemukan:

1. **Pola Dominan**
   - Kategori hoaks apa yang paling banyak?
   - Di mana hoaks paling aktif?
   - Platform apa yang paling banyak digunakan?

2. **Pola Temporal**
   - Kapan hoaks paling aktif?
   - Apakah ada pola musiman?
   - Seberapa cepat sistem merespons?

3. **Pola Geografis**
   - Apakah ada daerah yang lebih rawan?
   - Apakah ada korelasi antara lokasi dan kategori hoaks?

4. **Pola Platform**
   - Platform mana yang paling efektif untuk counter-narrative?
   - Platform mana yang perlu lebih banyak perhatian?

5. **Pola Clustering**
   - Apakah ada tema hoaks yang menggunakan narasi serupa?
   - Bagaimana karakteristik setiap cluster (lokasi, platform, waktu)?
   - Apakah ada cluster yang lebih berbahaya atau lebih viral?

### Rekomendasi Aksi:

1. **Targeted Counter-Narrative**
   - Fokus pada kategori hoaks yang paling dominan
   - Gunakan platform yang paling efektif
   - Timing yang tepat berdasarkan pola temporal

2. **Regional Strategy**
   - Fokus pada daerah yang paling rawan
   - Sesuaikan konten dengan karakteristik lokal

3. **Platform Strategy**
   - Prioritaskan platform dengan hoaks terbanyak
   - Optimalkan konten untuk platform tertentu

4. **Timing Strategy**
   - Identifikasi waktu-waktu kritis
   - Siapkan respons cepat untuk hoaks yang muncul

5. **Cluster-Based Strategy**
   - Fokus pada cluster yang paling berbahaya atau paling viral
   - Rancang counter-narrative yang spesifik untuk setiap cluster
   - Identifikasi pola narasi yang digunakan untuk mengembangkan strategi debunking yang lebih efektif

---

## 🎬 Closing: Call to Action

### Kesimpulan

Dashboard ini bukan sekadar tool visualisasi. Ini adalah **sistem analisis komprehensif** yang membantu kita memahami ekosistem hoaks di Indonesia dari berbagai dimensi.

**Key Takeaways:**

1. **Hoaks adalah fenomena kompleks** yang memiliki pola, karakteristik, dan dampak yang dapat dianalisis
2. **Data-driven approach** memungkinkan kita membuat keputusan yang lebih tepat dalam melawan hoaks
3. **Cross-dimensional analysis** mengungkapkan insight yang tidak terlihat dari analisis satu dimensi
4. **Real-time detection** menghubungkan masa kini dengan pola historis
5. **Clustering mengungkapkan pola tersembunyi** yang tidak terlihat dari analisis kategori formal

### Next Steps

1. **Eksplorasi Dashboard**: Gunakan filter interaktif untuk menemukan insight baru
2. **Analisis Mendalam**: Kombinasikan berbagai filter untuk melihat pola kompleks
3. **Aksi Berbasis Data**: Gunakan insight untuk merancang strategi counter-narrative yang lebih efektif

---

## 📝 Catatan untuk Presenter

### Tips Presentasi:

1. **Mulai dengan Hook**: Gunakan pertanyaan pembuka yang menarik
2. **Tunjukkan Interaktivitas**: Demo live filtering untuk menunjukkan koneksi antar visualisasi
3. **Ceritakan Story**: Setiap tab adalah bagian dari cerita yang lebih besar
4. **Highlight Insight**: Jangan hanya menunjukkan data, tapi juga insight yang bisa diambil
5. **End with Action**: Tutup dengan rekomendasi konkret

### Flow Presentasi yang Disarankan:

1. **Opening** (2 menit): Masalah hoaks di Indonesia
2. **KPI Overview** (1 menit): Skala masalah
3. **DeepHoaxID Demo** (2 menit): Deteksi real-time
4. **Segmentasi Topik** (3 menit): Apa yang diserang?
5. **Persebaran Geografis** (3 menit): Di mana hoaks tersebar?
6. **Platform dan Media** (2 menit): Melalui apa hoaks tersebar?
7. **Pola dan Timeline** (3 menit): Kapan hoaks terjadi?
8. **Clustering Konten** (3 menit): Bagaimana hoaks dikelompokkan? (Teknik data mining)
9. **Cross-Filtering Demo** (2 menit): Koneksi antar dimensi
10. **Insight dan Rekomendasi** (2 menit): Key takeaways
11. **Q&A** (5 menit)

**Total: ~28 menit**

---

## 🎯 Key Messages

1. **"Data adalah senjata terbaik melawan hoaks"**
   - Dengan memahami pola, kita bisa merancang strategi yang lebih efektif

2. **"Hoaks adalah fenomena multi-dimensi"**
   - Tidak bisa dipahami hanya dari satu sudut pandang

3. **"Real-time detection + Historical analysis = Powerful combination"**
   - Deteksi real-time terhubung dengan pola historis

4. **"Cross-filtering mengungkapkan insight tersembunyi"**
   - Koneksi antar dimensi mengungkapkan pola kompleks

5. **"Actionable insights untuk counter-narrative yang lebih efektif"**
   - Dashboard ini bukan hanya untuk analisis, tapi juga untuk aksi

6. **"Clustering mengungkapkan pola tersembunyi"**
   - Teknik data mining clustering membantu menemukan hubungan semantik antar hoaks yang tidak terlihat dari kategori formal

---

*Dashboard ini adalah hasil dari analisis data mining yang komprehensif, menggunakan teknik-teknik seperti **clustering (KMeans dengan Sentence-BERT embeddings)**, pattern recognition, dan temporal analysis untuk mengungkapkan insight yang actionable. Clustering memungkinkan kita menemukan pola tersembunyi dalam konten hoaks dan mengelompokkan artikel berdasarkan kesamaan semantik, bukan hanya berdasarkan kategori formal.*


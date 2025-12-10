import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import time
import logging
from pathlib import Path

from loaders.article_loader import load_articles_df, enrich_with_dates, enrich_with_locations

# Setup logger
logger = logging.getLogger(__name__)

# Add deephoaxid_detection to path
current_file = Path(__file__).resolve()
dashboard_root = current_file.parent
project_root = dashboard_root.parent
deephoaxid_path = project_root / "tb_scrapping" / "deephoaxid_detection"

if deephoaxid_path.exists():
    sys.path.insert(0, str(deephoaxid_path))
    
    # Import dengan error handling
    try:
        from helpers.deephoaxid_wrapper import DeepHoaxIDPostgreSQLWrapper as DeepHoaxIDSystem
        # Get version from wrapper instead of importing config directly
        # to avoid triggering firebase_admin imports
        SYSTEM_VERSION = "1.0.0"  # Default version, wrapper will use actual version
        DEEPHOAXID_AVAILABLE = True
    except ImportError as e:
        DEEPHOAXID_AVAILABLE = False
        DEEPHOAXID_ERROR = str(e)
else:
    DEEPHOAXID_AVAILABLE = False
    DEEPHOAXID_ERROR = f"Path tidak ditemukan: {deephoaxid_path}"

st.set_page_config(page_title="BI Hoax Analyzer", layout="wide")

# Initialize session state untuk hoax system
if 'hoax_system' not in st.session_state:
    st.session_state.hoax_system = None
    st.session_state.hoax_initialized = False
    st.session_state.last_hoax_result = None
    st.session_state.hoax_init_attempted = False

# Auto-initialize DeepHoaxID jika tersedia (silent initialization)
if DEEPHOAXID_AVAILABLE and not st.session_state.hoax_initialized and not st.session_state.hoax_init_attempted:
    st.session_state.hoax_init_attempted = True
    try:
        system = DeepHoaxIDSystem()
        if system.initialize():
            st.session_state.hoax_system = system
            st.session_state.hoax_initialized = True
        else:
            st.session_state.hoax_initialized = False
    except Exception as e:
        st.session_state.hoax_initialized = False
        logger.error(f"Failed to auto-initialize DeepHoaxID: {e}")

@st.cache_data(show_spinner=True)
def get_data():
    df = load_articles_df()
    df = enrich_with_dates(df)
    df = enrich_with_locations(df)
    if "relevant_date" in df.columns:
        df["relevant_date"] = pd.to_datetime(df["relevant_date"], errors="coerce")
    # Konversi published_at ke datetime jika ada
    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    return df

df = get_data()

st.markdown(
    "<h1 style='text-align:center; margin-bottom:0.5rem;'>Analisis Segmentasi Konten Hoaks di Indonesia</h1>",
    unsafe_allow_html=True,
)



if "relevant_date" in df.columns and not df["relevant_date"].dropna().empty:
    min_date = df["relevant_date"].min().date()
    max_date = df["relevant_date"].max().date()
    
    col_left, col_right = st.columns([3, 1])
    with col_right:
        date_range = st.date_input(
            "Pilih rentang tanggal",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    if isinstance(date_range, (list, tuple)):
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)

    filtered_with_date = df[df["relevant_date"].between(start_ts, end_ts)]

    filtered_no_date = df[df["relevant_date"].isna()]

    shown_df = pd.concat([filtered_with_date, filtered_no_date], ignore_index=True)

    def count_hoax_rows(df_):
        return len(df_)

    def count_unique_sources(df_):
        if "source_url" in df_.columns:
            return int(df_["source_url"].dropna().nunique())
        return 0

    def avg_per_day(df_):
        if "relevant_date" in df_.columns:
            compact = df_.dropna(subset=["relevant_date"])
            if compact.empty:
                return 0.0
            daily_counts = compact.groupby(compact["relevant_date"].dt.date).size()
            return float(daily_counts.mean())
        return 0.0

    def total_references(df_):
        if "references" not in df_.columns:
            return 0
        def cnt_refs(x):
            if x is None:
                return 0
            if isinstance(x, (list, tuple)):
                return len(x)
            s = str(x).strip()
            if s == "":
                return 0
            return len([p for p in s.split(",") if p.strip()])
        return int(df_["references"].apply(cnt_refs).sum())

    k_with_publication = len(filtered_with_date)
    k_without_publication = len(filtered_no_date)
    k_total_hoax = k_with_publication + k_without_publication
    k_unique_sources = count_unique_sources(shown_df)
    k_avg_per_day = avg_per_day(filtered_with_date)
    k_total_refs = total_references(shown_df)

    st.markdown(
        """
        <style>
        .kpi-card { background: var(--bg-color, #fff); border: 1px solid #e6e6e6; border-radius: 12px;
                    padding: 12px 16px; text-align:center; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
        .kpi-label { color: #6b7280; font-size:13px; margin-bottom:6px; }
        .kpi-value { font-size:28px; font-weight:700; color:#111827; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def render_kpi(col, label, value):
        col.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    render_kpi(k1, "Total Hoaks Terdeteksi", f"{k_total_hoax:,}")
    render_kpi(k2, "Hoaks dengan Publikasi", f"{k_with_publication:,}")
    render_kpi(k3, "Hoaks tanpa Publikasi", f"{k_without_publication:,}")
    render_kpi(k4, "Total Sumber Unik", f"{k_unique_sources:,}")
    render_kpi(k5, "Rata-rata / hari", f"{k_avg_per_day:.2f}")
    render_kpi(k6, "Total Referensi", f"{k_total_refs:,}")

    if not DEEPHOAXID_AVAILABLE:
        st.error(f"DeepHoaxID tidak tersedia: {DEEPHOAXID_ERROR}")
        st.info("Pastikan semua dependencies terinstall dan path benar.")
    else:
        # Main detector interface
        if not st.session_state.hoax_initialized:
            st.warning("DeepHoaxID belum terinisialisasi. Sistem sedang mencoba menginisialisasi...")
            if st.session_state.hoax_init_attempted:
                st.error("Gagal menginisialisasi DeepHoaxID. Pastikan semua dependencies terinstall.")
                st.info("""
                **Dependencies yang diperlukan:**
                ```bash
                pip install sentence-transformers faiss-cpu torch transformers nltk
                ```
                """)
        else:
            
            # Input area
            st.markdown("#### Masukkan Teks untuk Dianalisis")
            
            message_text = st.text_area(
                "Teks pesan:",
                value="",
                height=120,
                placeholder="Masukkan teks yang ingin dianalisis di sini...",
                help="Masukkan teks yang ingin dicek apakah mengandung hoax atau tidak",
                key="hoax_input"
            )
            
            col_analyze, col_clear = st.columns([1, 4])
            with col_analyze:
                analyze_button = st.button("Analisis", type="primary", width='stretch', key="hoax_analyze")
            
            if analyze_button and message_text.strip():
                with st.spinner("Menganalisis teks..."):
                    start_time = time.time()
                    
                    try:
                        result = st.session_state.hoax_system.analyze_message(message_text)
                        processing_time = time.time() - start_time
                        
                        st.session_state.last_hoax_result = result
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("### Hasil Analisis")
                        
                        # Check if message was skipped
                        should_analyze = result.get('should_analyze', True)
                        
                        if not should_analyze:
                            # Message was skipped (casual chat)
                            response = result.get('response', {})
                            response_text = response.get('text', 'Sepertinya ini chat biasa, tidak perlu dianalisis.')
                            
                            st.info(response_text)
                            st.markdown("---")
                            st.markdown("**Status:** Pesan di-skip karena terdeteksi sebagai chat biasa")
                        else:
                        
                            # Main result card
                            analysis_result = result.get('analysis_result')
                            if analysis_result is None:
                                st.error("Analysis result is None. System mungkin belum sepenuhnya initialized.")
                                st.info("Sistem sedang menginisialisasi ulang...")
                                # Check if similarity engine is available
                                if hasattr(st.session_state.hoax_system, 'similarity_engine'):
                                    if st.session_state.hoax_system.similarity_engine is None or st.session_state.hoax_system.similarity_engine.sbert_model is None:
                                        st.warning("Similarity Engine tidak tersedia. Pastikan sentence-transformers dan faiss-cpu sudah terinstall.")
                                        st.code("pip install sentence-transformers faiss-cpu")
                            else:
                                category = analysis_result.get('category', 'UNKNOWN')
                                confidence = analysis_result.get('confidence', 0.0)
                                response = result.get('response', {})
                                
                                # Main result display
                                col_cat, col_conf, col_time = st.columns([2, 2, 1])
                                
                                with col_cat:
                                    st.markdown(f"### **{category}**")
                                
                                with col_conf:
                                    st.markdown(f"### **{confidence:.1%}**")
                                    st.progress(confidence)
                                
                                with col_time:
                                    st.markdown(f"### **{processing_time:.2f}s**")
                                
                                # Response text
                                st.markdown("---")
                                st.markdown("### Response Bot")
                                response_text = response.get('text', 'No response generated')
                                st.markdown(response_text)
                                
                                # Similar articles
                                similar_articles = analysis_result.get('similar_articles', [])
                                if similar_articles:
                                    st.markdown("---")
                                    st.markdown("### Artikel Serupa")
                                    
                                    for i, article in enumerate(similar_articles[:3], 1):
                                        with st.expander(f"Artikel {i} - Similarity: {article.get('similarity_score', 0):.2%}"):
                                            st.markdown(f"**Title:** {article.get('title', 'N/A')}")
                                            st.markdown(f"**Category:** {article.get('truth_category', 'N/A')}")
                                            st.markdown(f"**Snippet:** {article.get('content_snippet', 'N/A')}")
                                            if article.get('url'):
                                                st.markdown(f"**URL:** {article.get('url')}")
                                
                                # Update statistics
                                st.session_state.hoax_system.system_info['stats']['messages_processed'] += 1
                                if category in ['HOAX', 'SUSPICIOUS']:
                                    st.session_state.hoax_system.system_info['stats']['hoax_detected'] += 1
                                else:
                                    st.session_state.hoax_system.system_info['stats']['clean_detected'] += 1
                        
                    except Exception as e:
                        st.error(f"Error saat analisis: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
            
            elif analyze_button:
                st.warning("Silakan masukkan teks terlebih dahulu")
    
    st.markdown("---")
    
    # Helper function untuk extract platform
    def extract_platform(url):
        if pd.isna(url) or url == "":
            return "Unknown"
        try:
            from urllib.parse import urlparse
            parsed = urlparse(str(url))
            domain = parsed.netloc.replace('www.', '').lower()
            
            # Kategorisasi platform
            if any(x in domain for x in ['facebook', 'fb.com']):
                return "Facebook"
            elif any(x in domain for x in ['twitter', 'x.com']):
                return "Twitter/X"
            elif any(x in domain for x in ['instagram']):
                return "Instagram"
            elif any(x in domain for x in ['youtube', 'youtu.be']):
                return "YouTube"
            elif any(x in domain for x in ['whatsapp', 'wa.me']):
                return "WhatsApp"
            elif any(x in domain for x in ['telegram', 't.me']):
                return "Telegram"
            elif any(x in domain for x in ['tiktok']):
                return "TikTok"
            elif any(x in domain for x in ['blogspot', 'blog']):
                return "Blog"
            elif any(x in domain for x in ['.co.id', '.id']):
                return "Media Indonesia"
            else:
                return "Website Lain"
        except:
            return "Unknown"
    
    # Initialize filter state (mirip dengan contoh.py - filter sekali, semua visualisasi pakai data yang sama)
    if 'active_filters' not in st.session_state:
        st.session_state.active_filters = {
            'categories': [],
            'classifications': [],
            'locations': [],
            'platforms': [],
            'date_range': None,
            'hoax_category': None  # Kategori dari hasil analisis DeepHoaxID
        }
    
    # Simpan hasil klasifikasi dari DeepHoaxID ke filter
    if 'last_hoax_result' in st.session_state and st.session_state.last_hoax_result:
        result = st.session_state.last_hoax_result
        analysis_result = result.get('analysis_result')
        if analysis_result:
            category = analysis_result.get('category', None)
            if category:
                st.session_state.active_filters['hoax_category'] = category
    
    # Check for chart selections from session state and update filters
    # Pattern: sama seperti contoh.py - filter diterapkan sekali, semua visualisasi pakai filtered_df yang sama
    chart_keys = {
        'cat_chart': ('categories', 'y'),
        'pie_chart': ('categories', 'label'),
        'class_chart': ('classifications', 'x'),
        'location_chart': ('locations', 'y'),
        'location_pie_chart': ('locations', 'label'),
        'platform_chart': ('platforms', 'x'),
        'platform_pie_chart': ('platforms', 'label')
    }
    
    for chart_key, (filter_type, data_key) in chart_keys.items():
        if chart_key in st.session_state:
            chart_data = st.session_state[chart_key]
            
            # Handle both selection (box select) and click events
            if isinstance(chart_data, dict):
                # Check for selection (box select/drag)
                if "selection" in chart_data:
                    selection = chart_data["selection"]
                    if isinstance(selection, dict) and "points" in selection:
                        points = selection["points"]
                        if points:
                            selected_values = []
                            for point in points:
                                if isinstance(point, dict):
                                    value = point.get(data_key)
                                    if value:
                                        selected_values.append(value)
                            if selected_values:
                                st.session_state.active_filters[filter_type] = selected_values
                                st.rerun()
                
                # Check for click event (single click)
                elif "click" in chart_data:
                    click = chart_data["click"]
                    if isinstance(click, dict) and "points" in click:
                        points = click["points"]
                        if points:
                            selected_values = []
                            for point in points:
                                if isinstance(point, dict):
                                    value = point.get(data_key)
                                    if value:
                                        selected_values.append(value)
                            if selected_values:
                                st.session_state.active_filters[filter_type] = selected_values
                                st.rerun()
    
    # Apply filters to dataframe (SAMA SEPERTI contoh.py: main_df = all_data[(filter conditions)])
    # Semua visualisasi akan menggunakan filtered_df yang sama ini
    filtered_df = shown_df.copy()
    
    # Filter berdasarkan kategori dari hasil analisis DeepHoaxID
    hoax_category = st.session_state.active_filters.get('hoax_category')
    if hoax_category:
        # Map kategori DeepHoaxID ke truth_category di database
        category_mapping = {
            'HOAX': ['HOAX', 'FALSE', 'MISLEADING'],
            'SUSPICIOUS': ['SUSPICIOUS', 'UNVERIFIED'],
            'CLEAN': ['TRUE', 'VERIFIED', 'CLEAN'],
            'UNKNOWN': ['UNKNOWN', None]
        }
        
        # Cari kategori yang sesuai
        target_categories = category_mapping.get(hoax_category, [hoax_category])
        if "truth_category" in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df["truth_category"].fillna("UNKNOWN").isin(target_categories)
            ]
    
    if st.session_state.active_filters.get('categories'):
        filtered_df = filtered_df[filtered_df["categories"].fillna("(unknown)").isin(st.session_state.active_filters['categories'])]
    
    if st.session_state.active_filters.get('classifications'):
        filtered_df = filtered_df[filtered_df["classifications"].fillna("(unknown)").isin(st.session_state.active_filters['classifications'])]
    
    if st.session_state.active_filters.get('locations'):
        filtered_df = filtered_df[filtered_df["relevant_location"].isin(st.session_state.active_filters['locations'])]
    
    if st.session_state.active_filters.get('platforms'):
        if "platform" not in filtered_df.columns and "source_url" in filtered_df.columns:
            filtered_df["platform"] = filtered_df["source_url"].apply(extract_platform)
        filtered_df = filtered_df[filtered_df["platform"].isin(st.session_state.active_filters['platforms'])]
    
    # Show filter summary and clear button
    active_count = sum([
        len(st.session_state.active_filters.get('categories', [])),
        len(st.session_state.active_filters.get('classifications', [])),
        len(st.session_state.active_filters.get('locations', [])),
        len(st.session_state.active_filters.get('platforms', [])),
        1 if st.session_state.active_filters.get('hoax_category') else 0
    ])
    
    # Tampilkan filter dari hasil analisis DeepHoaxID
    hoax_category = st.session_state.active_filters.get('hoax_category')
    if hoax_category:
        col_hoax, col_clear_hoax = st.columns([3, 1])
        with col_hoax:
            st.success(f"🔍 **Filter Aktif dari Analisis:** Kategori **{hoax_category}** - Menampilkan artikel dengan kategori serupa")
        with col_clear_hoax:
            if st.button("❌ Hapus Filter Analisis", use_container_width=True, key="clear_hoax_filter"):
                st.session_state.active_filters['hoax_category'] = None
                st.rerun()
    
    if active_count > 0:
        col_info, col_clear = st.columns([3, 1])
        with col_info:
            filter_details = []
            if hoax_category:
                filter_details.append(f"Analisis: {hoax_category}")
            if st.session_state.active_filters.get('categories'):
                filter_details.append(f"Kategori: {len(st.session_state.active_filters['categories'])}")
            if st.session_state.active_filters.get('classifications'):
                filter_details.append(f"Klasifikasi: {len(st.session_state.active_filters['classifications'])}")
            if st.session_state.active_filters.get('locations'):
                filter_details.append(f"Lokasi: {len(st.session_state.active_filters['locations'])}")
            if st.session_state.active_filters.get('platforms'):
                filter_details.append(f"Platform: {len(st.session_state.active_filters['platforms'])}")
            
            filter_text = " | ".join(filter_details) if filter_details else f"Filter aktif: {active_count}"
            st.info(f"📊 Menampilkan {len(filtered_df):,} dari {len(shown_df):,} artikel ({filter_text})")
        with col_clear:
            if st.button("🗑️ Hapus Semua Filter", use_container_width=True):
                st.session_state.active_filters = {
                    'categories': [],
                    'classifications': [],
                    'locations': [],
                    'platforms': [],
                    'date_range': None,
                    'hoax_category': None
                }
                st.rerun()
    
    # Tab untuk berbagai analisis
    tab1, tab2, tab3, tab4 = st.tabs([
        "Segmentasi Topik",
        "Persebaran Geografis", 
        "Platform dan Media",
        "Pola dan Timeline"
    ])
    
    with tab1:
        st.markdown("### Segmentasi Topik")
        
        # Segmentasi berdasarkan Categories
        if "categories" in filtered_df.columns:
            cat_counts = filtered_df["categories"].fillna("(unknown)").value_counts().reset_index()
            cat_counts.columns = ["categories", "count"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_cat = px.bar(
                    cat_counts.head(10),
                    x="count",
                    y="categories",
                    orientation='h',
                    text="count",
                    title="Top 10 Kategori (Klik untuk filter)",
                    color_discrete_sequence=px.colors.qualitative.Set3,
                )
                fig_cat.update_layout(
                    showlegend=False, 
                    xaxis_title="Jumlah", 
                    yaxis_title="", 
                    margin=dict(t=40, l=20, r=20, b=20),
                    clickmode='event+select',
                    dragmode='select'
                )
                fig_cat.update_traces(
                    textposition="outside",
                    selected=dict(marker=dict(color='red', opacity=0.8)),
                    unselected=dict(marker=dict(opacity=0.6))
                )
                selected_data = st.plotly_chart(fig_cat, use_container_width=True, on_select="rerun", key="cat_chart")
                
                # Process selection - check both selection and click events
                if selected_data:
                    # Check for selection (box select/drag)
                    if isinstance(selected_data, dict) and "selection" in selected_data:
                        points = selected_data["selection"].get("points", [])
                        if points:
                            selected_cats = [p.get("y") for p in points if p.get("y")]
                            if selected_cats and selected_cats != st.session_state.active_filters.get('categories', []):
                                st.session_state.active_filters['categories'] = selected_cats
                                st.rerun()
                    # Check for click event
                    elif isinstance(selected_data, dict) and "click" in selected_data:
                        points = selected_data["click"].get("points", [])
                        if points:
                            selected_cats = [p.get("y") for p in points if p.get("y")]
                            if selected_cats:
                                st.session_state.active_filters['categories'] = selected_cats
                                st.rerun()
            
            with col2:
                fig_pie = px.pie(
                    cat_counts.head(10),
                    values="count",
                    names="categories",
                    title="Distribusi Top 10 Kategori (Klik untuk filter)",
                )
                fig_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
                )
                fig_pie.update_layout(clickmode='event+select')
                selected_data = st.plotly_chart(fig_pie, use_container_width=True, on_select="rerun", key="pie_chart")
                
                # Process selection - check both selection and click events
                if selected_data:
                    # Check for selection
                    if "selection" in selected_data:
                        points = selected_data["selection"].get("points", [])
                        if points:
                            selected_cats = [p.get("label") for p in points if p.get("label")]
                            if selected_cats and selected_cats != st.session_state.active_filters.get('categories', []):
                                st.session_state.active_filters['categories'] = selected_cats
                                st.rerun()
                    # Check for click event
                    elif "click" in selected_data:
                        points = selected_data["click"].get("points", [])
                        if points:
                            selected_cats = [p.get("label") for p in points if p.get("label")]
                            if selected_cats:
                                st.session_state.active_filters['categories'] = selected_cats
                                st.rerun()
        
        # Segmentasi berdasarkan Classifications jika ada
        if "classifications" in filtered_df.columns:
            st.markdown("#### Segmentasi berdasarkan Klasifikasi")
            class_counts = filtered_df["classifications"].fillna("(unknown)").value_counts().reset_index()
            class_counts.columns = ["classifications", "count"]
            
            fig_class = px.bar(
                class_counts.head(10),
                x="classifications",
                y="count",
                text="count",
                title="Top 10 Klasifikasi (Klik untuk filter)",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_class.update_layout(
                showlegend=False, 
                xaxis_title="", 
                yaxis_title="Jumlah", 
                margin=dict(t=40, l=20, r=20, b=20),
                clickmode='event+select',
                dragmode='select'
            )
            fig_class.update_traces(
                textposition="outside",
                selected=dict(marker=dict(color='red', opacity=0.8)),
                unselected=dict(marker=dict(opacity=0.6))
            )
            fig_class.update_xaxes(tickangle=-45)
            selected_data = st.plotly_chart(fig_class, use_container_width=True, on_select="rerun", key="class_chart")
            
            # Process selection - check both selection and click events
            if selected_data:
                # Check for selection (box select/drag)
                if "selection" in selected_data:
                    points = selected_data["selection"].get("points", [])
                    if points:
                        selected_classes = [p.get("x") for p in points if p.get("x")]
                        if selected_classes and selected_classes != st.session_state.active_filters.get('classifications', []):
                            st.session_state.active_filters['classifications'] = selected_classes
                            st.rerun()
                # Check for click event
                elif "click" in selected_data:
                    points = selected_data["click"].get("points", [])
                    if points:
                        selected_classes = [p.get("x") for p in points if p.get("x")]
                        if selected_classes:
                            st.session_state.active_filters['classifications'] = selected_classes
                            st.rerun()
        
        # Word Cloud
        st.markdown("---")
        st.markdown("#### Word Cloud - Kata Kunci Paling Sering Muncul")
        
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            from collections import Counter
            import re
            
            # Extract text dari title dan content dari filtered data
            all_text = ""
            if "title" in filtered_df.columns:
                all_text += " ".join(filtered_df["title"].fillna("").astype(str))
            if "content" in filtered_df.columns:
                all_text += " " + " ".join(filtered_df["content"].fillna("").astype(str))
            
            # Clean text
            all_text = all_text.lower()
            # Remove URLs
            all_text = re.sub(r'http\S+|www\S+', '', all_text)
            # Remove email addresses
            all_text = re.sub(r'\S+@\S+', '', all_text)
            # Remove special characters, keep only words
            all_text = re.sub(r'[^\w\s]', ' ', all_text)
            # Remove numbers
            all_text = re.sub(r'\d+', '', all_text)
            # Remove single characters and very short words
            all_text = re.sub(r'\b\w{1,2}\b', '', all_text)
            
            # Comprehensive Indonesian stopwords
            stopwords = {
                # Prepositions and conjunctions
                'yang', 'di', 'ke', 'dari', 'dan', 'atau', 'untuk', 'pada', 'dengan', 'dalam',
                'adalah', 'ini', 'itu', 'tidak', 'akan', 'sudah', 'telah', 'juga', 'dapat', 'bisa',
                'ada', 'nya', 'oleh', 'kepada', 'terhadap', 'antara', 'karena', 'jika',
                'sebagai', 'seperti', 'bahwa', 'serta', 'namun', 'tetapi',
                'apabila', 'ketika', 'saat', 'setelah', 'sebelum', 'selama', 'hingga',
                'sampai', 'sementara', 'meskipun', 'walaupun', 'sebab',
                'maka', 'sehingga', 'agar', 'supaya', 'guna', 'demi',
                'menuju', 'tentang', 'mengenai', 'atas', 'bawah', 'depan', 'belakang', 'samping',
                # Common verbs
                'adalah', 'merupakan', 'menjadi', 'ada', 'terdapat', 'terdiri', 'mengenai',
                'mengatakan', 'menyatakan', 'menjelaskan', 'menyebutkan', 'mengungkapkan',
                'menunjukkan', 'mengindikasikan', 'menandakan', 'menyiratkan',
                # Common nouns (not relevant to hoax)
                'hal', 'halnya', 'masalah', 'permasalahan', 'keadaan', 'kondisi', 'situasi',
                'tempat', 'waktu', 'tanggal', 'hari', 'bulan', 'tahun', 'jam', 'menit',
                'orang', 'seseorang', 'seseorang', 'mereka', 'kami', 'kita', 'kamu', 'anda',
                'saya', 'dia', 'ia', 'beliau', 'nya', 'kita', 'kami',
                # Common adjectives/adverbs
                'sangat', 'amat', 'sekali', 'terlalu', 'cukup', 'agak', 'sedikit', 'banyak',
                'semua', 'seluruh', 'setiap', 'masing', 'beberapa', 'sebagian',
                'baru', 'lama', 'lama', 'sebelumnya', 'kemudian', 'selanjutnya',
                'pertama', 'kedua', 'ketiga', 'terakhir', 'akhirnya',
                # Common phrases
                'dapat', 'bisa', 'mampu', 'mungkin', 'kemungkinan', 'boleh', 'perlu',
                'harus', 'wajib', 'sebaiknya', 'seharusnya', 'sepatutnya',
                # Common words without meaning to hoax
                'tersebut', 'tadi', 'ini', 'itu', 'tersebut', 'demikian', 'begitu',
                'begini', 'begitu', 'demikian', 'seperti', 'sama', 'serupa',
                'lain', 'lainnya', 'lainnya', 'lainnya', 'lainnya',
                'saja', 'sahaja', 'hanya', 'cuma', 'semata',
                'juga', 'pula', 'lagi', 'kembali', 'sekali',
                'sudah', 'telah', 'pernah', 'belum', 'akan', 'mau',
                'bukan', 'tidak', 'tak', 'tiada', 'tanpa',
                # Common filler words
                'nah', 'oh', 'eh', 'ah', 'wah', 'aduh', 'astaga',
                'ya', 'iya', 'yap', 'ok', 'oke', 'baik', 'benar',
                # Common technical words (not relevant)
                'link', 'url', 'http', 'https', 'www', 'com', 'id', 'co',
                'click', 'klik', 'share', 'bagikan', 'like', 'suka',
                'comment', 'komentar', 'reply', 'balas', 'post', 'posting',
                # Common words that don't add meaning
                'sih', 'dong', 'deh', 'nih', 'tuh', 'kok', 'kan', 'dong',
                'dah', 'udah', 'udah', 'udah', 'udah',
                # Common media words (not relevant to hoax content)
                'foto', 'gambar', 'video', 'audio', 'file', 'dokumen',
                'sumber', 'referensi', 'link', 'tautan', 'url',
                # Common action words (not relevant)
                'lihat', 'baca', 'tonton', 'dengar', 'simak', 'perhatikan',
                'bagikan', 'share', 'kirim', 'send', 'post', 'upload',
                # Common location words (too generic)
                'disini', 'disana', 'disitu', 'dimana', 'kemana', 'darimana',
                # Common time words (too generic)
                'sekarang', 'nanti', 'besok', 'kemarin', 'lusa', 'hari',
                'minggu', 'bulan', 'tahun', 'jam', 'menit', 'detik',
                # Common quantity words
                'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh',
                'pertama', 'kedua', 'ketiga', 'keempat', 'kelima',
                # Common question words
                'apa', 'siapa', 'dimana', 'kemana', 'darimana', 'kapan', 'kenapa', 'mengapa', 'bagaimana',
                # Common pronouns
                'saya', 'aku', 'gue', 'gw', 'dia', 'ia', 'beliau', 'kamu', 'anda', 'kalian',
                'kami', 'kita', 'mereka', 'kita', 'kami',
                # Common possessive
                'ku', 'mu', 'nya', 'kita', 'kami', 'mereka',
            }
            
            # Words that are not meaningful for hoax analysis (common words without context)
            meaningless_words = {
                'tersebut', 'tadi', 'demikian', 'begitu', 'begini', 'saja', 'juga', 'pula',
                'sudah', 'telah', 'akan', 'belum', 'pernah', 'mau', 'ingin',
                'bisa', 'dapat', 'mampu', 'mungkin', 'kemungkinan',
                'sangat', 'amat', 'sekali', 'terlalu', 'cukup', 'agak',
                'semua', 'seluruh', 'setiap', 'beberapa', 'sebagian',
                'baru', 'lama', 'sebelumnya', 'kemudian', 'selanjutnya',
                'pertama', 'kedua', 'terakhir', 'akhirnya',
                'lihat', 'baca', 'tonton', 'dengar', 'simak',
                'bagikan', 'share', 'kirim', 'post', 'upload',
                'foto', 'gambar', 'video', 'audio', 'file',
                'link', 'url', 'tautan', 'sumber', 'referensi',
                'click', 'klik', 'like', 'suka', 'comment', 'komentar',
                'sekarang', 'nanti', 'besok', 'kemarin',
                'disini', 'disana', 'disitu', 'dimana',
            }
            
            # Split into words and filter
            words = all_text.split()
            # Filter: minimum 4 characters, not in stopwords, not in meaningless words, contains at least one vowel
            words = [
                w for w in words 
                if len(w) >= 4  # Minimum 4 characters
                and w not in stopwords
                and w not in meaningless_words
                and re.search(r'[aeiou]', w)  # Must contain at least one vowel
                and not w.isdigit()  # Not just numbers
                and not re.match(r'^[a-z]{1,3}$', w)  # Not just 1-3 letter words
                and not re.match(r'^[a-z]+[0-9]+$', w)  # Not alphanumeric codes
                and not re.match(r'^[0-9]+[a-z]+$', w)  # Not numeric codes with letters
            ]
            
            if words:
                # Count word frequency
                word_freq = Counter(words)
                top_words = dict(word_freq.most_common(100))
                
                if top_words:
                    # Create word cloud
                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color='white',
                        max_words=100,
                        colormap='viridis',
                        relative_scaling=0.5,
                        min_font_size=10
                    ).generate_from_frequencies(top_words)
                    
                    # Display word cloud
                    fig_wc, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig_wc)
                    
                    # Show top words table
                    st.markdown("#### Top 30 Kata Kunci")
                    top_words_df = pd.DataFrame(
                        list(word_freq.most_common(30)),
                        columns=['Kata', 'Frekuensi']
                    )
                    st.dataframe(top_words_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Tidak ada kata yang cukup untuk membuat word cloud.")
            else:
                st.info("Tidak ada teks yang dapat diproses untuk word cloud.")
                
        except ImportError:
            st.warning("Library wordcloud belum terinstall. Install dengan: pip install wordcloud matplotlib")
            st.code("pip install wordcloud matplotlib")
        except Exception as e:
            st.error(f"Error membuat word cloud: {str(e)}")
    
    with tab2:
        st.markdown("### Persebaran Geografis")
        
        # Gunakan data lokasi yang diekstrak dari content
        if "relevant_location" in filtered_df.columns:
            location_df = filtered_df[filtered_df["relevant_location"].notna()].copy()
            
            if not location_df.empty:
                location_counts = location_df["relevant_location"].value_counts().reset_index()
                location_counts.columns = ["location", "count"]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_location = px.bar(
                        location_counts.head(15),
                        x="count",
                        y="location",
                        orientation='h',
                        text="count",
                        title="Top 15 Lokasi (Klik untuk filter)",
                        color_discrete_sequence=px.colors.qualitative.Dark2,
                    )
                    fig_location.update_layout(
                        showlegend=False, 
                        xaxis_title="Jumlah Hoax", 
                        yaxis_title="Lokasi", 
                        margin=dict(t=40, l=20, r=20, b=20),
                        clickmode='event+select',
                        dragmode='select'
                    )
                    fig_location.update_traces(
                        textposition="outside",
                        selected=dict(marker=dict(color='red', opacity=0.8)),
                        unselected=dict(marker=dict(opacity=0.6))
                    )
                    selected_data = st.plotly_chart(fig_location, use_container_width=True, on_select="rerun", key="location_chart")
                    
                    # Process selection - check both selection and click events
                    if selected_data:
                        # Check for selection (box select/drag)
                        if "selection" in selected_data:
                            points = selected_data["selection"].get("points", [])
                            if points:
                                selected_locs = [p.get("y") for p in points if p.get("y")]
                                if selected_locs and selected_locs != st.session_state.active_filters.get('locations', []):
                                    st.session_state.active_filters['locations'] = selected_locs
                                    st.rerun()
                        # Check for click event
                        elif "click" in selected_data:
                            points = selected_data["click"].get("points", [])
                            if points:
                                selected_locs = [p.get("y") for p in points if p.get("y")]
                                if selected_locs:
                                    st.session_state.active_filters['locations'] = selected_locs
                                    st.rerun()
                
                with col2:
                    fig_location_pie = px.pie(
                        location_counts.head(10),
                        values="count",
                        names="location",
                        title="Distribusi Top 10 Lokasi (Klik untuk filter)",
                    )
                    fig_location_pie.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
                    )
                    fig_location_pie.update_layout(clickmode='event+select')
                    selected_data = st.plotly_chart(fig_location_pie, use_container_width=True, on_select="rerun", key="location_pie_chart")
                    
                    # Process selection - check both selection and click events
                    if selected_data:
                        # Check for selection
                        if "selection" in selected_data:
                            points = selected_data["selection"].get("points", [])
                            if points:
                                selected_locs = [p.get("label") for p in points if p.get("label")]
                                if selected_locs and selected_locs != st.session_state.active_filters.get('locations', []):
                                    st.session_state.active_filters['locations'] = selected_locs
                                    st.rerun()
                        # Check for click event
                        elif "click" in selected_data:
                            points = selected_data["click"].get("points", [])
                            if points:
                                selected_locs = [p.get("label") for p in points if p.get("label")]
                                if selected_locs:
                                    st.session_state.active_filters['locations'] = selected_locs
                                    st.rerun()
                
                # Statistik
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Lokasi Unik", len(location_counts))
                with col_stat2:
                    st.metric("Lokasi Teratas", location_counts.iloc[0]["location"] if len(location_counts) > 0 else "N/A")
                with col_stat3:
                    st.metric("Jumlah dari Lokasi Teratas", location_counts.iloc[0]["count"] if len(location_counts) > 0 else 0)
                
                # Tabel detail lokasi
                st.markdown("#### Detail Persebaran Lokasi")
                st.dataframe(
                    location_counts.head(20),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Tidak ada data lokasi yang berhasil diekstrak dari content artikel.")
                st.info("""
                **Catatan:** 
                - Lokasi diekstrak dari konten artikel menggunakan pattern matching
                - Sistem mencari nama provinsi, kota besar, dan referensi lokasi dalam teks
                - Jika tidak ada lokasi yang terdeteksi, mungkin artikel tidak menyebutkan lokasi spesifik
                """)
        else:
            st.warning("Kolom 'relevant_location' tidak tersedia. Pastikan fungsi enrich_with_locations sudah dipanggil.")
            st.info("Lokasi diekstrak dari content artikel menggunakan pattern matching untuk menemukan nama provinsi dan kota di Indonesia.")
    
    with tab3:
        st.markdown("### Platform dan Media")
        
        if "source_url" in filtered_df.columns:
            # Ensure platform column exists
            if "platform" not in filtered_df.columns:
                filtered_df["platform"] = filtered_df["source_url"].apply(extract_platform)
            
            platform_counts = filtered_df["platform"].value_counts().reset_index()
            platform_counts.columns = ["platform", "count"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_platform = px.bar(
                    platform_counts,
                    x="platform",
                    y="count",
                    text="count",
                    title="Distribusi Platform (Klik untuk filter)",
                    color="count",
                    color_continuous_scale=px.colors.sequential.Viridis,
                )
                fig_platform.update_layout(
                    showlegend=False, 
                    xaxis_title="", 
                    yaxis_title="Jumlah", 
                    margin=dict(t=40, l=20, r=20, b=20),
                    clickmode='event+select',
                    dragmode='select'
                )
                fig_platform.update_traces(
                    textposition="outside",
                    selected=dict(marker=dict(color='red', opacity=0.8)),
                    unselected=dict(marker=dict(opacity=0.6))
                )
                fig_platform.update_xaxes(tickangle=-45)
                selected_data = st.plotly_chart(fig_platform, use_container_width=True, on_select="rerun", key="platform_chart")
                
                # Process selection - check both selection and click events
                if selected_data:
                    # Check for selection (box select/drag)
                    if "selection" in selected_data:
                        points = selected_data["selection"].get("points", [])
                        if points:
                            selected_platforms = [p.get("x") for p in points if p.get("x")]
                            if selected_platforms and selected_platforms != st.session_state.active_filters.get('platforms', []):
                                st.session_state.active_filters['platforms'] = selected_platforms
                                st.rerun()
                    # Check for click event
                    elif "click" in selected_data:
                        points = selected_data["click"].get("points", [])
                        if points:
                            selected_platforms = [p.get("x") for p in points if p.get("x")]
                            if selected_platforms:
                                st.session_state.active_filters['platforms'] = selected_platforms
                                st.rerun()
            
            with col2:
                fig_platform_pie = px.pie(
                    platform_counts,
                    values="count",
                    names="platform",
                    title="Proporsi Platform (Klik untuk filter)",
                )
                fig_platform_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
                )
                fig_platform_pie.update_layout(clickmode='event+select')
                selected_data = st.plotly_chart(fig_platform_pie, use_container_width=True, on_select="rerun", key="platform_pie_chart")
                
                # Process selection - check both selection and click events
                if selected_data:
                    # Check for selection
                    if "selection" in selected_data:
                        points = selected_data["selection"].get("points", [])
                        if points:
                            selected_platforms = [p.get("label") for p in points if p.get("label")]
                            if selected_platforms and selected_platforms != st.session_state.active_filters.get('platforms', []):
                                st.session_state.active_filters['platforms'] = selected_platforms
                                st.rerun()
                    # Check for click event
                    elif "click" in selected_data:
                        points = selected_data["click"].get("points", [])
                        if points:
                            selected_platforms = [p.get("label") for p in points if p.get("label")]
                            if selected_platforms:
                                st.session_state.active_filters['platforms'] = selected_platforms
                                st.rerun()
    
    with tab4:
        st.markdown("### Pola dan Timeline")
        
        # Perbandingan Timeline: published_at vs relevant_date
        if "relevant_date" in filtered_df.columns and "published_at" in filtered_df.columns:
            # Konversi published_at ke datetime jika belum
            if filtered_df["published_at"].dtype == 'object':
                filtered_df["published_at"] = pd.to_datetime(filtered_df["published_at"], errors='coerce')
            
            # Filter: relevant_date < published_at dan kedua kolom tidak null
            comparison_df = filtered_df[
                (filtered_df["relevant_date"].notna()) & 
                (filtered_df["published_at"].notna())
            ].copy()
            
            if not comparison_df.empty:
                # Filter dengan kondisi relevant_date < published_at
                comparison_df = comparison_df[
                    pd.to_datetime(comparison_df["relevant_date"]) < pd.to_datetime(comparison_df["published_at"])
                ].copy()
                
                if not comparison_df.empty:
                    st.markdown("#### Perbandingan Timeline: Tanggal Publish vs Tanggal Relevan Hoax")
                    st.caption("📊 Menampilkan data dimana relevant_date < published_at (tanggal hoax terjadi sebelum artikel dipublish)")
                    
                    # Timeline berdasarkan published_at
                    comparison_df["published_date"] = pd.to_datetime(comparison_df["published_at"]).dt.date
                    published_daily = comparison_df.groupby("published_date").size().reset_index()
                    published_daily.columns = ["date", "count"]
                    published_daily = published_daily.sort_values("date")
                    published_daily["type"] = "Tanggal Publish"
                    
                    # Timeline berdasarkan relevant_date
                    comparison_df["relevant_date_only"] = pd.to_datetime(comparison_df["relevant_date"]).dt.date
                    relevant_daily = comparison_df.groupby("relevant_date_only").size().reset_index()
                    relevant_daily.columns = ["date", "count"]
                    relevant_daily = relevant_daily.sort_values("date")
                    relevant_daily["type"] = "Tanggal Relevan Hoax"
                    
                    # Gabungkan untuk chart
                    combined_timeline = pd.concat([
                        published_daily[["date", "count", "type"]],
                        relevant_daily[["date", "count", "type"]]
                    ], ignore_index=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Chart perbandingan timeline
                        fig_comparison = px.line(
                            combined_timeline,
                            x="date",
                            y="count",
                            color="type",
                            title="Perbandingan Timeline: Publish vs Relevan",
                            markers=True,
                            color_discrete_map={
                                "Tanggal Publish": "#FF6B6B",
                                "Tanggal Relevan Hoax": "#4ECDC4"
                            }
                        )
                        fig_comparison.update_layout(
                            xaxis_title="Tanggal",
                            yaxis_title="Jumlah Hoax",
                            legend=dict(
                                title="",
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            ),
                            margin=dict(t=60, l=20, r=20, b=20),
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_comparison, use_container_width=True)
                    
                    with col2:
                        # Statistik perbandingan
                        st.markdown("#### Statistik Perbandingan")
                        
                        avg_delay = (pd.to_datetime(comparison_df["published_at"]) - pd.to_datetime(comparison_df["relevant_date"])).dt.days
                        
                        col_stat1, col_stat2 = st.columns(2)
                        with col_stat1:
                            st.metric(
                                "Rata-rata Delay",
                                f"{avg_delay.mean():.1f} hari",
                                help="Rata-rata selisih hari antara tanggal relevan hoax dan tanggal publish artikel"
                            )
                            st.metric(
                                "Total Artikel",
                                len(comparison_df),
                                help="Jumlah artikel yang memenuhi kondisi relevant_date < published_at"
                            )
                        
                        with col_stat2:
                            st.metric(
                                "Median Delay",
                                f"{avg_delay.median():.0f} hari",
                                help="Median selisih hari antara tanggal relevan hoax dan tanggal publish artikel"
                            )
                            st.metric(
                                "Maks Delay",
                                f"{avg_delay.max():.0f} hari",
                                help="Maksimum selisih hari antara tanggal relevan hoax dan tanggal publish artikel"
                            )
                        
                        # Distribusi delay
                        st.markdown("#### Distribusi Delay (Hari)")
                        delay_df = pd.DataFrame({
                            'delay_days': avg_delay.values
                        })
                        delay_df = delay_df[delay_df['delay_days'] >= 0]  # Hanya delay positif
                        
                        if not delay_df.empty:
                            fig_delay = px.histogram(
                                delay_df,
                                x="delay_days",
                                nbins=30,
                                title="Distribusi Delay Publish",
                                labels={"delay_days": "Delay (Hari)", "count": "Jumlah Artikel"}
                            )
                            fig_delay.update_layout(
                                showlegend=False,
                                margin=dict(t=40, l=20, r=20, b=20)
                            )
                            st.plotly_chart(fig_delay, use_container_width=True)
                    
                    # Timeline bulanan perbandingan
                    st.markdown("---")
                    st.markdown("#### Perbandingan Bulanan")
                    
                    comparison_df["published_month"] = pd.to_datetime(comparison_df["published_at"]).dt.to_period('M').astype(str)
                    comparison_df["relevant_month"] = pd.to_datetime(comparison_df["relevant_date"]).dt.to_period('M').astype(str)
                    
                    published_monthly = comparison_df.groupby("published_month").size().reset_index()
                    published_monthly.columns = ["month", "count"]
                    published_monthly["type"] = "Tanggal Publish"
                    
                    relevant_monthly = comparison_df.groupby("relevant_month").size().reset_index()
                    relevant_monthly.columns = ["month", "count"]
                    relevant_monthly["type"] = "Tanggal Relevan Hoax"
                    
                    combined_monthly = pd.concat([
                        published_monthly[["month", "count", "type"]],
                        relevant_monthly[["month", "count", "type"]]
                    ], ignore_index=True)
                    
                    fig_monthly_comparison = px.bar(
                        combined_monthly,
                        x="month",
                        y="count",
                        color="type",
                        title="Perbandingan Distribusi Bulanan",
                        barmode='group',
                        color_discrete_map={
                            "Tanggal Publish": "#FF6B6B",
                            "Tanggal Relevan Hoax": "#4ECDC4"
                        }
                    )
                    fig_monthly_comparison.update_layout(
                        xaxis_title="Bulan",
                        yaxis_title="Jumlah Hoax",
                        legend=dict(
                            title="",
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        margin=dict(t=60, l=20, r=20, b=60),
                        xaxis=dict(tickangle=-45)
                    )
                    st.plotly_chart(fig_monthly_comparison, use_container_width=True)
                else:
                    st.warning("Tidak ada data yang memenuhi kondisi relevant_date < published_at.")
            else:
                st.warning("Tidak ada data dengan both relevant_date dan published_at yang tersedia.")
        
        # Timeline berdasarkan relevant_date (untuk semua data, tidak hanya yang memenuhi kondisi)
        if "relevant_date" in filtered_df.columns:
            st.markdown("---")
            st.markdown("#### Timeline Berdasarkan Tanggal Relevan Hoax (Semua Data)")
            
            date_df = filtered_df[filtered_df["relevant_date"].notna()].copy()
            if not date_df.empty:
                date_df["date"] = pd.to_datetime(date_df["relevant_date"]).dt.date
                daily_counts = date_df.groupby("date").size().reset_index()
                daily_counts.columns = ["date", "count"]
                daily_counts = daily_counts.sort_values("date")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_timeline = px.line(
                        daily_counts,
                        x="date",
                        y="count",
                        title="Timeline Hoax per Hari (Berdasarkan Relevant Date)",
                        markers=True,
                    )
                    fig_timeline.update_layout(xaxis_title="Tanggal", yaxis_title="Jumlah Hoax", margin=dict(t=40, l=20, r=20, b=20))
                    st.plotly_chart(fig_timeline, use_container_width=True)
                
                with col2:
                    # Pola bulanan
                    date_df["month"] = pd.to_datetime(date_df["relevant_date"]).dt.to_period('M').astype(str)
                    monthly_counts = date_df.groupby("month").size().reset_index()
                    monthly_counts.columns = ["month", "count"]
                    
                    fig_monthly = px.bar(
                        monthly_counts,
                        x="month",
                        y="count",
                        text="count",
                        title="Distribusi Bulanan (Berdasarkan Relevant Date)",
                        color="count",
                        color_continuous_scale=px.colors.sequential.Blues,
                    )
                    fig_monthly.update_layout(showlegend=False, xaxis_title="Bulan", yaxis_title="Jumlah", margin=dict(t=40, l=20, r=20, b=20))
                    fig_monthly.update_traces(textposition="outside")
                    fig_monthly.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig_monthly, use_container_width=True)
                
                # Pola harian (hari dalam minggu)
                date_df["day_of_week"] = pd.to_datetime(date_df["relevant_date"]).dt.day_name()
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_counts = date_df["day_of_week"].value_counts().reindex(day_order, fill_value=0).reset_index()
                day_counts.columns = ["day", "count"]
                
                fig_day = px.bar(
                    day_counts,
                    x="day",
        y="count",
        text="count",
                    title="Pola Harian (Hari dalam Minggu)",
                    color="count",
                    color_continuous_scale=px.colors.sequential.Reds,
                )
                fig_day.update_layout(showlegend=False, xaxis_title="Hari", yaxis_title="Jumlah", margin=dict(t=40, l=20, r=20, b=20))
                fig_day.update_traces(textposition="outside")
                st.plotly_chart(fig_day, use_container_width=True)
            else:
                st.warning("Tidak ada data tanggal yang tersedia untuk analisis timeline.")
        else:
            st.warning("Kolom 'relevant_date' tidak tersedia untuk analisis timeline.")
    

else:
    st.warning("Kolom 'relevant_date' tidak ditemukan atau kosong. Menampilkan semua data.")
    st.dataframe(df)


import streamlit as st
import pandas as pd
import plotly.express as px

from loaders.article_loader import load_articles_df, enrich_with_dates

st.set_page_config(page_title="BI Hoax Analyzer", layout="wide")

@st.cache_data(show_spinner=True)
def get_data():
    df = load_articles_df()
    df = enrich_with_dates(df)
    if "relevant_date" in df.columns:
        df["relevant_date"] = pd.to_datetime(df["relevant_date"], errors="coerce")
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

    # st.dataframe(shown_df)
    
    counts = shown_df["categories"].fillna("(unknown)").value_counts().reset_index()
    counts.columns = ["categories", "count"]
    fig = px.bar(
        counts,
        x="categories",
        y="count",
        color="categories",
        text="count",
        title="Jumlah Hoax per Kategori",
        color_discrete_sequence=px.colors.qualitative.Light24,
    )
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Jumlah", margin=dict(t=40, l=20, r=20, b=20))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)    

else:
    st.warning("Kolom 'relevant_date' tidak ditemukan atau kosong. Menampilkan semua data.")
    st.dataframe(df)


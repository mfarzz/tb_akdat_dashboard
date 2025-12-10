import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import streamlit as st
from babel.numbers import format_currency


def create_daily_orders_all_data(all_data):
    daily_orders_all_data = all_data.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_all_data = daily_orders_all_data.reset_index()
    daily_orders_all_data.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_orders_all_data

def product_sales(all_data):
    products_count = all_data.groupby('product_category_name_english')['product_id'].count().reset_index()
    product_count_sort = products_count.sort_values(by='product_id', ascending=False)
    return product_count_sort

def corrolation_products(all_data):
    product_sales = all_data.groupby('product_id').agg({
        'order_item_id': 'count',
        'price': 'mean',
        'product_category_name_english': 'first',
        'freight_value': 'mean'
    }).reset_index()
    product_sales.columns = ['product_id', 'total_sales', 'avg_price', 'category', 'avg_freight']
    return product_sales

def payment_type(all_data):
    payment_counts = all_data.groupby('payment_type')['payment_value'].size().reset_index(name='count')
    sorted_payment_counts = payment_counts.sort_values(by='count', ascending=False)
    return sorted_payment_counts

def sales_by_month(all_data):
    sales_per_month_new = all_data.groupby('month_purchase')['payment_value'].sum()
    sales_per_month_new = sales_per_month_new.sort_index(key=lambda x: pd.to_datetime(x, format='%B %Y'))
    return sales_per_month_new

def sales_by_year(all_data):
    sales_per_year = all_data.groupby(all_data['order_purchase_timestamp'].dt.to_period('Y')).agg(
        total_payment_value=('payment_value', 'sum'),
        year=('order_purchase_timestamp', lambda x: x.unique()[0].year)
    )
    sales_per_year.reset_index(inplace=True)
    return sales_per_year  

def rfm(all_data):
    now =  dt.datetime(2018,10,18)
    rfm_data = all_data.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": lambda x: (now - x.max()).days,
        "order_id": 'count',
        "price": 'sum'
    })
    rfm_data.columns = ["customer_id", "recency", "frequency", "monetary"]
    customer_mapping = {id_: str(index) for index, id_ in enumerate(rfm_data['customer_id'].unique())}
    rfm_data['customer_id_new'] = rfm_data['customer_id'].map(customer_mapping)
    return rfm_data


all_data = pd.read_csv('dashboard/main_data.csv')

all_data.sort_values(by="order_purchase_timestamp", inplace=True)
all_data.reset_index(inplace=True)

all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])

min_date = all_data["order_purchase_timestamp"].min()
max_date = all_data["order_purchase_timestamp"].max()

with st.sidebar:
    
    st.image("https://www.riotimesonline.com/wp-content/uploads/2020/12/ecommerce-brazil.jpeg", width=290)
    st.title("Brazilian E-Commerce Dashboard")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_data[(all_data["order_purchase_timestamp"] >= str(start_date)) & (all_data["order_purchase_timestamp"] <= str(end_date))]

daily_orders = create_daily_orders_all_data(main_df)
product_sales_data = product_sales(main_df)
corrolation_products_data = corrolation_products(main_df)
payment_type_data = payment_type(main_df)
sales_by_month_data = sales_by_month(main_df)
sales_by_year_data = sales_by_year(main_df)
rfm_data = rfm(main_df)


st.header('Dashboard Eccoomerce Public Brazil')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders["order_purchase_timestamp"],
    daily_orders["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.markdown('<h4 style="font-size: 24px;">Produk yang Memiliki Penjualan Terbanyak dan Terendah</h4>', unsafe_allow_html=True)
    
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["crimson"] + ["#D3D3D3"] * 4
sns.barplot(x="product_id", y="product_category_name_english",
        data=product_sales_data.head(5),
        palette=colors,
        hue='product_category_name_english',
        ax=ax[0],
        legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=35)
ax[0].set_title("Produk dengan Penjualan Paling Banyak", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=33)
ax[0].tick_params(axis='x', labelsize=33)
ax[0].grid(axis='x')
ax[0].set_axisbelow(True)

sns.barplot(x="product_id", y="product_category_name_english",
        data=product_sales_data.sort_values(by="product_id", ascending=True).head(5),
        palette=colors,
        hue='product_category_name_english',
        ax=ax[1],
        legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=35)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk dengan Penjualan Paling Sedikit", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=33)
ax[1].tick_params(axis='x', labelsize=33)
ax[1].grid(axis='x')
ax[1].set_axisbelow(True)

st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
            """Berdasarkan visualisasi bar chart yang ditampilkan 
            dapat disimpulkan produk dengan penjualan yang paling 
            banyak adalah bed_bath_table dan produk yang paling 
            sedikit penjualan adalah security_and_service.
            """
    )

st.subheader("Korelasi Produk dan Trend Penjualan")

col1, col2 = st.columns(2)

with col1:
    plt.figure(figsize=(6, 4))
    correlation_matrix = corrolation_products_data[['total_sales', 'avg_price', 'avg_freight']].corr()
    sns.heatmap(correlation_matrix,
            annot=True,  # Menampilkan nilai korelasi
            cmap='coolwarm',  # Colormap: merah untuk positif, biru untuk negatif
            vmin=-1, vmax=1,  # Range nilai
            center=0,  # Nilai tengah colormap
            fmt='.2f')  # Format angka dengan 2 desimal
    st.pyplot(plt)

with col2:
    plt.figure(figsize=(6, 4))
    correlation = corrolation_products_data['avg_price'].corr(corrolation_products_data['total_sales'])
    sns.scatterplot(data=corrolation_products_data,
                x='avg_price',
                y='total_sales',
                alpha=0.5)
    sns.regplot(data=corrolation_products_data,
            x='avg_price',
            y='total_sales',
            scatter=False,
            color='red',
            line_kws={'linestyle': '--'})
    plt.title('Hubungan antara Harga dan Jumlah Penjualan Produk')
    plt.xlabel('Rata-rata Harga Produk (R$)')
    plt.ylabel('Total Penjualan')
    st.pyplot(plt)

with st.expander("See explanation"):
    st.write(
            """ Kemudian dari heatmap dan scatter plot yang 
            ditampilkan menunjukkan bahwa harga produk tidak 
            mempengaruhi banyaknya produk itu terjual, hanya sebesar 
            -0.03 persen hubungan antara pengaruh harga terhadap penjualan.
            """
    )

st.subheader("Metode Pembayaran yang Paling Banyak Digunakan")

fig, ax = plt.subplots()
colors = ["crimson"] + ["#D3D3D3"] * 4

# Membuat barplot
sns.barplot(x="payment_type", y="count",
            data=payment_type_data,
            ax=ax,
            palette=colors)

# Menyesuaikan label dan judul
ax.set_ylabel("Count", fontsize=12)
ax.set_xlabel("Payment Type", fontsize=12)
ax.set_title("Distribution of Payment Types", loc="center", fontsize=15)
ax.tick_params(axis='x', labelsize=12, rotation=45)
ax.tick_params(axis='y', labelsize=12)
ax.grid(True, axis = 'y')
ax.set_axisbelow(True)

st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
            """Berdasarkan grafik dapat dilihat bahwa terdapat 
            4 metode pembayaran yang digunakan mulai 
            dari yang paling banyak digunakan yaitu, kredit card, boleto, 
            voucher, dan debit card. Kemudian terdapat data metode pembayaran 
            yang tidak diketahui
            """
    )

st.subheader("Pendapatan dari penjualan yang terjadi selama ini")

col1, col2= st.columns([1.5, 1])

with col1:
    st.write("Pendapatan Per Bulan")
    fig, ax = plt.subplots( figsize=(12, 10))
    ax.plot(
        sales_by_month_data.index, 
        sales_by_month_data, 
        color='crimson',
        marker='o')
    ax.set_xlabel('Tahun', fontsize=20)
    ax.set_ylabel('Total Harga Penjualan', fontsize=20)
    ax.grid()
    ax.tick_params(axis='x', rotation=90, labelsize=15)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

with col2:
    st.write("Pendapatan Per Tahun")
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#e8b5b5"] + ['#d06666'] + ["#b51010"] 
    bar_container = ax.bar(
        sales_by_year_data['year'].astype(str),  
        sales_by_year_data['total_payment_value'],  
        color=colors,    
    )
    ax.set_xlabel('Tahun', fontsize=17)
    ax.set_ylabel('Total Harga Penjualan', fontsize=17)
    ax.grid(axis='y')  
    ax.set_axisbelow(True)
    ax.bar_label(bar_container, fmt='{:,.0f}', fontsize=15)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
            """Berdasarkan grafik garis yang ditampilkan dapat 
            disimpulkan bahwa total penjualan per bulan itu 
            fluaktif dan cenderung meningkat hingga pada Oktober 
            2017 merupakan total penjualan paling tinggi. Kemudian 
            terjadi penurunan yang signifikan dari bulan Juli 2018 hingga
            Agustus 2018. Dapat diperkirakan pada bulan selanjutnya total 
            penjualan lebih sulit untuk meningkat
            """
    )

st.subheader('RFM Analysis')
tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

with tab1:
    fig, ax = plt.subplots(figsize=(24, 12))
    color = "crimson"
    recency_sorted = rfm_data.sort_values(by="recency", ascending=True).head(5)
    sns.barplot(y="recency", x="customer_id_new", data=recency_sorted, color=color, ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel('ordered_id_new', fontsize=26)
    ax.tick_params(axis='x', labelsize=24)
    ax.tick_params(axis='y', labelsize=24)
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(24, 12))
    color = "crimson"
    frequency_sorted = rfm_data.sort_values(by="frequency", ascending=False).head(5)
    sns.barplot(y="frequency", x="customer_id_new", data=frequency_sorted, color=color, ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel('ordered_id_new', fontsize=26)
    ax.tick_params(axis='x', labelsize=24)
    ax.tick_params(axis='y', labelsize=24)
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(24, 12))
    color = "crimson"
    monetary_sorted = rfm_data.sort_values(by="monetary", ascending=False).head(5)
    sns.barplot(y="monetary", x="customer_id_new", data=monetary_sorted, color=color, ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel('ordered_id_new', fontsize=26)
    ax.tick_params(axis='x', labelsize=24)
    ax.tick_params(axis='y', labelsize=24)
    st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
            """Pada visualisai RFM dapat dilihat pada visualisai 
            By Recency menunjukan transaksi customer dalam satu 
            hari yang paling sedikit. Pada By Frekuensi menunjukan 
            banyak transaksi yang dilakukan oleh customer seluruh 
            periode yang diurutkan dari paling banyak. Pada By 
            Monetery menunjukkan total pengeluaran customer pada 
            transaksi selama seluruh periode
            """
    )
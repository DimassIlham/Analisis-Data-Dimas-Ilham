import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st

# Load data
all_data_df = pd.read_csv("Data/all_data_tabel_df.csv")

# Menggabungkan data on order_id untuk mendapatkan hitungan antara product dan review score
product_count_and_score = pd.merge(all_data_df.groupby('order_id')['order_item_id'].count().reset_index(),
                                   all_data_df[['order_id', 'review_score']], on='order_id')


all_data_df['order_purchase_timestamp'] = pd.to_datetime(all_data_df['order_purchase_timestamp'])

now = dt.datetime(2018, 12, 30)

rfm_df = all_data_df.groupby(by='customer_id', as_index=False).agg({
    'order_purchase_timestamp': 'max',
    'order_id': 'count',
    'price': 'sum',
})

rfm_df.columns = ['customer_id', 'max_order_timestamp', 'frequency', 'monetary']

rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (now - x).days)
rfm_df.drop('max_order_timestamp', axis=1, inplace=True)

st.sidebar.title("Opsi Analisis")
analysis_choice = st.sidebar.radio("Pilih Analisis", ["Penjualan Produk", "Review dari Customer", "Pola Pembayaran", "Analisis RFM"])

st.title("Dashboard: Analisis Data E-Commerce Oleh Dimas Ilham")

if analysis_choice == "Penjualan Produk":
    st.header("Analisis Penjualan Produk")
    st.subheader("Top 5 Produk Terbanyak Terjual")
    best_selling_products = all_data_df.groupby("product_category_name_english").size().nlargest(5)
    st.bar_chart(best_selling_products)

    st.subheader("Top 5 Produk Tersedikit Terjual")
    worst_selling_products = all_data_df.groupby("product_category_name_english").size().nsmallest(5)
    st.bar_chart(worst_selling_products)

elif analysis_choice == "Review dari Customer":
    st.header("Analisis Review dari Customer")
    st.subheader("Distribusi dari Penilaian Skor Review")
    review_scores = all_data_df["review_score"].value_counts().sort_index()
    st.bar_chart(review_scores)

    st.subheader("Skor Review vs Kuantitas Prouduk")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='review_score', y='order_item_id', data=product_count_and_score, alpha=0.5, ax=ax)
    ax.set_title('Korelasi antara Skor Review dan Banyaknya Kuantitas Produk')
    ax.set_xlabel('Skor Review')
    ax.set_ylabel('Banyaknya Kuantitas Produk')
    st.pyplot(fig)


elif analysis_choice == "Pola Pembayaran":
    st.header("Ananlisi Pola Pembayaran")
    st.subheader("Grafik Metode Pembayaran")
    payment_methods = all_data_df["payment_type"].value_counts()
    st.bar_chart(payment_methods)

    st.subheader("Distribusi dari Jumlah Pembayaran")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(all_data_df['payment_value'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribusi dari Jumlah Pembayaran')
    ax.set_xlabel('Banyaknya Jumlah Pembayaran')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)


elif analysis_choice == "Analisis RFM":

    st.header("Analisis RFM")
    st.subheader("Top 5 Best Customers Based Berdasarkan RFM Parameter")

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

    sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel('Customer ID')
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis='x', labelsize=15)
    ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=90)
    ax[0].set_xticks([])

    sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel('Customer ID')
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)
    ax[1].set_xticklabels(ax[0].get_xticklabels(), rotation=90)
    ax[1].set_xticks([])

    sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel('Customer ID')
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)
    ax[2].set_xticklabels(ax[0].get_xticklabels(), rotation=90)
    ax[2].set_xticks([])

    plt.suptitle("Best Customer Based on RFM Parameters (Customer ID)", fontsize=20)

    st.pyplot(fig)

# menambah footer di sidebar
st.sidebar.title("About")
st.sidebar.info("Copyright (c) Dimas Ilham 2024")

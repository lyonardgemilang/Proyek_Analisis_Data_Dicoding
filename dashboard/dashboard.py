import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Proyek Analisis Data Dashboard")
st.caption("Dashboard made by MC006D5Y1165 - Lyonard Gemilang Putra Merdeka Gustiansyah")
uploaded_file = st.file_uploader("Pilih file CSV yang sudah bersih Anda", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['dteday'])

    try:
        min_date = df['dteday'].min().date()
        max_date = df['dteday'].max().date()
        start_date = st.sidebar.date_input("Pilih Start Date", value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input("Pilih End Date", value=max_date, min_value=min_date, max_value=max_date)
        
        if start_date > end_date:
            st.sidebar.error("Tanggal mulai harus sebelum atau sama dengan tanggal terakhir.")
        else:
            df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]
    except Exception as e:
        st.sidebar.error("Terjadi error pada filter tanggal: " + str(e))
    
    st.sidebar.title("Pilih Visualisasi")
    option = st.sidebar.selectbox(
        "Pilih visualisasi:",
        ("Home", "Total Sewa per Musim", "Total Sewa per Hari Kerja", "Total Sewa per Musim beserta Kondisi Iklim", "Tren Sewa Sepeda 2011-2012")
    )

    st.header("Data Overview")
    st.write(df.head())

    with st.expander("Keterangan"):
        st.write("""
        - **instant**: Record index
        - **dteday**: Date
        - **season**: Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)
        - **yr**: Year (0: 2011, 1: 2012)
        - **mnth**: Month (1 to 12)
        - **hr**: Hour (0 to 23)
        - **holiday**: Whether the day is a holiday (1: Yes, 0: No)
        - **weekday**: Day of the week
        - **workingday**: Whether the day is a working day (1: Yes, 0: No)
        - **weathersit**: Weather situation
          - 1: Clear, Few clouds, Partly cloudy
          - 2: Mist + Cloudy, Mist + Broken clouds
          - 3: Light Snow, Light Rain + Thunderstorm
          - 4: Heavy Rain + Thunderstorm + Snow
        - **temp**: Normalized temperature in Celsius
        - **atemp**: Normalized feeling temperature in Celsius
        - **hum**: Normalized humidity
        - **windspeed**: Normalized wind speed
        - **casual**: Count of casual users
        - **registered**: Count of registered users
        - **cnt**: Count of total rental bikes (casual + registered)
        """)
    if option == 'Home':
        st.write("Silakan pilih visualisasi yang ingin Anda lihat di sidebar.")
        
    elif option == "Total Sewa per Musim":
        st.subheader("Total Sewa per Musim")
        fig, ax = plt.subplots(figsize=(10, 6))
        season_counts = df.groupby('season')['cnt'].sum()
        colors = ['lightblue' if count != season_counts.max() else 'blue' for count in season_counts]
        season_counts.plot(kind='bar', color=colors, ax=ax)
        ax.set_xlabel('Season')
        ax.set_ylabel('Count')
        ax.set_title('Total Count berdasarkan Season')
        plt.xticks(rotation=0)
        st.pyplot(fig)
        
        with st.expander("Penjelasan"):
            st.write("""
            Bar chart di atas menunjukkan total sewa sepeda berdasarkan hari kerja.
            Dari bar chart yang ditampilkan, musim (season) fall (gugur) merupakan musim dengan 
            paling banyak sewa sepeda dan musim spring (semi) dengan paling sedikit sewa sepeda. 
            """)

    elif option == "Total Sewa per Hari Kerja":
        st.subheader("Total Sewa Berdasarkan Hari Kerja")
        fig, ax = plt.subplots(figsize=(10, 6))
        workingday_counts = df.groupby('workingday')['cnt'].sum()
        colors = ['lightblue' if cnt != workingday_counts.max() else 'blue' for cnt in workingday_counts]
        workingday_counts.plot(kind='bar', color=colors, ax=ax)
        ax.set_xlabel('Working day')
        ax.set_ylabel('Count')
        ax.set_title('Total Count berdasarkan workingday')
        plt.xticks(rotation=0)
        st.pyplot(fig)
        
        with st.expander("Penjelasan"):
            st.write("""
            Bar chart di atas menunjukkan total sewa sepeda berdasarkan hari kerja.
            Dari bar chart yang ditampilkan, para pengguna banyak menyewa sepeda 
            pada waktu kerja dibandingkan dengan waktu libur ataupun weekend. 
            """)
        
    elif option == "Total Sewa per Musim beserta Kondisi Iklim":
        bins = [0, 0.33, 0.66, 1.0]
        kategori = ['Low Temp', 'Medium Temp', 'High Temp']

        df['temp_category'] = pd.cut(df['temp'], bins=bins, labels=kategori, include_lowest=True)

        season_kondisi = df.groupby(['season', 'weathersit', 'temp_category']).agg({
            'cnt': ['sum', 'mean', 'max', 'min']
        }).reset_index()
        g = sns.catplot(data=season_kondisi, kind='bar', x='season', y=('cnt', 'sum'), hue='weathersit', col='temp_category', errorbar=None, height=5, aspect=1.2, palette='Set1')
        g.set_axis_labels("Season", "Total Count")
        st.pyplot(g.figure)

        with st.expander("Penjelasan"):
            st.write("""
            Bar chart di atas menunjukkan total sewa sepeda berdasarkan musim beserta kondisi iklimnya.
            Dari bar chart yang ditampilkan, musim (season) fall (gugur) merupakan musim dengan 
            paling banyak sewa sepeda dan musim spring (semi) dengan paling sedikit sewa sepeda. 
            Orang-orang banyak menyewa sepeda di suhu yang tinggi dan juga cuaca yang cerah.  
            """)

    elif option == "Tren Sewa Sepeda 2011-2012":
        st.subheader("Tren Sewa Sepeda dari 2011-2012")
        df['dteday'] = pd.to_datetime(df['dteday'])
        rental_bulanan = df.groupby(df['dteday'].dt.to_period('M'))['cnt'].sum()

        fig, ax = plt.subplots(figsize=(16, 7))
        ax.plot(rental_bulanan.index.to_timestamp(), rental_bulanan, marker='o', color='lightblue')

        start_2012 = rental_bulanan.index >= '2012-01'
        ax.plot(rental_bulanan.index.to_timestamp()[start_2012], rental_bulanan[start_2012], marker='o', color='blue')
        
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Total Rental')
        ax.set_title('Total Bike Rentals dari 2011 ke 2012')
        st.pyplot(fig)
        
        with st.expander("Penjelasan"):
            st.write("""
            Line chart di atas menunjukkan tren sewa sepeda secara bulanan dari 2011 hingga 2012.
            Dari line chart yang ditampilkan, total sewa sepeda terbanyak berada di September 2012 (2012-9). Selain itu, 
            dapat disimpulkan bahwa jumlah sewa sepeda tahun 2012 mengalami peningkatan 
            dibandingkan tahun 2011.
            """)
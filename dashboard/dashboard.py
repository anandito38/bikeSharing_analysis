import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import streamlit as st
import seaborn as sns

sns.set(style="dark")
hour_df = pd.read_csv('dashboard/hour.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)

drop = ['instant','windspeed', 'weathersit']

for i in hour_df.columns:
    if i in drop:
        hour_df.drop(labels=i, axis=1, inplace=True)

hour_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count',
    'hr': 'hour'
}, inplace=True)

hour_df['month'] = hour_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Ags', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
})

hour_df['season'] = hour_df['season'].map({
    1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'
})

hour_df['year'] = hour_df['year'].map({
    0: '2011', 1: '2012'
})

hour_df['weekday'] = hour_df['weekday'].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
})

hour_df['dateday'] = pd.to_datetime(hour_df['dateday'])

hour_df['season'] = hour_df.season.astype('category')
hour_df['year'] = hour_df.year.astype('category')
hour_df['month'] = hour_df.month.astype('category')
hour_df['holiday'] = hour_df.holiday.astype('category')
hour_df['weekday'] = hour_df.weekday.astype('category')
hour_df['workingday'] = hour_df.workingday.astype('category')

def create_hour(hour_df):
    hour_ds = hour_df.groupby(by='hour').agg({
        'count': 'sum'
    }).reset_index()
    return hour_ds

def create_day(hour_df):
    day_ds = hour_df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return day_ds

def create_month(hour_df):
    month_ds = hour_df.groupby(by='month', observed=True).agg({
        'count': 'sum'
    }).reset_index()
    return month_ds

min_dtday = pd.to_datetime(hour_df['dateday']).dt.date.min()
max_dtday = pd.to_datetime(hour_df['dateday']).dt.date.max()

with st.sidebar:
    st.text('Filter')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_dtday,
        max_value= max_dtday,
        value=[min_dtday, max_dtday]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

import matplotlib.pyplot as plt
main_df = hour_df[(hour_df['dateday'] >= start_date) & (hour_df['dateday'] <= end_date)]

hour_ds = create_hour(main_df)
day_ds = create_day(main_df)
month_ds = create_month(main_df)

st.title('Bikeshare Data Analysis Dashboard')
st.markdown('##')

st.subheader('Pola Penyewaan Sepeda berdasarkan rentang jam, hari kerja, hari libur, dan hari') 
plt.figure(figsize=(10, 6))
sns.lineplot(x='hour', y='count', hue='workingday', data=hour_df)

plt.xlabel('Jam pada Hari')
plt.ylabel('Banyak Penyewa Sepeda')
plt.title('Penyewa Sepeda berdasarkan jam Workingday')

plt.legend(title='Workingday')
st.pyplot()
#
plt.figure(figsize=(10, 6))
sns.lineplot(x='hour', y='count', hue='holiday', data=hour_df)

plt.xlabel('Jam pada Hari')
plt.ylabel('Banyak Penyewa Sepeda')
plt.title('Penyewa Sepeda berdasarkan jam holiday')

plt.legend(title='holiday')
st.pyplot()

plt.figure(figsize=(10, 6))
sns.lineplot(x='hour', y='count', hue='weekday', data=hour_df)

plt.xlabel('Jam pada Hari')
plt.ylabel('Banyak Penyewa Sepeda')
plt.title('Penyewa Sepeda berdasarkan jam Weekday')

plt.legend(title='Weekday')
st.pyplot()

st.subheader('Total Jumlah Penyewa Sepeda per Bulan dan Tahun') 
hour_df['month'] = pd.Categorical(hour_df['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'], ordered=True)

monthly_counts = hour_df.groupby(by=["month", "year"]).agg({"count": "sum"}).reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_counts, x="month", y="count", hue="year",
            palette="rocket", marker="o", ax=ax)

plt.title("Total Jumlah Penyewa Sepeda per Bulan dan Tahun")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Total Penyewa Sepeda")

plt.legend(title="Tahun", loc="upper right")
st.pyplot(fig)

st.subheader('Pola Penyewaan Sepeda berdasarkan temp, atemp, dan humidity')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

sns.kdeplot(
    x='temp',
    y='count',
    data=hour_df,
    ax=axes[0],
    fill=True
)
axes[0].set_title('Distribusi Frekuensi Jumlah Penyewaan Sepeda berdasarkan Temperature')
axes[0].set_xlabel('Temperature')
axes[0].set_ylabel('Counts')

sns.kdeplot(
    x='atemp',
    y='count',
    data=hour_df,
    ax=axes[1],
    fill=True
)
axes[1].set_title('Distribusi Frekuensi Jumlah Penyewaan Sepeda berdasarkan Feeling Temperature')
axes[1].set_xlabel('Feeling Temperature')
axes[1].set_ylabel('Counts')

sns.kdeplot(
    x='hum',
    y='count',
    data=hour_df,
    ax=axes[2],
    fill=True
)
axes[2].set_title('Distribusi Frekuensi Jumlah Penyewaan Sepeda berdasarkan Humidity')
axes[2].set_xlabel('Humidity')
axes[2].set_ylabel('Counts')

plt.subplots_adjust(hspace=0.5)
st.pyplot(fig)

st.subheader('Pola Penyewa Sepeda berdasarkan musim')
seasonal_usage = hour_df.groupby('season')[['registered', 'casual']].sum().reset_index()

plt.figure(figsize=(10, 6))
bar_width = 0.4
bar_position_reg = [1, 2, 3, 4]
bar_position_cas = [x + bar_width for x in bar_position_reg]

plt.bar(
    bar_position_reg,
    seasonal_usage['registered'],
    label='Registered',
    color='tab:blue',
    width=bar_width
)

plt.bar(
    bar_position_cas,
    seasonal_usage['casual'],
    label='Casual',
    color='tab:orange',
    width=bar_width
)

plt.xlabel('Season')
plt.ylabel('Total Penyewa Sepeda')
plt.title('Jumlah Penyewa Sepeda Berdasarkan Musim')

season_labels = sorted(hour_df['season'].unique())
plt.xticks(bar_position_reg, season_labels)

plt.legend()
st.pyplot(plt)

st.caption('Dashboard ini dibuat oleh Anandito Satria Asyraf')
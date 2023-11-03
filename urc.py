import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV dosyasını yükleme
url="ortalamalar.csv"
df = pd.read_csv(url)
st.set_page_config(layout="wide")
# Günlük maksimum ortalama rüzgar hızı
df_daily_max = df.groupby('TIME')['Wind120'].max()
df_daily_max = df_daily_max.reset_index()

# Günlük maksimum rüzgar hızına sahip çiftlikleri bulma
max_farms = []
for index, row in df_daily_max.iterrows():
    max_wind_speed = row['Wind120']
    max_farm = df[(df['TIME'] == row['TIME']) & (df['Wind120'] == max_wind_speed)]['farm_unique_name'].values
    max_farms.append(max_farm[0])

# Kullanıcıya seçenekleri sunma
farm_count = len(df['farm_unique_name'].unique())
st.sidebar.write(f"Toplam {farm_count} saha mevcut. Lütfen saha seç:")
selected_farms = []
for farm in df['farm_unique_name'].unique():
    selected = st.sidebar.checkbox(farm)
    if selected:
        selected_farms.append(farm)

# Seçilen çiftlikleri filtreleme
df_selected = df[df['farm_unique_name'].isin(selected_farms)]
selected_farms_str = ", ".join(selected_farms)
if selected_farms_str:
    st.title(f"Seçilen Sahalar: {selected_farms_str}")
else:
    st.title("Lütfen Saha Seç")
    
# Seçilen çiftliklerin genel 15 günlük ortalama rüzgar hızlarını hesaplama
farm_avg_wind_speed = {}
for farm in selected_farms:
    avg_wind_speed = df_selected[df_selected['farm_unique_name'] == farm]['Wind120'].mean()
    farm_avg_wind_speed[farm] = avg_wind_speed

# Sıralanmış ortalama rüzgar hızlarını alıp gösterme
sorted_farm_avg_wind_speed = sorted(farm_avg_wind_speed.items(), key=lambda x: x[1], reverse=True)
expander = st.expander("Hangi RES Önde? 15 günlük ortalama rüzgar sıralamasını görmek için tıkla!")
with expander:
    for i, (farm, avg_speed) in enumerate(sorted_farm_avg_wind_speed):
        avg_speed_rounded = round(avg_speed, 2)  # Virgülden sonra 2 hane
        if i == 0:
            st.write(f"🥇 1. {farm}: {avg_speed_rounded} m/s")  # Altın madalya
        elif i == 1:
            st.write(f"🥈 2. {farm}: {avg_speed_rounded} m/s")  # Gümüş madalya
        elif i == 2:
            st.write(f"🥉 3. {farm}: {avg_speed_rounded} m/s")  # Bronz madalya
        else:
            st.write(f"{i+1}. {farm}: {avg_speed_rounded} m/s")
# Grafiği oluşturma
if not df_selected.empty:
    fig, ax = plt.subplots(figsize=(10,2))  # Boyutları istediğiniz gibi ayarlayabilirsiniz
    for farm in selected_farms:
        df_farm = df_selected[df_selected['farm_unique_name'] == farm]
        ax.plot(df_farm['TIME'], df_farm['Wind120'], label=farm)

    ax.scatter(df_daily_max['TIME'], df_daily_max['Wind120'], color='red', label='İlgili günün en yüksek hızına sahip sahalar')
    for i, txt in enumerate(max_farms):
        ax.annotate(txt, (df_daily_max['TIME'][i], df_daily_max['Wind120'][i]), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_ylabel('Rüzgar Hızı (m/s)')
    ax.set_title('15 Günlük Ortalama Rüzgar Hızı ')
    ax.set_xlabel('Zaman')
    ax.legend()

    # Rotate x-axis labels
    plt.xticks(rotation=90)

    st.pyplot(fig)
else:
    st.write("Lütfen grafikleri görebilmek için sol seçim menüsünden en az bir saha seçin.")
    
    

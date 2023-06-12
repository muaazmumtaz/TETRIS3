# Lakukan Import Library
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from PIL import Image
from plotly.subplots import make_subplots

# Setting Streamlit
st.set_page_config(layout="wide")

# Title
st.title("Kemiskinan & Ketimpangan di Indonesia")
st.markdown('Oleh : Muhammad Atqa Adzkia Zaldi')
st.markdown('Medan, 12 Juni 2023')

# Baca Dataset (Untuk Menghindari Error)
data_ribu = pd.read_excel('DATA/Profil Kemiskinan.xlsx', sheet_name='Jumlah')
data_persen = pd.read_excel('DATA/Profil Kemiskinan.xlsx', sheet_name='Persentase')
data_GK = pd.read_excel('DATA/Profil Kemiskinan.xlsx', sheet_name='Garis Kemiskinan')
data_ART = pd.read_excel('DATA/Profil Kemiskinan.xlsx', sheet_name='GK_ART')
data_GR = pd.read_excel('DATA/Profil Kemiskinan.xlsx', sheet_name='Gini Ratio')
data_gdp = pd.read_excel('DATA/DATA Indonesia.xlsx')

def rupiah(number):
    # Convert the number to a string
    number_str = str(number)

    # Split the number into integer and decimal parts
    parts = number_str.split(".")

    # Format the integer part with a thousands separator
    integer_part = parts[0]
    integer_part = "{0:,}".format(int(integer_part)).replace(",", ".")

    # Format the decimal part or add ".00" if it's missing
    decimal_part = parts[1] if len(parts) > 1 else "00"

    # Combine the integer and decimal parts with the currency symbol
    formatted_number = f"Rp. {integer_part},{decimal_part}"

    return formatted_number

st.markdown('### BAB I. Pendahuluan')

'''
Kemiskinan merupakan salah satu permasalahan besar yang dihadapi terutama oleh negara berkembang. Penyebab utama dari kemiskinan yaitu tidak adanya pemerataan distribusi pendapatan yang menghasilkan ketimpangan penghasilan. Ketimpangan merupakan masalah yang harus dihadapi karena memiliki konsekuensi negatif dan dapat mempengaruhi kondisi sosial politik suatu negara.
'''

col1, col2, col3 = st.columns(3)

with col1:
   option1 = st.selectbox('Pilih Periode',
                         ('Maret 2017', 'September 2017',
                          'Maret 2018', 'September 2018',
                          'Maret 2019', 'September 2019',
                          'Maret 2020', 'September 2020',
                          'Maret 2021', 'September 2021',
                          'Maret 2022', 'September 2022'))
   if "Maret" in option1:
      bulan = "03-" + option1[-4:]
   else:
      bulan = "09-" + option1[-4:]

with col2:
   option2 = st.selectbox('Pilih Tipe',
                         ('Perkotaan', 'Pedesaan', 'Total'))
   if option2 == "Perkotaan":
      jenis = "Kota-"
   elif option2 == "Pedesaan":
      jenis = "Desa-"
   else :
      jenis = "Total-"

kolom = jenis + bulan

with col3:
   option3 = st.selectbox('Pilih Tipe',
                         ('Jumlah (Ribu)', 'Persentase', 'Garis Kemiskinan', 'Gini Ratio'))
   if option3 == 'Jumlah (Ribu)':
      df_show = data_ribu.copy()
   elif option3 == 'Persentase':
      df_show = data_persen.copy()
   elif option3 == 'Garis Kemiskinan':
      option3 = 'Garis'
      df_show = data_GK.copy()
   else:
      df_show = data_GR.copy()
   df_indo = df_show.copy()
   df_show = df_show[['Nama Provinsi', kolom, 'Latitude', 'Longitude']]
   df_show = df_show[df_show['Nama Provinsi'] != 'Indonesia']

if option3 == 'Jumlah (Ribu)':
   '''Jumlah Kemiskinan menampilkan jumlah dalam ribu rakyat Indonesia yang berada di bawah Garis Kemiskinan'''
elif option3 == 'Persentase':
   '''Persentase Kemiskinan menampilkan persentase dari jumlah rakyat Indonesia yang berada di bawah Garis Kemiskinan.'''
elif option3 == 'Garis':
   '''Garis Kemiskinan (GK) mencerminkan nilai rupiah pengeluaran minimum yang diperlukan seseorang untuk memenuhi kebutuhan pokok hidupnya selama sebulan, baik kebutuhan makanan maupun non-makanan.'''
else:
   '''Gini ratio atau koefisien Gini adalah ukuran statistik yang digunakan untuk mengukur tingkat ketimpangan atau distribusi pendapatan di dalam suatu populasi atau negara.'''

df_indo = df_indo.loc[df_indo['Nama Provinsi'] == 'Indonesia']
df_indo = df_indo[kolom].values[0]
if option3 == 'Jumlah (Ribu)':
   df_indo = str(df_indo) + ' Jiwa'
elif option3 == 'Persentase':
   df_indo = str(df_indo) + ' %'
elif option3 == 'Garis':
   df_indo = rupiah(int(df_indo))

st.metric(label=f'{option3} Kemiskinan Indonesia', value=df_indo, delta=None)

highest, lowest = st.columns(2)

with highest:
   high = df_show['Nama Provinsi'].loc[df_show[kolom] == df_show[kolom].max()].values[0]
   high_val = float(df_show[kolom].loc[df_show[kolom] == df_show[kolom].max()].values[0])
   if option3 == 'Jumlah (Ribu)':
      high_val = str(high_val) + ' Jiwa'
   elif option3 == 'Persentase':
      high_val = str(high_val) + ' %'
   elif option3 == 'Garis':
      high_val = rupiah(int(high_val))
   
   if option3 == 'Garis':
      st.metric(label=f'{option3} Kemiskinan Tertinggi', value=high, delta=high_val)
   else:
      st.metric(label=f'{option3} Kemiskinan Tertinggi', value=high, delta=high_val, delta_color= 'inverse')

with lowest:
   low = df_show['Nama Provinsi'].loc[df_show[kolom] == df_show[kolom].min()].values[0]
   low_val = float(df_show[kolom].loc[df_show[kolom] == df_show[kolom].min()].values[0])
   if option3 == 'Jumlah (Ribu)':
      low_val = str(low_val) + ' Jiwa'
   elif option3 == 'Persentase':
      low_val = str(low_val) + ' %'
   elif option3 == 'Garis':
      low_val = rupiah(int(low_val))

   if option3 == 'Garis':
      st.metric(label=f'{option3} Kemiskinan Terendah', value=low, delta=low_val, delta_color='inverse')
   else:
      st.metric(label=f'{option3} Kemiskinan Terendah', value=low, delta=low_val)


col4, col5 = st.columns([2,5])

with col4:
   df_rank = df_show.copy()
   df_rank = df_rank.dropna()
   df_rank = df_rank[['Nama Provinsi', kolom]]
   df_rank['Rank'] = df_rank[kolom].rank(method='min', ascending=False)
   df_rank = df_rank.set_index('Rank')
   df_rank = df_rank.sort_values('Rank')
   st.dataframe(df_rank)

with col5:
   df_show = df_show.dropna()
   fig = px.scatter_geo(df_show, 
                        lat='Latitude', 
                        lon='Longitude', 
                        hover_name='Nama Provinsi', 
                        size=kolom,
                        color=kolom)
   fig.update_layout(
    title=f'Peta {option3} Kemiskinan Indonesia',
    title_x = 0.5,
    geo=dict(
       projection_type='natural earth'  # Choose a projection type)
   ))
   fig.update_geos(fitbounds="locations")
   st.plotly_chart(fig, use_container_width=True)

st.caption('Sumber : Badan Pusat Statistik')

col6, col7, col8 = st.columns(3)

with col6:
   option6 = st.selectbox('Pilih Provinsi',
                         ('Nanggroe Aceh Darussalam', 'Sumatera Utara', 'Sumatera Barat', 'Riau',
                          'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung',
                          'Kepulauan Bangka Belitung', 'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat',
                          'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur', 'Banten',
                          'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
                          'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara',
                          'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara',
                          'Gorontalo', 'Sulawesi Barat', 'Maluku', 'Maluku Utara',
                          'Papua Barat', 'Papua'))

with col7:
   option7 = st.selectbox('Pilih Tipe',
                         ('Perkotaan ', 'Pedesaan ', 'Total '))
   if option7 == "Perkotaan ":
      jenis = "Kota-"
   elif option7 == "Pedesaan ":
      jenis = "Desa-"
   else :
      jenis = "Total-"

with col8:
   option8 = st.selectbox('Pilih Tipe',
                         ('Jumlah (Ribu) ','Jumlah (Ribu) Rata-Rata ', 'Persentase ', 'Garis Kemiskinan ', 'Gini Ratio '))
   if option8 == 'Jumlah (Ribu) ' or option8 == 'Jumlah (Ribu) Rata-Rata ':
      df_prov = data_ribu.copy()
   elif option8 == 'Persentase ':
      df_prov = data_persen.copy()
   elif option8 == 'Garis Kemiskinan ':
      df_prov = data_GK.copy()
      option8 = 'Garis '
   else:
      df_prov = data_GR.copy()

if option8 == 'Jumlah (Ribu) Rata-Rata ':
   df_indo = df_prov[df_prov['Nama Provinsi'] != 'Indonesia']
   numeric_cols = df_indo.select_dtypes(include='number')
   mean_row = numeric_cols.mean()
   df_indo.loc[len(df_indo)] = mean_row
   df_indo = df_indo.fillna('Indonesia')
   df_indo = df_indo.loc[df_indo['Nama Provinsi'] == 'Indonesia']

else:
   df_indo = df_prov.loc[df_prov['Nama Provinsi'] == 'Indonesia']

df_prov = df_prov.loc[df_prov['Nama Provinsi'] == option6]

kolom_prov = []
for i in df_prov.columns.tolist():
    if jenis in i :
        kolom_prov.append(i)
        kolom_prov.sort(reverse=True)

extracted_dates = [(item.split('-')[1], item.split('-')[2]) for item in kolom_prov]

# Sort the extracted dates based on the desired pattern
sorted_dates = sorted(extracted_dates, key=lambda x: (int(x[1]), int(x[0])))

# Reconstruct the sorted list with the desired pattern
kolom_prov = [f'{jenis}{month}-{year}' for month, year in sorted_dates]

kolom_prov.insert(0, 'Nama Provinsi')

df_prov = df_prov[kolom_prov].set_index('Nama Provinsi')
df_indo = df_indo[kolom_prov].set_index('Nama Provinsi')

a = df_prov.to_dict()
b = df_indo.to_dict()

x = list(a.keys())

y1 = [val[option6] for val in a.values()]
y2 = [val['Indonesia'] for val in b.values()]

y1_min = float(min(y1))
y1_max = float(max(y1))
y1_min_year = y1.index(y1_min)
y1_min_year = x[y1_min_year][-4::]
y1_max_year = y1.index(y1_max)
y1_max_year = x[y1_max_year][-4::]

highest2, lowest2 = st.columns(2)

with highest2:
   high = y1_max_year
   high_val = y1_max
   if option8 == 'Jumlah (Ribu) ' or option8 == 'Jumlah (Ribu) Rata-Rata ':
      high_val = str(high_val) + ' Jiwa'
   elif option8 == 'Persentase ':
      high_val = str(high_val) + ' %'
   elif option8 == 'Garis ':
      try :
         high_val = rupiah(int(high_val))
      except :
         high_val = np.nan
   
   if option8 == 'Garis ':
      st.metric(label=f'{option8} Kemiskinan Tertinggi Provinsi {option6}', value=high, delta=high_val)
   else:
      st.metric(label=f'{option8} Kemiskinan Tertinggi Provinsi {option6}', value=high, delta=high_val, delta_color= 'inverse')

with lowest2:
   low = y1_min_year
   low_val = y1_min
   if option8 == 'Jumlah (Ribu) ' or option8 == 'Jumlah (Ribu) Rata-Rata ':
      low_val = str(low_val) + ' Jiwa'
   elif option8 == 'Persentase ':
      low_val = str(low_val) + ' %'
   elif option8 == 'Garis ':
      try :
         low_val = rupiah(int(low_val))
      except :
         low_val = np.nan

   if option8 == 'Garis ':
      st.metric(label=f'{option8} Kemiskinan Terendah Provinsi {option6}', value=low, delta=low_val, delta_color='inverse')
   else:
      st.metric(label=f'{option8} Kemiskinan Terendah Provinsi {option6}', value=low, delta=low_val)



fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y1, name=option6))
fig.add_trace(go.Scatter(x=x, y=y2, name='Indonesia'))

fig.update_layout(
    title=f'{option8}Kemiskinan Provinsi {option6} vs Indonesia',
    xaxis_title='Bulan-Tahun',
    yaxis_title=f'{option8}Kemiskinan',
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

st.caption('Sumber : Badan Pusat Statistik')


st.markdown('#### Kondisi Ekonomi Indonesia')

'''
Salah satu cara untuk mengetahui kondisi ekonomi Indonesia yaitu melihat GDP (Gross Domestic Product). GDP mengukur nilai total barang dan jasa yang dihasilkan dalam wilayah negara selama periode tertentu, seperti satu tahun. Dengan memonitor perubahan GDP dari waktu ke waktu, kita dapat menilai pertumbuhan ekonomi Indonesia. Selain itu, analisis komposisi GDP juga memberikan wawasan tentang sektor-sektor ekonomi yang berkontribusi terhadap pertumbuhan. Walaupun perlu diingat bahwa GDP hanya memberikan gambaran umum dan tidak mencakup semua aspek kehidupan ekonomi dan kualitas hidup masyarakat.
'''

col9, col10, col11 = st.columns(3)

with col9:
   option9 = st.slider('Pilih Tahun', min_value=2015, max_value=2022, step=1)

with col10:
   value = data_gdp['Estimasi Pendapatan (Harga Konstan)'].loc[data_gdp['Tahun']==option9].values[0]
   value = rupiah(int(value))
   value2 = str(round(data_gdp['%HK'].loc[data_gdp['Tahun']==option9].values[0], 2)) + ' %'
   st.metric(label=f'Estimasi Pendapatan (Harga Konstan) Tahun {option9}', value=value, delta=value2 + f' dari Tahun {option9-1}')

with col11:
   value = data_gdp['Estimasi Pendapatan (Harga Berlaku)'].loc[data_gdp['Tahun']==option9].values[0]
   value = rupiah(int(value))
   value2 = str(round(data_gdp['%HB'].loc[data_gdp['Tahun']==option9].values[0], 2)) + ' %'
   st.metric(label=f'Estimasi Pendapatan (Harga Berlaku) Tahun {option9}', value=value, delta=value2 + f' dari Tahun {option9-1}')


fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=data_gdp['Tahun'], y=data_gdp['Harga Konstan 2010 (Miliar)'], name='Harga Konstan 2010 (Miliar)'))
fig2.add_trace(go.Scatter(x=data_gdp['Tahun'], y=data_gdp['Harga Berlaku (Miliar)'], name='Harga Berlaku (Miliar)'))

fig2.update_layout(
    title=f'Harga Konstan 2010 VS Harga Berlaku GDP Indonesia',
    xaxis_title='Tahun',
    yaxis_title=f'GDP Indonesia',
    title_x=0.5
)

st.plotly_chart(fig2, use_container_width=True)

st.caption('Sumber : Badan Pusat Statistik')

'''
Dengan menggunakan harga konstan maupun harga berlaku, GDP Indonesia terdapat kenaikan selama 8 tahun terakhir kecuali pada tahun 2020 saat terjadi COVID-19. Dari data GDP Indonesia, kita juga dapat untuk melakukan estimasi rata-rata pendapatan masyarakat Indonesia yaitu dengan membagi GDP dengan total populasi. Dari data yang didapat, estimasi pendapatan pada 2022 memiliki nilai Rp. 5.919.236,00 yang mana 11 kali lebih tinggi dibandingkan garis kemiskinan September 2022 yaitu Rp. 535.547,00. Hal ini menandakan secara nasional, ekonomi Indonesia masih jauh dari garis kemiskinan.
'''

st.markdown('#### Kondisi Tenaga Kerja Indonesia')

col9, col10, col11 = st.columns(3)

with col9:
   option9 = st.slider('Pilih Tahun', min_value=2017, max_value=2022, step=1)

with col10:
   pass

with col11:
   value = str(round(data_gdp['%URR-HB'].loc[data_gdp['Tahun']==option9].values[0], 2))
   st.metric(label=f'Persentase Upah Rata-Rata dengan Estimasi Pendapatan Tahun {option9}', value= value + ' %')

fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[2:], y=data_gdp['Estimasi Pendapatan (Harga Berlaku)'].iloc[2:], name='Estimasi Pendapatan (Harga Berlaku)'))
fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[2:], y=data_gdp['Upah Rata-Rata'].iloc[2:], name='Upah Rata-Rata'))

fig2.update_layout(
    title=f'Estimasi Pendapatan (Harga Berlaku) vs Upah Rata-Rata',
    xaxis_title='Tahun',
    yaxis_title=f'Rupiah',
    title_x=0.5
)

st.plotly_chart(fig2, use_container_width=True)

st.caption('Sumber : Badan Pusat Statistik')

'''
Estimasi pendapatan rata-rata per-bulan yang didapat menggunakan GDP masih jauh lebih besar daripada upah rata-rata tenaga kerja di Indonesia. Untuk tahun yang memiliki GDP tertinggi yaitu tahun 2022 dengan nilai upah rata-rata hanya sebesar 51.88% dari estimasi pendapatan Indonesia. Hal ini menyatakan bahwa ketimpangan di Indonesia cukup besar, mengingat untuk mendapatkan nilai estimasi tersebut merupakan pembagian GDP dengan total populasi sedangkan upah rata-rata hanya pada angkatan kerja di Indonesia yang pada Februari 2023 sebanyak 146.62 juta orang atau sekitar ± 54% dari total penduduk.
'''

options = st.multiselect(
    'Pilih Data',
    ['Tingkat Pengangguran Terbuka (Ribu)',
     'Kemiskinan Indonesia (Ribu)',
     'Tingkat Pengangguran Terbuka (Persen)',
     'Kemiskinan Indonesia (Persen)'],
    ['Tingkat Pengangguran Terbuka (Ribu)',
     'Kemiskinan Indonesia (Ribu)'])

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

if 'Tingkat Pengangguran Terbuka (Persen)' in options :
   fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[2:], y=data_gdp['Tingkat Pengangguran Terbuka (Persen)'].iloc[2:], name='Tingkat Pengangguran Terbuka (Persen)'), secondary_y=True)
if 'Kemiskinan Indonesia (Persen)' in options:
   fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[2:], y=data_gdp['%Miskin'].iloc[2:], name='Kemiskinan Indonesia (Persen)'), secondary_y=True)
if 'Tingkat Pengangguran Terbuka (Ribu)' in options:
   fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[2:], y=data_gdp['Jumlah (Ribu) TPT'].iloc[2:], name='Tingkat Pengangguran Terbuka (Ribu)'), secondary_y=False)
if 'Kemiskinan Indonesia (Ribu)' in options:
   fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[2:], y=data_gdp['Jumlah Miskin (Ribu)'].iloc[2:], name='Kemiskinan Indonesia (Ribu)'), secondary_y=False)

fig2.update_layout(
    title=f'Tingkat Pengangguran Terbuka vs Kemiskinan Indonesia',
    xaxis_title='Tahun',
    title_x=0.5
)

st.plotly_chart(fig2, use_container_width=True)

st.caption('Sumber : Badan Pusat Statistik')

'''
Pola antara jumlah tingkat pengangguran terbuka dengan jumlah kemiskinan cenderung sama, dimana apabila tingkat pengangguran terbuka naik grafik kemiskinan juga naik. Tetapi pada tahun 2022 dimana jumlah kemiskinan naik ± 100 ribu tetapi tingkat pengangguran terbuka turun secara signifikan dengan nilai ± 600 ribu. Hal ini dapat menggambarkan bahwa populasi masyarakat yang tidak termasuk dalam angkatan kerja tahun 2022 sedang mengalami masalah finansial.
'''

st.markdown('### BAB II. Solusi')

st.markdown('#### Peran Diri Sendiri')

'''
Dengan berkembangnya teknologi dan pengetahuan, membawa perubahan dalam dunia kerja. Banyak sektor pekerjaan yang hilang dan digantikan oleh sesuatu yang dianggap lebih efektif dan efisien seperti robot dan AI. Namun, hal tersebut justru membuka peluang baru dan menciptakan kebutuhan baru di pasar kerja. Meskipun beberapa pekerjaan tradisional mungkin mengalami pengurangan atau bahkan hilang, munculnya sektor-sektor baru seperti teknologi informasi, industri kreatif, energi terbarukan, dan layanan digital memberikan peluang baru untuk menciptakan pekerjaan yang sebelumnya belum ada.
'''

col1, col2, col3 = st.columns(3)
with col2:
   img1 = Image.open('DATA/LossNew Job.png')
   st.image(img1, caption='Sumber : World Economic Forum')

'''
Salah satu peran diri sendiri untuk terhindar dari kemiskinan yaitu meningkatkan kualitas pendidikan dan keterampilan. Hal ini dapat dilakukan dengan mengambil inisiatif untuk mengakses pendidikan formal maupun informal, seperti kursus online atau pelatihan profesional. Pencarian beasiswa juga akan membantu terutama bagi yang memiliki masalah finansial. Tentunya pilihan jenis pembelajaran yang tepat akan membantu meningkatkan kesempatan untuk memiliki pekerjaan. Di masa yang sudah banyak pekerjaan digantikan oleh AI ini penting untuk memilih jenis pembelajaran yang sesuai guna meningkatkan peluang mendapatkan pekerjaan. Salah satu pendekatan yang efektif adalah fokus pada keterampilan yang sulit digantikan oleh kecerdasan buatan, seperti kreativitas, pemecahan masalah kompleks, dan keahlian interpersonal. Hal ini dapat dilihat dari gambar yang disampaikan oleh World Economic Forum berikut tentang pekerjaan yang mengalami perkembangan dan penurunan.
'''

col1, col2, col3 = st.columns(3)

with col2:
   img1 = Image.open('DATA/Growing Job.jpg')
   st.image(img1, caption='Sumber : World Economic Forum')




st.markdown('#### Peran Masyarakat')

'''
Peran masyarakat sangat penting dalam mengatasi kemiskinan dan ketimpangan. Masyarakat memiliki potensi untuk berkontribusi dalam upaya pengentasan masalah ini melalui berbagai cara. Pertama, masyarakat dapat berperan aktif dalam program-program pemberdayaan ekonomi seperti koperasi, usaha mikro, kecil, dan menengah (UMKM), serta kemitraan usaha dengan menghasilkan produk atau layanan yang dapat meningkatkan pendapatan dan menciptakan lapangan kerja. Kedua, masyarakat dapat menjadi agen perubahan dalam memperjuangkan keadilan sosial dan mengadvokasi kebijakan publik yang progresif untuk mengurangi ketimpangan. Ini melibatkan partisipasi dalam kelompok advokasi, gerakan sosial, atau organisasi masyarakat sipil yang berfokus pada masalah kemiskinan dan ketimpangan. Ketiga, masyarakat dapat memberikan dukungan dan membantu mereka yang berada dalam kondisi terpinggirkan, seperti memberikan bantuan sosial, akses ke pendidikan, kesehatan, dan pemberdayaan perempuan. Selain itu, masyarakat juga dapat membentuk jaringan solidaritas dan kolaborasi dengan lembaga pemerintah, organisasi non-pemerintah, dan sektor swasta untuk menciptakan sinergi dalam mengatasi masalah kemiskinan dan ketimpangan. Dengan adanya partisipasi aktif dan tanggung jawab masyarakat, kita dapat menciptakan lingkungan yang inklusif dan berkeadilan, di mana setiap individu memiliki kesempatan yang sama untuk berkembang dan mencapai kesejahteraan.
'''
col1, col2, col3 = st.columns(3)

with col2:
   img1 = Image.open('DATA/UMKM.jpg')
   st.image(img1, caption='UMKM sebagai Sarana Peningkatan Ekonomi dan Membuka Lapangan Pekerjaan')



st.markdown('#### Peran Pemerintah')

'''
Pemerintah memegang peranan penting dalam mengatasi kemiskinan, ketimpangan dan pengangguran di Indonesia. Diantara beberapa cara, yaitu :
1. Meningkatkan mobilitas modal dan tenaga kerja
2. Menyelenggarakan pelatihan kerja sesuai kebutuhan pasar
3. Mendirikan industri padat karya untuk menciptakan lapangan kerja
4. Menyukseskan proyek-proyek infrastruktur yang melibatkan banyak tenaga kerja
5. Meningkatkan daya beli masyarakat
6. Menegakkan hukum dan Memerangi Korupsi

Dalam mengatasi kemiskinan, strategi yang dilakukan oleh pemerintah tidak dapat hanya melihat satu dimensi saja, tetapi memerlukan pendekatan yang menyeluruh. Pemerintah perlu melakukan diagnosa yang lengkap terhadap semua aspek yang menyebabkan kemiskinan secara lokal. Penyediaan lapangan kerja menjadi kunci dalam mengatasi kemiskinan yang disebabkan oleh pengangguran. Pemerintah dapat meningkatkan mobilitas tenaga kerja dengan memindahkan pekerja ke wilayah yang memiliki peluang kerja, serta melatih ulang keterampilan mereka agar sesuai dengan permintaan di tempat baru. Peningkatan mobilitas modal juga penting, dengan memindahkan industri yang padat karya ke wilayah yang mengalami pengangguran tinggi. Peran pemerintah dalam hal ini adalah memberikan kebijakan dan fasilitas yang mendukung upaya mengurangi kemiskinan dan pengangguran, seperti program pelatihan kerja, pendidikan, dan infrastruktur yang diperlukan untuk meningkatkan produktivitas tenaga kerja. Serta tak lupa untuk tetap menegakkan hukum terhadap berbagai pelanggaran-pelanggaran termasuk memerangi korupsi.
'''
fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[1:], y=data_gdp['Kerugian Negara (Miliar)'].iloc[1:], name='Kerugian Negara (Miliar)'))
fig2.add_trace(go.Scatter(x=data_gdp['Tahun'].iloc[1:], y=data_gdp['Potensi Kerugian Negara (Miliar)'].iloc[1:], name='Potensi Kerugian Negara (Miliar)'))

fig2.update_layout(
    title=f'Kerugian Negara Akibat Korupsi',
    xaxis_title='Tahun',
    yaxis_title=f'Rupiah (Miliar)',
    title_x=0.5
)

st.plotly_chart(fig2, use_container_width=True)
st.caption('Sumber : Indonesia Corruption Watch')

'''
Pemerintah memiliki tanggung jawab untuk menciptakan lingkungan yang adil dan transparan, di mana hukum ditegakkan secara tegas dan korupsi tidak dibiarkan berkembang. Dengan menegakkan hukum dan memberantas korupsi, pemerintah dapat menciptakan iklim investasi yang stabil, meningkatkan kepercayaan masyarakat terhadap pemerintah, dan memastikan alokasi sumber daya yang adil bagi seluruh lapisan masyarakat. Melalui penindakan terhadap tindak korupsi, pemerintah dapat mengurangi penyelewengan anggaran publik dan memastikan bahwa dana-dana yang seharusnya digunakan untuk pembangunan dan pelayanan publik benar-benar sampai kepada mereka yang membutuhkannya, sehingga mengurangi kemiskinan dan ketimpangan sosial.

Dengan peran aktif pemerintah, diharapkan dapat tercipta kebijakan yang efektif dan berkelanjutan untuk mengatasi masalah kemiskinan, ketimpangan, dan pengangguran. Melalui upaya pemerintah dan partisipasi masyarakat, diharapkan dapat terjadi perubahan yang positif dalam mengurangi kesenjangan sosial, meningkatkan kualitas hidup masyarakat, dan menciptakan kesempatan kerja yang lebih baik bagi semua.
'''

# Hyperlink ke Streamlit yang lain
url = "https://muaazmumtaz-tetris2-capstone-iqm6k2.streamlit.app/"
st.write("[Lihat juga tentang korupsi di Indonesia..](%s)" % url)

# Referensi
st.markdown('##### Referensi')

'''
[1] Badan Pusat Statistik. https://www.bps.go.id/.\n
[2] World Bank. https://databank.worldbank.org/\n
[3] Kurniawan, D. (2009). "Kemiskinan di Indonesia dan Solusinya". Gema Eksos, Vol 5, No. 1.\n
[4] World Economic Forum. https://www.weforum.org/\n
[5] Sanjaya P.N. (2022). "Analisis Peran Pemerintah dalam Mengatasi Kemiskinan, Ketimpangan dan Pengangguran di Indonesia". Islamic Economics Journal, Vol 3, No. 1.\n
[6] Indonesia Corruption Watch. https://www.antikorupsi.org/\n
'''
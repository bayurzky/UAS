import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
import streamlit as stl

# Opening Data Set produksi_minyak_mentah.csv
df = pd.read_csv("produksi_minyak_mentah.csv")
# Opening Data kode_negara_lengkap.json
f = open("kode_negara_lengkap.json")
info_negara = json.load(f)
f.close()

# TITLE
stl.set_page_config(layout="wide")
stl.title("Pengolahan Data Produksi Minyak Mentah")
stl.markdown("*Dibuat oleh : Muhamad Bayu Rizky Kautsar*")

# SIDEBAR
stl.sidebar.title("Setting")

# USER INPUT and CONTROL PANEL
stl.sidebar.subheader("Pengaturan Konfigurasi Pengolahan Data")
# Get kode_negara_unik
kode_negara_unik = df["kode_negara"].unique().tolist()
# Get dict_info {kode_negara: info_negara}
# info_negara["alpha-3"] = info_negara
dict_info = {}
for info in info_negara:
    dict_info[info["alpha-3"]] = info
# Preprocessing kode_negara
# Meng-exclude kode negara pada file produksi_minyak_mentah.csv yang tidak ada pada file kode_negara_lengkap.json
temp_kode_negara_unik = []
for kode in kode_negara_unik:
    if kode not in dict_info:
        df = df.loc[df["kode_negara"] != kode]
    else:
        temp_kode_negara_unik.append(kode)
kode_negara_unik = temp_kode_negara_unik
# Get list_nama_negara
list_nama_negara = []
dict_nama_negara = {}
for kode in kode_negara_unik:
    list_nama_negara.append(dict_info[kode]["name"])
    dict_nama_negara[dict_info[kode]["name"]] = kode
# Get list_tahun
list_tahun = df["tahun"].unique().tolist()

N = stl.sidebar.selectbox("Pilih Negara", list_nama_negara)
T = stl.sidebar.selectbox("Pilih Tahun", list_tahun)
B = stl.sidebar.number_input("Jumlah Negara yang Ingin Ditampilkan", min_value=1, max_value=len(list_nama_negara), value=10)

# IMPLEMENTASI FITUR A
stl.subheader(f"Grafik Jumlah Produksi Minyak Mentah Negara {N}")
dfN = df.loc[df["kode_negara"] == dict_nama_negara[N]]
dfN = dfN.sort_values(["tahun"], ascending = [True])
# MENAMPILKAN BAR CHART KE LAYAR
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(dfN["tahun"].tolist())]
fig, ax = plt.subplots()
ax.barh(dfN["tahun"].tolist(), dfN["produksi"].tolist(), color=colors)
ax.set_ylabel("Tahun", fontsize=12)
ax.set_xlabel("Total Produksi", fontsize=12)
plt.tight_layout()

stl.pyplot(fig)

left_col, right_col = stl.columns(2)
# IMPLEMENTASI FITUR B
left_col.subheader(f"{B} Besar Negara dengan Jumlah Produksi Minyak Mentah Terbesar Pada Tahun {T}")
dfB = df[df["tahun"] == T]
dfB = dfB.sort_values(["produksi"], ascending=[False])
dfB['Nama Negara'] = dfB.apply(lambda row: dict_info[row.kode_negara]["name"], axis=1)
dfB.index = np.arange(1, len(dfB)+1)
left_col.dataframe(dfB[["Nama Negara", "tahun", "produksi"]][:B])

# IMPLEMENTASI FITUR C
right_col.subheader(f"{B} Besar Negara dengan Jumlah Kumulatif Produksi Minyak Mentah Terbesar Keseluruhan Tahun")
dfC = df.groupby('kode_negara')
dfC = dfC[["kode_negara", "produksi"]].sum()
dfC = dfC.reset_index()
dfC = dfC.sort_values(["produksi"], ascending=[False])
dfC['Nama Negara'] = dfC.apply(lambda row: dict_info[row.kode_negara]["name"], axis=1)
dfC.index = np.arange(1, len(dfC)+1)
right_col.dataframe(dfC[["Nama Negara", "produksi"]][:B])

# IMPLEMENTASI FITUR D
# Summary
stl.subheader("SUMMARY")
# nama lengkap negara, kode negara, region, dan sub-region
# 1. Terbesar pada tahun T dan keseluruhan tahun
# 2. Terkecil tapi > 0 pada tahun T dan keseluruhan Tahun
# 3. 0 pada tahun T dan keseluruhan tahun

# Kode negara dengan produksi terbesar pada tahun T (d11)
d11 = dfB["kode_negara"][1]
# Kode negara dengan produksi terbesar pada keseluruhan tahun (d12)
d12 = dfC["kode_negara"][1]
# Kode negara dengan produksi terkecil tapi tidak sama dengan 0 pada tahun T (d21)
df21 = dfB[dfB["produksi"] > 0]
df21 = df21.sort_values(["produksi"], ascending=[True])
df21.index = np.arange(1, len(df21)+1)
d21 = df21["kode_negara"][1]
# Kode negara dengan produksi terkecil tapi tidak sama dengan 0 pada keseluruhan tahun (d22)
df22 = dfC[dfC["produksi"] > 0]
df22 = df22.sort_values(["produksi"], ascending=[True])
df22.index = np.arange(1, len(df22)+1)
d22 = df22["kode_negara"][1]
# Kode negara dengan produksi sama dengan 0 pada tahun T (d31)
df31 = dfB[dfB["produksi"] == 0]
df31.index = np.arange(1, len(df31)+1)
d31 = df31["kode_negara"][1]
# Kode negara dengan produksi sama dengan 0 pada keseluruhan tahun (d32)
df32 = dfC[dfC["produksi"] == 0]
df32.index = np.arange(1, len(df32)+1)
d32 = df32["kode_negara"][1]

stl.markdown(f'**Negara dengan jumlah produksi terbesar pada tahun {T}: ** \n Nama Negara: {dict_info[d11]["name"]}, Kode Negara: {d11}, Region: {dict_info[d11]["region"]}, Sub-region: {dict_info[d11]["sub-region"]}, Dengan Jumlah Produksi ({dfB["produksi"][1]:.2f})')
stl.markdown(f'**Negara dengan jumlah produksi kumulatif terbesar: ** \n Nama Negara: {dict_info[d12]["name"]}, Kode Negara: {d12}, Region: {dict_info[d12]["region"]}, Sub-region: {dict_info[d12]["sub-region"]}, Dengan Jumlah Produksi ({dfC["produksi"][1]:.2f})')
stl.markdown(f'**Negara dengan jumlah produksi terkecil (>0) pada tahun {T}: ** \n Nama Negara: {dict_info[d21]["name"]}, Kode Negara: {d21}, Region: {dict_info[d21]["region"]}, Sub-region: {dict_info[d21]["sub-region"]}, Dengan Jumlah Produksi ({df21["produksi"][1]:.2f})')
stl.markdown(f'**Negara dengan jumlah produksi kumulatif terkecil (>0): ** \n Nama Negara: {dict_info[d22]["name"]}, Kode Negara: {d22}, Region: {dict_info[d22]["region"]}, Sub-region: {dict_info[d22]["sub-region"]}, Dengan Jumlah Produksi ({df22["produksi"][1]:.2f})')
stl.markdown(f'**Negara dengan jumlah produksi sama dengan nol pada tahun {T}: ** \n Nama Negara: {dict_info[d31]["name"]}, Kode Negara: {d31}, Region: {dict_info[d31]["region"]}, Sub-region: {dict_info[d31]["sub-region"]}, Dengan Jumlah Produksi ({df31["produksi"][1]:.2f})')
stl.markdown(f'**Negara dengan jumlah produksi kumulatif sama dengan nol: ** \n Nama Negara: {dict_info[d32]["name"]}, Kode Negara: {d32}, Region: {dict_info[d32]["region"]}, Sub-region: {dict_info[d32]["sub-region"]}, Dengan Jumlah Produksi ({df32["produksi"][1]:.2f})')

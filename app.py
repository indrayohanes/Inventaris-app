import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("📦 Aplikasi Manajemen Inventaris")

# 1. Baca Data dari CSV
def load_data():
    return pd.read_csv("TableInventaris.csv")

data = load_data()

# 2. Tampilkan Data
st.subheader("Daftar Inventaris")
st.dataframe(data)

# 3. Form Tambah Barang
st.subheader("Tambah Barang Baru")
with st.form("form_tambah"):
    col1, col2 = st.columns(2)
    with col1:
        id_item = st.text_input("ID Item (Contoh: INV003)")
        nama = st.text_input("Nama Barang")
    with col2:
        kategori = st.selectbox("Kategori", ["Elektronik", "Alat Tulis", "Perlengkapan Kantor"])
        stok = st.number_input("Stok", min_value=0)
    
    lokasi = st.text_input("Lokasi Penyimpanan")
    
    if st.form_submit_button("Simpan"):
        new_data = {
            "ID_Item": id_item,
            "Nama_Barang": nama,
            "Kategori": kategori,
            "Stok": stok,
            "Lokasi": lokasi
        }
        data = data.append(new_data, ignore_index=True)
        data.to_csv("TableInventaris.csv", index=False)
        st.success("Data berhasil disimpan!")
        st.experimental_rerun()  # Refresh tampilan

# 3.5. Form Edit Data
st.subheader("Edit Barang")
edit_id = st.selectbox("Pilih ID Item untuk edit", data["ID_ITEM"])
selected_item = data[data["ID_ITEM"] == edit_id].iloc[0]

with st.form("form_edit"):
    new_nama = st.text_input("Nama Barang", value=selected_item["NAMA_BARANG"])
    new_stok = st.number_input("Stok", value=selected_item["STOK"])
    
    if st.form_submit_button("Update"):
        data.loc[data["ID_Item"] == edit_id, "Nama_Barang"] = new_nama
        data.loc[data["ID_Item"] == edit_id, "Stok"] = new_stok
        data.to_csv("TableInventaris.csv", index=False)
        st.success("Data diperbarui!")
        st.experimental_rerun()

# 4. Fitur Hapus Barang
st.subheader("Hapus Barang")
selected_id = st.selectbox("Pilih ID Item untuk dihapus", data["ID_ITEM"])
if st.button("Hapus"):
    data = data[data["ID_Item"] != selected_id]
    data.to_csv("TableInventaris.csv", index=False)
    st.success(f"Item {selected_id} dihapus!")
    st.experimental_rerun()
    
# Filter by Kategori
kategori_options = ["Semua"] + list(data["KATEGORI"].unique())
kategori_filter = st.selectbox("Filter by Kategori", kategori_options)

if kategori_filter == "Semua":
    filtered_data = data  # Tampilkan semua data
else:
    filtered_data = data[data["KATEGORI"] == kategori_filter]  # Filter berdasarkan kategori

st.dataframe(filtered_data)  # Tampilkan data yang sudah difilter
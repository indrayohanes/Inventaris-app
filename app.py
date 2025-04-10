import streamlit as st
import pandas as pd
import datetime

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
with st.form("form_tambah"):
    id_item = st.text_input("ID Item (Contoh: INV003)")
    nama = st.text_input("Nama Barang")
    kategori = st.selectbox("Kategori", ["Elektronik", "Alat Tulis", "Perlengkapan Kantor", "Aksesoris Komputer"])
    stok = st.number_input("Stok", min_value=0)
    lokasi = st.text_input("Lokasi Penyimpanan")
    tanggal = st.date_input("Tanggal Masuk", value=datetime.date.today())

    if st.form_submit_button("Simpan"):
        new_data = {
            "ID_ITEM": id_item,
            "NAMA_BARANG": nama,
            "KATEGORI": kategori,
            "STOK": stok,
            "LOKASI": lokasi,
            "TANGGAL": tanggal.strftime("%m/%d/%Y")
        }

        data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
        data.to_csv("TableInventaris.csv", index=False)
        st.success("✅ Data berhasil disimpan!")
        st.rerun()

        
# 3.5. Form Edit Data
st.subheader("Edit Barang")

if "form_updated" not in st.session_state:
    st.session_state["form_updated"] = False

if st.session_state["form_updated"]:
    st.session_state["form_updated"] = False
    st.experimental_set_query_params(updated="true")  # optional, bisa pakai ini biar rerun
    st.rerun()  # ini sekarang yang digunakan di v1.44.1

edit_id = st.selectbox("Pilih ID Item untuk edit", data["ID_ITEM"])
selected_item = data[data["ID_ITEM"] == edit_id].iloc[0]

with st.form("form_edit"):
    new_nama = st.text_input("Nama Barang", value=selected_item["NAMA_BARANG"])
    new_stok = st.number_input("Stok", min_value=0, value=int(selected_item["STOK"]), step=1, format="%d")

    
    if st.form_submit_button("Update"):
        data.loc[data["ID_ITEM"] == edit_id, "NAMA_BARANG"] = new_nama
        data.loc[data["ID_ITEM"] == edit_id, "STOK"] = new_stok
        data.to_csv("TableInventaris.csv", index=False)
        st.success("Data diperbarui!")
        st.session_state["form_updated"] = True
        st.rerun()

# 4. Fitur Hapus Barang
st.subheader("Hapus Barang")
selected_id = st.selectbox("Pilih ID Item untuk dihapus", data["ID_ITEM"])
if st.button("Hapus"):
    data = data[data["ID_ITEM"] != selected_id]
    data.to_csv("TableInventaris.csv", index=False)
    st.success(f"Item {selected_id} dihapus!")
    st.rerun()
    
# Filter by Kategori
kategori_options = ["Semua"] + list(data["KATEGORI"].unique())
kategori_filter = st.selectbox("Filter by Kategori", kategori_options)

if kategori_filter == "Semua":
    filtered_data = data  # Tampilkan semua data
else:
    filtered_data = data[data["KATEGORI"] == kategori_filter]  # Filter berdasarkan kategori

st.dataframe(filtered_data)  # Tampilkan data yang sudah difilter

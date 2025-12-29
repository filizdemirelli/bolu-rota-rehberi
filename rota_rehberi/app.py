import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Ayarlar ve Harita Sağlayıcısı
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto" # OSM benzeri haritalar için şart

# 2. Veriler (Koordinatlar Netleştirildi)
duraklar = [
    {"isim": "Şehir Oteli", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "0 dk"},
    {"isim": "Gölcük Tabiat Parkı", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 dk"},
    {"isim": "Sarıalan Yaylası", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 dk"},
    {"isim": "Aladağ Yaylaları", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 dk"}
]

# Doğru Navigasyon Linki (Koordinat bazlı - Yanlış yere gitmez)
# Bolu Merkez -> Gölcük -> Sarıalan -> Aladağlar
nav_link = "https://www.google.com/maps/dir/40.7325,31.6082/40.6552,31.6255/40.6120,31.6500/40.5850,31.6350"

if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.title("🌲 Bolu Ekolojik Rota Rehberi")
    if st.button("Keşfetmeye Başla"):
        st.session_state.giris = True
        st.rerun()
else:
    # --- HARİTA BÖLÜMÜ ---
    st.sidebar.title("Rota Kontrolü")
    st.sidebar.markdown(f"[🗺️ GERÇEK NAVİGASYONU AÇ]({nav_link})")
    
    # Estetik Rota Çizgisi
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in duraklar]
    
    path_layer = pdk.Layer(
        "PathLayer",
        pd.DataFrame([{"path": yol_noktalari}]),
        get_path="path",
        get_color=[255, 0, 0, 200], # Kırmızı
        width_scale=20,
        width_min_pixels=4,
        rounded=True
    )

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        pd.DataFrame(duraklar),
        get_position="[boylam, enlem]",
        get_color=[0, 128, 0], # Yeşil noktalar
        get_radius=200,
    )

    st.pydeck_chart(pdk.Deck(
        map_style="light", # Carto sayesinde artık gözükecek
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.62, zoom=10),
        layers=[path_layer, point_layer]
    ))

    # --- DURAKLAR ---
    for d in duraklar:
        with st.expander(f"📍 {d['isim']}"):
            if os.path.exists(d['foto']):
                st.image(d['foto'])
            else:
                st.info(f"{d['foto']} klasörde bulunamadı.")

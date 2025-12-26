import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(page_title="Rota Rehberi", layout="wide")

# Harita altlığı ayarı (Yolları net görmek için)
pdk.settings.map_provider = "carto"

st.title("📍 Tematik Koridorlar Rota Rehberi")
st.markdown("---")

rotalar = {
    "Ekolojik Koridor": {
        "aciklama": "Bolu Merkez'den başlayıp Karacasu üzerinden Gölcük ve yaylalara ulaşan karayolu güzergahı.",
        "duraklar": [
            {"isim": "Şehir Oteli", "enlem": 40.732, "boylam": 31.608, "foto": "otel.jpg", "sure": "0 dk", "ulasim": "Başlangıç 🏨", "aktivite": "Konaklama ve Bilgilendirme."},
            {"isim": "Bolu Gölcük Tabiat Parkı", "enlem": 40.655, "boylam": 31.625, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "ulasim": "Eko-Otobüs 🚌", "aktivite": "Doğa yürüyüşü."},
            {"isim": "Sarıalan Yaylası", "enlem": 40.612, "boylam": 31.650, "foto": "sarialan.jpg", "sure": "15 dk", "ulasim": "Minibüs 🚐", "aktivite": "Yayla kültürü."},
            {"isim": "Aladağ Yaylaları", "enlem": 40.585, "boylam": 31.635, "foto": "aladag.jpg", "sure": "10 dk", "ulasim": "Bisiklet 🚲", "aktivite": "Kamp alanı."}
        ]
    }
}

rota_secimi = st.sidebar.selectbox("Bir rota seçiniz:", list(rotalar.keys()))

# --- GERÇEK YOL KIYRIMLARI (Bolu-Karacasu-Gölcük Hattı) ---
# Bu koordinatlar karayolundaki ana dönüşleri takip eder
yol_verisi = [
    [31.608, 40.732], # Merkez (Otel)
    [31.612, 40.725], # Şehir çıkışı
    [31.610, 40.710], # Karacasu yolu girişi
    [31.620, 40.690], # Karacasu mevkii
    [31.628, 40.675], # Gölcük yolu tırmanışı
    [31.625, 40.655], # GÖLCÜK GÖLÜ
    [31.640, 40.640], # Yayla yolu ayrımı
    [31.650, 40.612], # SARIALAN
    [31.642, 40.600], # Aladağ geçişi
    [31.635, 40.585]  # ALADAĞLAR
]

layer_path = pdk.Layer(
    "PathLayer",
    pd.DataFrame([{"path": yol_verisi}]),
    get_path="path",
    get_color=[255, 75, 75, 200],
    width_scale=3, 
    width_min_pixels=3,
    get_dash_array=[7, 4], # Kesikli çizgi yapısı
)

layer_points = pdk.Layer(
    "ScatterplotLayer",
    pd.DataFrame(rotalar[rota_secimi]["duraklar"]),
    get_position="[boylam, enlem]",
    get_color=[0, 100, 255],
    get_radius=100,
)

st.pydeck_chart(pdk.Deck(
    map_style="light",
    initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.63, zoom=11, pitch=0),
    layers=[layer_path, layer_points]
))

# --- DURAK DETAYLARI ---
st.markdown("### Durak Noktaları")
for durak in rotalar[rota_secimi]["duraklar"]:
    with st.expander(f"📍 {durak['isim']}", expanded=False):
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if os.path.exists(durak["foto"]):
                st.image(durak["foto"], use_container_width=True)
            else:
                st.warning(f"🖼️ {durak['foto']} bulunamadı.")
        with col2:
            st.write(f"**Ulaşım:** {durak['ulasim']} | **Süre:** {durak['sure']}")
            st.write(f"**Aktivite:** {durak['aktivite']}")
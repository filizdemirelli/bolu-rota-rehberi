import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# Veri Seti
rotalar = {
    "Ekolojik Koridor": {
        "aciklama": "Bolu Merkez'den Gölcük ve yaylalara uzanan doğa dostu güzergah.",
        "duraklar": [
            {"isim": "Şehir Oteli", "enlem": 40.732, "boylam": 31.608, "foto": "otel.jpg", "sure": "0 dk", "ulasim": "Başlangıç 🏨", "aktivite": "Konaklama ve Bilgilendirme."},
            {"isim": "Bolu Gölcük Tabiat Parkı", "enlem": 40.655, "boylam": 31.625, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "ulasim": "Eko-Otobüs 🚌", "aktivite": "Doğa yürüyüşü."},
            {"isim": "Sarıalan Yaylası", "enlem": 40.612, "boylam": 31.650, "foto": "sarialan.jpg", "sure": "15 dk", "ulasim": "Minibüs 🚐", "aktivite": "Yayla kültürü."},
            {"isim": "Aladağ Yaylaları", "enlem": 40.585, "boylam": 31.635, "foto": "aladag.jpg", "sure": "10 dk", "ulasim": "Bisiklet 🚲", "aktivite": "Kamp alanı."}
        ]
    }
}

if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1000", use_container_width=True)
        st.markdown("<h1 style='text-align: center; color: #2E7D32;'>Bolu Rota Rehberine Hoş Geldiniz</h1>", unsafe_allow_html=True)
        if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
            st.session_state.giris_yapildi = True
            st.rerun()
else:
    st.title("📍 Tematik Koridorlar ve Yeni Odaklar")
    rota_secimi = st.sidebar.selectbox("Bir rota seçiniz:", list(rotalar.keys()))
    
    yol_verisi = [[31.608, 40.732], [31.612, 40.725], [31.610, 40.710], [31.620, 40.690], [31.628, 40.675], [31.625, 40.655], [31.640, 40.640], [31.650, 40.612], [31.642, 40.600], [31.635, 40.585]]

    layer_path = pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_verisi}]), get_path="path", get_color=[255, 75, 75, 200], width_scale=3, width_min_pixels=3, get_dash_array=[7, 4])
    layer_points = pdk.Layer("ScatterplotLayer", pd.DataFrame(rotalar[rota_secimi]["duraklar"]), get_position="[boylam, enlem]", get_color=[0, 100, 255], get_radius=100)

    st.pydeck_chart(pdk.Deck(map_style="light", initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.63, zoom=11), layers=[layer_path, layer_points]))

    for durak in rotalar[rota_secimi]["duraklar"]:
        with st.expander(f"📍 {durak['isim']}", expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                foto_adi = durak['foto']
                # Çoklu yol kontrolü
                yollar = [foto_adi, f"./{foto_adi}", f"rota_rehberi/{foto_adi}"]
                yuklendi = False
                for y in yollar:
                    if os.path.exists(y):
                        st.image(y, use_container_width=True)
                        yuklendi = True
                        break
                if not yuklendi:
                    st.warning(f"🖼️ {foto_adi} yüklenemedi.")
            with col2:
                st.write(f"**Ulaşım:** {durak['ulasim']} | **Süre:** {durak['sure']}")
                st.write(f"**Aktivite:** {durak['aktivite']}")

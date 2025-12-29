import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Sayfa Ayarları
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Veri Seti
duraklar = [
    {"isim": "Şehir Oteli", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "0 dk", "mod": "Yaya 🚶", "aktivite": "Konaklama"},
    {"isim": "Gölcük Tabiat Parkı", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "mod": "Otobüs 🚌", "aktivite": "Doğa Yürüyüşü"},
    {"isim": "Sarıalan Yaylası", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 dk", "mod": "Minibüs 🚐", "aktivite": "Gastronomi"},
    {"isim": "Aladağ Yaylaları", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 dk", "mod": "Bisiklet 🚲", "aktivite": "Kamp ve Macera"}
]

# Google Maps Rota Linki (Koordinatlarla)
nav_link = "https://www.google.com/maps/dir/40.7325,31.6082/40.6552,31.6255/40.6120,31.6500/40.5850,31.6350"

# 3. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.title("🌲 Bolu Ekolojik Rota Rehberi")
    if st.button("KEŞFETMEYE BAŞLA"):
        st.session_state.giris = True
        st.rerun()
else:
    # 4. Ana Panel
    st.sidebar.markdown(f'<a href="{nav_link}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#D32F2F; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">🚗 NAVİGASYONU BAŞLAT</button></a>', unsafe_allow_html=True)
    
    if st.sidebar.button("⬅️ Giriş Ekranına Dön"):
        st.session_state.giris = False
        st.rerun()

    st.title("📍 Bolu Ekolojik Koridor Tur Rotası")

    # Harita Çizimi
    df = pd.DataFrame(duraklar)
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in duraklar]
    
    path_layer = pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_noktalari}]), get_path="path", get_color=[211, 47, 47], width_scale=20, width_min_pixels=3)
    point_layer = pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[46, 125, 50], get_radius=250, pickable=True)

    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.62, zoom=10.5),
        layers=[path_layer, point_layer],
        tooltip={"text": "{isim}"}
    ))

    # 5. Durak Detayları ve Görseller
    st.markdown("---")
    for d in duraklar:
        with st.expander(f"📍 {d['isim']} Detayları", expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                if os.path.exists(d['foto']):
                    st.image(d['foto'], use_container_width=True)
                else:
                    st.warning(f"🖼️ {d['foto']} bulunamadı.")
            with col2:
                st.subheader(d['isim'])
                st.write(f"⏱️ **Süre:** {d['sure']} | 🚌 **Mod:** {d['mod']}")
                st.write(f"🎭 **Aktivite:** {d['aktivite']}")

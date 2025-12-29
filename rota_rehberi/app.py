import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Sayfa ve Harita Ayarları 🎨
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Veri Seti (Koordinatlar Navigasyon İçin Sabitlendi) 📍
duraklar = [
    {
        "isim": "Şehir Oteli", 
        "enlem": 40.7325, "boylam": 31.6082, 
        "foto": "otel.jpg", "sure": "Başlangıç", "mod": "Yaya 🚶", 
        "aktivite": "Konaklama ve Bilgilendirme"
    },
    {
        "isim": "Bolu Gölcük Tabiat Parkı", 
        "enlem": 40.6552, "boylam": 31.6255, 
        "foto": "golcuk_bolu.jpg", "sure": "20 dk", "mod": "Eko-Otobüs 🚌", 
        "aktivite": "Doğa Yürüyüşü ve Rekreasyon"
    },
    {
        "isim": "Sarıalan Yaylası", 
        "enlem": 40.6120, "boylam": 31.6500, 
        "foto": "sarialan.jpg", "sure": "15 dk", "mod": "Minibüs 🚐", 
        "aktivite": "Yayla Gastronomisi"
    },
    {
        "isim": "Aladağ Yaylaları", 
        "enlem": 40.5850, "boylam": 31.6350, 
        "foto": "aladag.jpg", "sure": "10 dk", "mod": "Bisiklet 🚲", 
        "aktivite": "Kamp ve Macera Turizmi"
    }
]

# Google Haritalar Koordinat Bazlı Rota Linki (Niğde'ye gitmez!) 🚗
nav_link = "https://www.google.com/maps/dir/40.7325,31.6082/40.6552,31.6255/40.6120,31.6500/40.5850,31.6350"

# 3. Giriş Kontrolü
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
    # 4. Ana Panel
    st.title("📍 Ekolojik Koridor Tur Rotası")
    
    # Navigasyon Butonu (Sidebar)
    nav_button_html = f"""
    <a href="{nav_link}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#D32F2F; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold; cursor:pointer; margin-bottom:20px;">
            NAVİGASYONU BAŞLAT
        </div>
    </a>
    """
    st.sidebar.markdown(nav_button_html, unsafe_allow_html=True)
    
    if st.sidebar.button("⬅️ Giriş Ekranına Dön"):
        st.session_state.giris_yapildi = False
        st.rerun()

    # Harita Çizimi 🗺️
    df = pd.

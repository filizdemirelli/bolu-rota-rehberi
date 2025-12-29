import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Genel Ayarlar ve Harita Sağlayıcısı
st.set_page_config(page_title="Bolu Ekolojik Tur Rehberi", layout="wide")
pdk.settings.map_provider = "carto" # Ücretsiz ve stabil OSM tabanlı altlık

# 2. Tur Veri Seti (Koordinat, Süre ve Mod Bilgileri) 📋
duraklar = [
    {
        "isim": "Şehir Oteli", 
        "enlem": 40.7325, "boylam": 31.6082, 
        "foto": "otel.jpg", "sure": "Başlangıç", "mod": "Yaya 🚶", 
        "aktivite": "Konaklama ve Bilgilendirme"
    },
    {
        "isim": "Gölcük Tabiat Parkı", 
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

# Koordinat Bazlı Güvenli Navigasyon Linki (Bolu dışına çıkarmaz!) 🚗
nav_link = "https://www.google.com/maps/dir/40.7325,31.6082/40.6552,31.6255/40.6120,31.6500/40.5850,31.6350"

# 3. Giriş Kontrolü
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1000", use_container_width=True)
    st.title("🌲 Bolu Ekolojik Tur Rehberi")
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()

else:
    # 4. Ana Panel ve Harita 🗺️
    st.title("📍 Ekolojik Koridor Tur Rotası")
    
    # Navigasyon Butonu (Sidebar)
    st.sidebar.markdown(f'<a href="{nav_link}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#D32F2F; color:white; border:none; padding:12px;

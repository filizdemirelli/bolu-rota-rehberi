import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Klasör ve Sayfa Ayarları
BASE_DIR = Path(__file__).parent
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")

# 2. RENK UYUMU VE KOYU YEŞİL YAZI TASARIMI (CSS)
st.markdown("""
    <style>
    /* Ana Arka Plan ve Yan Menü Pastel Yeşil */
    .stApp, section[data-testid="stSidebar"] {
        background-color: #E8F5E9 !important;
    }

    /* Yazı Renklerini Koyu Yeşil Yapma (Arka planla uyumlu olması için) */
    h1, h2, h3, h4, h5, h6, p, span, label, li {
        color: #1B5E20 !important; /* Koyu yeşil tonu */
        font-weight: 500;
    }

    /* Açılır Paneller (Expander) Arka Planı ve Yazıları */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important; /* Beyaz panel başlığı */
        color: #1B5E20 !important;
        border: 1px solid #A5D6A7 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #F1F8E9 !important; /* Çok açık yeşil içerik alanı */
        border: 1px solid #C8E6C9 !important;
    }

    /* Buton Tasarımları */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
    }

    /* Navigasyon Butonu (Yan Menü) */
    .nav-btn-custom {
        display: block;
        padding: 15px;
        background-color: #1B5E20;
        color: white !important;
        text-align: center;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Rota Verileri
rotalar = {
    "EKOLOJİK KORİDOR (YAYLALAR)": [
        {"isim": "ŞEHİR OTELİ", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "BAŞLANGIÇ", "mod": "YAYA", "aktivite": "Şehrin kalbinde konforla buluşun."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Doğanın sessizliğini dinleyin."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "MİNİBÜS", "aktivite": "Geleneksel yayla lezzetlerini deneyimleyin."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BİSİKLET", "aktivite": "Yıldızlar altında kamp deneyimi."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kış masalı için hazırlık noktası."},
        {"isim": "KINDIRA YAYLASI", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 ARAÇ", "aktivite": "Soba başında otantik kahvaltı."},
        {"isim": "SARIALAN (KIŞ SENARYOSU)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 DK", "mod": "4x4 ARAÇ", "aktivite": "Bembeyaz bir kış rüyası fotoğrafçılığı."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 DK", "mod": "KAR ARACI", "aktivite": "Zirvede kayak keyfi ve lüks konaklama."}
    ]
}

# 4. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # GÜNCELLENMİŞ YEDİGÖLLER FOTOĞRAFI
    st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.markdown("##### DOĞANIN KALBİNDE SİZE ÖZEL BİR DENEYİM TASARLADIK")
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # 5. Sidebar ve Navigasyon
    st.sidebar.title("MENÜ")
    secilen_rota_adi = st.sidebar.selectbox("B

import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Sayfa Ayarları
try:
    st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
except:
    pass

BASE_DIR = Path(__file__).parent

# 2. EN SERT CSS: YAZILARI BEYAZA, ZEMİNİ YEŞİLE ZORLA
st.markdown("""
    <style>
    /* Arka Plan Renkleri */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* Tüm Butonlar İçin Ortak Ayar */
    div.stButton > button {
        background-color: #1B5E20 !important; /* Koyu Yeşil Arka Plan */
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        padding: 15px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* BUTON İÇİNDEKİ YAZIYI BEYAZA ZORLAMA (Giriş ve Dön Butonları) */
    div.stButton > button p, 
    div.stButton > button span, 
    div.stButton > button div {
        color: #FFFFFF !important;  /* KESİN BEYAZ */
        font-weight: 900 !important;
        font-size: 22px !important;
        text-transform: uppercase !important;
    }

    /* Panel Başlıkları */
    .streamlit-expanderHeader {
        background-color: #C8E6C9 !important;
        color: #1B5E20 !important;
    }

    /* Navigasyon Linki */
    .nav-btn-link {
        display: block;
        padding: 15px;
        background-color: #1B5E20;
        color: #FFFFFF !important;
        text-align: center;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 900;
        font-size: 18px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Rotalar (Gölcük ve Diğerleri Tam Liste)
rotalar = {
    "GÜNEY EKOLOJİK KORİDOR (GÖLCÜK HATTI)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "ARAÇ", "aktivite": "Şehir merkezinden doğaya açılan kapı."},
        {"isim": "KARACASU TERMAL", "enlem": 40.7000, "boylam": 31.6200, "foto": "karacasu.jpg", "sure": "10 DK", "mod": "ELEKTRİKLİ ARAÇ", "aktivite": "Şifalı sular ve termal dinlenme noktası."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "15 DK", "mod": "YÜRÜYÜŞ", "aktivite": "Bolu'nun simgesi, göl kenarında eşsiz bir yürüyüş deneyimi."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "BİSİKLET", "aktivite": "Yayla evleri ve yöresel kahvaltı durağı."},
        {"isim": "ALADAĞLAR KAMP ALANI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "20 DK", "mod": "KAMP", "aktivite": "Yıldızlar altında macera ve kamp finali."}

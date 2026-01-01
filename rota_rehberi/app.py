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
    ],
    "KUZEY ORMANLARI VE YEDİGÖLLER": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kuzey ormanlarına yolculuk."},
        {"isim": "YEDİGÖLLER MİLLİ PARKI", "enlem": 40.9415, "boylam": 31.7483, "foto": "yedigoller.jpg", "sure": "60 DK", "mod": "DOĞA KEŞFİ", "aktivite": "7 farklı göl ve bitki çeşitliliği."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP", "aktivite": "Ekipman hazırlığı."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "45 DK", "mod": "KAR ARACI", "aktivite": "Zirvede kış sporları."}
    ]
}

# 4. Uygulama Mantığı
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # GİRİŞ GÖRSELİ ÇALIŞMA GARANTİSİ
    giris_resmi = BASE_DIR / "yedigoller_yeni.jpg"
    if giris_resmi.exists():
        st.image(str(giris_resmi), use_container_width=True)
    else:
        # Eğer dosya yoksa internetten benzerini çeker (hata vermez)
        st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
        st.error("DİKKAT: 'yedigoller_yeni.jpg' GitHub klasöründe bulunamadı!")
    
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.write("Doğanın kalbinde size özel bir deneyim.")
    
    if st.button("KEŞFETMEYE BAŞLA"):
        st.session_state.giris = True
        st.rerun()
else:
    # Sidebar
    st.sidebar.title("NAVİGASYON")
    secilen_rota = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    duraklar = rotalar[secilen_rota]
    
    # 🚗 Navigasyon Butonu
    start, end = duraklar[0], duraklar[-1]
    g_url = f"https://www.google.com/maps/dir/{start['enlem']},{start['boylam']}/{end['enlem']},{end['boylam']}"
    st.sidebar.markdown(f'<a href="{g_url}" target="_blank" class="nav-btn-link">NAVİGASYONU BAŞLAT</a>', unsafe_allow_html=True)
    
    if st.sidebar.button("GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota)

    # Harita
    df = pd.DataFrame(duraklar)
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=df['enlem'].mean(), longitude=df['boylam'].mean(), zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=[46, 125, 50], width_scale=20),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[27, 94, 32], get_radius=400)
        ]
    ))

    # Kartlar
    st.markdown("---")
    for d in duraklar:
        with st.expander(d['isim'], expanded=True):
            c1, c2 = st.columns([1, 1.5])
            with c1:
                f_yolu = BASE_DIR / d['foto']
                if f_yolu.exists():
                    st.image(str(f_yolu), use_container_width=True)
                else:
                    st.info(f"Görsel: {d['foto']}")
            with c2:
                st.write(f"**ULAŞIM:** {d['mod']} | **SÜRE:** {d['sure']}")
                st.write(f"**DENEYİM:** {d['aktivite']}")

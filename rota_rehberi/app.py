import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Klasör ve Sayfa Ayarları
BASE_DIR = Path(__file__).parent
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")

# 2. RENK TUTARSIZLIKLARINI GİDEREN GELİŞMİŞ CSS
st.markdown("""
    <style>
    /* 1. Ana Arka Plan */
    .stApp {
        background-color: #E8F5E9 !important;
    }

    /* 2. Yan Menü (Sidebar) Tam Uyum */
    section[data-testid="stSidebar"] {
        background-color: #C8E6C9 !important;
        border-right: 1px solid #A5D6A7;
    }
    
    /* Yan menü içindeki tüm metinler */
    section[data-testid="stSidebar"] .stText, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox div {
        color: #000000 !important;
    }

    /* 3. Expander (Açılır Kartlar) Başlık ve İçerik Uyumu */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #A5D6A7 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #F1F8E9 !important;
        border: 1px solid #C8E6C9 !important;
        border-top: none;
    }

    /* 4. Seçim Kutusu (Selectbox) Renk Uyumu */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #A5D6A7 !important;
    }

    /* 5. Genel Yazı Rengi Zorlaması (Siyah) */
    h1, h2, h3, h4, h5, h6, p, li, span, label {
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 6. Butonlar */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #1B5E20 !important;
    }

    /* 7. Navigasyon Butonu (Sidebar) */
    .nav-link-custom {
        display: block;
        padding: 15px;
        background-color: #1B5E20;
        color: white !important;
        text-align: center;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Rota Verileri (Aynı Kalıyor)
rotalar = {
    "EKOLOJİK KORİDOR (YAYLALAR)": [
        {"isim": "ŞEHİR OTELİ", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "BAŞLANGIÇ", "mod": "YAYA", "aktivite": "Şehrin kalbinde, konforun ve modernizmin buluştuğu noktada keşfe hazırlanın."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Yansımaların büyüsüne kapılacağınız bu durakta, doğanın sessizliğini dinleyin."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "MİNİBÜS", "aktivite": "Yerel lezzetlerin izini sürerken, geleneksel yayla yaşamının modern sunumuna tanıklık edin."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BİSİKLET", "aktivite": "Doğanın tam merkezinde, dijital dünyadan uzaklaşıp kendinizi keşfedin."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Bolu'nun kış masalı için stratejik bir başlangıç noktası."},
        {"isim": "KINDIRA YAYLASI", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 ARAÇ", "aktivite": "Karlar altında saklı bir köy kahvaltısı ile güne enerjik bir başlangıç yapın."},
        {"isim": "SARIALAN (KIŞ SENARYOSU)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 DK", "mod": "4x4 ARAÇ", "aktivite": "Bembeyaz bir tuval üzerinde doğanın kış estetiğini ölümsüzleştirin."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 DK", "mod": "KAR ARACI", "aktivite": "Zirvede adrenalin ve lüksün buluştuğu noktada kış sporlarının keyfini sürün."}
    ]
}

# 4. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.markdown("<div style='text-align: center;'><br>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590059393164-904c632616f9?q=80&w=1200", use_container_width=True)
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.markdown("##### DOĞANIN KALBİNDE SİZE ÖZEL BİR DENEYİM TASARLADIK")
    if st.button("KEŞFETMEYE BAŞLA"):
        st.session_state.giris = True
        st.rerun()
else:
    # 5. Yan Menü (Sidebar) Tasarımı
    st.sidebar.header("MENÜ")
    secilen_rota_adi = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    secilen_duraklar = rotalar[secilen_rota_adi]
    
    # Google Maps Dinamik Link
    start = secilen_duraklar[0]
    end = secilen_duraklar[-1]
    nav_url = f"https://www.google.com/maps/dir/{start['enlem']},{start['boylam']}/{end['enlem']},{end['boylam']}/"

    st.sidebar.markdown(f'<a href="{nav_url}" target="_blank" class="nav-link-custom">NAVİGASYONU BAŞLAT</a>', unsafe_allow_html=True)
    
    if st.sidebar.button("GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota_adi)

    # 6. Harita
    df = pd.DataFrame(secilen_duraklar)
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in secilen_duraklar]
    line_color = [30, 136, 229] if "KIŞ" in secilen_rota_adi else [46, 125, 50]
    
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.70, zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_noktalari}]), get_path="path", get_color=line_color, width_scale=20, width_min_pixels=3),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=line_color, get_radius=300, pickable=True)
        ],
        tooltip={"text": "{isim}"}
    ))

    # 7. Detay Kartları
    st.markdown("---")
    for d in secilen_duraklar:
        with st.expander(d['isim'], expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                foto_yolu = BASE_DIR / d['foto']
                if foto_yolu.exists():
                    st.image(str(foto_yolu), use_container_width=True)
                else:
                    try:
                        st.image(d['foto'], use_container_width=True)
                    except:
                        st.info(f"GÖRSEL YÜKLENİYOR: {d['foto']}")
            with col2:
                st.write(f"**ULAŞIM SÜRESİ:** {d['sure']}")
                st.write(f"**ERİŞİM MODU:** {d['mod']}")
                st.write(f"**DENEYİM:** {d['aktivite']}")

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

# 2. Gelişmiş Tasarım (Okunabilir Yazılar ve Pastel Yeşil Tema)
st.markdown("""
    <style>
    /* Ana Arka Plan ve Sidebar */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* Panel Başlıkları (Gri Çubuklar Yerine Açık Yeşil) */
    .streamlit-expanderHeader {
        background-color: #C8E6C9 !important;
        color: #1B5E20 !important;
        border: 1px solid #A5D6A7 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #F1F8E9 !important;
        border: 1px solid #A5D6A7 !important;
    }

    /* Tüm Yazılar Koyu Yeşil */
    h1, h2, h3, h4, h5, h6, p, span, label, li {
        color: #1B5E20 !important;
    }

    /* KEŞFETMEYE BAŞLA BUTONU - BEYAZ YAZI VE KOYU YEŞİL ARKA PLAN */
    div.stButton > button {
        background-color: #1B5E20 !important; /* Koyu Orman Yeşili */
        color: #FFFFFF !important; /* PARLAK BEYAZ YAZI */
        border-radius: 12px;
        padding: 18px 36px;
        font-weight: 800 !important;
        font-size: 22px !important;
        border: none;
        width: 100%;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    
    div.stButton > button:hover {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    /* Sidebar Geri Dön Butonu */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1B5E20 !important;
        font-size: 14px !important;
        padding: 8px 12px;
        border: 1px solid #1B5E20;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Rota Verileri (Merkezden Kuzeye Yedigöller Rotası Dahil)
rotalar = {
    "KUZEY ORMANLARI VE YEDİGÖLLER": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kuzey ormanlarının derinliklerine uzanan serüven için hazırlık."},
        {"isim": "YAZIÖREN YAYLASI", "enlem": 40.8200, "boylam": 31.6500, "foto": "yazioren.jpg", "sure": "25 DK", "mod": "ARAÇ", "aktivite": "Kuzey rotasının ilk orman durağı ve temiz hava molası."},
        {"isim": "AYI KAYASI MEVKİİ", "enlem": 40.8800, "boylam": 31.7200, "foto": "ayikayasi.jpg", "sure": "20 DK", "mod": "YÜRÜYÜŞ", "aktivite": "Yedigöller yolu üzerinde vahşi yaşam gözlemi ve seyir terası deneyimi."},
        {"isim": "YEDİGÖLLER MİLLİ PARKI", "enlem": 40.9415, "boylam": 31.7483, "foto": "yedigoller.jpg", "sure": "30 DK", "mod": "KAMP", "aktivite": "Yedi gölün büyüleyici atmosferinde kamp ve fotoğrafçılık finali."}
    ],
    "GÜNEY EKOLOJİK KORİDOR (YAYLALAR)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "ARAÇ", "aktivite": "Güney yaylalarına geçiş."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Huzur dolu göl yürüyüşü."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "ARAÇ", "aktivite": "Geleneksel yayla gastronomi durağı."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BİSİKLET", "aktivite": "Macera odaklı kamp deneyimi."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kış masalı rotası başlangıcı."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "45 DK", "mod": "KAR ARACI", "aktivite": "Zirvede kayak ve kış sporları keyfi."}
    ]
}

# 4. Uygulama Akışı
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # Giriş Görseli (GitHub'daki yedigoller.jpg)
    giris_resmi = BASE_DIR / "yedigoller.jpg"
    if giris_resmi.exists():
        st.image(str(giris_resmi), use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
    
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.write("Doğanın kalbinde size özel bir deneyim tasarladık.")
    
    # Yazı rengi beyaz olan buton
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # Sidebar Tasarımı
    st.sidebar.title("NAVİGASYON")
    secilen_rota = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    duraklar = rotalar[secilen_rota]
    
    if st.sidebar.button("← GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota)

    # 5. Harita (Seçilen rotaya odaklı)
    df = pd.DataFrame(duraklar)
    mid_lat, mid_lon = df['enlem'].mean(), df['boylam'].mean()
    
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=mid_lat, longitude=mid_lon, zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=[46, 125, 50], width_scale=20, width_min_pixels=3),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[27, 94, 32], get_radius=400, pickable=True)
        ],
        tooltip={"text": "{isim}"}
    ))

    # 6. Detay Panelleri (Açık Yeşil Gri Değil)
    st.markdown("---")
    for d in duraklar:
        with st.expander(d['isim'], expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                f_path = BASE_DIR / d['foto']
                if f_path.exists():
                    st.image(str(f_path), use_container_width=True)
                else:
                    st.info(f"Görsel Bekleniyor: {d['foto']}")
            with col2:
                st.write(f"**ULAŞIM MODU:** {d['mod']}")
                st.write(f"**SÜRE:** {d['sure']}")
                st.markdown(f"**DENEYİM:** {d['aktivite']}")


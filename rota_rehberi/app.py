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

# 2. GELİŞMİŞ TASARIM (Beyaz Yazılı Butonlar ve Pastel Tema)
st.markdown("""
    <style>
    /* Ana Arka Plan ve Sidebar */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* Panel Başlıkları (Gri Değil, Açık Yeşil) */
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

    /* KEŞFETMEYE BAŞLA BUTONU (Beyaz Yazı Garantili) */
    div.stButton > button {
        background-color: #1B5E20 !important; /* Koyu Yeşil Arka Plan */
        color: #FFFFFF !important; /* BEMBEYAZ YAZI */
        border-radius: 10px;
        padding: 15px 30px;
        font-weight: 800 !important;
        font-size: 20px !important;
        border: none;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Sidebar'daki Geri Dön Butonu */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1B5E20 !important;
        font-size: 14px !important;
        padding: 5px 10px;
        border: 1px solid #1B5E20;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Rota Verileri (Kuzeye Doğru Yedigöller Odaklı)
rotalar = {
    "KUZEY ORMANLARI VE YEDİGÖLLER": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "ARAÇ / VIP", "aktivite": "Kuzeyin derinliklerine doğru yolculuk hazırlığı."},
        {"isim": "YAZIÖREN YAYLASI", "enlem": 40.8200, "boylam": 31.6500, "foto": "yazioren.jpg", "sure": "25 DK", "mod": "OFF-ROAD / ARAÇ", "aktivite": "Kuzey rotasının ilk durağı, çam ormanları arasında temiz hava molası."},
        {"isim": "AYI KAYASI MEVKİİ", "enlem": 40.8800, "boylam": 31.7200, "foto": "ayikayasi.jpg", "sure": "20 DK", "mod": "YÜRÜYÜŞ", "aktivite": "Deneyim odaklı doğa gözlemi ve vahşi yaşam izleri takibi."},
        {"isim": "YEDİGÖLLER MİLLİ PARKI", "enlem": 40.9415, "boylam": 31.7483, "foto": "yedigoller.jpg", "sure": "30 DK", "mod": "KAMP", "aktivite": "Rotanın finali: 7 gölün etrafında eşsiz kamp ve fotoğraf deneyimi."}
    ],
    "GÜNEY EKOLOJİK KORİDOR (YAYLALAR)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "ARAÇ", "aktivite": "Güney yaylalarına geçiş noktası."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Göl etrafında huzurlu bir yürüyüş."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "ARAÇ", "aktivite": "Yayla kültürü ve yöresel lezzetler."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BİSİKLET", "aktivite": "Güneyin en yükseklerinde kamp keyfi."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kış masalı rotası."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "45 DK", "mod": "KAR ARACI", "aktivite": "Zirvede kayak ve kış sporları."}
    ]
}

# 4. Uygulama Akışı
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # Giriş Görseli (GitHub'daki yedigoller.jpg'i okur)
    giris_resmi = BASE_DIR / "yedigoller.jpg"
    if giris_resmi.exists():
        st.image(str(giris_resmi), use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
    
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.write("Doğanın kalbinde size özel bir deneyim tasarladık.")
    # Buton yazısı artık b-e-y-a-z!
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # Sidebar
    st.sidebar.title("NAVİGASYON")
    secilen_rota = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    duraklar = rotalar[secilen_rota]
    
    if st.sidebar.button("← GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota)

    # 5. Harita Ayarı
    df = pd.DataFrame(duraklar)
    # Haritayı rota merkezine odakla
    mid_lat = df['enlem'].mean()
    mid_lon = df['boylam'].mean()
    
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=mid_lat, longitude=mid_lon, zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=[46, 125, 50], width_scale=20, width_min_pixels=3),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[27, 94, 32], get_radius=400, pickable=True)
        ],
        tooltip={"text": "{isim}"}
    ))

    # 6. Detay Panelleri
    st.markdown("---")
    for d in duraklar:
        with st.expander(d['isim'], expanded=True):
            c1, c2 = st.columns([1, 1.5])
            with c1:
                f_path = BASE_DIR / d['foto']
                if f_path.exists():
                    st.image(str(f_path), use_container_width=True)
                else:
                    st.info(f"Görsel Bekleniyor: {d['foto']}")
            with c2:
                st.write(f"**ULAŞIM MODU:** {d['mod']}")
                st.write(f"**SÜRE:** {d['sure']}")
                st.markdown(f"**DENEYİM:** {d['aktivite']}")

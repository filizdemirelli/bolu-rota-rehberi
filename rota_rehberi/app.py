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

# 2. SERT CSS MÜDAHALESİ (Buton Yazısı ve Pastel Tema)
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* Panel Başlıkları */
    .streamlit-expanderHeader {
        background-color: #C8E6C9 !important;
        color: #1B5E20 !important;
        border: 1px solid #A5D6A7 !important;
        border-radius: 8px !important;
    }

    /* Yazılar */
    h1, h2, h3, h4, h5, h6, p, span, label, li {
        color: #1B5E20 !important;
    }

    /* KEŞFETMEYE BAŞLA BUTONU - KESİN BEYAZ YAZI ZORLAMASI */
    div.stButton > button {
        background-color: #1B5E20 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    /* Butonun içindeki metni doğrudan hedef alan beyazlatma */
    div.stButton > button p, div.stButton > button div, div.stButton > button span {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 24px !important;
        text-transform: uppercase !important;
    }
    
    div.stButton > button:hover {
        background-color: #2E7D32 !important;
        transform: translateY(-2px);
    }

    /* Sidebar Geri Dön Butonu */
    section[data-testid="stSidebar"] div.stButton > button p {
        color: #1B5E20 !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Güncellenmiş Rota Verileri
rotalar = {
    "KIŞ TURİZMİ (KARTALKAYA HATTI)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kış rotası hazırlığı ve ekipman kontrolü."},
        {"isim": "KINDIRA KÖYÜ", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 ARAÇ", "aktivite": "Karlar altında otantik bir köy kahvaltısı ve soba başı sohbetleri."},
        {"isim": "SARIALAN (KIŞ SENARYOSU)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 DK", "mod": "4x4 ARAÇ", "aktivite": "Donmuş göletler ve bembeyaz çam ormanları arasında kış fotoğrafçılığı."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 DK", "mod": "KAR ARACI", "aktivite": "Zirvede kayak, snowboard ve lüks şömine keyfi."}
    ],
    "KUZEY ORMANLARI VE YEDİGÖLLER": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "ARAÇ", "aktivite": "Kuzeye doğru orman yolculuğu."},
        {"isim": "YAZIÖREN YAYLASI", "enlem": 40.8200, "boylam": 31.6500, "foto": "yazioren.jpg", "sure": "25 DK", "mod": "ARAÇ", "aktivite": "Sessiz yayla atmosferinde orman molası."},
        {"isim": "YEDİGÖLLER MİLLİ PARKI", "enlem": 40.9415, "boylam": 31.7483, "foto": "yedigoller.jpg", "sure": "50 DK", "mod": "KAMP", "aktivite": "Doğa harikası 7 göl etrafında kamp ve keşif."}
    ],
    "GÜNEY EKOLOJİK KORİDOR": [
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Ekolojik yürüyüş hattı."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "30 DK", "mod": "BİSİKLET", "aktivite": "Macera odaklı yayla kampı."}
    ]
}

# 4. Uygulama Akışı
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # YENİ YEDİGÖLLER GÖRSELİ (GitHub: yedigoller_yeni.jpg)
    giris_resmi = BASE_DIR / "yedigoller_yeni.jpg"
    if giris_resmi.exists():
        st.image(str(giris_resmi), use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
        st.info("İpucu: Kendi görselini 'yedigoller_yeni.jpg' adıyla GitHub'a yüklersen burada o görünecek.")
    
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.write("Doğanın kalbinde size özel bir deneyim tasarladık.")
    
    # Buton ve Beyaz Yazı Denetimi
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

    # 5. Harita
    df = pd.DataFrame(duraklar)
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=df['enlem'].mean(), longitude=df['boylam'].mean(), zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=[46, 125, 50], width_scale=20),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[27, 94, 32], get_radius=400, pickable=True)
        ],
        tooltip={"text": "{isim}"}
    ))

    # 6. Detaylar
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

import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Sayfa Ayarları
try:
    st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide", initial_sidebar_state="expanded")
except:
    pass

BASE_DIR = Path(__file__).parent

# 2. TEMAYI AÇIK RENGE ZORLAYAN CSS (Of dedirtmeyen versiyon)
st.markdown("""
    <style>
    /* 1. Tüm Arka Planı Pastel Yeşil Yap */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* 2. O Koyu Gri Çubukları (Expander) Açık Yeşil Yap */
    .streamlit-expanderHeader {
        background-color: #C8E6C9 !important; /* Açık Pastel Yeşil */
        color: #1B5E20 !important; /* Koyu Yeşil Yazı */
        border: 1px solid #A5D6A7 !important;
        border-radius: 8px !important;
    }
    
    /* 3. Panel İçlerini de Aynı Renk Yap */
    .streamlit-expanderContent {
        background-color: #E8F5E9 !important;
        border: 1px solid #A5D6A7 !important;
        border-top: none;
    }

    /* 4. Tüm Yazıları Siyaha/Koyu Yeşile Zorla */
    h1, h2, h3, h4, h5, h6, p, span, label, li, small {
        color: #1B5E20 !important;
    }

    /* 5. Buton Tasarımı */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }

    /* 6. Sidebar (Yan Menü) İçindeki Yazılar */
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #1B5E20 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Rota Verileri
rotalar = {
    "EKOLOJİK KORİDOR (YAYLALAR)": [
        {"isim": "ŞEHİR OTELİ", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "BAŞLANGIÇ", "mod": "YAYA", "aktivite": "Şehrin kalbinde konforlu bir başlangıç."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Doğanın ve huzurun merkezi."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "MİNİBÜS", "aktivite": "Geleneksel yayla gastronomi deneyimi."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BİSİKLET", "aktivite": "Macera ve sürdürülebilir kamp."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kış rotası hazırlık noktası."},
        {"isim": "KINDIRA YAYLASI", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 ARAÇ", "aktivite": "Otantik kış kahvaltısı."},
        {"isim": "SARIALAN (KIŞ)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 DK", "mod": "4x4 ARAÇ", "aktivite": "Kış fotoğrafçılığı rotası."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 DK", "mod": "KAR ARACI", "aktivite": "Pistlerde kayak ve kış keyfi."}
    ]
}

# 4. Uygulama Akışı
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # GitHub'daki yedigoller.jpg dosyasını oku
    giris_resmi = BASE_DIR / "yedigoller.jpg"
    if giris_resmi.exists():
        st.image(str(giris_resmi), use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
    
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.write("Doğanın kalbinde size özel bir deneyim tasarladık.")
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # Sidebar
    st.sidebar.title("SEÇENEKLER")
    secilen_rota = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    duraklar = rotalar[secilen_rota]
    
    if st.sidebar.button("GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota)

    # Harita
    df = pd.DataFrame(duraklar)
    line_color = [30, 136, 229] if "KIŞ" in secilen_rota else [46, 125, 50]
    
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.70, zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=line_color, width_scale=20, width_min_pixels=3),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=line_color, get_radius=300, pickable=True)
        ],
        tooltip={"text": "{isim}"}
    ))

    # Detaylar (Açık Yeşil Paneller)
    st.markdown("---")
    for d in duraklar:
        with st.expander(d['isim'], expanded=True):
            c1, c2 = st.columns([1, 1.5])
            with c1:
                f_path = BASE_DIR / d['foto']
                if f_path.exists():
                    st.image(str(f_path), use_container_width=True)
                else:
                    st.info(f"Görsel Yükleniyor: {d['foto']}")
            with c2:
                st.write(f"**ULAŞIM:** {d['mod']}")
                st.write(f"**DENEYİM:** {d['aktivite']}")

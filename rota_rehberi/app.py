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

# 2. OKUNABİLİRLİK VE PASTEL TEMA (Gelişmiş CSS)
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* Panel Başlıkları (Açık Yeşil) */
    .streamlit-expanderHeader {
        background-color: #C8E6C9 !important;
        color: #1B5E20 !important;
        border: 1px solid #A5D6A7 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #E8F5E9 !important;
        border: 1px solid #A5D6A7 !important;
    }

    /* Yazılar */
    h1, h2, h3, h4, h5, h6, p, span, label, li {
        color: #1B5E20 !important;
    }

    /* BUTONLARIN OKUNABİLİRLİĞİ (Keşfet ve Dön Butonları) */
    div.stButton > button {
        background-color: #1B5E20 !important; /* Çok Koyu Yeşil */
        color: #FFFFFF !important; /* Bembeyaz Yazı - Net Okunur */
        border-radius: 10px;
        border: 2px solid #1B5E20;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 18px !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #2E7D32 !important;
        color: white !important;
        border-color: #2E7D32;
    }

    /* Sidebar İçindeki Buton Özel Ayarı */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1B5E20 !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Güncellenmiş Rota Verileri (Kuzey Rotası Eklendi)
rotalar = {
    "KUZEY MACERA VE KAMP": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "4x4 / KAMP KARAVANI", "aktivite": "Kuzeyin derin ormanlarına yolculuk için hazırlık ve lojistik nokta."},
        {"isim": "YEDİGÖLLER YOLU", "enlem": 40.8500, "boylam": 31.7000, "foto": "yedigoller_yol.jpg", "sure": "45 DK", "mod": "ARAÇ", "aktivite": "Sisli orman yollarında sürüş keyfi ve yol üstü seyir terasları."},
        {"isim": "ALADAĞ KAMP ALANI", "enlem": 40.9500, "boylam": 31.8000, "foto": "aladag_kamp.jpg", "sure": "30 DK", "mod": "PİYADE / BİSİKLET", "aktivite": "Deneyim odaklı çadır kampı, gece ateşi ve vahşi doğa gözlemi."},
        {"isim": "KUZEY ZİRVE NOKTASI", "enlem": 41.0500, "boylam": 31.8500, "foto": "zirve.jpg", "sure": "20 DK", "mod": "TREKKING", "aktivite": "Bolu'nun en kuzeyinde panoramik manzara eşliğinde final."}
    ],
    "EKOLOJİK KORİDOR (YAYLALAR)": [
        {"isim": "ŞEHİR OTELİ", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "BAŞLANGIÇ", "mod": "YAYA", "aktivite": "Şehir konforundan doğaya ilk adım."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", "aktivite": "Huzur ve doğa yürüyüşü."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "MİNİBÜS", "aktivite": "Gastronomi ve yerel yaşam."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BİSİKLET", "aktivite": "Kamp ve macera."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", "aktivite": "Kış rotası başlangıcı."},
        {"isim": "KINDIRA YAYLASI", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 ARAÇ", "aktivite": "Karlar altında kahvaltı."},
        {"isim": "KARTALKAYA", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 DK", "mod": "KAR ARACI", "aktivite": "Kayak ve zirve keyfi."}
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
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # Sidebar
    st.sidebar.title("NAVİGASYON")
    secilen_rota = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    duraklar = rotalar[secilen_rota]
    
    # Buton artık beyaz zemin üzerine koyu yeşil yazı, çok net!
    if st.sidebar.button("← GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota)

    # 5. Harita
    df = pd.DataFrame(duraklar)
    line_color = [30, 136, 229] if "KIŞ" in secilen_rota else [46, 125, 50]
    
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.80, longitude=31.70, zoom=9),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=line_color, width_scale=20, width_min_pixels=3),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=line_color, get_radius=400, pickable=True)
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

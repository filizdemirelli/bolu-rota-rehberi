import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Klasör ve Sayfa Ayarları
BASE_DIR = Path(__file__).parent
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")

# 2. Pastel Yeşil Tema ve Özel Tasarım (CSS)
st.markdown("""
    <style>
    /* Arka Plan Pastel Yeşil */
    .stApp {
        background-color: #E8F5E9;
        animation: fadeIn 1.2s ease-in;
    }
    
    /* Tüm Yazıları Siyah Yapma */
    html, body, [class*="st-"] {
        color: #000000 !important;
    }

    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }

    /* Yan Menü (Sidebar) Uygun Renk */
    [data-testid="stSidebar"] {
        background-color: #C8E6C9 !important;
        border-right: 1px solid #A5D6A7;
    }

    /* Kartlar (Expander) Krem Rengi ve Siyah Yazı */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 8px !important;
        border: 1px solid #A5D6A7 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    /* Modern Siyah Buton */
    div.stButton > button {
        background-color: #2E7D32;
        color: white !important;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
    }
    
    div.stButton > button:hover {
        background-color: #1B5E20;
        color: white !important;
    }

    /* Navigasyon Butonu */
    .nav-btn {
        background-color: #1B5E20;
        color: white !important;
        padding: 15px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        text-decoration: none;
        display: block;
        border: 1px solid #000;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Eksiksiz Rota Verileri
rotalar = {
    "EKOLOJİK KORİDOR (YAYLALAR)": [
        {
            "isim": "ŞEHİR OTELİ", 
            "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", 
            "sure": "BAŞLANGIÇ", "mod": "YAYA", 
            "aktivite": "Şehrin kalbinde, konforun ve modernizmin buluştuğu noktada keşfe hazırlanın. Yolculuğunuzun ilk adımı, Bolu'nun misafirperverliği ile başlıyor."
        },
        {
            "isim": "GÖLCÜK TABİAT PARKI", 
            "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", 
            "sure": "20 DK", "mod": "ELEKTRİKLİ OTOBÜS", 
            "aktivite": "Yansımaların büyüsüne kapılacağınız bu durakta, doğanın sessizliğini dinleyin. Kartpostallık manzaralar eşliğinde sürdürülebilir turizmin tadını çıkarın."
        },
        {
            "isim": "SARIALAN YAYLASI", 
            "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", 
            "sure": "15 DK", "mod": "MİNİBÜS", 
            "aktivite": "Yerel lezzetlerin izini sürerken, geleneksel yayla yaşamının modern sunumuna tanıklık edin. Gastronomi durağımızda organik ürünlerle hazırlanan reçeteleri deneyimleyin."
        },
        {
            "isim": "ALADAĞ YAYLALARI", 
            "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", 
            "sure": "10 DK", "mod": "BİSİKLET", 
            "aktivite": "Sınırları zorlayan bir macera ve yıldızlar altında kusursuz bir kamp deneyimi sizi bekliyor. Doğanın tam merkezinde, dijital dünyadan uzaklaşıp kendinizi keşfedin."
        }
    ],
    "KIŞ TURİZMİ (KARTALKAYA)": [
        {
            "isim": "BOLU MERKEZ", 
            "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", 
            "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", 
            "aktivite": "Bolu'nun kış masalı için stratejik bir başlangıç noktası. Ekipman kontrolü ve kış senaryosuna dair son hazırlıklarımızı burada tamamlıyoruz."
        },
        {
            "isim": "KINDIRA YAYLASI", 
            "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", 
            "sure": "25 DK", "mod": "4x4 ARAÇ", 
            "aktivite": "Karlar altında saklı bir köy kahvaltısı ile güne enerjik ve otantik bir başlangıç yapın. Soba başında ısınırken köylülerin kış hikayelerine ortak olun."
        },
        {
            "isim": "SARIALAN (KIŞ SENARYOSU)", 
            "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", 
            "sure": "15 DK", "mod": "4x4 ARAÇ", 
            "aktivite": "Bembeyaz bir tuval üzerinde, doğanın kış estetiğini ölümsüzleştireceğiniz fotoğraf rotası. Donmuş göletler ve kar yüklü çam ağaçları arasında bir kış rüyası."
        },
        {
            "isim": "KARTALKAYA KAYAK MERKEZİ", 
            "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", 
            "sure": "20 DK", "mod": "KAR ARACI", 
            "aktivite": "Zirvede adrenalin ve lüksün buluştuğu noktada, kış sporlarının keyfini sürün. Pistlerin sonunda şömine başında yorgunluk atarken gün batımını izleyin."
        }
    ]
}

# 4. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.markdown("<div style='text-align: center;'><br>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590059393164-904c632616f9?q=80&w=1200", use_container_width=True)
    st.title("BOLU TEMATİK ROTA REHBERİ")
    st.markdown("<h5 style='color: black;'>DOĞANIN KALBİNDE SİZE ÖZEL BİR DENEYİM TASARLADIK</h5>", unsafe_allow_html=True)
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # 5. Yan Menü
    st.sidebar.title("ROTA SEÇİMİ")
    secilen_rota_adi = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    secilen_duraklar = rotalar[secilen_rota_adi]
    
    start = secilen_duraklar[0]
    end = secilen_duraklar[-1]
    nav_url = f"https://www.google.com/maps/dir/{start['enlem']},{start['boylam']}/{end['enlem']},{end['boylam']}/"

    st.sidebar.markdown(f'<a href="{nav_url}" target="_blank" class="nav-btn">NAVİGASYONU BAŞLAT</a>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("GİRİŞ EKRANINA DÖN", use_container_width=True):
        st.session_state.giris = False
        st.rerun()

    st.markdown(f"<h1 style='color: black;'>{secilen_rota_adi}</h1>", unsafe_allow_html=True)

    # 6. Harita
    df = pd.DataFrame(secilen_duraklar)
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in secilen_duraklar]
    line_color = [30, 136, 229] if "KIŞ" in secilen_rota_adi else [46, 125, 50]
    
    path_layer = pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_noktalari}]), get_path="path", get_color=line_color, width_scale=20, width_min_pixels=3)
    point_layer = pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=line_color, get_radius=300, pickable=True)

    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.70, zoom=10),
        layers=[path_layer, point_layer],
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
                st.markdown(f"<p style='color: black;'><b>ULAŞIM SÜRESİ:</b> {d['sure']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black;'><b>ERİŞİM MODU:</b> {d['mod']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black;'><b>DENEYİM:</b> {d['aktivite']}</p>", unsafe_allow_html=True)

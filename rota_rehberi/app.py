import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Klasör ve Sayfa Ayarları
BASE_DIR = Path(__file__).parent
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Reklam Diliyle Düzenlenmiş Rota Verileri
rotalar = {
    "EKOLOJIK KORIDOR (YAYLALAR)": [
        {"isim": "SEHIR OTELI", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "BASLANGIC", "mod": "YAYA", "aktivite": "SEHRIN KALBINDE, KONFORUN VE MODERNIZMIN BULUSTUGU NOKTADA KESFE HAZIRLANIN."},
        {"isim": "GOLCUK TABIAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "ELEKTRIKLI OTOBUS", "aktivite": "YANSIMALARIN BUYUSUNE KAPILACAGINIZ BU DURAKTA, DOGANIN SESSIZLIGINI DINLEYIN."},
        {"isim": "SARIALAN YAYLASI", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 DK", "mod": "MINIBUS", "aktivite": "YEREL LEZZETLERIN IZINI SURERKEN, GELENEKSEL YAYLA YASAMININ MODERN SUNUMUNA TANIKLIK EDIN."},
        {"isim": "ALADAG YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 DK", "mod": "BISIKLET", "aktivite": "SINIRLARI ZORLAYAN BIR MACERA VE YILDIZLAR ALTINDA KUSURSUZ BIR KAMP DENEYIMI SIZI BEKLIYOR."}
    ],
    "KIS TURIZMI (KARTALKAYA)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BASLANGIC", "mod": "VIP TRANSFER", "aktivite": "BOLU'NUN KIS MASALI ICIN STRATEJIK BIR BASLANGIC VE SON HAZIRLIK NOKTASI."},
        {"isim": "KINDIRA YAYLASI", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 ARAC", "aktivite": "KARLAR ALTINDA SAKLI BIR KOY KAHVALTISI ILE GUNE ENERJIK VE OTANTIK BIR BASLANGIC YAPIN."},
        {"isim": "SARIALAN (KIS SENARYOSU)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 DK", "mod": "4x4 ARAC", "aktivite": "BEMBEYAZ BIR TUVAL UZERINDE, DOGANIN KIS ESTETIGINI OLUMSUZLESTIRECEGINIZ FOTOGRAF ROTASI."},
        {"isim": "KARTALKAYA KAYAK MERKEZI", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 DK", "mod": "KAR ARACI", "aktivite": "ZIRVEDE ADRENALIN VE LUKSUN BULUSTUGU NOKTADA, KIS SPORLARININ KEYFINI SURUN."}
    ]
}

# 3. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590059393164-904c632616f9?q=80&w=1200", use_container_width=True)
    st.title("BOLU TEMATIK ROTA REHBERI")
    st.markdown("##### DOGANIN KALBINDE SIZE OZEL BIR DENEYIM TASARLADIK")
    
    if st.button("KESFETMEYE BASLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # 4. Yan Menü
    st.sidebar.title("ROTA SECIMI")
    secilen_rota_adi = st.sidebar.selectbox("BIR DENEYIM SECIN", list(rotalar.keys()))
    secilen_duraklar = rotalar[secilen_rota_adi]
    
    start = secilen_duraklar[0]
    end = secilen_duraklar[-1]
    nav_url = f"https://www.google.com/maps/dir/{start['enlem']},{start['boylam']}/{end['enlem']},{end['boylam']}/"

    st.sidebar.markdown(f"""
        <a href="{nav_url}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#1E1E1E; color:white; padding:15px; border-radius:4px; text-align:center; font-weight:bold; letter-spacing:1px; border: 1px solid #444;">
                NAVIGASYONU BASLAT
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("GIRIS EKRANINA DON", use_container_width=True):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota_adi)

    # 5. Harita ve Görselleştirme
    df = pd.DataFrame(secilen_duraklar)
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in secilen_duraklar]
    line_color = [0, 100, 255] if "KIS" in secilen_rota_adi else [34, 139, 34]
    
    path_layer = pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_noktalari}]), get_path="path", get_color=line_color, width_scale=20, width_min_pixels=3)
    point_layer = pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=line_color, get_radius=300, pickable=True)

    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.70, zoom=10),
        layers=[path_layer, point_layer],
        tooltip={"text": "{isim}"}
    ))

    # 6. Detay Kartları
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
                        st.info(f"GORSEL HAZIRLANIYOR: {d['foto']}")
            with col2:
                st.write(f"**ULASIM SURESI:** {d['sure']}")
                st.write(f"**ERISIM MODU:** {d['mod']}")
                st.markdown(f"**DENEYIM:** {d['aktivite']}")

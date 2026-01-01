import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from pathlib import Path

# 1. Klasör ve Sayfa Ayarları
BASE_DIR = Path(__file__).parent
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Rota Verileri
rotalar = {
    "Ekolojik Koridor (Yaylalar)": [
        {"isim": "Şehir Oteli", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "Başlangıç", "mod": "Yaya 🚶", "aktivite": "Konaklama"},
        {"isim": "Gölcük Tabiat Parkı", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "mod": "Otobüs 🚌", "aktivite": "Doğa Yürüyüşü"},
        {"isim": "Sarıalan Yaylası", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 dk", "mod": "Minibüs 🚐", "aktivite": "Gastronomi"},
        {"isim": "Aladağ Yaylaları", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 dk", "mod": "Bisiklet 🚲", "aktivite": "Macera"}
    ],
    "Kış Turizmi (Kartalkaya)": [
        {"isim": "Bolu Merkez", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "Başlangıç", "mod": "Şahsi Araç 🚗", "aktivite": "Hazırlık"},
        {"isim": "Kındıra Yaylası", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 dk", "mod": "4x4 Araç 🚙", "aktivite": "Köy Kahvaltısı"},
        {"isim": "Sarıalan (Kar Altında)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 dk", "mod": "4x4 Araç 🚙", "aktivite": "Fotoğrafçılık"},
        {"isim": "Kartalkaya Kayak Merkezi", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 dk", "mod": "Kar Aracı ❄️", "aktivite": "Kayak/Snowboard"}
    ]
}

# 3. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # GİRİŞ EKRANI VE FOTOĞRAF
    st.markdown("<br>", unsafe_allow_html=True)
    # Bolu için kaliteli ve kalıcı bir doğa görseli linki
    st.image("https://images.unsplash.com/photo-1590059393164-904c632616f9?q=80&w=1200", caption="Doğanın Kalbi Bolu'ya Hoş Geldiniz", use_container_width=True)
    st.title("🌲 Bolu Tematik Rota Rehberi")
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # 4. Ana Panel ve Seçimler
    st.sidebar.title("🗺️ Rota Seçimi")
    secilen_rota_adi = st.sidebar.selectbox("Bir rota seçin:", list(rotalar.keys()))
    secilen_duraklar = rotalar[secilen_rota_adi]
    
    # Navigasyon Linki (Koordinat Bazlı)
    start = secilen_duraklar[0]
    end = secilen_duraklar[-1]
    nav_url = f"https://www.google.com/maps/dir/{start['enlem']},{start['boylam']}/{end['enlem']},{end['boylam']}/"

    st.sidebar.markdown(f"""
        <a href="{nav_url}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#D32F2F; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; cursor:pointer;">
                🚗 SEÇİLİ ROTAYI BAŞLAT
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("⬅️ Giriş Ekranına Dön", use_container_width=True):
        st.session_state.giris = False
        st.rerun()

    st.title(f"📍 {secilen_rota_adi}")

    # 5. Harita ve Tooltip (Hata Giderildi)
    df = pd.DataFrame(secilen_duraklar)
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in secilen_duraklar]
    
    line_color = [30, 144, 255] if "Kış" in secilen_rota_adi else [211, 47, 47]
    
    path_layer = pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_noktalari}]), get_path="path", get_color=line_color, width_scale=20, width_min_pixels=3)
    point_layer = pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[0, 0, 139] if "Kış" in secilen_rota_adi else [46, 125, 50], get_radius=300, pickable=True)

    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.70, zoom=10),
        layers=[path_layer, point_layer],
        tooltip={"text": "{isim}"} # Buradaki parantez hatası düzeltildi
    ))

    # 6. Durak Detayları ve Görsel Kontrolü
    st.markdown("---")
    for d in secilen_duraklar:
        with st.expander(f"📍 {d['isim']} Detayları", expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                # Görsel arama mantığı
                foto_yolu = BASE_DIR / d['foto']
                if foto_yolu.exists():
                    st.image(str(foto_yolu), use_container_width=True)
                else:
                    try:
                        st.image(d['foto'], use_container_width=True)
                    except:
                        st.warning(f"🖼️ {d['foto']} GitHub'da bulunamadı.")
            with col2:
                st.subheader(d['isim'])
                st.info(f"⏱️ **Süre:** {d['sure']} | 🚌 **Ulaşım:** {d['mod']}")
                st.write(f"🎭 **Aktivite:** {d['aktivite']}")

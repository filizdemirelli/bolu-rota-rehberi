import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Sayfa ve Harita Ayarları
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Veri Seti (Koordinatlar Navigasyon İçin Sabitlendi)
duraklar = [
    {
        "isim": "Şehir Oteli", 
        "enlem": 40.7325, "boylam": 31.6082, 
        "foto": "otel.jpg", "sure": "Başlangıç", "mod": "Yaya 🚶", 
        "aktivite": "Konaklama ve Bilgilendirme"
    },
    {
        "isim": "Gölcük Tabiat Parkı", 
        "enlem": 40.6552, "boylam": 31.6255, 
        "foto": "golcuk_bolu.jpg", "sure": "20 dk", "mod": "Eko-Otobüs 🚌", 
        "aktivite": "Doğa Yürüyüşü ve Rekreasyon"
    },
    {
        "isim": "Sarıalan Yaylası", 
        "enlem": 40.6120, "boylam": 31.6500, 
        "foto": "sarialan.jpg", "sure": "15 dk", "mod": "Minibüs 🚐", 
        "aktivite": "Yayla Gastronomisi"
    },
    {
        "isim": "Aladağ Yaylaları", 
        "enlem": 40.5850, "boylam": 31.6350, 
        "foto": "aladag.jpg", "sure": "10 dk", "mod": "Bisiklet 🚲", 
        "aktivite": "Kamp ve Macera Turizmi"
    }
]

# Google Haritalar Koordinat Bazlı Rota Linki
nav_link = "https://maps.google.com/?cid=2839309371406536670&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ5"

# 3. Giriş Kontrolü
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1000", use_container_width=True)
        st.markdown("<h1 style='text-align: center; color: #2E7D32;'>Bolu Rota Rehberine Hoş Geldiniz</h1>", unsafe_allow_html=True)
        if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
            st.session_state.giris_yapildi = True
            st.rerun()
else:
    # 4. Ana Panel
    st.title("📍 Ekolojik Koridor Tur Rotası")
    
    # Navigasyon Butonu (Sidebar)
    st.sidebar.markdown(
        f"""
        <a href="{nav_link}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#D32F2F; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold; cursor:pointer; margin-bottom:20px;">
                🚗 GERÇEK TUR ROTASINI BAŞLAT
            </div>
        </a>
        """, 
        unsafe_allow_html=True
    )
    
    if st.sidebar.button("⬅️ Giriş Ekranına Dön"):
        st.session_state.giris_yapildi = False
        st.rerun()

    # Harita Çizimi
    df = pd.DataFrame(duraklar)
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in duraklar]
    
    path_layer = pdk.Layer(
        "PathLayer", 
        pd.DataFrame([{"path": yol_noktalari}]), 
        get_path="path", 
        get_color=[211, 47, 47, 200], 
        width_scale=20, 
        width_min_pixels=3
    )
    
    point_layer = pdk.Layer(
        "ScatterplotLayer", 
        df, 
        get_position="[boylam, enlem]", 
        get_color=[46, 125, 50], 
        get_radius=250,
        pickable=True
    )

    st.pydeck_chart(pdk.Deck(
        map_style="light", 
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.62, zoom=10.5), 
        layers=[path_layer, point_layer],
        tooltip={"text": "{isim}"}
    ))

    # 5. Durak Detayları
    st.markdown("---")
    for d in duraklar:
        with st.expander(f"📍 {d['isim']} Detayları", expanded=True):
            col_img, col_txt = st.columns([1, 1.5])
            with col_img:
                # Fotoğraf yolu kontrolü
                foto_yolu = d['foto']
                if not os.path.exists(foto_yolu):
                    foto_yolu = f"./{foto_yolu}"
                
                if os.path.exists(foto_yolu):
                    st.image(foto_yolu, use_container_width=True)
                else:
                    st.warning(f"🖼️ {d['foto']} bulunamadı.")
            with col_txt:
                st.subheader(d['isim'])
                st.write(f"⏱️ **Süre:** {d['sure']}")
                st.write(f"🚌 **Ulaşım Modu:** {d['mod']}")
                st.write(f"🎭 **Aktivite:** {d['aktivite']}")

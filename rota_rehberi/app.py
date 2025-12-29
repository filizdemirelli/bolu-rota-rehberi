import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Sayfa ve Harita Ayarları 🎨
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Zengin Veri Seti 📋
rotalar = {
    "Ekolojik Koridor": {
        "navigasyon_linki": "https://www.google.com/maps/dir/40.732,31.608/40.655,31.625/40.612,31.650/40.585,31.635",
        "duraklar": [
            {"isim": "Şehir Oteli", "enlem": 40.732, "boylam": 31.608, "foto": "otel.jpg", "sure": "0 dk", "ulasim": "Başlangıç 🏨", "aktivite": "Konaklama ve Bilgilendirme."},
            {"isim": "Bolu Gölcük Tabiat Parkı", "enlem": 40.655, "boylam": 31.625, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "ulasim": "Eko-Otobüs 🚌", "aktivite": "Doğa yürüyüşü ve Manzara seyri."},
            {"isim": "Sarıalan Yaylası", "enlem": 40.612, "boylam": 31.650, "foto": "sarialan.jpg", "sure": "15 dk", "ulasim": "Minibüs 🚐", "aktivite": "Yayla kültürü ve Gastronomi."},
            {"isim": "Aladağ Yaylaları", "enlem": 40.585, "boylam": 31.635, "foto": "aladag.jpg", "sure": "10 dk", "ulasim": "Bisiklet 🚲", "aktivite": "Kamp alanı ve Macera turizmi."}
        ]
    }
}

# 3. Giriş Sistemi 🚪
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
    # 4. Ana Sayfa ve Harita 🗺️
    st.title("📍 Tematik Koridorlar ve Yeni Odaklar")
    
    # Sidebar Navigasyon Butonu
    st.sidebar.markdown("---")
    st.sidebar.markdown(f'<a href="{rotalar["Ekolojik Koridor"]["navigasyon_linki"]}" target="_blank" style="text-decoration: none;"><button style="width: 100%; cursor: pointer; background-color: #D32F2F; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold;">NAVİGASYONU BAŞLAT</button></a>', unsafe_allow_html=True)
    
    if st.sidebar.button("⬅️ Giriş Ekranına Dön"):
        st.session_state.giris_yapildi = False
        st.rerun()

    # Rota Çizgisi ve Katmanlar
    df = pd.DataFrame(rotalar["Ekolojik Koridor"]["duraklar"])
    yol_noktalari = [[d["boylam"], d["enlem"]] for d in rotalar["Ekolojik Koridor"]["duraklar"]]
    
    path_layer = pdk.Layer("PathLayer", pd.DataFrame([{"path": yol_noktalari}]), get_path="path", get_color=[211, 47, 47, 200], width_scale=20, width_min_pixels=3)
    point_layer = pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[46, 125, 50], get_radius=250)

    st.pydeck_chart(pdk.Deck(map_style="light", initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.62, zoom=11), layers=[path_layer, point_layer]))

    # 5. Durak Detayları 📸
    st.markdown("### 🔍 Durak ve Ulaşım Detayları")
    for durak in rotalar["Ekolojik Koridor"]["duraklar"]:
        with st.expander(f"📍 {durak['isim']}", expanded=True):
            col_img, col_txt = st.columns([1, 1.5])
            with col_img:
                foto_adi = durak['foto']
                # Fotoğrafı hem doğrudan hem de ./ ile aramayı deneyelim
                if os.path.exists(foto_adi):
                    st.image(foto_adi, use_container_width=True)
                elif os.path.exists(f"./{foto_adi}"):
                    st.image(f"./{foto_adi}", use_container_width=True)
                else:
                    st.warning(f"🖼️ {foto_adi} bulunamadı.")
            with col_txt:
                st.subheader(durak['isim'])
                st.write(f"⏱️ **Ulaşım Süresi:** {durak['sure']}")
                st.write(f"🚌 **Ulaşım Modu:** {durak['ulasim']}")
                st.write(f"🎭 **Aktivite:** {durak['aktivite']}")

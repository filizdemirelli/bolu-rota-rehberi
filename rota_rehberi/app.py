import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# Sayfa ayarları
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")

# Harita altlığı ayarı (Siyah ekranı önler)
pdk.settings.map_provider = "carto"

# Rota Verileri
rotalar = {
    "Ekolojik Koridor": {
        "aciklama": "Bolu Merkez'den Gölcük ve Aladağlar'a uzanan sürdürülebilir turizm aksı.",
        "navigasyon_linki": "https://www.google.com/maps/dir/Bolu+City+Hotel/G%C3%B6lc%C3%BCk+Tabiat+Park%C4%B1/Sar%C4%B1alan+Yaylas%C4%B1/Alada%C4%9F+Yaylalar%C4%B1",
        "duraklar": [
            {"isim": "Şehir Oteli", "enlem": 40.732, "boylam": 31.608, "foto": "otel.jpg", "sure": "0 dk", "ulasim": "Başlangıç 🏨", "aktivite": "Konaklama ve Bilgilendirme."},
            {"isim": "Bolu Gölcük Tabiat Parkı", "enlem": 40.655, "boylam": 31.625, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "ulasim": "Eko-Otobüs 🚌", "aktivite": "Doğa yürüyüşü."},
            {"isim": "Sarıalan Yaylası", "enlem": 40.612, "boylam": 31.650, "foto": "sarialan.jpg", "sure": "15 dk", "ulasim": "Minibüs 🚐", "aktivite": "Yayla kültürü."},
            {"isim": "Aladağ Yaylaları", "enlem": 40.585, "boylam": 31.635, "foto": "aladag.jpg", "sure": "10 dk", "ulasim": "Bisiklet 🚲", "aktivite": "Kamp alanı."}
        ]
    }
}

# Giriş kontrolü
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

# --- GİRİŞ EKRANI ---
if not st.session_state.giris_yapildi:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1000", use_container_width=True)
        st.markdown("<h1 style='text-align: center; color: #2E7D32;'>Bolu Rota Rehberine Hoş Geldiniz</h1>", unsafe_allow_html=True)
        if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
            st.session_state.giris_yapildi = True
            st.rerun()

# --- ANA SAYFA ---
else:
    st.title("📍 Tematik Koridorlar ve Yeni Odaklar")
    rota_secimi = st.sidebar.selectbox("Bir rota seçiniz:", list(rotalar.keys()))
    
    # Gerçek Navigasyon Butonu (Yolları takip eden link)
    st.sidebar.markdown("---")
    st.sidebar.write("🛣️ **Gerçek Yol Navigasyonu**")
    st.sidebar.markdown(f'<a href="{rotalar[rota_secimi]["navigasyon_linki"]}" target="_blank" style="text-decoration: none;"><button style="width: 100%; cursor: pointer; background-color: #2E7D32; color: white; border: none; padding: 10px; border-radius: 5px;">NAVİGASYONU BAŞLAT</button></a>', unsafe_allow_html=True)

    # Harita Katmanları
    df_duraklar = pd.DataFrame(rotalar[rota_secimi]["duraklar"])
    layer_points = pdk.Layer("ScatterplotLayer", df_duraklar, get_position="[boylam, enlem]", get_color=[0, 100, 255], get_radius=150, pickable=True)

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11", 
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.63, zoom=11),
        layers=[layer_points]
    ))

    # Durak Detayları
    st.markdown("### 📸 Durak Detayları")
    for durak in rotalar[rota_secimi]["duraklar"]:
        with st.expander(f"📍 {durak['isim']}", expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                # Fotoğraf kontrolü
                foto_adi = durak['foto']
                if os.path.exists(foto_adi):
                    st.image(foto_adi, use_container_width=True)
                else:
                    st.warning(f"🖼️ {foto_adi} bulunamadı.")
            with col2:
                st.write(f"**Ulaşım:** {durak['ulasim']} | **Süre:** {durak['sure']}")
                st.write(f"**Aktivite:** {durak['aktivite']}")

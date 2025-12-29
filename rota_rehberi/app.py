import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# 1. Sayfa Ayarları
st.set_page_config(page_title="Bolu Rota Rehberi", layout="wide")
pdk.settings.map_provider = "carto"

# 2. Rota Verileri (Duraklar ve Bilgiler)
rotalar = {
    "Ekolojik Koridor": {
        "aciklama": "Bolu Merkez'den Gölcük ve Aladağlar'a uzanan sürdürülebilir turizm aksı.",
        "navigasyon_linki": "https://www.google.com/maps/dir/Bolu+City+Hotel/Gölcük+Tabiat+Parkı/Sarıalan+Yaylası/Aladağlar",
        "duraklar": [
            {"isim": "Şehir Oteli", "enlem": 40.732, "boylam": 31.608, "foto": "otel.jpg", "sure": "0 dk", "ulasim": "Başlangıç 🏨", "aktivite": "Konaklama ve Bilgilendirme."},
            {"isim": "Bolu Gölcük Tabiat Parkı", "enlem": 40.655, "boylam": 31.625, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "ulasim": "Eko-Otobüs 🚌", "aktivite": "Doğa yürüyüşü."},
            {"isim": "Sarıalan Yaylası", "enlem": 40.612, "boylam": 31.650, "foto": "sarialan.jpg", "sure": "15 dk", "ulasim": "Minibüs 🚐", "aktivite": "Yayla kültürü."},
            {"isim": "Aladağ Yaylaları", "enlem": 40.585, "boylam": 31.635, "foto": "aladag.jpg", "sure": "10 dk", "ulasim": "Bisiklet 🚲", "aktivite": "Kamp alanı."}
        ]
    }
}

# 3. Giriş Kontrolü
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

# --- KARŞILAMA EKRANI ---
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
    
    # Profesyonel Navigasyon Butonu
    st.sidebar.markdown("---")
    st.sidebar.write("🛣️ **Gerçek Yol Navigasyonu**")
    st.sidebar.markdown(f'<a href="{rotalar[rota_secimi]["navigasyon_linki"]}" target="_blank" style="text-decoration: none;"><button style="width: 100%; cursor: pointer; background-color: #2E7D32; color: white; border: none; padding: 10px; border-radius: 5px;">NAVİGASYONU BAŞLAT</button></a>', unsafe_allow_html=True)
    # 4. Estetik Rota Çizgisi (Path)
    # Bu noktalar yolları biraz daha kavisli takip edecek şekilde artırıldı
    yol_noktalari = [
        [31.608, 40.732], [31.612, 40.725], [31.625, 40.710], 
        [31.628, 40.690], [31.630, 40.670], [31.625, 40.655], 
        [31.640, 40.635], [31.650, 40.612], [31.645, 40.600], [31.635, 40.585]
    ]

    path_layer = pdk.Layer(
        "PathLayer",
        pd.DataFrame([{"path": yol_noktalari}]),
        get_path="path",
        get_color=[255, 75, 75, 200], # Estetik Kırmızı
        width_scale=20,
        width_min_pixels=3,
        rounded=True
    )

    # Durak Noktaları
    point_layer = pdk.Layer(
        "ScatterplotLayer",
        pd.DataFrame(rotalar[rota_secimi]["duraklar"]),
        get_position="[boylam, enlem]",
        get_color=[30, 130, 70],
        get_radius=200,
        pickable=True
    )

    # Harita Görüntüsü
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state=pdk.ViewState(latitude=40.66, longitude=31.63, zoom=11),
        layers=[path_layer, point_layer]
    ))

    # 5. Durak Detayları ve Fotoğraflar
    st.markdown("### 📸 Durak Detayları")
    for durak in rotalar[rota_secimi]["duraklar"]:
        with st.expander(f"📍 {durak['isim']}", expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                # Fotoğrafı her yerde arayan akıllı sistem
                foto = durak['foto']
                yollar = [foto, f"./{foto}", f"rota_rehberi/{foto}"]
                bulundu = False
                for y in yollar:
                    if os.path.exists(y):
                        st.image(y, use_container_width=True)
                        bulundu = True
                        break
                if not bulundu:
                    st.warning(f"🖼️ {foto} yüklenemedi.")
            with col2:
                st.write(f"**Ulaşım:** {durak['ulasim']} | **Süre:** {durak['sure']}")
                st.write(f"**Aktivite:** {durak['aktivite']}")


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
    "Ekolojik Koridor (Yaylalar)": [
        {"isim": "Şehir Oteli", "enlem": 40.7325, "boylam": 31.6082, "foto": "otel.jpg", "sure": "Başlangıç", "mod": "Yaya", "aktivite": "Şehrin kalbinde, konforun ve modernizmin buluştuğu noktada keşfe hazırlanın."},
        {"isim": "Gölcük Tabiat Parkı", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 dk", "mod": "Elektrikli Otobüs", "aktivite": "Yansımaların büyüsüne kapılacağınız bu durakta, doğanın sessizliğini dinleyin."},
        {"isim": "Sarıalan Yaylası", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan.jpg", "sure": "15 dk", "mod": "Minibüs", "aktivite": "Yerel lezzetlerin izini sürerken, geleneksel yayla yaşamının modern sunumuna tanıklık edin."},
        {"isim": "Aladağ Yaylaları", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "10 dk", "mod": "Bisiklet", "aktivite": "Sınırları zorlayan bir macera ve yıldızlar altında kusursuz bir kamp deneyimi sizi bekliyor."}
    ],
    "Kış Turizmi (Kartalkaya)": [
        {"isim": "Bolu Merkez", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "Başlangıç", "mod": "VIP Transfer", "aktivite": "Bolu'nun kış masalı için stratejik bir başlangıç ve son hazırlık noktası."},
        {"isim": "Kındıra Yaylası", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 dk", "mod": "4x4 Araç", "aktivite": "Karlar altında saklı bir köy kahvaltısı ile güne enerjik ve otantik bir başlangıç yapın."},
        {"isim": "Sarıalan (Kış Senaryosu)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 dk", "mod": "4x4 Araç", "aktivite": "Bembeyaz bir tuval üzerinde, doğanın kış estetiğini ölümsüzleştireceğiniz fotoğraf rotası."},
        {"isim": "Kartalkaya Kayak Merkezi", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "20 dk", "mod": "Kar Aracı", "aktivite": "Zirvede adrenalin ve lüksün buluştuğu noktada, kış sporlarının keyfini sürün."}
    ]
}

# 3. Giriş Sistemi
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590059393164-904c632616f9?q=80&w=1200", use_container_width=True)
    st.title("BOLU TEMATIK ROTA REHBERI")
    st.markdown("### Doğanın kalbinde size özel bir deneyim tasarladık.")
    
    # Estetik Buton Tasarımı
    if st.button

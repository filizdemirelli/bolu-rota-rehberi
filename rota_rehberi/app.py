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

# 2. PREMIUM CSS: BEYAZ YAZI VE PASTEL YEŞİL DENGESİ
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp, [data-testid="stSidebar"], .stSidebarNav {
        background-color: #E8F5E9 !important;
    }

    /* TÜM BUTONLAR: KOYU YEŞİL ZEMİN ÜZERİNE BEYAZ YAZI */
    div.stButton > button {
        background-color: #1B5E20 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        padding: 18px !important;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease;
    }

    /* Buton Yazılarını Beyaza Zorla */
    div.stButton > button p, 
    div.stButton > button span, 
    div.stButton > button div {
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        font-size: 22px !important;
        letter-spacing: 1px;
    }

    /* Panel Tasarımları */
    .streamlit-expanderHeader {
        background-color: #C8E6C9 !important;
        color: #1B5E20 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    /* Navigasyon Link Butonu */
    .nav-btn-link {
        display: block;
        padding: 15px;
        background-color: #1B5E20;
        color: #FFFFFF !important;
        text-align: center;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 900;
        font-size: 18px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 3. ZENGİNLEŞTİRİLMİŞ ROTA VERİLERİ
rotalar = {
    "KUZEY ORMANLARI VE YEDİGÖLLER": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP ARAÇ", 
         "aktivite": "Kuzeyin gizemli ormanlarına yolculuk için tüm hazırlıklar tamamlanıyor. Bolu'nun modern yüzünden doğanın kalbine uzanan köprünün ilk basamağı."},
        {"isim": "YAZIÖREN YAYLASI", "enlem": 40.8200, "boylam": 31.6500, "foto": "yazioren.jpg", "sure": "25 DK", "mod": "OFF-ROAD ARAÇ", 
         "aktivite": "Kuzey rotasının ilk nefes durağı. Geleneksel yayla mimarisinin çam kokularıyla harmanlandığı, zamanın yavaş aktığı bir sığınak. Burada yerel halkın sunduğu taze bitki çaylarını deneyimleyebilirsiniz."},
        {"isim": "AYI KAYASI YAYLASI", "enlem": 40.8800, "boylam": 31.7200, "foto": "ayikayasi.jpg", "sure": "20 DK", "mod": "TREKKING / YÜRÜYÜŞ", 
         "aktivite": "Yedigöller yolu üzerinde, vahşi yaşamın izlerini sürebileceğiniz sarp kayalıklar. Seyir terasından aşağı baktığınızda, Bolu'nun uçsuz bucaksız orman denizini tüm ihtişamıyla göreceksiniz."},
        {"isim": "PİSİS YAYLASI", "enlem": 40.9100, "boylam": 31.7400, "foto": "pisis.jpg", "sure": "10 DK", "mod": "DOĞA YÜRÜYÜŞÜ", 
         "aktivite": "Milli parkın kapı komşusu olan bu bakir yaylada, endemik bitki türlerini inceleyebilir ve su kaynaklarının doğallığına tanıklık edebilirsiniz."},
        {"isim": "YEDİGÖLLER MİLLİ PARKI", "enlem": 40.9415, "boylam": 31.7483, "foto": "yedigoller.jpg", "sure": "15 DK", "mod": "EKOLOJİK KAMP", 
         "aktivite": "Büyükgöl, Sazlıgöl ve diğerleri... Doğanın en görkemli renk paletine sahip olan bu bölgede, kuş sesleri eşliğinde kamp kurup huzurun zirvesine ulaşacaksınız."}
    ],
    "KIŞ TURİZMİ (KARTALKAYA HATTI)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "VIP TRANSFER", 
         "aktivite": "Kar macerası için özel transfer araçlarımızla buluşma noktası. Soğuk havaya inat, sıcak bir karşılama ile kış masalı başlıyor."},
        {"isim": "KINDIRA KÖYÜ", "enlem": 40.6850, "boylam": 31.7550, "foto": "kindira.jpg", "sure": "25 DK", "mod": "4x4 KAR ARACI", 
         "aktivite": "Karlar altında saklı bir cennet. Geleneksel köy evlerinde, yanan sobanın çıtırtısı eşliğinde, Bolu'nun meşhur ürünleriyle donatılmış bir köy kahvaltısı sizi bekliyor."},
        {"isim": "SARIALAN YAYLASI (KIŞ)", "enlem": 40.6120, "boylam": 31.6500, "foto": "sarialan_kis.jpg", "sure": "15 DK", "mod": "4x4 KAR ARACI", 
         "aktivite": "Donmuş göletlerin ve bembeyaz bir örtüyle kaplanan çam ağaçlarının yarattığı estetik şölen. Fotoğraf tutkunları için benzersiz kadrajlar sunan bir kış rüyası."},
        {"isim": "KARTALKAYA KAYAK MERKEZİ", "enlem": 40.6010, "boylam": 31.7950, "foto": "kartalkaya.jpg", "sure": "10 DK", "mod": "KAYAK / SNOWBOARD", 
         "aktivite": "Köroğlu Dağları'nın zirvesinde, adrenalin ve lüksün buluştuğu nokta. Pistlerde geçen aktif bir günün ardından şömine başında günün yorgunluğunu atın."}
    ],
    "GÜNEY EKOLOJİK KORİDOR (GÖLCÜK HATTI)": [
        {"isim": "BOLU MERKEZ", "enlem": 40.7350, "boylam": 31.6050, "foto": "merkez.jpg", "sure": "BAŞLANGIÇ", "mod": "ELEKTRİKLİ ARAÇ", 
         "aktivite": "Sürdürülebilir turizm ilkeleriyle hazırlanan rotamızda, doğaya en az iz bırakacak şekilde yolculuğumuza başlıyoruz."},
        {"isim": "GÖLCÜK TABİAT PARKI", "enlem": 40.6552, "boylam": 31.6255, "foto": "golcuk_bolu.jpg", "sure": "20 DK", "mod": "YÜRÜYÜŞ", 
         "aktivite": "Bolu'nun kartpostalları süsleyen simge yapısı. Göl etrafında yapacağınız yürüyüşte her mevsim ayrı bir renk cümbüşüne tanıklık edecek, ciğerlerinize temiz hava dolduracaksınız."},
        {"isim": "ALADAĞ YAYLALARI", "enlem": 40.5850, "boylam": 31.6350, "foto": "aladag.jpg", "sure": "30 DK", "mod": "KAMP / BİSİKLET", 
         "aktivite": "Derin vadiler ve yüksek platolar... Macera tutkunları için tasarlanan bu durakta, doğanın tam ortasında kamp kurup sessizliğin sesini dinleyeceksiniz."}
    ]
}

# 4. Uygulama Akışı
if 'giris' not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    # Giriş Görseli
    giris_resmi = BASE_DIR / "yedigoller_yeni.jpg"
    if giris_resmi.exists():
        st.image(str(giris_resmi), use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1570737197686-3974274c7d83?q=80&w=1200", use_container_width=True)
    
    st.title("BOLU TEMATİK ROTA REHBERİ")
    if st.button("KEŞFETMEYE BAŞLA", use_container_width=True):
        st.session_state.giris = True
        st.rerun()
else:
    # Sidebar
    st.sidebar.title("NAVİGASYON")
    secilen_rota = st.sidebar.selectbox("BİR DENEYİM SEÇİN", list(rotalar.keys()))
    duraklar = rotalar[secilen_rota]
    
    # Navigasyon Linki
    start, end = duraklar[0], duraklar[-1]
    g_url = f"https://www.google.com/maps/dir/{start['enlem']},{start['boylam']}/{end['enlem']},{end['boylam']}"
    st.sidebar.markdown(f'<a href="{g_url}" target="_blank" class="nav-btn-link">NAVİGASYONU BAŞLAT</a>', unsafe_allow_html=True)
    
    if st.sidebar.button("GİRİŞ EKRANINA DÖN"):
        st.session_state.giris = False
        st.rerun()

    st.title(secilen_rota)

    # 5. Harita
    df = pd.DataFrame(duraklar)
    st.pydeck_chart(pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(latitude=df['enlem'].mean(), longitude=df['boylam'].mean(), zoom=10),
        layers=[
            pdk.Layer("PathLayer", pd.DataFrame([{"path": [[d["boylam"], d["enlem"]] for d in duraklar]}]), get_path="path", get_color=[46, 125, 50], width_scale=20),
            pdk.Layer("ScatterplotLayer", df, get_position="[boylam, enlem]", get_color=[27, 94, 32], get_radius=400)
        ]
    ))

    # 6. Bilgi Kartları
    st.markdown("---")
    for d in duraklar:
        with st.expander(d['isim'], expanded=True):
            c1, c2 = st.columns([1, 1.5])
            with c1:
                f_yolu = BASE_DIR / d['foto']
                if f_yolu.exists():
                    st.image(str(f_yolu), use_container_width=True)
                else:
                    st.info(f"Görsel Bekleniyor: {d['foto']}")
            with c2:
                st.write(f"**ULAŞIM MODU:** {d['mod']}")
                st.write(f"**TAHMİNİ SÜRE:** {d['sure']}")
                st.write(f"**DENEYİM DETAYI:** {d['aktivite']}")

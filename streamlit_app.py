import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.title("🏗️ Endüstriyel Poz Okuyucu")
st.write("Cihaz kamerasından fotoğrafı çekin, AI pozu okusun.")

@st.cache_resource
def load_model():
    # Model yüklenirken bekletir
    return easyocr.Reader(['en'], gpu=False)

reader = load_model()

# Kamerayı açan buton ve yükleme alanı
img_file = st.camera_input("Pozu çek") # Bu direkt telefonun kamerasını açar

if img_file is not None:
    image = Image.open(img_file)
    img_array = np.array(image)
    
    with st.spinner('Karakterler analiz ediliyor...'):
        results = reader.readtext(img_array)
        
    if results:
        st.subheader("Okunan Poz Numaraları:")
        for (bbox, text, prob) in results:
            if prob > 0.3: # %30'dan yüksek ihtimalleri göster
                st.success(f"**{text}** (Güven: %{int(prob*100)})")
    else:
        st.warning("Poz bulunamadı, lütfen daha yakından çekin.")

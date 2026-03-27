import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="지도 데모", page_icon="🌍")

st.title('🌍 지도 데모')

st.write('서울 주변 랜덤 위치 100개를 지도에 표시합니다.')

np.random.seed(42)
map_data = pd.DataFrame({
    'lat': np.random.uniform(37.4, 37.7, 100),
    'lon': np.random.uniform(126.8, 127.1, 100)
})

st.map(map_data)

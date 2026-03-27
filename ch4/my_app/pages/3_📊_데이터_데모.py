import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="데이터 데모", page_icon="📊")

st.title('📊 데이터 데모')

np.random.seed(42)
df = pd.DataFrame({
    '이름': [f'항목_{i}' for i in range(1, 21)],
    '값A': np.random.randint(0, 100, 20),
    '값B': np.random.uniform(0, 1, 20).round(3),
    '카테고리': np.random.choice(['X', 'Y', 'Z'], 20)
})

st.subheader('인터랙티브 데이터프레임')
st.dataframe(df, use_container_width=True)

with st.expander('기술통계 보기'):
    st.dataframe(df.describe())

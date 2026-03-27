import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="차트 데모", page_icon="📈")

st.title('📈 차트 데모')

np.random.seed(42)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

st.subheader('선 차트')
st.line_chart(chart_data)

st.subheader('바 차트')
st.bar_chart(chart_data)

st.subheader('영역 차트')
st.area_chart(chart_data)

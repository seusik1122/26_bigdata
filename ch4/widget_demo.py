# selectbox_demo.py
import streamlit as st 
import pandas as pd 
st.title('위젯 실습 - selectbox') 
# 선택지 만들기 
category = st.selectbox( 
'카테고리를 선택하세요', 
    ['전자제품', '의류', '식품', '도서'] 
) 
st.write(f'선택한 카테고리: **{category}**') 
# 선택에 따라 다른 데이터 표시 
data = { 
'전자제품': {'평균가격': '₩35만', '판매량': 150}, 
'의류':     {'평균가격': '₩5만',  '판매량': 320}, 
'식품':     {'평균가격': '₩1만',  '판매량': 890}, 
'도서':     {'평균가격': '₩2만',  '판매량': 210}, 
} 
info = data[category] 
st.write(f"평균 가격: {info['평균가격']}") 
st.write(f"월 판매량: {info['판매량']}개") 
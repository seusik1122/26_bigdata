import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='기초 EDA 대시보드', layout='wide')
st.title('기초 EDA 대시보드')

np.random.seed(42)
df = pd.DataFrame({
    '날짜': pd.date_range('2026-01-01', periods=100),
    '카테고리': np.random.choice(['전자제품', '의류', '식품'], 100),
    '매출': np.random.randint(100, 1000, 100),
    '고객수': np.random.randint(10, 200, 100),
    '전환율': np.random.uniform(0.01, 0.20, 100).round(4)
})

st.sidebar.header('필터')

selected_category = st.sidebar.selectbox(
    '카테고리 선택',
    ['전체'] + list(df['카테고리'].unique())
)

date_range = st.sidebar.date_input(
    '날짜 범위',
    value=(df['날짜'].min(), df['날짜'].max()),
    min_value=df['날짜'].min(),
    max_value=df['날짜'].max()
)

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered_df = filtered_df[(filtered_df['날짜'] >= start_date) & (filtered_df['날짜'] <= end_date)]

if selected_category != '전체':
    filtered_df = filtered_df[filtered_df['카테고리'] == selected_category]

st.sidebar.write('---')
st.sidebar.write(f'필터링된 데이터: **{len(filtered_df)}행**')

tab1, tab2, tab3 = st.tabs(['요약 대시보드', '원본 데이터', '카테고리별 비교'])

with tab1:
    if len(filtered_df) == 0:
        st.warning('데이터가 없습니다')
    else:
        st.subheader('핵심 지표')
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(
            label='총 매출',
            value=f"₩{filtered_df['매출'].sum():,}만",
            delta=f"{filtered_df['매출'].mean():.0f} (평균)"
        )
        kpi2.metric(
            label='총 고객수',
            value=f"{filtered_df['고객수'].sum():,}명",
            delta=f"{filtered_df['고객수'].mean():.0f} (평균)"
        )
        kpi3.metric(
            label='평균 전환율',
            value=f"{filtered_df['전환율'].mean():.2%}",
            delta=f"{filtered_df['전환율'].std():.2%} (표준편차)"
        )
        st.write('---')
        st.subheader('매출 추이')
        col_left, col_right = st.columns([2, 1])
        with col_left:
            chart_data = filtered_df.groupby('날짜')['매출'].sum().reset_index().set_index('날짜')
            st.line_chart(chart_data)
        with col_right:
            bar_data = filtered_df.groupby('카테고리')['매출'].sum().reset_index().set_index('카테고리')
            st.bar_chart(bar_data)

with tab2:
    if len(filtered_df) == 0:
        st.warning('데이터가 없습니다')
    else:
        st.subheader('필터링된 원본 데이터')
        st.write(f'총 **{len(filtered_df)}건**의 데이터')
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )
        with st.expander('기술통계 보기'):
            st.dataframe(filtered_df.describe())
        st.download_button(
            label='CSV 다운로드',
            data=filtered_df.to_csv(index=False).encode('utf-8-sig'),
            file_name='filtered_data.csv',
            mime='text/csv'
        )

with tab3:
    if len(filtered_df) == 0:
        st.warning('데이터가 없습니다')
    else:
        st.subheader('카테고리별 평균 매출 비교')
        category_avg = filtered_df.groupby('카테고리')['매출'].mean().reset_index().set_index('카테고리')
        st.bar_chart(category_avg)

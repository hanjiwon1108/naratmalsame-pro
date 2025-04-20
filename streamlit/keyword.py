import streamlit as st
import pandas as pd

from pytrends.request import TrendReq
import altair as alt
from streamlit_tags import st_tags

pytrends = TrendReq(hl='ko-KR', tz=1260)

st.title("🇰🇷 키워드 검색")

with st.form("keyword_form"):
  keyword_input = (st_tags(
    label="키워드 입력",
    text="키워드를 입력하세요",
    key="keyword_input",
  ))
  isTest = st.checkbox("테스트 모드", value=True)
  submitted = st.form_submit_button("검색")

  if submitted:
    st.write(f"검색된 키워드: {keyword_input}")
    if isTest:
      st.write("테스트 모드가 활성화되었습니다.")
      df = pd.read_csv("2025-04-20T05-05_export.csv",
                       encoding='utf-8', header=0)
    else:
      pytrends.build_payload(kw_list=keyword_input,
                             timeframe='today 1-m', geo='KR')
      df = pytrends.interest_over_time()
    st.write("검색량 데이터")
    st.dataframe(df)
    # 데이터프레임을 melt하여 'date', 'keyword', 'value' 컬럼으로 변환
    df_reset = df.reset_index()
    df_melted = df_reset.melt(id_vars=['date'], value_vars=keyword_input,
                              var_name='keyword', value_name='value')

    def chart(symbol, color): return alt.Chart(df_melted).transform_filter(
      alt.datum.keyword == symbol
    ).mark_area(
      point={
        'shape': 'circle',
        'size': 40,
        'color': color,
      },
      interpolate='cardinal',
      line={'color': color},
      opacity=0.5,
      color=alt.Gradient(
        gradient='linear',
        stops=[
          alt.GradientStop(color='transparent', offset=0),
          alt.GradientStop(color=color, offset=1)
        ],
        x1=1,
        x2=1,
        y1=1,
        y2=0,
      ),
    ).encode(
      x='date:T',
      y=alt.Y('value:Q'),
    )

    layeredChart = alt.layer(
      *[chart(keyword, color) for keyword, color in zip(keyword_input,
                                                        ["skyblue", "lightcoral", "lightgreen", "lightpink", "lightyellow"])],
    ).configure_legend(
      orient="top",
    ).interactive(
      bind_x=True,
      bind_y=False,
    )
    st.altair_chart(layeredChart, use_container_width=True)

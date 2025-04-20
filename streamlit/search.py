import pandas as pd
import altair as alt
import streamlit as st


st.title("🇰🇷 순화 사례 검색")
data = pd.read_csv("searched.csv", encoding='utf-8', header=0)


with st.form("search_form"):
  cols = st.columns([5, 1, 1], vertical_alignment="bottom")
  name = cols[0].text_input("검색", placeholder="검색어를 입력하세요")
  # pro = cols[1].toggle("Pro")
  submitted = cols[2].form_submit_button("검색")

  if submitted:

    filtered_data = data[
      data['원어'].astype(str).apply(lambda x: name in x) |
      data['다듬을 말'].astype(str).apply(lambda x: name in x) |
      data['다듬은 말'].astype(str).apply(lambda x: name in x) |
      data['의미/용례'].astype(str).apply(lambda x: name in x)
    ]
    cols1 = st.columns([1, 1, 1])
    cols1[0].write(f"검색어: {name}")
    cols1[1].write(f"검색 결과: {len(filtered_data)}")
    # cols1[2].write(f"Pro: {pro}")

    display_data = filtered_data.copy()
    display_data['다듬은 말 검색량 비율'] = display_data.apply(
      lambda row: round(row['다듬은말_검색량'] / (row['원어_검색량'] + row['다듬은말_검색량']) if row['원어_검색량'] + row['다듬은말_검색량'] != 0 else 0, 3), axis=1,
    )
    display_data['선호도 점수'] = display_data.apply(
      lambda row: row['검색량_가산점'] + row['제출 점수'], axis=1,
    )
    # Display the filtered dataframe with clickable rows
    selected_idx = st.dataframe(
      display_data.reset_index(drop=True),
      key="원어",
      use_container_width=True,
      hide_index=True,
      on_select="rerun",
      selection_mode=["multi-row"],
      column_config={
        '제출 점수': st.column_config.ProgressColumn(
          '제출 점수', width='small',
          format="%d",
          min_value=1,
          max_value=5
        ),
        '다듬은 말 검색량 비율': st.column_config.ProgressColumn(
          '다듬은 말 검색량 비율', width='medium',
        ),
        '선호도 점수': st.column_config.ProgressColumn(
          '선호도 점수', width='small',
          format="%d",
          min_value=-1,
          max_value=9
        ),
      },
      height=700,
    )
    # selected_idx.selection

    # Prepare data for chart
    chart_data = filtered_data[['원어_검색량', '다듬은말_검색량']].copy()
    chart_data['index'] = filtered_data.index
    # selected_idx.selection.rows 내부 index 목록 데이터만 필터
    if selected_idx.selection.rows:
      selected_rows = selected_idx.selection.rows
      chart_data = chart_data[chart_data['index'].isin(selected_rows)]

    # Melt data for Altair
    chart_data = chart_data.melt(
      id_vars=['index'], var_name='검색량종류', value_name='검색량')

    selection = alt.selection_interval(bind='scales')

    chart = alt.Chart(chart_data).mark_bar().encode(
      y='검색량:Q',
      x='다듬을 말:O',
      color='검색량종류:N',
      tooltip=[
          alt.Tooltip('검색량종류:N', title='종류'),
          alt.Tooltip('검색량:Q', title='검색량'),
          alt.Tooltip('index:O', title='행 인덱스'),
          alt.Tooltip('다듬을 말:N', title='다듬을 말'),
          alt.Tooltip('다듬은 말:N', title='다듬은 말'),
      ]
    ).transform_lookup(
      lookup='index',
      from_=alt.LookupData(filtered_data.reset_index(),
                           'index', ['다듬을 말', '다듬은 말'])
    ).interactive(bind_x=True, bind_y=True).configure_legend(
      titleFontSize=14,
      labelFontSize=12,
      symbolSize=100,
      direction="horizontal",
      orient="top"
    )

    st.altair_chart(chart, use_container_width=True)

# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.express as px
import seaborn as sns

import geopandas as gpd
from shapely.geometry import Polygon
import folium
import base64
import pyproj
def transform_coordinates(x, y):
    epsg5181 = pyproj.CRS("EPSG:5181")
    wgs84 = pyproj.CRS("EPSG:4326")
    transformer = pyproj.Transformer.from_crs(epsg5181, wgs84, always_xy=True)
    longitude, latitude = transformer.transform(x, y)
    return f"{longitude}, {latitude}"

def run_geo_app():
    st.subheader("시각화 페이지")

    geo_data0 = gpd.read_file('data/geometry4.geojson', encoding='utf-8')
    geo_data0 = geo_data0.to_crs(epsg=4326)

    # 좌표 변환 적용하여 상권 중앙위경도 값 추가하고 float 튜플로 변환

    
    # 그냥 아예 lat, longi 칼럼 두개로 만들고 
    # 각 "lat, logi" 로 반환하는 for 반복문을 만들어보는 건 어떤지

    geo_data = geo_data0[geo_data0['SIGNGU_CD'] == '11680']
    
    # 메뉴지정
    submenu = st.sidebar.selectbox("submenu", ['통계', '지도'])
    if submenu == "통계":
        st.subheader("통계")
        st.write(geo_data)

    elif submenu == "지도":
    # 위도와 경도를 설정합니다.
        latitude = 37.517324
        longitude = 127.041203

        # folium 맵 생성
        m = folium.Map(location=[latitude, longitude],
                    zoom_start=14, 
                    width=750, 
                    height=500
                    )

        # GeoJSON 형식으로 변환합니다.
        polygon_geojson = geo_data['geometry'].__geo_interface__

        # Folium에 다각형을 추가합니다.
        folium.GeoJson(
            polygon_geojson,
            style_function=lambda x: {'fillColor': '#ffff00', 'color': '#000000'}
        ).add_to(m)

        # center_points 열을 이용하여 마커를 추가
        for index, row in geo_data.iterrows():
            latitude, longitude = row['center_points']
            popup_text = f"{row['TRDAR_SE_C']} Center"  # 팝업 텍스트
            tooltip_text = f"{row['TRDAR_SE_C']} path"  # 툴팁 텍스트
            
            folium.Marker([latitude, longitude],
                        popup=popup_text,
                        tooltip=tooltip_text).add_to(m)
            
        # folium 맵을 이미지로 저장
        m.save('map.html')

        # HTML 파일을 읽어 Base64로 변환
        with open('map.html', 'r') as f:
            html = f.read()
            b64 = base64.b64encode(html.encode()).decode()

        # Base64로 인코딩된 HTML을 출력
        st.markdown(f'<iframe src="data:text/html;base64,{b64}" width=750 height=500></iframe>', unsafe_allow_html=True)


    
    else:
        pass










"""

def run_geo_app():
    st.subheader("시각화 페이지")

    shp_df1 = pd.read_csv("data/2023상권영역/최종_재료_Seoul_Shp_Data.csv")
    shp_df = shp_df1[shp_df1['SIGNGU_CD'] == 11680]
    

    # 메뉴지정
    submenu = st.sidebar.selectbox("submenu", ['통계', '지도'])
    if submenu == "통계":
        st.subheader("통계")
        st.write(shp_df)

    elif submenu == "지도":
        # 위도
        latitude = 37.4974135
        # 경도
        longitude = 127.028008

        # 스트림릿 애플리케이션 시작
        st.title("지도 출력 예제")

        # folium 맵 생성
        m = folium.Map(location=[latitude, longitude],
                    zoom_start=15, 
                    width=750, 
                    height=500
                    )

        # folium 맵에 마커 추가
        folium.Marker([latitude, longitude], popup='Marker').add_to(m)

        # folium 맵을 이미지로 저장
        m.save('map.html')
    
        # HTML 파일을 읽어 Base64로 변환
        with open('map.html', 'r') as f:
            html = f.read()
            b64 = base64.b64encode(html.encode()).decode()

        # Base64로 인코딩된 HTML을 출력
        st.markdown(f'<iframe src="data:text/html;base64,{b64}" width=750 height=500></iframe>', unsafe_allow_html=True)
    else:
        pass
    
"""        
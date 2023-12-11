# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd

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
    return {'latitude': latitude, 'longitude': longitude}

def run_geo_app():
    st.subheader("상권 영역")
    st.markdown('마우스 커서의 위치에 따라 상권 이름이 보입니다.')


    geo_data0 = gpd.read_file('data/geometry4.geojson', encoding='utf-8')
    geo_data0 = geo_data0.to_crs(epsg=4326)

    # 변환된 좌표를 새로운 lat, longit 칼럼에 추가
    geo_data0[['latitude', 'longitude']] = geo_data0.apply(lambda row: pd.Series(transform_coordinates(row['XCNTS_VALU'], row['YDNTS_VALU'])), axis=1)    

    geo_data = geo_data0[geo_data0['SIGNGU_CD'] == '11680']

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

    # 각 위도,경도 열을 이용하여 마커를 추가
    for index, row in geo_data.iterrows():
        latitude = row['latitude']  # 'latitude' 열에서 값 가져오기
        longitude = row['longitude']  # 'longitude' 열에서 값 가져오기
        
        # popup_text = f"{row['TRDAR_CD_N']}"  # 팝업 텍스트
        # tooltip_text = f"{row['TRDAR_CD_N']}"  # 툴팁 텍스트
        # popup_text = f"{row['TRDAR_CD_N'].encode('utf-8').decode('utf-8')}"  # 팝업 텍스트
        tooltip_text = f"{row['TRDAR_CD_N'].encode('utf-8').decode('utf-8')}"  # 툴팁 텍스트

        folium.Marker([latitude, longitude],
                    # popup=popup_text, # 팝업 텍스트
                    tooltip=tooltip_text).add_to(m)
        
    # folium 맵을 이미지로 저장
    m.save('map.html')

    ## --------------------------------------------- 메인 텍스트 영역 -------------------------------------
    st.subheader('📊  강남구 편의점 매출 예측 서비스')
    st.markdown('###### 좌측 사이드바에서 상권과 분기를 선택하면, 시간대별 예상 매출을 확인하실 수 있습니다')
    st.caption('하단 지도에서 상권의 영역을 확인해보세요!👀')
    ##------------------------------------------------ 지도 영역 -------------------------------------------
    # HTML 파일을 읽어 Base64로 변환
    # with open('map.html', 'r') as f:
    # html = f.read()
    # b64 = base64.b64encode(html.encode()).decode()
    with open('map.html', 'r', encoding='utf-8') as f:
        html = f.read()
        b64 = base64.b64encode(html.encode()).decode()

    st.components.v1.html(html, height=600)
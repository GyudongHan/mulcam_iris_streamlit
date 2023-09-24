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
    st.subheader("시각화 페이지")

    geo_data0 = gpd.read_file('data/geometry4.geojson', encoding='utf-8')
    geo_data0 = geo_data0.to_crs(epsg=4326)

    # 변환된 좌표를 새로운 lat, longit 칼럼에 추가
    geo_data0[['latitude', 'longitude']] = geo_data0.apply(lambda row: pd.Series(transform_coordinates(row['XCNTS_VALU'], row['YDNTS_VALU'])), axis=1)    

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

        # 각 위도,경도 열을 이용하여 마커를 추가
        for index, row in geo_data.iterrows():
            latitude = row['latitude']  # 'latitude' 열에서 값 가져오기
            longitude = row['longitude']  # 'longitude' 열에서 값 가져오기
            
            # popup_text = f"{row['TRDAR_CD_N']}"  # 팝업 텍스트
            # tooltip_text = f"{row['TRDAR_CD_N']}"  # 툴팁 텍스트
            popup_text = f"{row['TRDAR_CD_N'].encode('utf-8').decode('utf-8')}"  # 팝업 텍스트
            tooltip_text = f"{row['TRDAR_CD_N'].encode('utf-8').decode('utf-8')}"  # 툴팁 텍스트

            folium.Marker([latitude, longitude],
                        popup=popup_text,
                        tooltip=tooltip_text).add_to(m)
            
        # folium 맵을 이미지로 저장
        m.save('map.html')

        # HTML 파일을 읽어 Base64로 변환
        # with open('map.html', 'r') as f:
        #     html = f.read()
        #     b64 = base64.b64encode(html.encode()).decode()
        with open('map.html', 'r', encoding='utf-8') as f:
            html = f.read()
            b64 = base64.b64encode(html.encode()).decode()


        # Base64로 인코딩된 HTML을 출력
        st.markdown(f'<iframe src="data:text/html;base64,{b64}" width=750 height=500></iframe>', unsafe_allow_html=True)


    
    else:
        pass
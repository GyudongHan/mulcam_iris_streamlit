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

def folium_static(fig, width=700, height=500):
            """
            Renders a folium map in Streamlit.
            """
            folium_tmp = "/tmp/folium.html"
            fig.save(folium_tmp)
            st.components.v1.html(open(folium_tmp, "r").read(), width=width, height=height)

def run_geo_app():
    st.subheader("시각화 페이지")

    shp_df1 = pd.read_csv("data/2023상권영역/최종_재료_Seoul_Shp_Data.csv")
    shp_df = shp_df1[shp_df1['SIGNGU_CD'] == 11680]
    shp_gdf = gpd.GeoDataFrame(shp_df, geometry=gpd.points_from_xy(shp_df.longitude, shp_df.latitude))

    # 메뉴지정
    submenu = st.sidebar.selectbox("submenu", ['통계', '지도'])
    if submenu == "통계":
        st.subheader("통계")
        st.write(shp_df)

    elif submenu == "지도":
        # Folium을 사용하여 지도 시각화
        m = folium.Map(location=[shp_df['geometry'].centroid.y.mean(), shp_df['geometry'].centroid.x.mean()], zoom_start=10)

        # 폴리곤 추가
        for _, row in shp_df.iterrows():
            folium.GeoJson(row['geometry']).add_to(m)

        # Folium 지도를 Streamlit에 표시
        folium_static(m)


    else:
        pass
    
# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

def run_eda_app():

    st.subheader("탐색적 자료 분석 페이지")
    st.subheader("잘 진행중...!")

    iris_df = pd.read_csv("data/iris.csv")

    st.dataframe(iris_df)
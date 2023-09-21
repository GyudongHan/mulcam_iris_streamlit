# -*- coding:utf-8 -*-

import streamlit as st
from eda_app import run_eda_app
from ml_app import run_ml_app
from geo_app import run_geo_app

def main():

    menu = ["Home", "탐색적 자료 분석", "머신러닝", "지도"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "Home":
        st.subheader("Home")
    elif choice == "탐색적 자료 분석":
        # st.subheader("탐색적 자료 분석")
        run_eda_app()
    elif choice == "머신러닝": 
        # st.subheader("머신러닝")
        run_ml_app()
    elif choice == "지도": 
        run_geo_app()    
    else:
        pass
    

if __name__ == "__main__":
    main()
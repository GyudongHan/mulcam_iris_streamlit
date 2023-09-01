# -*- coding:utf-8 -*-

import streamlit as st
import joblib
import os
import numpy as np

def run_ml_app():
    st.subheader("머신러닝 페이지")

    # layout
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("수치를 입력해주세요")
        sepal_length = st.select_slider("sepal Length", options = np.arange(1,11))
        sepal_width = st.select_slider("sepal_width", options = np.arange(1,11))
        petal_length = st.select_slider("petal Length", options = np.arange(1,11))
        petal_width = st.select_slider("petal_width", options = np.arange(1,11))

        sample_list = [sepal_length, sepal_width, petal_length, petal_width]
        st.write(sample_list)

    with col2:
        st.subheader("모델 결과를 확인해주세요")

        # 모델 불러오기
        model_file = "models/lgr_model_iris230331.pkl"
        model = joblib.load(open(os.path.join(model_file), "rb"))
        st.write(model)

        # 배열로 만듦
        one_sample = np.array(sample_list).reshape(1,-1)
        st.write(one_sample)
        st.write(one_sample.shape)

        # 범주 예측
        prediction = model.predict(one_sample)
        st.write(prediction)

        # 확률값 예측
        pred_prob = model.predict_proba(one_sample)
        st.write(pred_prob)
        
        if prediction == 0:
            st.success("Setosa 종")
            pred_proba_scores = {
                "1일 확률": pred_prob[0][0] * 100, 
                "0일 확률": pred_prob[0][1] * 100, 
            }
            st.write(pred_proba_scores)
            st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Irissetosa1.jpg/220px-Irissetosa1.jpg')
        elif prediction == 1:
            st.success("00 종")
            pred_proba_scores = {
                "1일 확률": pred_prob[0][0] * 100, 
                "0일 확률": pred_prob[0][1] * 100, 
            }
            st.write(pred_proba_scores)
            st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Blue_Flag%2C_Ottawa.jpg/220px-Blue_Flag%2C_Ottawa.jpg')
        else:
            st.warning("아이돈노!")
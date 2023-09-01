# -*- coding:utf-8 -*-

import numpy as np
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly as px


def main():

    st.markdown("# Hello World")
    st.write(np.__version__)
    st.write(st.__version__)
    st.write(pd.__version__)
    st.write(sns.__version__)
    st.write(px.__version__)
    

if __name__ == "__main__":
    main()
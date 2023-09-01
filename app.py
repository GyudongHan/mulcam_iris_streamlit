# -*- coding:utf-8 -*-

import numpy as np
import streamlit as st
import pandas as pd


def main():

    st.markdown("# Hello World")
    st.write(np.__version__)
    st.write(st.__version__)
    st.write(pd.__version__)

    

if __name__ == "__main__":
    main()
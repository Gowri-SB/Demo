import streamlit as st

def set_page_style():
    st.markdown("""
        <style>
            body {
                background-color: #f5faff;  /* Light Blue Background */
            }
            .stApp {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }
            .stButton>button {
                background-color: #0044cc;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            h1, h2, h3, h4, h5, h6, p, span {
                color: black;  /* Font color changed */
            }
            .stImage {
                max-width: 150px !important;  /* Set logo size */
                display: block;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)

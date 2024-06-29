import streamlit as st
from .pages.cadastro import cadastro_extintor


def main_page():
    st.sidebar.header('MENU PRINCIPAL')
    st.sidebar.markdown('-----------')
    page = st.sidebar.selectbox(label='', options=['Cadastro Extintores'])

    if page == 'Cadastro Extintores':
        cadastro_extintor()

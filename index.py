import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from page.main import main_page

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)
authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    main_page()
elif st.session_state["authentication_status"] is False:
    st.error('Nome de usuário/senha incorretos')




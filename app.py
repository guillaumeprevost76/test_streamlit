import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit_google_oauth as oauth

load_dotenv()
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]

def validate_data():
    # user_data = {"Beer Quantity": st.session_state.beer_quantity}
    df = pd.read_csv("./beer_gestion.csv",sep=";")
    df2 = pd.concat([df, pd.DataFrame({"Beer Quantity": [st.session_state.beer_quantity], "User": [st.session_state.user]})], ignore_index=True)
    df2.to_csv("./beer_gestion.csv", index=False, sep=";", encoding="utf-8")

def page_saisie():
    st.header("Page de saisie des composants")

    with st.form(key="form1"):
        st.selectbox(label="Beer Quantity", options= [25,33,50], key="beer_quantity")
        st.text_input(label="User", key="user", value=st.session_state.user_name)
    
        st.form_submit_button("Submit", type="primary", on_click=validate_data)

def reset_state():
    st.session_state.beer_quantity = None
    # st.session_state.user = None

def page_affichage():
    st.header("Recap infos")
    table_beer = pd.read_csv("./beer_gestion.csv", sep=";")
    
    st.table(table_beer)

    st.button("New input", on_click=reset_state)


def get_user_name():
    st.session_state.user_name = st.session_state.user_name

def login():
    with st.form(key="form2"):
        st.text_input(label="User", key="user_name")

        st.form_submit_button("Submit", type="primary", on_click=get_user_name)

def login_google():
    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        app_name="Continue with Google",
        logout_button_text="Logout",
    )
    if login_info is not None:
        user_id, user_email = login_info
        st.session_state.user_name = user_email
        st.write(st.session_state)

def main():
    st.title("Application avec Streamlit")

    # Utilisation d'une variable d'état pour gérer la navigation
    if "beer_quantity" not in st.session_state:
        st.session_state.beer_quantity = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    if st.session_state.user_name is None:
        login_google()
        # login()
    elif st.session_state.beer_quantity is None:
        page_saisie()
    else:
        page_affichage()
    
if __name__ == "__main__":
    main()
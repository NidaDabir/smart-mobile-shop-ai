import streamlit as st

users = {

"user":"user",

"admin":"admin"

}

def login_user(username,password):

    if username in users and users[username]==password:

        st.session_state.logged_in=True

        st.session_state.user=username

        return True

    return False

def logout_user():

    st.session_state.logged_in=False

    st.session_state.user=""

def is_logged_in():

    return st.session_state.get("logged_in",False)








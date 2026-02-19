import streamlit as st


def login():

    if "role" not in st.session_state:

        st.session_state.role = None


    if st.session_state.role is None:

        st.title("Login")

        user = st.text_input("Username")

        password = st.text_input("Password", type="password")


        if st.button("Login"):

            if user == "admin" and password == "admin":

                st.session_state.role = "admin"

                st.rerun()

            elif user == "user" and password == "user":

                st.session_state.role = "user"

                st.rerun()

            else:

                st.error("Wrong login")

        st.stop()



def logout():

    if st.sidebar.button("Logout"):

        st.session_state.role = None

        st.rerun()





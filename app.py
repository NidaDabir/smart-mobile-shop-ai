# ============================================
# SMART MOBILE SHOP AI ASSISTANT
# FINAL DEPLOYMENT VERSION (STREAMLIT CLOUD SAFE)
# ============================================

import streamlit as st
import pandas as pd
import datetime
import os

# SAFE IMPORT
from auth import login, logout


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Smart Mobile Shop AI",
    page_icon="📱",
    layout="wide"
)


# ============================================
# SESSION STATE FIX (VERY IMPORTANT FOR CLOUD)
# ============================================

if "role" not in st.session_state:
    st.session_state.role = None


# ============================================
# LOGIN
# ============================================

login()

# STOP APP if not logged in
if st.session_state.role is None:
    st.stop()


# ============================================
# LOAD DATA (DEPLOY SAFE PATH)
# ============================================

DATA_PATH = "mobile_shop_dataset.csv"

if not os.path.exists(DATA_PATH):

    st.error("Dataset not found")
    st.stop()

df = pd.read_csv(DATA_PATH)


# ============================================
# SIDEBAR
# ============================================

st.sidebar.write(f"Welcome: {st.session_state.role}")

logout()

st.sidebar.header("Filter Mobiles")

# CLEAN BRAND COLUMN FIRST

df["Brand"] = df["Brand"].astype(str)


brand = st.sidebar.selectbox(

    "Select Brand",

    ["All"] + sorted(df["Brand"].dropna().unique())

)

df["Segment"] = df["Segment"].astype(str)

segment = st.sidebar.selectbox(

    "Select Segment",

    ["All"] + sorted(df["Segment"].dropna().unique())

)



price = st.sidebar.slider(
    "Select Max Price",
    int(df["Price"].min()),
    int(df["Price"].max()),
    int(df["Price"].max())
)


# ============================================
# FILTER LOGIC
# ============================================

filtered_df = df.copy()

if brand != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand]

if segment != "All":
    filtered_df = filtered_df[filtered_df["Segment"] == segment]

filtered_df = filtered_df[filtered_df["Price"] <= price]


# ============================================
# TITLE
# ============================================

st.title("📱 Smart Mobile Shop AI Assistant")


# ============================================
# FEATURED MOBILES
# ============================================

st.header("📱 Featured Mobiles")

if len(filtered_df) == 0:

    st.warning("No phones found")

else:

    cols = st.columns(3)

    for i, (_, row) in enumerate(filtered_df.head(6).iterrows()):

        with cols[i % 3]:

            if pd.notna(row["Image"]) and os.path.exists(row["Image"]):
                st.image(row["Image"], width=120)

            st.subheader(row["Brand"] + " " + row["Model"])

            st.write(f"💰 ₹{row['Price']}")
            st.write(f"📷 {row['Camera_MP']} MP")
            st.write(f"🔋 {row['Battery_mAh']} mAh")


# ============================================
# AI RECOMMENDATION
# ============================================

st.header("🤖 AI Recommendation")

col1, col2 = st.columns(2)

with col1:

    ram = st.selectbox("RAM", [4,6,8,12])
    storage = st.selectbox("Storage", [64,128,256])

with col2:

    battery = st.slider("Battery",3000,6000)
    camera = st.slider("Camera",12,200)
    budget = st.slider("Budget",10000,150000)


def recommend_mobile():

    data = df[df["Price"] <= budget].copy()

    if len(data) == 0:
        return "No phone found"

    data["Score"] = (

        (data["RAM_GB"] / ram) * 25 +
        (data["Storage_GB"] / storage) * 20 +
        (data["Battery_mAh"] / battery) * 25 +
        (data["Camera_MP"] / camera) * 30

    )

    best = data.sort_values("Score", ascending=False).iloc[0]

    return best["Brand"] + " " + best["Model"]


# ============================================
# BUTTON
# ============================================

if st.button("Recommend Mobile"):

    result = recommend_mobile()

    st.success(result)

    log = pd.DataFrame([{

        "Time": datetime.datetime.now(),
        "RAM": ram,
        "Storage": storage,
        "Battery": battery,
        "Camera": camera,
        "Budget": budget,
        "Recommended": result

    }])

    log.to_csv(
        "user_tracking.csv",
        mode="a",
        header=not os.path.exists("user_tracking.csv"),
        index=False
    )

    log.to_csv(
        "user_data.csv",
        mode="a",
        header=not os.path.exists("user_data.csv"),
        index=False
    )


# ============================================
# ADMIN PANEL
# ============================================

if st.session_state.role == "admin":

    st.sidebar.header("Admin Panel")

    if st.sidebar.button("View Tracking"):

        st.header("Tracking")

        if os.path.exists("user_tracking.csv"):

            track = pd.read_csv("user_tracking.csv")

            st.dataframe(track)

        else:

            st.warning("No tracking data")


    if st.sidebar.button("View Inputs"):

        st.header("Inputs")

        if os.path.exists("user_data.csv"):

            inputs = pd.read_csv("user_data.csv")

            st.dataframe(inputs)

        else:

            st.warning("No input data")


# ============================================
# ANALYTICS
# ============================================

st.header("📊 Dashboard Analytics")

st.subheader("Brand Distribution")

st.bar_chart(df["Brand"].value_counts())

st.subheader("Price Distribution")

st.line_chart(df["Price"])

st.subheader("Camera vs Price")

st.scatter_chart(df[["Camera_MP","Price"]])

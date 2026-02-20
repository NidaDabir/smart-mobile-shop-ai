# ===============================
# SMART MOBILE SHOP AI - FINAL
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pyttsx3   # FIXED

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Smart Mobile Shop AI", layout="wide")

# ---------------- TALK FUNCTION ----------------

def speak(text):

    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except:
        pass   # prevents crash in deployment


# ---------------- LOAD DATA@st.cache_data
def load_data():

    df = pd.read_csv(os.path.join(BASE_DIR, "mobile_shop_dataset.csv"))

    df.columns = df.columns.str.strip().str.upper()

    # FIX NUMERIC COLUMNS
    df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")
    df["RAM_GB"] = pd.to_numeric(df["RAM_GB"], errors="coerce")
    df["STORAGE_GB"] = pd.to_numeric(df["STORAGE_GB"], errors="coerce")
    df["BATTERY_MAH"] = pd.to_numeric(df["BATTERY_MAH"], errors="coerce")
    df["CAMERA_MP"] = pd.to_numeric(df["CAMERA_MP"], errors="coerce")

    df = df.dropna()

    return df
df = load_data()


# ---------------- BRAND IMAGES ----------------

brand_images = {

    "APPLE": "images/apple.png",
    "SAMSUNG": "images/samsung.png",
    "REALME": "images/realme.png",
    "XIAOMI": "images/xiaomi.png",
    "VIVO": "images/vivo.png",
    "OPPO": "images/oppo.png",
    "ONEPLUS": "images/oneplus.png",
    "GOOGLE": "images/google.png",
    "MOTOROLA": "images/motorola.png"

}


# ---------------- LOGIN ----------------

users = {

    "admin": "admin",
    "user": "user"

}

if "login" not in st.session_state:

    st.session_state.login = False


if not st.session_state.login:

    st.title("📱 Smart Mobile Shop AI Login")

    u = st.text_input("Username")

    p = st.text_input("Password", type="password")

    if st.button("Login"):

        if u in users and users[u] == p:

            st.session_state.login = True
            st.session_state.user = u
            st.rerun()

        else:

            st.error("Wrong login")

    st.stop()


# ---------------- SIDEBAR ----------------

st.sidebar.title("👤 Welcome " + st.session_state.user)

if st.sidebar.button("Logout"):

    st.session_state.login = False
    st.rerun()


brand = st.sidebar.selectbox(

    "Brand",
    ["All"] + sorted(df["BRAND"].unique())

)


segment = st.sidebar.selectbox(

    "Segment",
    ["All"] + sorted(df["SEGMENT"].unique())

)


max_price = st.sidebar.slider(

    "Max Price",
    int(df["PRICE"].min()),
    int(df["PRICE"].max()),
    int(df["PRICE"].max())

)


# ---------------- ADMIN ----------------

admin_view=None

if st.session_state.user=="admin":

    st.sidebar.title("⚙ Admin Panel")

    admin_view=st.sidebar.radio(

        "Select",
        ["User Tracking","User Inputs"]

    )


# ---------------- FILTER ----------------

filtered=df.copy()

if brand!="All":

    filtered=filtered[filtered["BRAND"]==brand]

if segment!="All":

    filtered=filtered[filtered["SEGMENT"]==segment]

filtered=filtered[filtered["PRICE"]<=max_price]


# ---------------- SEARCH FIXED ----------------

search=st.sidebar.text_input("🔎 Search phone")

if search:

    search_results=df[

        df["MODEL"].astype(str).str.lower().str.contains(search.lower())

        |

        df["BRAND"].astype(str).str.lower().str.contains(search.lower())

    ]


    st.header(f"🔎 Search Results for '{search}'")

    if len(search_results)>0:

        cols=st.columns(3)

        for i,(_,row) in enumerate(search_results.iterrows()):

            with cols[i%3]:

                img=brand_images.get(row["BRAND"].upper(),None)

                if img and os.path.exists(img):

                    st.image(img,width=80)

                st.write(f"**{row['BRAND']} {row['MODEL']}**")

                st.write(f"₹ {row['PRICE']}")

    else:

        st.error("No phone found")


# ---------------- TITLE ----------------

st.markdown("<h1 style='text-align:center;'>📱 Smart Mobile Shop AI</h1>",unsafe_allow_html=True)


# ---------------- FEATURED ----------------

st.header("Featured Mobiles")

cols=st.columns(3)

for i,(_,row) in enumerate(filtered.head(6).iterrows()):

    with cols[i%3]:

        img=brand_images.get(row["BRAND"].upper(),None)

        if img and os.path.exists(img):

            st.image(img,width=100)

        st.markdown(f"""

### 📱 {row['BRAND']} {row['MODEL']}

💰 Price ₹{row['PRICE']}

⚡ RAM {row['RAM_GB']} GB

🔋 Battery {row['BATTERY_MAH']} mAh

📸 Camera {row['CAMERA_MP']} MP

""")

# ---------------- RECOMMENDATION ----------------

st.header(" 💡 AI Recommendation")


c1, c2, c3, c4, c5 = st.columns(5)

ram = c1.selectbox("RAM", sorted(df["RAM_GB"].unique()))

storage = c2.selectbox("Storage", sorted(df["STORAGE_GB"].unique()))

battery = c3.slider("Battery", int(df["BATTERY_MAH"].min()), int(df["BATTERY_MAH"].max()))

camera = c4.slider("Camera", int(df["CAMERA_MP"].min()), int(df["CAMERA_MP"].max()))

budget = c5.slider("Budget", int(df["PRICE"].min()), int(df["PRICE"].max()))


if st.button("Recommend Mobile"):

    rec = df[

        (df["RAM_GB"] == ram)
        & (df["STORAGE_GB"] == storage)
        & (df["BATTERY_MAH"] >= battery)
        & (df["CAMERA_MP"] >= camera)
        & (df["PRICE"] <= budget)

    ]

    if len(rec) > 0:

        phone = rec.iloc[0]

        st.success("✅ Recommended: " + phone["BRAND"] + " " + phone["MODEL"])

    else:

        st.error("No phone found")


# ---------------- CHATBOT FIXED ----------------

st.header("🤖 AI Chatbot")

msg=st.text_input("Ask question")

if st.button("Send"):

    msg=msg.lower()

    if "hello" in msg:

        reply="Hello welcome to Smart Mobile Shop"

    elif "samsung" in msg:

        reply="Best Samsung phone is Galaxy S23"

    elif "apple" in msg:

        reply="Best Apple phone is iPhone 15"

    elif "camera" in msg:

        reply="Best camera phone is Pixel"

    elif "battery" in msg:

        reply="Best battery phone is Samsung M34"

    else:

        reply="Ask about Apple Samsung Camera Battery Budget"

    st.success(reply)

    speak(reply)


# ---------------- ADMIN DISPLAY ----------------

if admin_view=="User Tracking":

    st.header("User Tracking")

    st.dataframe(pd.read_csv(os.path.join(BASE_DIR,"user_tracking.csv")))


elif admin_view=="User Inputs":

    st.header("User Inputs")

    st.dataframe(pd.read_csv(os.path.join(BASE_DIR,"user_data.csv")))



# ---------------- BEAUTIFUL DARK PLOTS ----------------

st.header("📊 Market Insights Dashboard")

# USE DARK THEME
plt.style.use("dark_background")

# CREATE FIGURE
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# -------- PIE --------

colors = plt.cm.Set3(np.linspace(0,1,len(df["BRAND"].unique())))

df["BRAND"].value_counts().plot.pie(

    autopct="%1.0f%%",
    colors=colors,
    textprops={'color':"white", 'fontsize':10},
    ax=axes[0]

)

axes[0].set_title("Brand Share", color="white", fontsize=14)
axes[0].set_ylabel("")


# -------- SCATTER --------

axes[1].scatter(

    df["PRICE"],
    df["BATTERY_MAH"],

    c=df["PRICE"],
    cmap="plasma",

    s=120,
    alpha=0.8

)

axes[1].set_title("Price vs Battery", color="white", fontsize=14)
axes[1].set_xlabel("Price")
axes[1].set_ylabel("Battery")


# -------- BUBBLE --------

axes[2].scatter(

    df["PRICE"],
    df["CAMERA_MP"],

    s=df["BATTERY_MAH"]/15,

    c=df["CAMERA_MP"],
    cmap="cool",

    alpha=0.7

)

axes[2].set_title("Camera vs Price", color="white", fontsize=14)
axes[2].set_xlabel("Price")
axes[2].set_ylabel("Camera")


# REMOVE BACKGROUND
fig.patch.set_alpha(0)

# SHOW IN STREAMLIT
st.pyplot(fig)





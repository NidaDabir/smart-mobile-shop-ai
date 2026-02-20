import pandas as pd

def recommend_mobile(ram, storage, battery, camera, budget):

    df = pd.read_csv("mobile_shop_dataset.csv")

    result = df[

        (df["RAM_GB"] >= ram) &
        (df["STORAGE_GB"] >= storage) &
        (df["BATTERY_MAH"] >= battery) &
        (df["CAMERA_MP"] >= camera) &
        (df["PRICE"] <= budget)

    ]

    if len(result) > 0:

        result = result.sort_values("PRICE")

        phone = result.iloc[0]

        return phone["BRAND"] + " " + phone["MODEL"]

    return "No phone found"







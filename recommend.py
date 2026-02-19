import pandas as pd

# Load dataset
data = pd.read_csv("mobile_shop_dataset.csv")

# Remove bad rows
data = data.dropna()

# Performance Score
data["Performance_Score"] = (
    data["RAM_GB"] * 4 +
    data["Storage_GB"] * 0.5 +
    data["Camera_MP"] * 2 +
    data["Battery_mAh"] * 0.01
)


def recommend_mobile(ram, storage, battery, camera, budget):

    # Filter only by budget
    filtered = data[data["Price"] <= budget].copy()

    if filtered.empty:
        return "No phone found"

    # Similarity score
    filtered["Match"] = (

        abs(filtered["RAM_GB"] - ram) * 3 +

        abs(filtered["Storage_GB"] - storage) +

        abs(filtered["Battery_mAh"] - battery) * 0.01 +

        abs(filtered["Camera_MP"] - camera) * 2

    )

    filtered["Final"] = filtered["Performance_Score"] - filtered["Match"]

    best = filtered.sort_values("Final", ascending=False).iloc[0]

    return f"{best['Brand']} {best['Model']}"



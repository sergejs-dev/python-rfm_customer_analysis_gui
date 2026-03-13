import pandas as pd
from datetime import datetime


def load_data(file_path):
    df = pd.read_csv(file_path)

    # convert date column
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    return df


def calculate_rfm(df):

    snapshot_date = df["OrderDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg({
        "OrderDate": lambda x: (snapshot_date - x.max()).days,
        "CustomerID": "count",
        "Revenue": "sum"
    })

    rfm.rename(columns={
        "OrderDate": "Recency",
        "CustomerID": "Frequency",
        "Revenue": "Monetary"
    }, inplace=True)

    return rfm


def create_segments(rfm):

    rfm["R_score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
    rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
    rfm["M_score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

    rfm["RFM_score"] = (
        rfm["R_score"].astype(str) +
        rfm["F_score"].astype(str) +
        rfm["M_score"].astype(str)
    )

    def segment(row):

        if row["RFM_score"] >= "444":
            return "Champions"

        elif row["RFM_score"] >= "344":
            return "Loyal Customers"

        elif row["RFM_score"] >= "244":
            return "Potential Loyalists"

        elif row["RFM_score"] >= "144":
            return "At Risk"

        else:
            return "Lost"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    return rfm
import pandas as pd


def export_excel(raw_df, rfm_df, segment_counts, file_path):

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:

        # Raw Data
        raw_df.to_excel(writer, sheet_name="Raw Data", index=False)

        # RFM Table
        rfm_df.to_excel(writer, sheet_name="RFM Table")

        # Segment Summary
        segment_df = segment_counts.reset_index()
        segment_df.columns = ["Segment", "Customers"]
        segment_df.to_excel(writer, sheet_name="Segments", index=False)
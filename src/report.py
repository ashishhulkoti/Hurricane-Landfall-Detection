def save_to_csv(df, state: str):
    """
    Save detected landfall events to a CSV file.

    Args:
        df (pd.DataFrame): Detected landfall events.
        state (str): State name for output file naming.

    Returns:
        str: The path to the saved CSV file.
    """
    if df.empty:
        raise ValueError("❌ No data to save. The DataFrame is empty.")

    output_path = f"{state.lower()}_hurricane_landfall_report.csv"
    try:
        df.to_csv(output_path, index=False)
        print(f"✅ Report saved to {output_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to save report: {e}")

    return output_path

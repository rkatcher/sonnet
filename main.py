"""Fetch rows from a Google Sheet and POST them to a URL."""

import os
import sys
import json
import requests
import pandas as pd
from dotenv import load_dotenv


def rows_to_dicts(values: list[list[str]]) -> list[dict[str, str]]:
    """Convert sheet rows into a list of dicts using the first row as headers."""
    if not values:
        return []

    headers = values[0]
    rows = []
    for row in values[1:]:
        # Pad short rows so zip() does not drop trailing columns.
        padded = row + [""] * (len(headers) - len(row))
        rows.append(dict(zip(headers, padded)))
    return rows


def post_data(url: str, payload: dict, headers: dict[str, str] | None = None) -> requests.Response:
    """POST merge_variables JSON to the target URL."""
    response = requests.post(url, json=payload, headers=headers or {}, timeout=30)
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
    response.raise_for_status()
    return response


def main() -> None:
    # load .env file 
    load_dotenv() 
    
    # 1. Replace with your actual spreadsheet ID
    sheet_id = os.environ.get("SHEET_ID")
    sheet_name = os.environ.get("SHEET_NAME")

    # 2. Construct the export URL for CSV format
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    # 3. Read directly into a pandas DataFrame
    df = pd.read_csv(url)

    # Display the data
    #print(df.head())
    #data_dict = df.to_dict(orient='list')
    data_dict = {col: [x for x in df[col] if pd.notna(x)] for col in df.columns}
    print (data_dict)
    
    plugin_id=os.environ.get("TRMNL_PLUGIN_ID")
    post_url = "https://trmnl.com/api/custom_plugins/" + plugin_id
    #payload = {"merge_variables": {"title": "sonnet_data", "ingredients": ["kale", "habaneros", "poblanos"], "meal_plan": ["frittata", "soup", "brownies"]} }
#    payload = {"merge_variables": {"title": "Ingredients", "ingredients": ["chard", "jalapenos", "eggplant"]}}
    payload = {"merge_variables": {"title": "sonnet_data"}}
    payload["merge_variables"].update(data_dict)

    response = post_data(post_url, payload)
    print(f"Posted to {post_url} (status {response.status_code})")
    print(response.json())


if __name__ == "__main__":
    main()

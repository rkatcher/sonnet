"""Fetch rows from a Google Sheet and POST them to a URL."""

import os
import sys
import json
import requests
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
    #spreadsheet_id = os.environ.get("GOOGLE_SHEET_ID")
    #post_url = os.environ.get("POST_URL")
    #range_name = os.environ.get("GOOGLE_SHEET_RANGE", "Sheet1!A:Z")
    # credentials_path = os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    # if not spreadsheet_id or not post_url:
    #     print("Set GOOGLE_SHEET_ID and POST_URL environment variables.", file=sys.stderr)
    #     sys.exit(1)
    # values = fetch_sheet_data(spreadsheet_id, range_name, credentials_path)

    # load .env file 
    load_dotenv() 
    plugin_id=os.environ.get("TRMNL_PLUGIN_ID")
    post_url = "https://trmnl.com/api/custom_plugins/" + plugin_id
    payload = {"merge_variables": {"title": "Ingredients", "ingredients": ["chard", "jalapenos", "eggplant"]}}

    response = post_data(post_url, payload)
    print(f"Posted to {post_url} (status {response.status_code})")
    print(response.json())


if __name__ == "__main__":
    main()

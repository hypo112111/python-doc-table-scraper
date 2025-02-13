import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_table_from_published_doc(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve the document. Check the URL.")

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    extracted_tables = []

    for table in tables:
        rows = table.find_all("tr")
        table_data = []

        for row in rows:
            cells = row.find_all(["td", "th"])
            table_data.append([cell.get_text(strip=True) for cell in cells])

        extracted_tables.append(pd.DataFrame(table_data))  # Convert to DataFrame

    # Save tables to CSV
    for i, table in enumerate(extracted_tables):
        table.to_csv(f"table_{i+1}.csv", index=False, header=False)

    # Print tables

    secret_text = {" "}

    for i, table in enumerate(extracted_tables):
        #print(table.iloc[0].values[1])
        for row in range(len(table)):
          secret_text[table.iloc[row].values[2]][table.iloc[row].values[0]] = table.iloc[row].values[1]

    print(secret_text)

    # Print tables
    for i, table in enumerate(extracted_tables):
        print(f"\nTable {i+1}:\n", table)

    return extracted_tables

# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
tables = extract_table_from_published_doc(doc_url)

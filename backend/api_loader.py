import requests

from langchain_core.documents import Document


def load_worldbank_api(url: str):
    """
    Fetch World Bank API data and convert it into LangChain Documents.
    """

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    documents = []

    if len(data) > 1:

        records = data[1]

        for row in records:

            country = row.get("country", {}).get("value", "Unknown Country")

            indicator = row.get("indicator", {}).get("value", "Unknown Indicator")

            year = row.get("date", "Unknown Year")

            value = row.get("value")

            if value is None:
                continue

            text = f"{country} " f"{indicator} " f"for year {year} " f"was {value}."

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": url,
                        "country": country,
                        "indicator": indicator,
                        "year": year,
                    },
                )
            )

    return documents

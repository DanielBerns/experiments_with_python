import httpx


def fetch_rss_feed():
    url = "https://www.ambito.com/rss/pages/home.xml"
    headers = {"X-Client-ID": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"}
    try:
        with httpx.Client(headers=headers) as client:
            response = client.get(url)
            # Check if the request was successful
            response.raise_for_status()
            # Output the XML content
            print("Successfully fetched the RSS feed:\n")
            print(response.text)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

if __name__ == "__main__":
    fetch_rss_feed()

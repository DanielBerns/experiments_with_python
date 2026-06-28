import feedparser
from typing import Any
import structlog

from ana.agents.inbound_node import ExpectedDomainException

logger = structlog.get_logger("ana.adapters.rss_client")

class RSSFeedClient:
    """
    Adapter for rss feeds. No need to manage authentication state and exposes
    actions compatible with GatewayRegistry's ActionCallable signature.
    """

    def __init__(self, base_url: str = ""):
        # base_url can be empty if full URLs are passed via parameters
        self.base_url = base_url

    def _get_trace_headers(self) -> dict[str, str]:
        context = structlog.contextvars.get_contextvars()
        correlation_id = context.get("correlation_id")
        return {"X-Correlation-ID": str(correlation_id)} if correlation_id else {}

    async def get_feed(self, parameters: dict[str, Any]) -> tuple[bytes, str]:
        """
        Registry Action: get content from a public rss feed (no need for auth credentials)
        Returns raw bytes and mime type. Expects 'url' in parameters.
        """
        logger.info(f"rss_client: {str(parameters)}")
        target_url = parameters.get("url")
        if not target_url:
            logger.error("Missing 'url' in parameters dictionary")
            raise ExpectedDomainException(
                "Missing 'url' in parameters to fetch public website."
            )

        trace_headers = self._get_trace_headers()

        logger.info("Fetching content from rss_feed", url=target_url)

        try:
            # feedparser.parse() automatically downloads and parses the URL
            response = feedparser.parse(args.url)

            # Check for parsing errors (bozo flag)
            if response.bozo:
                logger.warning(f"There was a problem parsing the feed {response.bozo_exception}")

            logger.debug(
                "Successfully fetched rss feed",
                url=target_url,
            )

            # Loop through entries and extract key information
            entries = [{ "title": entry.get("title", "No Title"),
                         "link": entry.get("link", ""),
                         "published": entry.get("published", ""),
                         "summary": entry.get("summary", "")
                       } for entry in response.entries]

            # Extract the main feed information
            output_data = {
                "feed_info": {
                    "title": response.feed.get("title", "No Title"),
                    "link": response.feed.get("link", ""),
                    "subtitle": response.feed.get("subtitle", "")
                },
                "entries": entries
            }
            # 1. Serialize the dictionary to a JSON-formatted string
            json_string = json.dumps(output_data)
            # 2. Encode the string to bytes
            json_bytes = json_string.encode('utf-8')
            # 3. Build the headers
            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(json_bytes))
            }
            # 4. Serialize the headers
            json_headers = json.dumps(headers)
            return json_bytes, json_headers
        except Exception as e:
            logger.warning(
                "feedparser error fetching public website",
                url=target_url
            )
            raise ExpectedDomainException(
                f"Failed to fetch rss feed from URL {target_url}: {e}"
            )

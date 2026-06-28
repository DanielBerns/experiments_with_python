import feedparser
import argparse
import json
import sys

def main():
    # Set up the command-line interface argument parser
    parser = argparse.ArgumentParser(description="Fetch, parse, and save an RSS/Atom feed using feedparser.")
    parser.add_argument("url", help="The URL of the RSS/Atom feed to download.")
    parser.add_argument("-o", "--output", default="feed_data.json", help="The output JSON file name (default: feed_data.json).")

    args = parser.parse_args()

    print(f"Fetching and parsing feed from: {args.url}")

    # feedparser.parse() automatically downloads and parses the URL
    feed = feedparser.parse(args.url)

    # Check for parsing errors (bozo flag)
    if feed.bozo:
        print(f"Warning: There was a problem parsing the feed. Exception: {feed.bozo_exception}", file=sys.stderr)
        print("Attempting to save any recovered data anyway...")

    # Extract the main feed information
    output_data = {
        "feed_info": {
            "title": feed.feed.get("title", "No Title"),
            "link": feed.feed.get("link", ""),
            "subtitle": feed.feed.get("subtitle", "")
        },
        "entries": []
    }

    # Loop through entries and extract key information
    for entry in feed.entries:
        output_data["entries"].append({
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")
        })

    # Save the extracted data to a JSON file
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {len(feed.entries)} entries to {args.output}")
    except IOError as e:
        print(f"Error saving file to {args.output}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

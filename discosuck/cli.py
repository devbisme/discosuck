import argparse
import json
import re
import requests
import sys
import time

def get_topics_page(url, page_num):
    resp = requests.get(url, params={"ascending":"false", "no_definition":"true", "page":str(page_num)})
    return json.loads(resp.text)

def get_topic_posts(url):
    resp = requests.get(url)
    return json.loads(resp.text)

def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Suck posts out of a Discourse forum")
    parser.add_argument("base_url", help="URL of Discourse forum.")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay in seconds between website accesses.")
    parser.add_argument("-s", "--start_page", type=int, default=0, help="Starting page number of forum topic lists.")
    parser.add_argument("-n", "--num_pages", type=int, default=1<<32, help="Number of topic listing pages to process.")
    parser.add_argument("-o", "--output_file", help="File for storing posts.")
    parser.add_argument("-p", "--show_progress", action="store_true", help="File for storing posts.")
    args = parser.parse_args()

    # Get the URL of the Discourse forum.
    base_url = args.base_url
    try:
        # Test the URL to see if it's acceptable.
        requests.get(base_url)
    except requests.exceptions.MissingSchema:
        # Attempt to make the URL acceptable.
        base_url = "https://" + base_url
        # Try the modified URL and abort with exception if it's still not right.
        requests.get(base_url)

    # This is the entrypoint for scraping the forum as JSON (not HTML).
    forum_url = f'{base_url}/latest.json'

    # Set the starting and ending pages of forum topics.
    page_num = args.start_page
    end_page = args.start_page + args.num_pages - 1

    # Make a list of all topics from the start to the end topics pages.
    topics = []
    while True:
        # Get a page with a list of topics.
        topics_page = get_topics_page(forum_url, page_num)

        if args.show_progress:
            print(f"Fetched topic list page {page_num}.")

        # Add the topics to the total list.
        topics.extend(topics_page["topic_list"]["topics"])

        # Break from loop if no more topic list pages or got to end page.
        if not topics_page["topic_list"].get("more_topics_url") or page_num==end_page:
            break

        # Go to the list of topics on the next page.
        page_num += 1

        # Sleep so we don't gather pages too fast.
        time.sleep(args.delay)

    # Gather posts for each topic and add them to the topic.
    for n_topic, topic in enumerate(topics):

        # Get the page with posts on the topic.
        topic_url = f"{base_url}/t/{topic['slug']}/{topic['id']}.json"
        topic["posts"] = get_topic_posts(topic_url)

        if args.show_progress:
            print(f"Fetched posts for \"{topic['slug']}.\"")

        # Sleep so we don't gather pages too fast.
        time.sleep(args.delay)

    # Store the list of topics and associated posts into a JSON file.
    if not args.output_file:
        json_filename = re.sub("\W+", "_", base_url.split("://")[1]) + ".json"
    else:
        json_filename = args.output_file
    with open(json_filename, 'w') as f:
        json.dump(topics, f, ensure_ascii=False, indent=4)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

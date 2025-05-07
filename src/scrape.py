import argparse
import json

import requests
from bs4 import BeautifulSoup


def get_reviews(base_url, output_file):
    page = 1
    total_reviews = 0

    with open(output_file, "w", encoding="utf-8") as file:
        while True:
            print(f"Processing page {page}...")
            response = requests.get(f"{base_url}?pagina={page}")

            if response.status_code != 200:
                print(f"Error requesting page {page}: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            review_list = soup.select(
                "body > div.mdc-drawer-app-content > div.row.mdc-top-app-bar--fixed-adjust > div.main > div.alter-padding.content-opiniones > ul > li"
            )

            if not review_list:
                break

            for review in review_list:
                author_date = review.select_one(".autor")
                author_name = (
                    review.select(".autor")[1]
                    if len(review.select(".autor")) > 1
                    else None
                )
                rating = review.select_one(".calificacion")
                rating_value = (
                    rating["content"]
                    if rating and "content" in rating.attrs
                    else "Not available"
                )
                text = review.select_one(".comentario")

                review_data = {
                    "date": (
                        author_date.text.strip() if author_date else "Not available"
                    ),
                    "author": author_name.text.strip() if author_name else "Unknown",
                    "rating": rating_value.strip() if rating else "Not available",
                    "text": text.text.strip() if text else "No review",
                }

                file.write(json.dumps(review_data, ensure_ascii=False) + "\n")
                total_reviews += 1

            page += 1

    print(
        f"Scraping completed: {page - 1} pages processed, {total_reviews} reviews extracted."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape reviews from Alternativa Teatral website"
    )
    parser.add_argument("url", help="Base URL of the review page")
    parser.add_argument(
        "-o",
        "--output",
        default="reviews.jsonl",
        help="Output file name (default: reviews.jsonl)",
    )

    args = parser.parse_args()
    get_reviews(args.url, args.output)

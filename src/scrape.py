import argparse
import json

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_total_pages(base_url):
    response = requests.get(f"{base_url}?pagina=1")
    if response.status_code != 200:
        raise Exception(f"Error fetching initial page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    pagination_links = soup.select("ul.pagination li.page-item a")

    page_numbers = []
    for link in pagination_links:
        href = link.get("href", "")
        if "pagina=" in href:
            try:
                page_number = int(href.split("pagina=")[1])
                page_numbers.append(page_number)
            except ValueError:
                continue

    return max(page_numbers) if page_numbers else 1


def get_reviews(base_url, output_file):
    total_reviews = 0
    total_pages = get_total_pages(base_url)

    with open(output_file, "w", encoding="utf-8") as file:
        for page in tqdm(range(1, total_pages + 1), desc="Scraping pages"):
            response = requests.get(f"{base_url}?pagina={page}")

            if response.status_code != 200:
                print(f"\nError requesting page {page}: {response.status_code}")
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

    print(
        f"\nScraping completed: {total_pages} pages processed, {total_reviews} reviews extracted."
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

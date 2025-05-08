import argparse
import asyncio
import json

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm


async def get_total_pages(base_url, session):
    async with session.get(f"{base_url}?pagina=1") as response:
        if response.status != 200:
            raise Exception(f"Error fetching initial page: {response.status}")
        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
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


async def scrape_page(base_url, page, session):
    url = f"{base_url}?pagina={page}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error requesting page {page}: {response.status}")
                return []

            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            review_list = soup.select(
                "body > div.mdc-drawer-app-content > div.row.mdc-top-app-bar--fixed-adjust > div.main > div.alter-padding.content-opiniones > ul > li"
            )

            reviews = []
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

                reviews.append(
                    {
                        "date": (
                            author_date.text.strip() if author_date else "Not available"
                        ),
                        "author": (
                            author_name.text.strip() if author_name else "Unknown"
                        ),
                        "rating": rating_value.strip(),
                        "text": text.text.strip() if text else "No review",
                    }
                )

            return reviews
    except Exception as e:
        print(f"Exception in page {page}: {e}")
        return []


async def get_reviews(base_url, output_file):
    async with ClientSession() as session:
        total_pages = await get_total_pages(base_url, session)

        tasks = [
            scrape_page(base_url, page, session) for page in range(1, total_pages + 1)
        ]

        all_reviews = []
        for coro in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Scraping pages",
            unit=" pages",
        ):
            reviews = await coro
            all_reviews.extend(reviews)

        with open(output_file, "w", encoding="utf-8") as file:
            for review in all_reviews:
                file.write(json.dumps(review, ensure_ascii=False) + "\n")

        print(
            f"Scraping completed: {total_pages} pages processed, {len(all_reviews)} reviews extracted."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape reviews from Alternativa Teatral website"
    )
    parser.add_argument("url", help="Base URL of the review page")
    parser.add_argument(
        "-o", "--output", default="reviews.jsonl", help="Output file name"
    )

    args = parser.parse_args()
    print()
    asyncio.run(get_reviews(args.url, args.output))

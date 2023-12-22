"""
This script will fetch the questions from advent of code and
save it as a Markdown file
"""

import datetime
import os

import requests
from bs4 import BeautifulSoup


class AdventOfCodeTaskScraper:
    def __init__(self, year: int = None, day: int = None) -> None:
        self._BASE_URL = "https://adventofcode.com"
        self._year = year if year else datetime.datetime.now().year
        self._day = day if day else datetime.datetime.now().day

        self.TASK_URL = f"{self._BASE_URL}/{self._year}/day/{self._day}"

        self._path_output = f"{self._year}/questions"
        self._filepath_output = os.path.join(self._path_output, f"day{self._day}.md")

    def _already_got_today(self):
        """Check if markdown file exists for current date"""
        return True if os.path.exists(self._filepath_output) else False

    def _link_exists_not(self):
        return False if RequestsUtils.is_valid_url(url=self.TASK_URL) else True

    def start(self):
        """Start script"""
        if self._already_got_today() or self._link_exists_not():
            print("No need to start, quitting.")
            return

        task_in_html = self.__scrape_description_html()
        self.__save_to_local_md(task_in_html)

    def __scrape_description_html(self):
        """Use requests to retrieve html data and return relevant results"""
        try:
            print(f"Scraping from {self.TASK_URL}...")
            response = requests.get(self.TASK_URL)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                article_element = soup.find("article", class_="day-desc")
                final_result = SoupUtils.fix_local_links(
                    soup=article_element, base_url=self._BASE_URL
                )
                return final_result.prettify()

            else:
                print(
                    f"Failed to retrieve content. Status code: {response.status_code}"
                )

        except Exception as e:
            print(f"An error occurred: {e}")

    def __save_to_local_md(self, html: str):
        """Save the modified HTML content to a Markdown file"""
        filepath = f"{self._year}/questions/day{self._day}.md"
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html)
        print(f"Saved to {filepath}")


class SoupUtils:
    def fix_local_links(soup, base_url: str):
        """Find all href links without https and add accordingly"""
        # Find all <a> tags within the <article> element
        all_a_tags = soup.select("article.day-desc a")

        # Modify the href attribute for each <a> tag
        for a_tag in all_a_tags:
            # Check if the href attribute exists before modifying
            if "href" in a_tag.attrs:
                # Modify the href attribute if local
                if not a_tag["href"].startswith("http"):
                    a_tag["href"] = base_url + a_tag["href"]

        return soup


class RequestsUtils:
    def is_valid_url(url: str):
        """Returns True if url has 200/300 response"""
        try:
            # Send a HEAD request to the URL (a lightweight request that only fetches headers)
            response = requests.head(url, timeout=5)

            # Check if the response status code indicates success (2xx or 3xx)
            return response.status_code // 100 == 2 or response.status_code // 100 == 3

        except requests.RequestException:
            # An exception occurred (e.g., connection error, timeout)
            return False


if __name__ == "__main__":
    # Config (optional)
    year = None
    day = None

    # Start
    md_generator = AdventOfCodeTaskScraper(year=year, day=day)
    md_generator.start()

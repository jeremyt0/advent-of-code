"""
scrape_task.

This script will fetch the questions from advent of code and
    save it as a Markdown file.
"""

import argparse
import datetime
import os

import requests
from bs4 import BeautifulSoup


class AdventOfCodeTaskScraper:
    def __init__(self, year: int | None = None, day: int | None = None) -> None:
        """Initialize AdventOfCodeTaskScraper."""
        self._BASE_URL = "https://adventofcode.com"
        self._year = year or datetime.datetime.now().year
        self._day = day or datetime.datetime.now().day

        self.TASK_URL = f"{self._BASE_URL}/{self._year}/day/{self._day}"
        self._path_output = f"{self._year}/questions"
        self._filepath_output = os.path.join(self._path_output, f"day{self._day}.md")

    def _already_got_today(self) -> bool:
        """Check if markdown file exists for the current date."""
        return os.path.exists(self._filepath_output)

    def _link_exists_not(self) -> bool:
        """Check if the task URL is valid."""
        return not RequestsUtils.is_valid_url(url=self.TASK_URL)

    def start(self) -> None:
        """Start the script."""
        if self._already_got_today() or self._link_exists_not():
            print("No need to start, quitting.")
            return

        task_in_html = self.__scrape_description_html()
        self.__save_to_local_md(task_in_html)

    def __scrape_description_html(self) -> str:
        """Retrieve HTML data and return relevant results."""
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

    def __save_to_local_md(self, html: str) -> None:
        """Save the modified HTML content to a Markdown file."""
        filepath = f"{self._year}/questions/day{self._day}.md"
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(html)
            print(f"Saved to {filepath}")
        except TypeError as e:
            print(f"Error saving to local: {e}")



class SoupUtils:
    @classmethod
    def fix_local_links(cls, soup: BeautifulSoup, base_url: str) -> BeautifulSoup:
        """Find all href links without https and add accordingly.

        Args:
            cls: The class itself.
            soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML.
            base_url (str): The base URL to prepend to local href links.

        Returns:
            BeautifulSoup: The modified BeautifulSoup object.
        """
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


class RequestsUtils(object):
    """Utility class for handling requests."""

    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """Check if the URL has a 200/300 response.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the response status code indicates success (2xx or 3xx),
                  False otherwise.
        """
        try:
            # Send a HEAD request to the URL (a lightweight request that only fetches headers)
            response = requests.head(url, timeout=5)

            # Check if the response status code indicates success (2xx or 3xx)
            return response.status_code // 100 == 2 or response.status_code // 100 == 3

        except requests.RequestException:
            # An exception occurred (e.g., connection error, timeout)
            return False


class Args:
    @classmethod
    def parser():
        parser = argparse.ArgumentParser(
            description="Fetch and save Advent of Code tasks to local MD.",
        )
        parser.add_argument(
            "--year", type=int, default=None, help="The year you want to scrape from.",
        )
        parser.add_argument(
            "--day", type=int, default=None, help="The day you want to scrape from.",
        )

        args = parser.parse_args()

        return args.year, args.day


if __name__ == "__main__":
    # Config (optional)
    year, day = Args.parser()

    # Start
    md_generator = AdventOfCodeTaskScraper(year=year, day=day)
    md_generator.start()

#!/usr/bin/env python3

import json
import requests
import sys

from bs4 import BeautifulSoup
from openai import OpenAI


class AIScrape:
    """
    A class for scraping and analyzing the content of web pages using OpenAI's GPT models.

    Attributes:
        client (OpenAI): An instance of the OpenAI API client.
        model (str): The model identifier used for GPT completions.

    Methods:
        __init__(**kwargs): Initializes the AIScrape instance with a specified model.
        _begin_end(text): Internal method to determine the beginning and end of the main content of a webpage.
        scrape(url): Public method to scrape and extract the main content of a webpage.
    """

    def __init__(self, **kwargs):
        self.client = OpenAI()
        ## gpt-4-turbo is significantly more expensive and in testing hasn't been necessary
        self.model = kwargs.get("model", "gpt-3.5-turbo")

    def _begin_end(self, text):
        """
        An internal method that uses OpenAI's GPT model to find where the actual content of
        the webpage begins and ends based on the provided text.

        Parameters:
            text (str): The text extracted from a webpage to analyze.

        Returns:
            tuple: A tuple containing two elements:
                   - BEGIN (str): The first 10 words of where the content of the webpage begins.
                   - END (str): The last 10 words of where the main content ends.
        """
        system = "You are a webpage analyzer that finds where the actual content of the webpage begins. When you receive text, return a JSON dict that contains the key 'BEGIN' with the value of the first 10 words of where the content of the webpage begins, and the key 'END' with the value of the last 10 words of where the main content ends"
        messages = [
            {
                "role": "system",
                "content": system,
            },
            {"role": "user", "content": text},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
        )
        data = json.loads(completion.choices[0].message.content)
        return data["BEGIN"], data["END"]

    def scrape(self, url, retries=3):
        """
        Scrapes a webpage, extracts its main content using the GPT model, and provides
        a debugging interface.

        Parameters:
            url (str): The URL of the webpage to scrape.
            retries (int, optional): The number of times to retry the content extraction
                                     if the first attempt fails. Defaults to 3.

        Returns:
            string: The content of the specified webpage.
        """
        text = get_url_text(url)
        begin, end = self._begin_end(text)
        content = None
        retries = min(0, retries)
        while content is None and retries >= 0:
            content = extract_content(text, begin, end)
            retries -= 1
        return content


def extract_content(text, begin, end):
    """
    Extracts and returns a portion of the given text string that lies between specified
    beginning and ending substrings, inclusive of these substrings. If the 'begin' substring
    is found but the 'end' substring is not found after 'begin', the function returns the
    text from 'begin' to the end of the input text. If 'begin' is not found, it returns None.

    Parameters:
    - text (str): The text from which to extract the portion.
    - begin (str): The substring that marks the beginning of the portion to extract.
    - end (str): The substring that marks the end of the portion to extract.

    Returns:
    - str: The extracted text including 'begin' and 'end' if both are found.
    - str: The text from 'begin' to the end of 'text' if 'end' is not found after 'begin'.
    - None: If 'begin' is not found in the text.
    """
    start_index = text.find(begin)

    if start_index == -1:
        return None

    start_index += len(begin)
    end_index = text.find(end, start_index)

    if end_index == -1:
        return text[start_index - len(begin) :]

    return text[start_index - len(begin) : end_index + len(end)]


def get_url_text(url):
    """
    Retrieves the textual content from a specified URL and returns it as a cleaned,
    contiguous string. The function fetches the webpage using an HTTP GET request,
    checks for successful response status, parses the HTML content, and extracts all
    text, removing any excess whitespace.

    Parameters:
    - url (str): The URL of the webpage from which to extract the text.

    Returns:
    - str: A single string containing the extracted text of the webpage, with all
           HTML tags removed and whitespace normalized.

    Raises:
    - requests.HTTPError: If the HTTP request returned an unsuccessful status code.
    - requests.ConnectionError: If there was a problem with the network connection.
    - requests.Timeout: If the request timed out.
    - requests.RequestException: For any other type of exception raised during the HTTP request.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def main():
    aiscrape = AIScrape()
    try:
        url = sys.argv[1]
    except IndexError:
        print(f"Usage: {sys.argv[0]} [url]")
        return 1
    content = aiscrape.scrape(url)
    if content is None:
        print(f"Failed to extract content url: {url}")
        return 2
    print(content)


if __name__ == "__main__":
    main()

# AIScrape

AIScrape is a Python tool for scraping and analyzing web content using OpenAI's GPT models. It leverages the GPT-3.5-turbo by default to identify the main content of webpages and extract it efficiently.

## Description

The `AIScrape` class within the `aiscrape.py` file is designed to initiate with an optional model parameter, use an AI model to determine the start and end of meaningful content on a webpage, and print the extracted content. This tool is useful for extracting clean, main content from any given webpage, avoiding navigation and extraneous information typically found in HTML pages.

## Installation

Before you can use AIScrape, you need to ensure that you have Python installed, along with the `requests` and `bs4` (BeautifulSoup) libraries. If you haven't already set up an OpenAI API key, you will need to do that as well.

1. **Clone this Repository**:
   ```bash
   git clone https://github.com/brosenberg/aiscrape
   cd aiscrape
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements
   ```

3. **Set up OpenAI API Key**:
   - Obtain an API key from OpenAI.
   - Export the API key in your shell or add it to your environment variables:
     ```bash
     export OPENAI_API_KEY='Your-OpenAI-API-Key-Here'
     ```

## Usage

To run AIScrape, you need to pass a URL as a command-line argument:

```bash
python aiscrape.py https://example.com
```

### Troubleshooting

1. **API Key Issues**:
   - Ensure that your OPENAI_API_KEY is set correctly in your environment variables.
   - Check if the API key is active and has the necessary permissions.

2. **Connection Errors**:
   - Verify that the URL is correct and accessible.
   - Ensure your network connection is stable and allows HTTP requests to external sites.

3. **Dependency Errors**:
   - Make sure all required Python packages are installed.
   - Check for compatibility issues between package versions.

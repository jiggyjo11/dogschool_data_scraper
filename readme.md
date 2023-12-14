# Dog School Business Data Extractor

This Python script asynchronously scrapes a list of dog school websites provided in a CSV file, extracts specific business information using OpenAI's GPT-4, and saves this information in a structured CSV format.

## Features

- **Asynchronous Web Scraping**: Fetches content from multiple URLs simultaneously.
- **AI-Powered Data Extraction**: Uses OpenAI's GPT-4 to extract detailed business information.
- **CSV Output**: Outputs the extracted data in an easy-to-use CSV format.

## Requirements

To run this script, you need Python 3.x and the following packages:

- aiohttp
- BeautifulSoup4 (bs4)
- openai
- python-dotenv

You can install these packages using pip:
or

```bash
pip install -r requirements.txt
```

```bash
pip install aiohttp beautifulsoup4 openai python-dotenv
```

## Setup

Clone the Repository to your local machine:

```bash
git clone https://github.com/your-github-username/dog-school-data-extractor.git
cd dog-school-data-extractor
```

## Environment Variables:

Create a .env file in the root directory of the project and add your OpenAI API key:

plaintext
Copy code inside .env

```bash
OPENAI_API_KEY=your_openai_api_key_here´
```

## CSV File:

Prepare a CSV file named urls.csv in the root directory, with each line containing one URL of a dog school website.

## Usage

To run the script, use the following command in the terminal:

bash
Copy code

```bash
python dog_school_data_extractor.py
```

The script will read the URLs from urls.csv, scrape and process each website, and save the extracted information into dogschool_data.csv.

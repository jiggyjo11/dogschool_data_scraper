import aiohttp
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import os
import json
import logging
import csv


load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def get_website_text_async(url, session):
    try:
        async with session.get(url) as response:
            page_content = await response.read()
            soup = BeautifulSoup(page_content, "html.parser")
            return soup.get_text()
    except Exception as e:
        logging.error("Error in async web scraping: %s", e)
        return None


async def process_urls(file_path):
    async with aiohttp.ClientSession() as session:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            tasks = [get_website_text_async(row[0], session) for row in reader]
            websites = await asyncio.gather(*tasks)
            return websites


def gpt_extract_business_data(websiteText):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You help extracting business info from a dog school website impressum. We need dogschool_name, email, dogschool_owner (search for related german word is Inhaber before name), phone_nr, address. Short 3 sentence business overview summary.",
                },
                {"role": "user", "content": websiteText},
            ],
            max_tokens=600,
        )
        logging.info("Received response for website extraction")

    except Exception as e:
        logging.error("Error in website extraction: %s", str(e))

    # print(response)
    choice_object = response.choices[0]
    function_data = choice_object.message.content

    function_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": function_data}],
        functions=[
            {
                "name": "get_business_info",
                "description": "extract the data from business website in a structured way",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dogschool_name": {
                            "type": "string",
                            "description": "The dog schools name",
                        },
                        "dogschool_owner": {
                            "type": "string",
                            "description": "The dog school owner full name",
                        },
                        "phone_nr": {
                            "type": "string",
                            "description": "The dog schools phone nr",
                        },
                        "email": {
                            "type": "string",
                            "description": "The email address of the dog school.",
                        },
                        "address": {
                            "type": "string",
                            "description": "The physical address",
                        },
                        "business_summary": {
                            "type": "string",
                            "description": "Short business summary.",
                        },
                    },
                    "required": [
                        "dogschool_name",
                        "dogschool_owner",
                        "phone_nr",
                        "email",
                        "address",
                        "business_summary",
                    ],
                },
            }
        ],
        function_call={"name": "get_business_info"},
    )
    completion = function_response
    reply_content = completion.choices[0].message
    function_call = reply_content.function_call
    json_string = function_call.arguments

    arguments_dict = json.loads(json_string)
    return arguments_dict


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    try:
        websites_data = asyncio.run(process_urls("urls.csv"))
        with open("dogschool_data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "dogschool_name",
                    "dogschool_owner",
                    "phone_nr",
                    "email",
                    "address",
                    "business_summary",
                ],
            )
            writer.writeheader()
            for website in websites_data:
                if website:
                    business_data = gpt_extract_business_data(website)
                    if business_data:
                        writer.writerow(business_data)
    except Exception as e:
        logging.error("Error in main execution: %s", e)

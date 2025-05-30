import logging
import requests
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

API_URL = "https://ai.qeapps.com/sidekick/post_generate_content_only"
cookies = {
    '_ga_17JT343DSW': 'GS1.1.1743759017.1.0.1743759017.0.0.0',
    '_ga': 'GA1.1.1543127679.1743759017',
    '_clck': 'iwmsvv%7C2%7Cfvh%7C0%7C1926',
    'twk_idm_key': 't5HWpSDJgnDq_5OFblGcb',
    'TawkConnectionTime': '0',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://ai.qeapps.com',
    'priority': 'u=1, i',
    'referer': 'https://ai.qeapps.com/sidekick/?owner=rishabh',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def generate_folder_name():
    return datetime.now().strftime("%Y-%m-%d__%H-%M-%S-%f")[:-3]

def chat_with_gpt(prompt, hash_session="", api_call=1):
    try:
        # This is the inner payload to be sent as actual input content
        inner_payload = {
            "input_content": prompt,
            "api_call": api_call,
            "hash_session": hash_session,
            "aiGpt": "continue",
            "ai_presentation": "@o1"
        }

        outer_payload = {
            "api_call": api_call,
            "folder_name": generate_folder_name(),
            "file_name": "main_chapter.html",
            "bookCheck": "",
            "aiGpt": "",
            "input_content": f"@claude-sonnet-3.7 {json.dumps(inner_payload)}"
        }

        logging.info(f"Final Payload Sent:\n{json.dumps(outer_payload, indent=2)}")

        response = requests.post(API_URL, headers=HEADERS, cookies=cookies, json=outer_payload, timeout=60)

        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"API Error {response.status_code}: {response.text}")
            return f"Error from external API: {response.status_code} - {response.text}"

    except Exception as e:
        logging.exception("Exception during chat_with_gpt")
        return f"Exception occurred: {e}"

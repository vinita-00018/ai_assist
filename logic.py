import logging
import requests
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

API_URL = "https://ai.qeapps.com/sidekick/post_generate_content_only"
cookies = {
    '_clck': 'tuurk7%7C2%7Cfwc%7C0%7C1973',
    'connect.sid': 's%3AYfI7ooqZMSZOgg4Fp7cqxe_kqQ1R-Dpj.rs%2FLqN5aSx6ANq6M1XiE2mCOswvUvp1YyNgf4ldmQ%2BE',
    'TawkConnectionTime': '0',
    'twk_uuid_65a8c13d0ff6374032c19e70': '%7B%22uuid%22%3A%221.1hHY7r9RpAtOmAKbJoN3XjgZqRObPn3R6LzR6QTFQuJRNl8qzOKDNAOhmdwMq8AWA4XvoEnTT7P2LpcfwRvs3NXBf27PqylzHeTcDXOwLNFVd6dRwFh%22%2C%22version%22%3A3%2C%22domain%22%3A%22qeapps.com%22%2C%22ts%22%3A1748589339943%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://ai.qeapps.com',
    'priority': 'u=1, i',
    'referer': 'https://ai.qeapps.com/sidekick/?owner=rishabh',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_clck=tuurk7%7C2%7Cfwc%7C0%7C1973; connect.sid=s%3AYfI7ooqZMSZOgg4Fp7cqxe_kqQ1R-Dpj.rs%2FLqN5aSx6ANq6M1XiE2mCOswvUvp1YyNgf4ldmQ%2BE; TawkConnectionTime=0; twk_uuid_65a8c13d0ff6374032c19e70=%7B%22uuid%22%3A%221.1hHY7r9RpAtOmAKbJoN3XjgZqRObPn3R6LzR6QTFQuJRNl8qzOKDNAOhmdwMq8AWA4XvoEnTT7P2LpcfwRvs3NXBf27PqylzHeTcDXOwLNFVd6dRwFh%22%2C%22version%22%3A3%2C%22domain%22%3A%22qeapps.com%22%2C%22ts%22%3A1748589339943%7D',
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

        response = requests.post(API_URL, headers=headers, cookies=cookies, json=outer_payload, timeout=120)

        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"API Error {response.status_code}: {response.text}")
            return f"Error from external API: {response.status_code} - {response.text}"

    except Exception as e:
        logging.exception("Exception during chat_with_gpt")
        return f"Exception occurred: {e}"

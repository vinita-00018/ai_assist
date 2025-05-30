import streamlit as st
from logic import chat_with_gpt
import json
from datetime import datetime, timedelta
import os
import sys
from bs4 import BeautifulSoup
import requests
import io
import time
import uuid

# === Session Initialization ===
# if "hash_session" not in st.session_state:
#     st.session_state.hash_session = "c5e2ba3f-98fc-479e-83f8-5d052498c354525"

if "hash_session" not in st.session_state:
    st.session_state.hash_session = str(uuid.uuid4())

if "api_call" not in st.session_state:
    st.session_state.api_call = 1

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Extract GPT's Python code from HTML-wrapped output ===
def extract_bot_response(raw_response):
    print(f"Raw Response: {raw_response}")  # Debugging

    if isinstance(raw_response, str):
        try:
            parsed = json.loads(raw_response)
        except json.JSONDecodeError:
            parsed = raw_response

        if isinstance(parsed, dict) and parsed.get("success") and "responseData" in parsed:
            html_content = parsed["responseData"]
            soup = BeautifulSoup(html_content, 'html.parser')
            bot_text = soup.get_text(separator="\n", strip=True)

            # Clean up extra UI words
            bot_response = bot_text.replace("WEB", "").replace("VIDEOS", "").replace("|", "").strip()
            return bot_response
    
    return raw_response

def clean_code_format(code):
    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove UI words like 'Run', '1', '2', ...
        if line.strip().lower() in {"run", "web", "videos"} or line.strip().isdigit():
            continue
        # Comment out or fix any suspicious lines
        if line.strip().startswith("Calculate"):
            cleaned_lines.append("# " + line.strip())
        else:
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


# === Handle User Input and Generate Code ===
def handle_send():
    user_input = st.session_state.input_text
    if user_input:
        st.session_state.chat_history.append({"sender": "You", "content": user_input})

        full_prompt = f"""
        User Question:
        {user_input}
        here is the following information:
        SHOP=qeapptest
        ACCESS_TOKEN=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
        You are a Python coding agent that generates code using the requests library to call the Shopify Admin REST API (2023-10).
        Use requests with the shop and token from environment variables.
        Only return clean Python code (no markdown, no explanations,no loop,no conditional statement).
        The last line must be: print(final_output)
        The variable final_output should hold the data to return.
        """

        max_retries = 10
        retries = 0
        clean_code = ""

        while retries < max_retries:
            try:
                raw_response = chat_with_gpt(full_prompt, st.session_state.hash_session, st.session_state.api_call)
                extracted = extract_bot_response(raw_response)
                clean_code = clean_code_format(extracted)

                if "print(final_output)" in clean_code:
                    break  # Code is complete, proceed to execution
            except Exception as e:
                print(f"Retry {retries + 1} failed with error: {e}")

            retries += 1
            time.sleep(5)  # Short pause before retry

        if "print(final_output)" not in clean_code:
            st.session_state.chat_history.append({"sender": "AI Bot", "content": "Error: Failed to generate complete code after 10 retries."})
            st.session_state.input_text = ""
            return

        # === Execute the cleaned code ===
        try:
            print("\n======= GPT Generated Code =======")
            print(clean_code)
            print("==================================\n")

            output_buffer = io.StringIO()
            sys_stdout_backup = sys.stdout
            sys.stdout = output_buffer

            os.environ["SHOP"] = "qeapptest"
            os.environ["ACCESS_TOKEN"] = "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"

            exec_globals = {
                "__builtins__": __builtins__,
                "os": os,
                "requests": requests,
                "datetime": datetime,
                "timedelta": timedelta
            }
            exec(clean_code, exec_globals)

            sys.stdout = sys_stdout_backup
            final_output = output_buffer.getvalue().strip()
            st.session_state.chat_history.append({"sender": "AI Bot", "content": final_output})

        except Exception as e:
            sys.stdout = sys_stdout_backup
            st.session_state.chat_history.append({"sender": "AI Bot", "content": f"Error during execution: {e}"})

        st.session_state.input_text = ""
        st.session_state.api_call += 1

# === Clear Chat ===
def clear_chat():
    st.session_state.chat_history = []
    st.session_state.input_text = ""
    st.session_state.api_call = 1

# === UI Layout ===
st.title("AI + Shopify Assistant")

for message in st.session_state.chat_history:
    st.markdown(f"**{message['sender']}**: {message['content']}")

st.text_input("You:", key="input_text", placeholder="Ask about orders, customers, products, etc...")
st.button("Send", on_click=handle_send)
st.button("Clear Chat", on_click=clear_chat)

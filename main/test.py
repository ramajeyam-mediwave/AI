from flask import Flask, render_template, request, jsonify
import json
import random
import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_response(user_input, intents):
    user_input = user_input.lower()
    for intent in intents["intents"]:
        if user_input in map(str.lower, intent["patterns"]):
            return random.choice(intent["responses"])

    scraped_response = scrape_website(user_input)
    if scraped_response:
        return scraped_response

    return random.choice(["Theriyala Bro", "crt aaa keelu da", "Oru alavuku thaa bro"])

def scrape_website(query):
    url = f'https://www.mediwavedigital.com/q={query}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        first_paragraph = soup.find('p')
        if first_paragraph:
            return first_paragraph.get_text()

    return None

@app.route("/chat", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg
    gpt_response = get_Chat_response(input_text)

    chatbot_config = load_config('chatbot_config.json')
    intent_response = get_response(input_text, chatbot_config)

    final_response = f"GPT Response: {gpt_response}\nIntent Response: {intent_response}"

    return jsonify({'response': final_response})

def get_Chat_response(text):
    new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = new_user_input_ids

    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.form['msg']
    chatbot_config = load_config('chatbot_config.json')
    bot_response = get_response(user_input, chatbot_config)
    return jsonify({'response': bot_response})

@app.route('/')
def index():
    chatbot_config = load_config('chatbot_config.json')
    return render_template('index.html', chatbot_config=chatbot_config)

if __name__ == '__main__':
    app.run(debug=True)

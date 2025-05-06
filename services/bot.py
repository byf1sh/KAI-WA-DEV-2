import requests

def send(Message):
    token = '7846183880:AAGRBet7B2rYs3T79lzIoKsYXG54gNSEcMo'
    chat_id = '5825923030'
    message = Message
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, data=payload)
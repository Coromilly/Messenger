import requests

response = requests.get('http://127.0.0.1:5000/status')
print(response.text)

print('Введите имя:')
username = input()

print('Введите пароль:')
password = input()

response = requests.post(
    'http://127.0.0.1:5000/auth',
    json={'username': username, 'password': password}
)

if not response.json()['ok']:
    print('Неверный пароль')
    exit()

while True:
    print('Введите сообщение:')
    text = input()
    response = requests.post(
        'http://127.0.0.1:5000/send',
        json={'username': username, 'password': password, 'text': text}
    )
    print()

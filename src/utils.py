import requests


companies = {'VK': '15478', 'Сбер-IT': '3529', 'Yandex': '1740', 'Merlion': '816',
             'Альфа-банк': '80', 'Алабуга': '68587', 'Surf-It': '5998412', 'Тинькофф': '78638',
             'Doubletapp': '3096092', 'Почта Банк': '1049556'}


url = "https://api.hh.ru/vacancies"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def get_vacancies(vacancy):
    params = {"text": vacancy}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"'Ошибка при обращении к API:', {response.status_code}")
        return []


print(get_vacancies('python'))

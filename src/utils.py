import requests
import psycopg2

companies = {'VK': '15478', 'Сбер-IT': '3529', 'Yandex': '1740', 'Merlion': '816',
             'Альфа-банк': '80', 'Алабуга': '68587', 'Surf-It': '5998412', 'Тинькофф': '78638',
             'Doubletapp': '3096092', 'Почта Банк': '1049556'}

url = "https://api.hh.ru/vacancies"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def get_vacancies(vacancy_name, employer_id):
    params = {"text": vacancy_name,
              'employer_id': employer_id,
              'per_page': 100}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"'Ошибка при обращении к API:', {response.status_code}")
        return []


def employers_list(vacancies):
    """
    Возвращает имя и id работодателя в виде кортежа
    :param vacancies: Полученные через API запрос данные о вакансиях
    :return: Имя и id работодателя
    """
    if len(vacancies) == 0:
        return []
    else:
        vac = vacancies[0]
        return vac['employer']['id'], vac['employer']['name']


def vacancies_list(vacancies):
    """
    Возвращает список кортежей с данными о вакансиях работодателя
    :param vacancies: Полученные через API запрос данные о вакансиях
    :return: Список кортежей с данными о вакансиях
    """
    vac_lst = []
    for vac in vacancies:
        vac = (vac['id'],
               vac['employer']['id'],
               vac['name'],
               vac['salary'] if vac['salary'] is not None else 'NULL',
               vac['published_at'],
               vac['snippet']['requirement'],
               vac['experience']['name']
               )
        vac_lst.append(vac)
    return vac_lst


def create_tables():
    """
    Создает таблицы работодатель и вакансии работодателя
    :return: None
    """
    conn = psycopg2.connect(host='localhost',
                            database='vacancies',
                            user='postgres',
                            password='12345')

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                    employer_id int PRIMARY KEY,
                    company_name varchar
                    )""")
                cur.execute("""
                    CREATE TABLE vacancies (
                    vacancy_id int PRIMARY KEY,
                    employer_id int REFERENCES employers(employer_id),
                    vacancy_name varchar(100),
                    salary varchar,
                    published date,
                    requirements text,
                    experience varchar(30)
                    )""")
    finally:
        conn.close()


def filling_database(employer, vacancies, db_name):
    conn = psycopg2.connect(host='localhost',
                            database=db_name,
                            user='postgres',
                            password='12345')

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO employers VALUES (%s, %s)', employer)
                count = 0
                for vac in vacancies:
                    print(vac)
                    cur.executemany('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)', vac)
                    count += 1
                    print(count)
    finally:
        conn.close()


v = get_vacancies('python', '1740')
print(vacancies_list(v))
vac = vacancies_list(v)
emp = employers_list(v)
filling_database(emp, vac, 'vacancies')
import requests
import psycopg2


url = "https://api.hh.ru/vacancies"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def get_vacancies(vacancy_name, employer_id):
    """
    Возвращает все вакансии работодателя по API запросу
    :param vacancy_name: Название искомой вакансии
    :param employer_id: Id работодателя на сайте hh.ru
    :return:
    """
    all_vacancies = []
    params = {"text": vacancy_name,
              'employer_id': employer_id,
              'per_page': 100}
    total_pages = requests.get(url, headers=headers, params=params).json()["pages"]

    for i in range(total_pages):
        params = {"text": vacancy_name,
                  'employer_id': employer_id,
                  'per_page': 100,
                  'page': i}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            vacs = response.json().get("items", [])
            all_vacancies.extend(vacs)
        else:
            print(f"'Ошибка при обращении к API:', {response.status_code}")
    return all_vacancies


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
               vac['salary'].get('from', None) if vac['salary'] is not None else None,
               vac['salary'].get('to', None) if vac['salary'] is not None else None,
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
                    employer_id varchar(20) PRIMARY KEY,
                    company_name varchar
                    )""")
                cur.execute("""
                    CREATE TABLE vacancies (
                    vacancy_id varchar(20) PRIMARY KEY,
                    employer_id varchar(20) REFERENCES employers(employer_id),
                    vacancy_name varchar(200),
                    salary_from varchar,
                    salary_to varchar,
                    published date,
                    requirements text,
                    experience varchar(30)
                    )""")
    finally:
        conn.close()


def filling_database(employer, vacancies):
    """
    Заполняет таблицы "employers" и "vacancies" базы данных "vacancies"
    :param employer: Данные работодателя
    :param vacancies: Данные вакансий рабоодателя
    :return: None
    """
    conn = psycopg2.connect(host='localhost',
                            database='vacancies',
                            user='postgres',
                            password='12345')

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO employers VALUES (%s, %s)', employer)
                for vac in vacancies:
                    print(vac)
                    cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', vac)
    finally:
        conn.close()

from src.utils import (get_vacancies, employers_list, vacancies_list, filling_database, create_tables)
from src.processing import db_operations

companies = {'VK': '15478', 'Сбер-IT': '3529', 'Yandex': '1740', 'Merlion': '816',
             'Альфа-банк': '80', 'Алабуга': '68587', 'Surf-It': '5998412', 'Тинькофф': '78638',
             'Doubletapp': '3096092', 'Почта Банк': '1049556'}


def main():
    print('Приветствую! Введите название базы данных, к которой хотите подключиться')
    user_input_db = input(':')

    print('Продолжить с заполнением базы данных? (y/n)')
    user_input = input().lower()

    if user_input == 'y':
        try:
            create_tables(user_input_db)
            print('По какому ключевому слову производить поиск вакансий?')
            vacancy_name = input(':').lower()

            print('Идет заполнение базы данных')
            for company in companies.values():
                vacancies = get_vacancies(vacancy_name, company)
                if len(vacancies) == 0:
                    continue
                vac = vacancies_list(vacancies)
                emp = employers_list(vacancies)
                filling_database(emp, vac, user_input_db)

            db_operations(user_input_db)

        except Exception as e:
            print(e)

    elif user_input == 'n':
        db_operations(user_input_db)


if __name__ == '__main__':
    main()

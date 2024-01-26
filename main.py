from src.utils import (get_vacancies, employers_list, vacancies_list, filling_database, create_tables)


companies = {'VK': '15478', 'Сбер-IT': '3529', 'Yandex': '1740', 'Merlion': '816',
             'Альфа-банк': '80', 'Алабуга': '68587', 'Surf-It': '5998412', 'Тинькофф': '78638',
             'Doubletapp': '3096092', 'Почта Банк': '1049556'}


def main():
    create_tables()
    vacancy_name = 'python'

    for company in companies.values():
        vacancies = get_vacancies(vacancy_name, company)
        if len(vacancies) == 0:
            continue
        vac = vacancies_list(vacancies)
        emp = employers_list(vacancies)

        filling_database(emp, vac)


if __name__ == '__main__':
    main()

from src.utils import (get_vacancies, employers_list, vacancies_list, filling_database, create_tables)


def main():
    vacancies = get_vacancies('python', '1740')
    vac = vacancies_list(vacancies)
    emp = employers_list(vacancies)
    create_tables()
    filling_database(emp, vac, 'vacancies')


if __name__ == '__main__':
    main()

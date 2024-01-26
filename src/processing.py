from src.db_manager import DBManager


def db_operations(user_input_db):
    """
    Исполняет операции с базами данных, часть кода main
    :param user_input_db: База данных пользователя
    :return: None
    """
    hh = DBManager('localhost', user_input_db,
                   'postgres', '12345')
    while True:
        print("""\nВыберите действие для исполнения:
    1. Получить список всех компаний и количество вакансий у каждой компании.
    2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    3. Получить среднюю зарплату по вакансиям.
    4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова (например python).
    6. Получить список последних 50-ти опубликованных вакансий.
    7. Получить среднюю зарплату работодателя по вакансиям.
    8. Выход.
    """)
        user_input = input(':')
        if user_input == '1':
            result = hh.get_companies_and_vacancies_count()
            print(*result, sep='\n')
        elif user_input == '2':
            result = hh.get_all_vacancies()
            print(*result, sep='\n')
        elif user_input == '3':
            result = hh.get_avg_salary()
            print(result)
        elif user_input == '4':
            result = hh.get_vacancies_with_higher_salary()
            print(*result, sep='\n')
        elif user_input == '5':
            print('Введите ключевое слово для поиска')
            user_input = input(':')
            result = hh.get_vacancies_with_keyword(user_input)
            print(*result, sep='\n')
        elif user_input == '6':
            result = hh.get_vacancies_by_date()
            print(*result, sep='\n')
        elif user_input == '7':
            result = hh.get_avg_salary_by_employers()
            print(*result, sep='\n')
        elif user_input == '8':
            break

import psycopg2


class DBManager:
    def __init__(self, host, database_name, user, password):
        self.conn = psycopg2.connect(host=host,
                                     database=database_name,
                                     user=user,
                                     password=password)

    def get_companies_and_vacancies_count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT company, COUNT(vacancy) FROM vacancies GROUP BY company")
        companies_and_vacancies = cursor.fetchall()
        cursor.close()
        return companies_and_vacancies

    def get_all_vacancies(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT company, vacancy, salary, link FROM vacancies")
        all_vacancies = cursor.fetchall()
        cursor.close()
        return all_vacancies

    def get_avg_salary(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT AVG(salary) FROM vacancies")
        avg_salary = cursor.fetchone()[0]
        cursor.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        cursor = self.conn.cursor()
        cursor.execute("SELECT company, vacancy, salary, link FROM vacancies WHERE salary > %s", (avg_salary,))
        high_salary_vacancies = cursor.fetchall()
        cursor.close()
        return high_salary_vacancies

    def get_vacancies_with_keyword(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute("SELECT company, vacancy, salary, link FROM vacancies WHERE LOWER(vacancy) LIKE %s",
                       ('%' + keyword.lower() + '%',))
        keyword_vacancies = cursor.fetchall()
        cursor.close()
        return keyword_vacancies


hh = DBManager('localhost', 'HH_vacancies_DB',
               'postgres', '12345')

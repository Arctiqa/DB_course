import psycopg2


class DBManager:
    def __init__(self, host, database_name, user, password):
        self.conn = psycopg2.connect(host=host,
                                     database=database_name,
                                     user=user,
                                     password=password)

    def get_companies_and_vacancies_count(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT employers.company_name, COUNT(vacancy_name) FROM employers
                       JOIN vacancies ON employers.employer_id = vacancies.employer_id
                       GROUP BY employers.company_name""")
        companies_and_vacancies = cursor.fetchall()
        cursor.close()
        return companies_and_vacancies

    def get_all_vacancies(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT employers.company_name, vacancy_name, salary_from, salary_to, url 
        FROM employers 
        JOIN vacancies ON employers.employer_id = vacancies.employer_id""")
        all_vacancies = cursor.fetchall()
        cursor.close()
        return all_vacancies

    def get_avg_salary(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT AVG(salary_to) FROM vacancies")
        avg_salary = cursor.fetchone()[0]
        cursor.close()
        return avg_salary

    def get_avg_salary_by_employers(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT employers.company_name, AVG(vacancies.salary_to) FROM employers
        JOIN vacancies ON employers.employer_id = vacancies.employer_id
        GROUP BY employers.company_name, vacancies.employer_id
        """)
        avg_salary = cursor.fetchall()
        cursor.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT employers.company_name, vacancy_name, salary_from, salary_to, published
        FROM employers
        JOIN vacancies ON employers.employer_id = vacancies.employer_id
        WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)
        """)
        high_salary_vacancies = cursor.fetchall()
        cursor.close()
        return high_salary_vacancies

    def get_vacancies_with_keyword(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT employers.company_name, vacancy_name, salary_from, salary_to, published, requirements, experience
        FROM employers
        JOIN vacancies ON employers.employer_id = vacancies.employer_id
        WHERE LOWER(vacancy_name) LIKE '%{keyword}%'
        """)
        keyword_vacancies = cursor.fetchall()
        cursor.close()
        return keyword_vacancies

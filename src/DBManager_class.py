import psycopg2
from config import config


class DBManager:
    """
    Класс, который подключается к БД PostgreSQL и работает с ним
    """

    def __init__(self, db_name, params=config()):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Метод получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.curs() as cur:
            cur.execute('SELECT name_company, COUNT(*)'
                           'FROM companies'
                           'JOIN vacancies USING (company_id) '
                           'GROUP BY name_company;')

            data = cur.fetchall()
        conn.close()
        return data

    def get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.curs() as cur:
            cur.execute('SELECT name_vacancy, name_company, salary, url'
                           'FROM vacancies'
                           'JOIN companies USING (company_id);')

            data = cur.fetchall()
        conn.close()
        return data

    def get_avg_salary(self):
        """
        Метод получает среднюю зарплату по вакансиям
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.curs() as cur:
            cur.execute('SELECT AVG(salary_average)'
                           'FROM vacancies'
                           'WHERE salary_average > 0;')

            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.curs() as cur:
            cur.execute('SELECT * '
                           'FROM vacancies'
                           'WHERE salary > (SELECT AVG(salary) FROM vacancies);')

            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_keyword(self):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.curs() as cur:
            cur.execute(f"""
                        SELECT * 
                        FROM vacancies
                        WHERE lower(title_vacancy) LIKE '%{keyword}%'
                        OR lower(title_vacancy) LIKE '%{keyword}'
                        OR lower(title_vacancy) LIKE '{keyword}%'""")

            data = cur.fetchall()
            conn.close()
            return data
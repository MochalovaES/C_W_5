import psycopg2
from config import config


class DBManager:
    """
    Класс, который подключается к БД PostgresSQL и работает с ним
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

        with conn.cursor() as cur:
            cur.execute("SELECT name_company, COUNT(*) FROM companies JOIN vacancies USING (company_id) GROUP BY name_company;")

            data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT name_vacancy, name_company, salary, url_vacancies FROM vacancies JOIN companies USING (company_id);""")

            data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def get_avg_salary(self):
        """
        Метод получает среднюю зарплату по вакансиям
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary) FROM vacancies WHERE salary > 0;""")

            data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies);""")

            data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, word):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :return:
        """
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT name_company, name_vacancy, salary, url_vacancies
        FROM vacancies
        JOIN companies USING (company_id)
        WHERE name_vacancy LIKE '%{word.lower()}%' OR name_vacancy LIKE '%{word.title()}%' OR name_vacancy LIKE '%{word.upper()}%';""")

            data = cur.fetchall()
            cur.close()
            conn.close()
            return data

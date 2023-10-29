import json
import os
import psycopg2
from src.Vacancy_class import Vacancy

vacancy = Vacancy()


def load_jsonfile(filename: str):
    """
    Функция загружает данные из файла JSON
    """
    with open(filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data


def create_database(params, db_name) -> None:
    """
    Создает новую базу данных.
    """
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f'CREATE DATABASE {db_name}')

    conn.close()


def create_tables(db_name, params):
    """
    Функция создает таблицы в БД
    """
    conn = psycopg2.connect(database=db_name, **params)

    with conn.curs() as cur:
        cur.execute('CREATE TABLE companies('
                       'company_id int PRIMARY KEY,'
                       'name_company varchar(50) NOT NULL'
                       'url_vacancies varchar(200) NOT NULL)')

        cur.execute('CREATE TABLE vacancies('
                       'company_id int PRIMARY KEY REFERENCES companies (company_id) NOT NULL,'
                       'name_vacancy varchar(150) NOT NULL,'
                       'salary int,'
                       'url varchar(200) NOT NULL,'
                       'description text')

    conn.commit()
    conn.close()


def insert_data_companies(db_name, params):

    conn = psycopg2.connect(database=db_name, **params)

    with conn.curs() as cur:
        cur.execute('INSERT INTO companies (company_id, name_company, url_vacancies)'
                    'VALUES (%s, %s, %s)'
                    'returning company_id',
                     (int(data["employer"]["id"],
                      data["employer"]["name"]),
                      data["employer"]["alternate_url"]))

        company_id = cur.fetchone()[0]

        cur.execute('INSERT INTO vacancies (company_id, name_vacancy, salary, url, description)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (company_id,
                     vacancy.name_vacancy,
                     vacancy.salary_vacancy,
                     vacancy.url_vacancy,
                     vacancy.info_vacancy))

    conn.commit()
    conn.close()








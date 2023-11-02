import json
import psycopg2


def load_jsonfile(filename: str):
    """
    Функция загружает данные из файла JSON
    """
    with open(filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data


def create_database(db_name, params) -> None:
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

    with conn.cursor() as cur:
        cur.execute('CREATE TABLE companies('
                    'company_id int PRIMARY KEY,'
                    'name_company varchar(50) NOT NULL)')

        cur.execute('CREATE TABLE vacancies('
                    'company_id int,'
                    'name_vacancy varchar(150) NOT NULL,'
                    'salary int,'
                    'url_vacancies varchar(200) NOT NULL,'
                    'description text)')

    conn.commit()
    conn.close()


def insert_data_companies(db_name, params, name_company, id_company):

    conn = psycopg2.connect(database=db_name, **params)

    with conn.cursor() as cur:
        cur.execute('INSERT INTO companies (company_id, name_company)'
                    'VALUES (%s, %s)'
                    'returning company_id',
                    (id_company,
                     name_company))
    conn.commit()
    conn.close()


def insert_data_vacancies(db_name, params, list_data):

    conn = psycopg2.connect(database=db_name, **params)

    with conn.cursor() as cur:

        cur.execute('INSERT INTO vacancies (company_id, name_vacancy, salary, url_vacancies, description)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (list_data[0],
                     list_data[2],
                     list_data[4],
                     list_data[3],
                     list_data[5]))

    conn.commit()
    conn.close()

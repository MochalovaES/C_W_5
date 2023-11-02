from config import config
from src.API_class import HeadHunterAPI
from src.DBManager_class import DBManager
from utils import create_database, create_tables, insert_data_companies, load_jsonfile, insert_data_vacancies


def main():
    db_name = 'job_vacancies'
    json_file = 'data/selected_companies.json'
    companies = load_jsonfile(json_file)
    params = config()
    conn = None
    create_database(db_name, params) # Создание БД
    create_tables(db_name, params)  # Создание таблиц
    hh_api = HeadHunterAPI()
    for company in companies:
        insert_data_companies(db_name, params, company['name'], company['id'])
        hh_api.add_employer(company['id'])
        json_list = hh_api.get_vacancies()
        vacancies_list = hh_api.get_parsing(json_list)
        for vacancy in vacancies_list:
            insert_data_vacancies(db_name, params, vacancy)

    db_manager = DBManager(db_name, params)

    db_manager.get_companies_and_vacancies_count()
    db_manager.get_all_vacancies()
    db_manager.get_avg_salary()
    db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword('python')


if __name__ == '__main__':
    main()

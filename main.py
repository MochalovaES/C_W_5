from config import config
from src.API_class import HeadHunterAPI
from src.DBManager_class import DBManager
from utils import create_database, create_tables, insert_data_companies, load_jsonfile


def main():
    db_name = 'job_vacancies'
    json_file = 'data/selected_companies.json'
    companies = load_jsonfile(json_file)
    params = config()
    conn = None
    hh_api = HeadHunterAPI()
    create_database(db_name, params)
    create_tables(db_name, params)
    insert_data_companies(db_name, params)

    db_manager = DBManager(db_name, params)

    db_manager.get_companies_and_vacancies_count()
    db_manager.get_all_vacancies()
    db_manager.get_avg_salary()
    db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword('python')


if __name__ == '__main__':
    main()

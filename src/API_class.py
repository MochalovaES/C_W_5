import requests
import copy

class HeadHunterAPI:
    """
    Класс получает данные о работодателях и их вакансиях с сайта hh.ru
    """
    HH_API_URL = 'https://api.hh.ru/vacancies'
    param_zero = {
        'period': 14,
        'per_page': 100
    }

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):
        response = requests.get(self.HH_API_URL, self.param)
        json_list = response.json()['items']
        return json_list

    def get_parssing(self, json_list):
        vacancy_list = []
        for item in json_list:
            name_vacancy = item['name']
            url_vacancy = 'Нет информации'
            if 'vacancies_url' == item['employer']:
                url_vacancy = item['employer']['vacancies_url']
            salary_vacancy_min = 0
            salary_vacancy_max = 0
            if item['salary'] is not None:
                if item['salary']['from'] is not None:
                    salary_vacancy_min = int(item['salary']['from'])
                if item['salary']['to'] is not None:
                    salary_vacancy_max = int(item['salary']['to'])
            salary_vacancy = 0
            if salary_vacancy_min != 0 and salary_vacancy_max != 0:
                salary_vacancy = round((salary_vacancy_min + salary_vacancy_max) / 2)
            elif salary_vacancy_min == 0:
                salary_vacancy = salary_vacancy_max
            elif salary_vacancy_max == 0:
                salary_vacancy = salary_vacancy_min
            info_vacancy = ''
            if item['snippet']['responsibility'] is not None:
                info_vacancy += "Обязанности:" + item['snippet']['responsibility'] + "\n"
            if item['snippet']['requirement'] is not None:
                info_vacancy += "Требования:" + item['snippet']['requirement']
            vacancy = [name_vacancy, url_vacancy, salary_vacancy, info_vacancy]
            vacancy_list.append(vacancy)
        return vacancy_list

    def add_words(self, words):
        self.param['text'] = words
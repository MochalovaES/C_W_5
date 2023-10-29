class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, name_vacancy, url_vacancy, salary_vacancy, info_vacancy):
        self.name_vacancy = name_vacancy
        self.url_vacancy = url_vacancy
        self.salary_vacancy = salary_vacancy
        self.info_vacancy = info_vacancy

    def __str__(self):
        return f"""Вакансия: {self.name_vacancy}
Ссылка на вакансию: {self.url_vacancy}  
Предложения по зар.плате вакансии: {self.salary_vacancy}
Информация по вакансии: {self.info_vacancy}      
"""
import requests
from datetime import datetime


class HeadHunterAPI:
    """
    Класс для работы с API сайта hh.ru
    """
    def __init__(self, keyword):
        self.keyword = keyword

    def get_employers(self):
        """
        Метод для получения списка работодателей с сайта hh.ru
        """
        v_hh = []
        url = 'https://api.hh.ru/employers'
        params = {
            'page': 1,
            # количество работодателей = 10
            'per_page': 10,
            'text': self.keyword,
            # выбираем работодателей из России (id = 113)
            'area': 113,
            'type': "company",
            'only_with_vacancies': True
        }
        response = requests.get(url, params=params).json()
        v_hh.extend(response['items'])
        return v_hh

    def get_formatted_employers(self):
        """
        Метод для получения отформатированного списка работодателей с сайта hh.ru
        """
        formatted_e_hh = []
        for employer in self.get_employers():
            formatted_e_hh.append({
                'id': employer['id'],
                'name': employer['name'],
                'url': employer['alternate_url'],
                'vacancies_url': employer['vacancies_url'],
                'open_vacancies': employer['open_vacancies']
            })
        return formatted_e_hh

    def get_employers_id(self):
        """
        Метод для получения id работодателей с сайта hh.ru
        """
        employers_id = []
        for employer in self.get_employers():
            employers_id.append(employer['id'])
        return employers_id

    def get_vacancies(self):
        """
        Метод для получения списка вакансий заданных работодателей с сайта hh.ru
        """
        v_hh = []
        # число вакансий = 1000
        for page in range(1, 11):
            url = 'https://api.hh.ru/vacancies'
            params = {
                'page': page,
                'per_page': 100,
                'employer_id': self.get_employers_id(),
                'type': 'open'
            }
            response = requests.get(url, params=params).json()
            v_hh.extend(response['items'])
        return v_hh

    def get_formatted_vacancies(self):
        """
        Метод для получения отформатированного списка вакансий заданных работодателей с сайта hh.ru
        """
        formatted_v_hh = []
        for vacancy in self.get_vacancies():
            try:
                formatted_v_hh.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'url': vacancy['alternate_url'],
                    'salary_from': vacancy['salary']['from'],
                    'salary_to': vacancy['salary']['to'],
                    'salary_cur': vacancy['salary']['currency'].lower(),
                    'employer_id': vacancy['employer']['id'],
                    'employer_name': vacancy['employer']['name'],
                    'requirement': vacancy['snippet']['requirement'],
                    'experience': vacancy['experience']['name'],
                    'employment': vacancy['employment']['name'],
                    'area': vacancy['area']['name'],
                    'source': 'hh.ru'
                })
            except TypeError:
                formatted_v_hh.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'url': vacancy['alternate_url'],
                    'salary_from': None,
                    'salary_to': None,
                    'salary_cur': None,
                    'employer_id': vacancy['employer']['id'],
                    'employer_name': vacancy['employer']['name'],
                    'requirement': vacancy['snippet']['requirement'],
                    'experience': vacancy['experience']['name'],
                    'employment': vacancy['employment']['name'],
                    'area': vacancy['area']['name'],
                    'source': 'hh.ru'
                })
        return formatted_v_hh

    @staticmethod
    def get_currency_rate():
        """
        Метод для получения курса валюты заработной платы к российскому рублю
        """
        current_date = datetime.now().date()
        url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/' + str(current_date) + '/currencies/rub.json'
        response = requests.get(url).json()
        currency_rate = response['rub']
        return currency_rate
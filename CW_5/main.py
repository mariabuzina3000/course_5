from utils import create_database, save_employer_data_to_database, save_vacancy_data_to_database, \
    save_currency_data_to_database
from config import config
from HHAPI import HeadHunterAPI


def main():
    # создаем экземпляр класса HeadHunterAPI для поиска вакансий по банкам
    hh_api = HeadHunterAPI('банк')
    # получаем данные о работодателях и их вакансиях с сайта hh.ru, а также данные о курсах валют
    employer_data = hh_api.get_formatted_employers()
    vacancy_data = hh_api.get_formatted_vacancies()
    currency_data = HeadHunterAPI.get_currency_rate()
    # создаем БД и таблицы
    params = config()
    create_database('hh_vacancies', params)
    # сохраняем данные о работодателях, их вакансиях и курсах валют в БД
    save_employer_data_to_database(employer_data, 'hh_vacancies', params)
    save_vacancy_data_to_database(vacancy_data, 'hh_vacancies', params)
    save_currency_data_to_database(currency_data, 'hh_vacancies', params)


if __name__ == '__main__':
    main()

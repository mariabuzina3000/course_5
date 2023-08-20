import psycopg2
from config import config


class DBManager:
    """
    Класс для работы с данными в БД
    """

    @staticmethod
    def get_companies_and_vacancies_count(database_name: str, params: dict):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT employer_name, vacancies_cnt FROM employers
            """)
            rows = cur.fetchall()
            for row in rows:
                print(row)

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_vacancies(database_name: str, params: dict):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                employer_name,
                vacancy_name,
                salary_from * currency_rate AS salary_from,
                salary_to * currency_rate AS salary_to,
                vacancy_url
                FROM vacancies
                INNER JOIN employers USING (employer_id)
                LEFT JOIN currency_rates
                ON (CASE WHEN vacancies.salary_cur = 'rur' THEN 'rub'
                ELSE vacancies.salary_cur
                END) = currency_rates.currency_id
            """)
            rows = cur.fetchall()
            for row in rows:
                print(row)

        conn.commit()
        conn.close()

    @staticmethod
    def get_avg_salary(database_name: str, params: dict):
        """
        Получает среднюю зарплату по вакансиям
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ROUND(AVG(salary_from * currency_rate)) AS avg_salary
                FROM vacancies
                LEFT JOIN currency_rates
                ON (CASE WHEN vacancies.salary_cur = 'rur' THEN 'rub'
                ELSE vacancies.salary_cur
                END) = currency_rates.currency_id
                WHERE salary_from IS NOT NULL
            """)
            rows = cur.fetchall()
            for row in rows:
                print(row)

        conn.commit()
        conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary(database_name: str, params: dict):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies
                LEFT JOIN currency_rates
                ON (CASE WHEN vacancies.salary_cur = 'rur' THEN 'rub'
                ELSE vacancies.salary_cur
                END) = currency_rates.currency_id
                WHERE salary_from * currency_rate >
                (SELECT ROUND(AVG(salary_from * currency_rate)) AS avg_salary
                FROM vacancies
                LEFT JOIN currency_rates
                ON (CASE WHEN vacancies.salary_cur = 'rur' THEN 'rub'
                ELSE vacancies.salary_cur
                END) = currency_rates.currency_id
                WHERE salary_from IS NOT NULL)
            """)
            rows = cur.fetchall()
            for row in rows:
                print(row)

        conn.commit()
        conn.close()

    @staticmethod
    def get_vacancies_with_keyword(database_name: str, params: dict, key_word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{key_word}%'")
            rows = cur.fetchall()
            for row in rows:
                print(row)

        conn.commit()
        conn.close()


params = config()
DBManager.get_companies_and_vacancies_count('hh_vacancies', params)
DBManager.get_all_vacancies('hh_vacancies', params)
DBManager.get_avg_salary('hh_vacancies', params)
DBManager.get_vacancies_with_higher_salary('hh_vacancies', params)
DBManager.get_vacancies_with_keyword('hh_vacancies', params, 'разработчик')
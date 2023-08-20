import psycopg2
from datetime import datetime


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях, вакансиях и курсах валют."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                employer_name VARCHAR(255),
                employer_url TEXT,
                vacancies_url TEXT,
                vacancies_cnt INT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name TEXT,
                vacancy_url TEXT,
                salary_from INT,
                salary_to INT,
                salary_cur VARCHAR(10),
                experience TEXT,
                employment VARCHAR(50),
                area VARCHAR(50)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE currency_rates (
                currency_id VARCHAR(10),
                currency_rate float,
                date DATE
            )
        """)

    conn.commit()
    conn.close()


def save_employer_data_to_database(employer_data: list, database_name: str, params: dict):
    """Сохранение данных о работодателях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employer_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, employer_url, vacancies_url, vacancies_cnt)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (employer['id'], employer['name'], employer['url'],
                 employer['vacancies_url'], employer['open_vacancies'])
            )

    conn.commit()
    conn.close()


def save_vacancy_data_to_database(vacancy_data: list, database_name: str, params: dict):
    """Сохранение данных о вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in vacancy_data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, vacancy_url, 
                salary_from, salary_to, salary_cur, experience, employment, area)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id'], vacancy['employer_id'], vacancy['name'], vacancy['url'],
                 vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_cur'],
                 vacancy['experience'], vacancy['employment'], vacancy['area'])
            )

    conn.commit()
    conn.close()


def save_currency_data_to_database(currency_data: dict, database_name: str, params: dict):
    """Сохранение данных о курсах валют в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)
    current_date = datetime.now().date()

    with conn.cursor() as cur:
        for currency, rate in currency_data.items():
            cur.execute(
                """
                INSERT INTO currency_rates (currency_id, currency_rate, date)
                VALUES (%s, %s, %s)
                """,
                (currency, rate, current_date)
            )

    conn.commit()
    conn.close()
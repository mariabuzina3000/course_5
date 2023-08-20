--удаление БД
DROP DATABASE hh_vacancies;

--создание БД
CREATE DATABASE hh_vacancies;

--создание таблицы employers
CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                employer_name VARCHAR(255),
                employer_url TEXT,
                vacancies_url TEXT,
                vacancies_cnt INT
            );

--создание таблицы vacancies
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
            );

--создание таблицы currency_rates
CREATE TABLE currency_rates (
                currency_id VARCHAR(10),
                currency_rate float,
                date DATE
            );

--получает список всех компаний и количество вакансий у каждой компании
SELECT employer_name, vacancies_cnt FROM employers;

--получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
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
END) = currency_rates.currency_id;

--получает среднюю зарплату по вакансиям
SELECT ROUND(AVG(salary_from * currency_rate)) AS avg_salary
FROM vacancies
LEFT JOIN currency_rates
ON (CASE WHEN vacancies.salary_cur = 'rur' THEN 'rub'
ELSE vacancies.salary_cur
END) = currency_rates.currency_id
WHERE salary_from IS NOT NULL;

--получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
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
WHERE salary_from IS NOT NULL);

--получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
SELECT * FROM vacancies
WHERE vacancy_name LIKE '%разработчик%';
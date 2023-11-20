# Диплом
[![Automated tests](https://github.com/Chifir31/diplom/actions/workflows/run_tests.yml/badge.svg)](https://github.com/Chifir31/diplom/actions/workflows/run_tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Chifir31/diplom/badge.svg?branch=master)](https://coveralls.io/github/Chifir31/diplom?branch=master)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Chifir31_diplom&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Chifir31_diplom)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Chifir31_diplom&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Chifir31_diplom)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Chifir31_diplom&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Chifir31_diplom)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Chifir31_diplom&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Chifir31_diplom)

# Аттестационное тестирование
**Тест А1 (положительный)**
- Начальное состояние: Сервер запущен.
- Действие: Пользователь заходит на Начальную страницу.
- Ожидаемый результат: У пользователя открывается Начальная страница.

**Тест А2 (положительный)**
- Начальное состояние: Пользователь находится на любой странице.
- Действие: Пользователь выбирает в навигационном меню раздел "Информация о профессиях".
- Ожидаемый результат: У пользователя открывается страница "Информация о профессиях" со списком профессий.

**Тест А3 (положительный)**
- Начальное состояние: Пользователь находится на странице "Информация о профессиях" со списком профессий.
- Действие: Пользователь выбирает какую-то профессию.
- Ожидаемый результат: У пользователя открывается страница с информацией о выбранной профессии.

**Тест А4 (положительный)**
- Начальное состояние: Пользователь находится на любой странице.
- Действие: Пользователь выбирает в навигационном меню раздел "Сравнение профессий".
- Ожидаемый результат: У пользователя открывается страница, содержащая форму для сравнения профессий.

**Тест А5 (положительный)**
- Начальное состояние: Пользователь находится на странице "Сравнение профессий".
- Действие: Пользователь корректно заполняет форму сравнения профессий.
- Ожидаемый результат: У пользователя открывается страница с результатами сравнения.

**Тест А6 (положительный)**
- Начальное состояние: Пользователь находится на странице "Сравнение профессий".
- Действие: Пользователь некорректно заполняет форму сравнения профессий.
- Ожидаемый результат: В форме появляется текст об ошибке, что введенные профессии не найдены.

**Тест А7 (положительный)**
- Начальное состояние: Пользователь находится на любой странице.
- Действие: Пользователь выбирает в навигационном меню раздел "Поиск по знаниям и умениям".
- Ожидаемый результат: У пользователя открывается страница "Поиск по знаниям и умениям".

**Тест А8 (положительный)**
- Начальное состояние: Пользователь находится на странице "Поиск по знаниям и умениям".
- Действие:  Пользователь заполняет форму для поиск по знаниям и умениям.
- Ожидаемый результат: У пользователя открывается страница с результатами поиска.

**Тест А9 (положительный)**
- Начальное состояние: Пользователь находится на странице с результатами поиска по знаниям и умениям.
- Действие:  Пользователь выбирает профессию в таблице.
- Ожидаемый результат: У пользователя открывается страница с информацией о выбранной профессии.

# Блочное тестирование

## Класс ComparisonOfFormulations

**Тест Б1 (положительный)**
- Описание: Проверка корректности метода-инициализатора.
- Метод: *\_\_init\_\_*.
- Входные данные: Отсутстувуют.
- Ожидаемый результат: Создан экземпляр класса, где свойства класса *formulations1* и *formulations2* равны {}.

# Интеграционное тестирование

**Тест И1 (положительный)**
- Взаимодействие классов: *Comparison_Of_Formulations*, *Professional_Standard*.
- Описание: Тест проверяет, что свойство *__knowledge_embeddings* класса *Professional_Standard* подходит в качестве исходных данных для метода *find_similar_formulationsV1()  класса *Comparison_Of_Formulations**.
- Метод: *find_similar_formulationsV1()*.
- Входные данные: *formulations1* = *Professional_Standard.get_knowledge_with_embeddings*, *formulations2* = *Professional_Standard.get_knowledge_with_embeddings*.
- Ожидаемый результат: Списки схожих и идентичных формулировок.

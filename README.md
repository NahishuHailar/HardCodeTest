
# Тестовое задание Django/Backend


Проект представляет собой площадку для размещения онлайн-курсов с набором уроков. Доступ к урокам предоставляется после покупки курса (подписки). Внутри курса студенты автоматически распределяются по группам.



# Построение системы для обучения


1. Реализовать API на список продуктов, доступных для покупки(доступных к покупке = они еще не куплены пользователем и у них есть флаг доступности), которое бы включало в себя основную информацию о продукте и количество уроков, которые принадлежат продукту.
2. Реализовать API оплаты продукты за бонусы. Назовем его …/pay/ 
3. По факту оплаты и списания бонусов с баланса пользователя должен быть открыт доступ к курсу.
4. После того, как доступ к курсу открыт, пользователя необходимо распределить в одну из 10 групп студентов.

### Результат выполнения:

1. Выполненная архитектура на базе данных SQLite с использованием Django.

Необходимо отобразить список всех продуктов на платформе, к каждому продукту приложить информацию:

1. Количество учеников занимающихся на продукте.
2. На сколько % заполнены группы? (среднее значение по количеству участников в группах от максимального значения участников в группе, где максимальное = 30).
3. Процент приобретения продукта (рассчитывается исходя из количества полученных доступов к продукту деленное на общее количество пользователей на платформе).


### __OpenAPI документация__
* Swagger: http://127.0.0.1:8000/api/v1/swagger/
* ReDoc: http://127.0.0.1:8000/api/v1/redoc/


### __Реализуйте следующее API__

<details><summary> GET: http://127.0.0.1:8000/api/v1/courses/  - показать список всех курсов.</summary>

    200 OK:
    ```
    [
        {
            "id": 3,
            "author": "Михаил Потапов",
            "title": "Backend developer",
            "start_date": "2024-03-03T12:00:00Z",
            "price": "150000",
            "lessons_count": 0,
            "lessons": [],
            "demand_course_percent": 0,
            "students_count": 0,
            "groups_filled_percent": 0
        },
        {
            "id": 2,
            "author": "Михаил Потапов",
            "title": "Python developer",
            "start_date": "2024-03-03T12:00:00Z",
            "price": "120000",
            "lessons_count": 3,
            "lessons": [
                {
                    "title": "Урок №1"
                },
                {
                    "title": "Урок №2"
                },
                {
                    "title": "Урок №3"
                }
            ],
            "demand_course_percent": 84,
            "students_count": 10,
            "groups_filled_percent": 83
        },
        {
            "id": 1,
            "author": "Иван Петров",
            "title": "Онлайн курс",
            "start_date": "2024-03-03T12:00:00Z",
            "price": "56000",
            "lessons_count": 3,
            "lessons": [
                {
                    "title": "Урок №1"
                },
                {
                    "title": "Урок №2"
                },
                {
                    "title": "Урок №3"
                }
            ],
            "demand_course_percent": 7,
            "students_count": 1,
            "groups_filled_percent": 10
        }
    ]
    ```
</details>


<details><summary> GET: http://127.0.0.1:8000/api/v1/courses/2/groups/  - показать список групп определенного курса.</summary> 

    200 OK:
    ```
    [
        {
            "title": "Группа №3",
            "course": "Python developer",
            "students": [
                {
                    "first_name": "Иван",
                    "last_name": "Грозный",
                    "email": "user9@user.com"
                },
                {
                    "first_name": "Корней",
                    "last_name": "Чуковский",
                    "email": "user8@user.com"
                },
                {
                    "first_name": "Максим",
                    "last_name": "Горький",
                    "email": "user7@user.com"
                }
            ]
        },
        {
            "title": "Группа №2",
            "course": "Python developer",
            "students": [
                {
                    "first_name": "Ольга",
                    "last_name": "Иванова",
                    "email": "user6@user.com"
                },
                {
                    "first_name": "Саша",
                    "last_name": "Иванов",
                    "email": "user5@user.com"
                },
                {
                    "first_name": "Дмитрий",
                    "last_name": "Иванов",
                    "email": "user4@user.com"
                }
            ]
        },
        {
            "title": "Группа №1",
            "course": "Python developer",
            "students": [
                {
                    "first_name": "Андрей",
                    "last_name": "Петров",
                    "email": "user10@user.com"
                },
                {
                    "first_name": "Олег",
                    "last_name": "Петров",
                    "email": "user3@user.com"
                },
                {
                    "first_name": "Сергей",
                    "last_name": "Петров",
                    "email": "user2@user.com"
                },
                {
                    "first_name": "Иван",
                    "last_name": "Петров",
                    "email": "user@user.com"
                }
            ]
        }
    ]
    ```
</details>

### __Технологии__
* [Python 3.10.12](https://www.python.org/doc/)
* [Django 4.2.10](https://docs.djangoproject.com/en/4.2/)
* [Django REST Framework  3.14.0](https://www.django-rest-framework.org/)
* [Djoser  2.2.0](https://djoser.readthedocs.io/en/latest/getting_started.html)

# Task

1. В базе PostgreSQL есть две таблицы. Одна называется Persons и содержит в себе колонку params типа JSONB с данными вида {‘grade’: ‘A’, ‘specId’: 1}. Напишите SQL-запрос, который выдает количество Персон (Persons, разумеется) в базе для каждой специализации (specId), содержащихся в таблице Specs.
2. Напишите то же самое с использованием Django ORM и/или SQLAlchemy.
3. Напишите метод, принимающий на вход два параметра: список URL’ов изображений и строку пути для записи. В данном методе должно производиться ПАРАЛЛЕЛЬНОЕ скачивание этих изображений с последующей записью этих URL’ов в БД MongoDB, а также сохранением скаченных файлов по пути, указанном во втором параметре.  Преимущественно выполнение данного пункта с использованием библиотек asyncio/aiohttp.

# My Response

### 1. PostgreSQL query
```sql
select s.id as id, s.name as name, count(p.id) as persons_count 
from 
  specs as s left join persons as p 
    on s.id = cast(p.params->>'specId' as integer) 
group by s.id order by s.id;
```

### 2. Не нашел ничего лучше, чем использовать "сырой" запрос, тк django модели не поддерживают подписки на deferred поля
```python
Specs.objects.raw("select s.id as id, s.name as name, count(p.id) as persons_count from spec as s left join person as p on s.id = cast(p.params->>'specId' as integer) group by s.id order by s.id;")
```

### 3. [Python script](./main.py) with calling example

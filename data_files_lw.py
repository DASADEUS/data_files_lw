# -*- coding: utf-8 -*-
"""
## Лабораторная работа
"""

import numpy as np
from google.colab import files
import pandas as pd
from pandas import concat
import json
import requests
import pickle
import os

uploaded = files.upload()

"""### JSON

1.1 Считайте файл `contributors_sample.json`. Воспользовавшись модулем `json`, преобразуйте содержимое файла в соответствующие объекты python. Выведите на экран информацию о первых 3 пользователях.
"""

with open('contributors_sample (1).json', 'r', encoding='utf-8') as f:  
    data = json.load(f)

data[0:3]

"""1.2 Выведите уникальные почтовые домены, содержащиеся в почтовых адресах людей"""

uniq=[]
for i in data:
  uniq.append(i['mail'])
print(np.unique(uniq))
len(np.unique(uniq))

"""1.3 Напишите функцию, которая по `username` ищет человека и выводит информацию о нем. Если пользователь с заданным `username` отсутствует, возбудите исключение `ValueError`"""

def resurch(name):
  for i in data:
    if i['username']==name:
      return i
      break
  return ValueError('Нет такого')

resurch('jmiller')

"""1.4 Посчитайте, сколько мужчин и женщин присутсвует в этом наборе данных."""

sex=[]
for i in data:
  sex.append(i['sex'])
print(sex.count('M'))
print(sex.count('F'))

"""1.5 Создайте `pd.DataFrame` `contributors`, имеющий столбцы `id`, `username` и `sex`."""

contr=pd.json_normalize(data)
contributors=contr[['id','username','sex']]
contributors

"""1.6 Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в таблицу `recipes`. Объедините `recipes` с таблицей `contributors` с сохранением строк в том случае, если информация о человеке отсутствует в JSON-файле. Для скольких человек информация отсутствует? """

recipes = pd.read_csv('recipes_sample.csv')

dt= recipes.merge(contributors [["id","username","sex"]], left_on='contributor_id', right_on='id', how="right")
dt

len(np.unique(recipes['contributor_id']))-len(np.unique(dt['id_y']))

recipes[recipes['contributor_id']==405004]

contributors[contributors['username']=='nicolewhite']

"""### pickle

2.1 На основе файла `contributors_sample.json` создайте словарь следующего вида: 
```
{
    должность: [список username людей, занимавших эту должность]
}
```
"""

job=[]
for i in contr['jobs']:
  for j in i:
    job.append(j)
jobs=np.unique(job)

workers = []
for i in jobs:
    peopl = []
    for j in data:
      if i in j['jobs']:
        peopl.append(j['username'])
    workers.append(peopl)

professins=dict(zip(jobs,workers))

"""2.2 Сохраните результаты в файл `job_people.pickle` и в файл `job_people.json` с использованием форматов pickle и JSON соответственно. Сравните объемы получившихся файлов. При сохранении в JSON укажите аргумент `indent`."""

with open('job_people.pickle','wb') as f:
  pickle.dump(professins, f)
os.path.getsize("job_people.pickle")

with open('job_people.json', 'w') as f:
  json.dump(professins, f,indent=1)
os.path.getsize("job_people.json")

"""2.3 Считайте файл `job_people.pickle` и продемонстрируйте, что данные считались корректно. """

with open('job_people.pickle','rb') as f:
  d = pickle.load(f)
print(d)

"""### XML

3.1 По данным файла `steps_sample.xml` сформируйте словарь с шагами по каждому рецепту вида `{id_рецепта: ["шаг1", "шаг2"]}`. Сохраните этот словарь в файл `steps_sample.json`
"""

with open('steps_sample.xml') as f:  
    data = BeautifulSoup(f,'xml')

res=list()
for i in data.recipes.find_all('recipe'):
  ph=[st.next for st in i.steps.find_all('step')]
  res.append({i.find('id').next: ph})

res

data

"""3.2 По данным файла `steps_sample.xml` сформируйте словарь следующего вида: `кол-во_шагов_в_рецепте: [список_id_рецептов]`"""

res=list()
for i in data.recipes.find_all('recipe'):
  ph=len([st.next for st in i.steps.find_all('step')])
  res.append({ ph: i.find('id').next})

temp_dict = {list(res[0].items())[0][0]: [int(list(res[0].items())[0][1])]}
for item in res:
  for key, value in item.items():
    if key in temp_dict:
      temp_dict[key].append(value)
    else:
      temp_dict[key] = [value]

temp_dict

"""3.3 Получите список рецептов, в этапах выполнения которых есть информация о времени (часы или минуты). Для отбора подходящих рецептов обратите внимание на атрибуты соответствующих тэгов."""

mihour=set()
for i in data.recipes.find_all('recipe'):
  for j in i.steps.find_all('step'):
    if j.has_attr('has_hours') or i.has_attr('has_minutes'):
      mihour.add(i.find('id').next)

mihour

"""3.4 Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в таблицу `recipes`. Для строк, которые содержат пропуски в столбце `n_steps`, заполните этот столбец на основе файла  `steps_sample.xml`. Строки, в которых столбец `n_steps` заполнен, оставьте без изменений."""

uploaded = files.upload()

recipes = pd.read_csv('recipes_sample.csv')
recipes = recipes.set_index("id")
recipes

res=list()
for i in data.recipes.find_all('recipe'):
  ph=len([st.next for st in i.steps.find_all('step')])
  res.append({  i.find('id').next:ph})

temp_dict = {}
for item in res:
  for key, value in item.items():
      temp_dict[key] = value

idcsteps=pd.DataFrame.from_dict(temp_dict, orient='index')
idcsteps

for index, row in recipes.iterrows():
   if pd.isnull(recipes['n_steps'][index]):
      recipes['n_steps'][index] =  idcsteps.loc[str(index)]
recipes

"""3.5 Проверьте, содержит ли столбец `n_steps` пропуски. Если нет, то преобразуйте его к целочисленному типу и сохраните результаты в файл `recipes_sample_with_filled_nsteps.csv`"""

recipes[recipes["n_steps"].isna()].shape[0]

recipes["n_steps"] = recipes["n_steps"].astype(int)

recipes.to_csv("recipes_sample_with_filled_nsteps.csv")

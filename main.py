import json
import csv
import requests

# нужен одноразово чтобы сохранить ответ в json-файл, разобраться какие поля имеюся в ответе get-запроса
# ---------------------------------------------------------------------------------------------------------------------------------------------
# url = 'https://api.technodom.kz/katalog/api/v1/products/category/smartfony?city_id=5f5f1e3b4c8a49e692fefd70&limit=305&sorting=score&price=0'
# response = requests.get(url).json()
# with open('data.json', 'w', encoding='utf-8') as file:
#     json.dump(response, file, indent=3, ensure_ascii=False)
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Пока ввожу категории вручную, хотя надо получать с сайта
categories = ['smartfony', 'planshety',
              'smart-chasy', 'naushniki', 'televizory']


# фунция возвращает словарь, которая по апишке получает тотал категории, то есть максимальное количество из категории
def get_total(names: list) -> dict:
    total = {}
    for el in names:
        url = f'https://api.technodom.kz/katalog/api/v1/products/category/{el}?city_id=5f5f1e3b643d490d8a416160&limit=24&sorting=score&price=0'
        response = requests.get(url).json()
        total[el] = response.get('total')
    return total


# получаем словарь
data = get_total(categories)

# делаем get запрос и получаем нужные поля, подготовливаем данные к сохранению
def get_pages(category: str, total: int) -> list:
    url = f'https://api.technodom.kz/katalog/api/v1/products/category/{category}?city_id=5f5f1e3b4c8a49e692fefd70&limit={total}&sorting=score&price=0'
    response = requests.get(url).json()
    items = response['payload']
    names = [[el.get('title'), el.get('price')] for el in items]
    return names


# вызываем функцию get_pages(), подставляя категорию товара и тотал, записываем одноименным csv-файлом
for category, total in data.items():
    result = get_pages(category, total)
    with open(f'csv_files/{category}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price'])
        writer.writerows(result)
        print(f'{category} готов')

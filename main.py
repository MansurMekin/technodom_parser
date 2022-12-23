import requests
import json
import csv

# url = 'https://api.technodom.kz/katalog/api/v1/products/category/smartfony?city_id=5f5f1e3b4c8a49e692fefd70&limit=305&sorting=score&price=0'

# response = requests.get(url).json()

# with open('data.json', 'w', encoding='utf-8') as file:
#     json.dump(response, file, indent=3, ensure_ascii=False)


categories = ['smartfony', 'planshety', 'smart-chasy', 'naushniki', 'televizory']


def get_total(names):
    total = {}
    for el in names:
        url = f'https://api.technodom.kz/katalog/api/v1/products/category/{el}?city_id=5f5f1e3b643d490d8a416160&limit=24&sorting=score&price=0'
        response = requests.get(url).json()
        total[el] = response.get('total')
    return total


data = get_total(categories)


def get_pages(category, total):
    url = f'https://api.technodom.kz/katalog/api/v1/products/category/{category}?city_id=5f5f1e3b4c8a49e692fefd70&limit={total}&sorting=score&price=0'
    response = requests.get(url).json()
    items = response['payload']
    names = [[el.get('title'), el.get('price')] for el in items]
    return names


for category, total in data.items():
    result = get_pages(category, total)
    with open(f'csv_files/{category}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price'])
        writer.writerows(result)
        print(f'{category} готов')

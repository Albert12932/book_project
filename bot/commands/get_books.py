import requests
import json
def get_books_disk():
    token = 'y0_AgAAAAB1VcOdAAuV-AAAAAEBTgdeAABiC2LQcFZHLZnqWrWpVpkTgurrVg'
    headers = {'Authorization': 'OAuth ' + token}

    url = 'https://cloud-api.yandex.net/v1/disk/resources?path=/BOOKS/&fields=items(name, download_url)'
    response = requests.get(url, headers=headers)
    books_names = []
    if response.status_code == 200:
        data = json.loads(response.text)
        files = data['_embedded']['items']
        for file in files:
            books_names.append(file['name'])
    return books_names

def get_book_link(name):
    token = 'y0_AgAAAAB1VcOdAAuV-AAAAAEBTgdeAABiC2LQcFZHLZnqWrWpVpkTgurrVg'

    headers = {'Authorization': 'OAuth ' + token}

    url = f'https://cloud-api.yandex.net/v1/disk/resources?path=/BOOKS/{name}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        download_url = response.json()['file']
        return download_url
    else:
        print('Ошибка при получении информации о файле')

def delete_book_disk(name):
    token = 'y0_AgAAAAB1VcOdAAuV-AAAAAEBTgdeAABiC2LQcFZHLZnqWrWpVpkTgurrVg'
    url = f'https://cloud-api.yandex.net/v1/disk/resources?path=/BOOKS/{name}'
    headers = {
        'Authorization': f'OAuth {token}',
    }

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print('Файл успешно удален')
    else:
        print('Ошибка при удалении файла')
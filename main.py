import json

import requests

from progress.bar import ChargingBar

with open('token_VK.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('token_YD.txt', 'r') as file_object:
    token1 = file_object.read().strip()

res_dict = dict()


class SaveDisk:
    url = 'https://api.vk.com/method/'

    def __init__(self, owner_id):
        self.token1 = token1
        self.params = {
            'access_token': token,
            'v': '5.131',
            'owner_id': owner_id
        }

    def get_url_photo(self):
        photo_url = self.url + 'photos.get'
        photo_params = {
            'album_id': 'profile',
            'extended': 1
        }
        res = requests.get(url=photo_url, params={**self.params, **photo_params}).json()
        url_list = res['response']['items']
        for item in url_list:
            name_key = str(item['likes']['count'])
            date_photo = item['date']
            sizes_list = item['sizes']
            max_size_url = sizes_list[-1]
            temp_dict = {name_key: max_size_url}
            size = max_size_url['type']
            if name_key not in res_dict:
                res_dict.update(temp_dict)
            else:
                temp_dict = {str(name_key) + '_' + str(date_photo): max_size_url}
                res_dict.update(temp_dict)
        return res_dict

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f"OAuth {self.token1}"
        }

    def create_a_folder(self, disk_file_path):
        folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        folder_params = {
            "path": disk_file_path
        }
        response = requests.put(url=folder_url, params=folder_params, headers=headers)
        return response.json()

    def uploads_file_to_disk(self, disk_file_path, limit=5):
        print_list = list()
        headers = self.get_headers()
        index = 0
        bar = ChargingBar('Прогресс загрузки', max=limit)
        for name, value in res_dict.items():
            filename = name
            size = value['type']
            file_url = value['url']
            index += 1
            if index > limit:
                break
            bar.next()
            uploads_params = {
                'path': f'{disk_file_path}/{filename}',
                'url': f'{file_url}'
            }
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            r = requests.post(url=url, params=uploads_params, headers=headers)
            temp_dict = {"file_name": filename + ".jpg", "size": size}
            print_list.append(temp_dict)
        bar.finish()
        print(json.dumps(print_list, sort_keys=True, indent=2))


Cl = SaveDisk(552934290)

Cl.get_url_photo()
Cl.create_a_folder('Photo')
Cl.uploads_file_to_disk('Photo')

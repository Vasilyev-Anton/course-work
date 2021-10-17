import VKSave

import json

import requests

from progress.bar import ChargingBar

token_YD = ''


class YaDisk:

    def __init__(self):
        self.token = token_YD

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f"OAuth {self.token}"
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
        for name, value in VKSave.res_dict.items():
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

import json
import requests
from progress.bar import ChargingBar
from VKSave import res_dict


class YaDisk:

    def __init__(self, token_ya):
        self.token_ya = token_ya

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token_ya}'}

    def create_a_folder(self, disk_file_path):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        folder_params = {"path": disk_file_path}
        response = requests.put(url=folder_url, params=folder_params, headers=headers)
        return response.json()

    def upload_photo_to_disk(self, disk_file_path, limit=5):
        info_list = list()
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
            uploads_params = {'path': f'{disk_file_path}/{filename}', 'url': f'{file_url}'}
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            requests.post(url=url, params=uploads_params, headers=headers)
            temp_dict = {'file_name': filename + '.jpg', 'size': size}
            info_list.append(temp_dict)
        bar.finish()
        json.dumps(info_list, sort_keys=True, indent=2)
        res_info = str(info_list)
        with open('info.txt', 'w') as info_file:
            info_file.write(res_info)

    def _get_upload_url(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path):
        href = self._get_upload_url(disk_file_path=disk_file_path).get('href', '')
        requests.put(href, data=open('info.txt', 'rb'))

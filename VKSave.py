import requests

token_VK = ''

res_dict = dict()


class VKSave:
    url = 'https://api.vk.com/method/'

    def __init__(self, owner_id):
        self.params = {
            'access_token': token_VK,
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
            if name_key not in res_dict:
                res_dict.update(temp_dict)
            else:
                temp_dict = {str(name_key) + '_' + str(date_photo): max_size_url}
                res_dict.update(temp_dict)
        return res_dict

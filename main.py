import json
from VKSave import VKsave
from YaDisk import YaDisk

with open('config.json') as f:
    config = json.load(f)

user_id = '552934290'


if __name__ == '__main__':
    Cl = VKsave(user_id, config['token_vk'])
    Cl.get_url_photo()
    Cl = YaDisk(config['token_ya'])
    Cl.create_a_folder('photo')
    Cl.upload_photo_to_disk('photo')
    Cl.upload_file_to_disk('info.txt')


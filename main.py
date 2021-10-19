from VKSave import VKsave
from YaDisk import YaDisk

token_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
token_ya = ''
user_id = '552934290'


if __name__ == '__main__':
    Cl = VKsave(user_id, token_vk)
    Cl.get_url_photo()
    Cl = YaDisk(token_ya)
    Cl.create_a_folder('photo')
    Cl.upload_photo_to_disk('photo')
    Cl.upload_file_to_disk('info.txt')


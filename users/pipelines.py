from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'personal', 'photo_max')), access_token=response['access_token'],
                    v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    print(data)
    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass

    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

    age = timezone.now().date().year - bdate.year
    user.age = age
    # минимальный возраст,исключение выдаст ошибку и сайт упадет
    if age < 10:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['personal']:
        user.userprofile.language = ', '.join(data['personal']['langs'])

    if data['photo_max']:
        photo = requests.get(data['photo_max'])
        url_photo = f'users_image/{user.username}.jpg'
        with open(f'media/{url_photo}','wb') as f:
            f.write(photo.content)
        user.image = url_photo

    user.save()

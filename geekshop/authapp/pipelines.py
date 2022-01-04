from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden
from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return None
    
    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
    urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
        access_token=response['access_token'], v=5.131)), None))
    
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return None
        
    data = resp.json()['response'][0]
    
    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE

    if data['about']:
        user.userprofile.about = data['about']
    
    birth_date = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    user_age = timezone.now().date().year - birth_date.year

    user.age = user_age
    
    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    elif age >= 100:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        
    user.save()

# bdate
# about
# sex

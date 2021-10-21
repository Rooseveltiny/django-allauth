import requests
from hashlib import md5

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import MailRuProvider


class MailRuOAuth2Adapter(OAuth2Adapter):
    provider_id = MailRuProvider.id
    access_token_url = "https://oauth.mail.ru/token"
    profile_url = "https://o2.mail.ru/userinfo"
    authorize_url = "https://connect.mail.ru/oauth/authorize"

    def complete_login(self, request, app, token, **kwargs):
        '''
            new version of getting data from mailru
        '''
        data = {'access_token': token.token}
        response = requests.get(self.profile_url, params=data)
        extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(MailRuOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(MailRuOAuth2Adapter)

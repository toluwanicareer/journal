from . import TokenInfo


class TokenManager():
    def __init__(self, token_info):
        self.__token_info__ = token_info

    def get_token_info(self):
        return self.__token_info__

    def set_token_info(self, token, refresh_token=None, expiration=None, scope="epc.api"):
        self.__token_info__ = TokenInfo.TokenInfo(token, refresh_token, expiration, scope)

    def get_access_token(self):
        return self.__token_info__.get_access_token()

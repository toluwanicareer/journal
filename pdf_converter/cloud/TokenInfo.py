

class TokenInfo():
    def __init__(self, a_token, r_token=None, expiration=None, scope="epc.api"):
        self.__access_token__ = a_token
        self.__refresh_token__ = r_token
        self.__expiration__ = expiration
        self.__scope__ = scope

    def get_access_token(self):
        return self.__access_token__

    def get_refresh_token(self):
        return self.__refresh_token__

    def get_expiration(self):
        return self.__expiration__

    def get_scope(self):
        return self.__scope__
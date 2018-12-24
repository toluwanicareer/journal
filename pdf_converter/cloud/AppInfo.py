

class AppInfo():
    def __init__(self, client_id, client_secret, redirect_uri=None):
        self.__client_id__ = client_id
        self.__client_secret__ = client_secret
        self.__redirect_uri__ = redirect_uri

    def get_c_id(self):
        return self.__client_id__

    def get_secret(self):
        return self.__client_secret__

    def get_redirect_uri(self):
        return self.__redirect_uri__
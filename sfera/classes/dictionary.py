class Dictionary(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as error:
            raise AttributeError(*error.args)
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as error:
            raise AttributeError(*error.args)
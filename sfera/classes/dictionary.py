import sfera


class Dictionary(dict):

    def __getattr__(self, key):
        with sfera.replace_error(KeyError, AttributeError):
            return self[key]
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __delattr__(self, key):
        with sfera.replace_error(KeyError, AttributeError):
            del self[key]
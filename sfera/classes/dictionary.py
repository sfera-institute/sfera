from ..functions.replaceerror import replace_error


class Dictionary(dict):

    def __getattr__(self, key):
        with replace_error(KeyError, AttributeError):
            return self[key]
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __delattr__(self, key):
        with replace_error(KeyError, AttributeError):
            del self[key]
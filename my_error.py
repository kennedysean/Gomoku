class MyError(Exception):
    """Method creates an error exception class."""
    def __init__(self,value):
        self.__value = value
    def __str__(self):
        return self.__value
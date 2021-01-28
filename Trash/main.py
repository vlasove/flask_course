class Book:
    def __init__(self, title:str):
        self.__title = title 

    def __str__(self):
        """
        String representation
        """
        return self.__title 

    def __repr__(self):
        """
        Unificate representation
        """
        return self.__title + "__repr__"

b = Book("LOTR:1")
print(b)
str(b)


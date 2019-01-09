from my_error import MyError

class GoPiece(object):
    """This class represents the black and white pieces used to play Gomoku."""
    
    def __init__(self, color='black'):
        """This method has a private attribute named 'color' (default value is
        'black') which must have a value of either 'black' or 'white'. The 
        method creates a Gomoku piece, and raises an error if the color is not
        'black' or 'white'.
        """
        if str(color).lower().strip() != 'black' and \
        str(color).lower().strip() != 'white':
            raise MyError('Wrong color.')
        else:
            self.__color = str(color).lower().strip()

    def __str__(self):
        """This method displays the black piece (' ● ') or white piece (' ○ ').
        """
        if self.__color == 'black':
             return ' ● '
        else:
             return ' ○ '
    
    def get_color(self):
        """This method returns the color of the piece ('black' or 'white')."""
        return self.__color
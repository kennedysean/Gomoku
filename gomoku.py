##############################################################################
#    The program allows the game Gomoku to be played between two human users
#      running the program. 
#    The board in the game is a square grid (default 15 x 15) with valid 
#      spots to put black and white pieces. It is updated and displayed 
#      after each turn.
#    Each player takes turns placing a piece on valid places on the 
#      board when prompted.
#    The game is terminated if at any point a player inputs 'q'.
#    If an error is displayed when adding a piece, the user must try again
#      until a valid move is made.     
#    The winner of the game is the first player to get 5 pieces-in-a-row, 
#      whether that be horizontally, vertically, or diagonally. 
##############################################################################

from go_piece import GoPiece
from my_error import MyError

class Gomoku(object):
    """This class creates methods for setting up, displaying, and playing the
    game Gomoku.
    """
    def __init__(self, board_size=15, win_count=5, current_player='black'):
        """This method has four private attributes. board_size (default value
        is 15) represents the size of the game board. win_count (default value
        is 5) is the number of pieces in a row needed to win the game. 
        current_player (default value is 'black') is the color of the current
        player. go_board is a list of row lists representing the game board.
        """    
        if str(current_player).lower().strip() != 'black' and \
           str(current_player).lower().strip() != 'white':
            raise MyError('Wrong color.')
        else:
            self.__current_player = str(current_player).lower().strip()
        self.__win_count = int(win_count)
        self.__board_size = int(board_size)
        self.__go_board = [[' - ' for j in range(self.__board_size)] \
                             for i in range(self.__board_size)]
        
    def assign_piece(self, piece, row, col):
        """This method places a piece from GoPiece to a specific position on
        the game board. It returns an error if the specified position is 
        invalid or if the position is already taken.
        """
        row = int(row)
        col = int(col)
        row_index = row - 1
        col_index = col - 1
        if  row > self.__board_size or row < 1:
            raise MyError('Invalid position.')
        elif col > self.__board_size or col < 1:
            raise MyError('Invalid position.')
        elif self.__go_board[row_index][col_index] != " - ":
            raise MyError('Position is occupied.')
        else:
            self.__go_board[row_index][col_index]=piece
        
    def get_current_player(self):
        """This method returns the current player: 'black' or 'white'."""
        return self.__current_player 
    
    def switch_current_player(self):
        """This method switches the current player from 'black' to 'white' or 
        from 'white' to 'black'.
        """
        if Gomoku.get_current_player(self) == 'white':
            self.__current_player = 'black'
        else:
            self.__current_player = 'white'
    
    def __str__(self):
        """This method displays the game board."""
        s = '\n'
        for i,row in enumerate(self.__go_board):
            s += '{:>3d}|'.format(i+1)
            for item in row:
                s += str(item) 
            s += '\n'
        line = '___'*self.__board_size
        s += '    ' + line + '\n'
        s += '   '
        for i in range(1,self.__board_size+1):
            s += '{:>3d}'.format(i)
        s += '\n'
        s += 'Current player: '\
             + ('●' if self.__current_player == 'black' else '○')
        return s
        
    def current_player_is_winner(self):
        """This method checks if a player has a continuous sequence of size
        win_count (default is 5) pieces in-a-row in either a row, column, or 
        diagonal, making that player a winner. The method returns True if the
        player is a winner and returns False otherwise.
        """
        player = self.__current_player 
        piece = GoPiece(player)
        current_player = str(piece)
        board_size = int(self.__board_size)
        win_count = self.__win_count 
        """Iterate on the rows to check if the current player has win_count
        consecutive pieces in a row.
        """
        for i,row in enumerate(self.__go_board):
            in_a_row = 0
            for element in row: 
                if str(element) == current_player:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == win_count:
                    return True
        """Make a list of tuples containing the coordinates of each entry but
        with the column number as the new row number and the row number as the
        new column number.
        """
        transpose_list = []
        for i,row in enumerate(self.__go_board):
            for j,element in enumerate(row):
                coordinate = (j, i, str(element))
                transpose_list.append(coordinate)
        transpose_go_board=[[' - ' for j in range(self.__board_size)] \
                             for i in range(self.__board_size)]
        """Add entries of previous board to new board to create the transpose
        of the original board (columns of old board are now rows of new board
        and vice versa).
        """
        for tup in transpose_list:
            transpose_go_board[tup[0]][tup[1]] = tup[2]
        """Iterate on the rows of the transpose board (columns of original) to
        check if the current player has win_count consecutive pieces in a row.
        """
        for i,row in enumerate(transpose_go_board):
            in_a_row = 0
            for element in row:
                if str(element) == current_player:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == win_count:
                    return True
        """Make a list of tuples with coordinates and each board entry."""
        coordinate_list = []
        for i,row in enumerate(self.__go_board):
            for j,element in enumerate(row):
                coordinate = (i, j, str(element))
                coordinate_list.append(coordinate)
        """Iterate through coordinate list and return list of tuples such that
        the first entry in each tuple is shared by entries in the same upward
        sloping diagonal.
        """
        diagonal_list = []
        for i in range(2, (2*board_size)+1):
            for coordinate in coordinate_list:
                """In any given upward-sloping diagonal, the sum of the row and
                column numbers in each entry is equal.
                """
                if coordinate[0] + coordinate[1] == i:
                    diagonal = (i, coordinate[2])
                    diagonal_list.append(diagonal)
        """Iterate on the diagonal list to check if in any diagonal, the 
        current player has win_count consecutive pieces in a row.
        """
        for i in range(2, (2*board_size)+1):
            in_a_row = 0
            for diagonal in diagonal_list:
                if diagonal[0] == i:
                    if diagonal[1] == current_player:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row == win_count:
                        return True   
        """Make a list of tuples containing each entry with its coordinates 
        for the board reflected on its vertical axis of symmetry (col1 becomes
        col(board_size), col2 becomes col(board_size-1), etc.).
        """
        reflection_list = []
        for i,row in enumerate(self.__go_board):
            for j,element in enumerate(row):
                coordinate = (i, (board_size-1)-j, str(element))
                reflection_list.append(coordinate)
        reflection_go_board=[[' - ' for j in range(self.__board_size)] \
                             for i in range(self.__board_size)]
        """Add entries of old board to new board to create the original board
        reflected on its vertical line of symmetry (downward-sloping diagonals
        of original board become upward-sloping diagonals of new board).
        """
        for tup in reflection_list:
            reflection_go_board[tup[0]][tup[1]] = tup[2]
        """Repeat same code as above that was used to check the upward-sloping
        diagonals on the original board, except do this on the reflected board.
        Checking the upward-sloping diagonals of the reflected board is 
        equivalent to checking downward-sloping diagonals of the original.
        """
        coordinate_list = []
        for i,row in enumerate(reflection_go_board):
            for j,element in enumerate(row):
                coordinate = (i, j, str(element))
                coordinate_list.append(coordinate)
        diagonal_list = []
        for i in range(2, (2*board_size)+1):
            for coordinate in coordinate_list:
                if coordinate[0] + coordinate[1] == i:
                    diagonal = (i, coordinate[2])
                    diagonal_list.append(diagonal)
        for i in range(2, (2*board_size)+1):
            in_a_row = 0
            for diagonal in diagonal_list:
                if diagonal[0] == i:
                    if diagonal[1] == current_player:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row == win_count:
                        return True
        return False     # if there are no winning sequences of pieces


def main():
    """The main function of the program creates an instance of the Gomoku 
    class. It then lets the two players take turns placing pieces on the game
    board until a player wins or until a player quits by entering "q". The 
    board is printed and the board is checked for a winner after each player
    takes their turn. Any errors are dealt with by this function by displaying
    an error message and reprompting the player to place their piece."""
    board = Gomoku()
    print(board)
    play = input('Input a row then column separated by a comma (q to quit): ')
    while play.lower() != 'q':
        play_list = play.strip().split(',')
        while play.lower() != 'q':
            try:
                if len(play_list) != 2:
                    raise MyError('Incorrect input.')
                row = int(play_list[0].strip())
                col = int(play_list[1].strip())
                break
            except ValueError:
                print('Incorrect input.')
                print('Try again.')
                print(board)
                play = input('Input a row then column separated by\
                             a comma (q to quit): ')
                play_list = play.strip().split(',')
            except MyError as error_message:
                print(error_message)
                print('Try again.')
                print(board)
                play = input('Input a row then column separated by a\
                             comma (q to quit): ')
                play_list = play.strip().split(',')
        try: 
            current_player = board.get_current_player()
            piece = GoPiece(current_player)
            board.assign_piece(piece,row,col)
            if board.current_player_is_winner():
                print(board)
                print('{} wins!'.format(current_player))
                return
            else:
                board.switch_current_player()
        except MyError as error_message:
            print('{:s}\nTry again.'.format(str(error_message)))
        print(board)
        play = input('Input a row then column separated \
                     by a comma (q to quit): ')


if __name__ == '__main__':
    main()
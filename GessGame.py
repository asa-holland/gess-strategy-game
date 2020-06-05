# Author: Asa Holland
# Date: 06/01/2020
# Description: An implementation of the game of Gess


class GessBoard:
    """
    A GessBoard object contains the structure of the board and the locations of the player's pieces.
    The GessBoard object interacts with the GessGame class.
    The GessBoard creates a Gess board and places tokens on it for two players, Black and White.
    The GessBoard can return the current state of the board to the GessGame class.
    The GessBoard has_rings function determines whether a player has rings of tokens on the board.
    Finally the GessBoard object has a function to take a set of board coordinates and return the square of the board,
    and a function to take a square from the board and receive the piece of nine squares centered around that square.
    """
    def __init__(self):
        """
        Initiates the GessBoard object.
        Has private data members representing the board and a reference of coordinates for squares on the board.
        """
        self._gess_board = []
        self._square_coords = {}
        # Create a dictionary of the letters represented on the Gess board.
        # Use enumerate to obtain the placement of that letter in the dictionary.
        self._LETTERS = {index: letter for letter, index in enumerate('abcdefghijklmnopqrst', 1)}

        # Label the Rows using numbers 20 (top) through 1 (bottom)
        for number in range(20, 0, -1):
            row = [' ' for _ in range(20)]
            row.append(str(number))
            self._gess_board.append(row)

        # Label the Columns using the letters a (left) through t (right)
        self._gess_board.append([letter for letter in 'abcdefghijklmnopqrst '])

        # Create two lists of squares that contain white and black tokens respectively at the start of the game
        white_tokens = [x + '19' for x in 'ceghijklmnpr'] + \
                       [x + '18' for x in 'bcdfhijkmoqrs'] + \
                       [x + '17' for x in 'ceghijklmnpr'] + \
                       [x + '14' for x in 'cfilor']

        black_tokens = [x + '7' for x in 'cfilor'] + \
                       [x + '4' for x in 'ceghijklmnpr'] + \
                       [x + '3' for x in 'bcdfhijkmoqrs'] + \
                       [x + '2' for x in 'ceghijklmnpr']

        def place_token(square_coord, token):
            """
            Places a token at a given square using the coordinates on the Gess game board.
            :param square_coord: A string representing the column and row coordinates of a square on the Gess Board
            :param token: A character ('B' for Black or 'W' for White) representing the color of the token to place
            :return: Returns True if the token was successfully placed in the square, or False if not.
            """
            # Square coord is the column followed by the row, so this must be reversed to access the board row first
            self._gess_board[square_coord[1]][square_coord[0]] = token
            return True

        # Iterate over the lists of starting tokens by color and place tokens in each square in the list
        [place_token(self.get_square_from_coords(coords), 'W') for coords in white_tokens]
        [place_token(self.get_square_from_coords(coords), 'B') for coords in black_tokens]

    def has_rings(self, token):
        """
        Returns a boolean based on the presence or absence of token rings of the requested player on the Gess board.
        :param token: A single character ('W' or 'B') referring to which player whose ring status is desired
        :return: If the player whose token was searched has rings remaining, return True. If not, return False.
        """
        # Iterate through the rows of the board
        # Ignore rows that are not part of the board (row 20, row 1, and the column header row)
        # Then iterate through the columns of each row
        # Ignore columns that are not part of the board (column a, column t, and the row header column)
        # If the middle square is empty, then check if the piece around that square is a ring for the player
        # If it is, return True.
        # If we iterate through to the end of the board without finding a ring, return False.
        for row_index, row_contents in enumerate(self._gess_board):
            if row_index not in [0, 20, 21]:
                for column_index, square_contents in enumerate(row_contents):
                    if column_index not in [0, 20, 21]:
                        if square_contents == ' ':
                            piece = self.get_piece_from_square([row_index, column_index])
                            if piece == [token, token, token, token, ' ', token, token, token, token]:
                                return True
        return False

    def get_board(self):
        """
        Returns the current state of the Gess board.
        :return: Returns a list of lists representing the Gess Board.
        """
        return self._gess_board

    def get_square_from_coords(self, center_square_coords):
        """
        Converts a string of the column letter and row number of a Gess board square into a list of coordinates.
        :param center_square_coords: String of column letter and row number of a square on the Gess board.
        :return: A list of the contents of the row number and column number of the desired square.
        """

        # First, check to see if the coordinates have already been referenced once this game.
        # If so, return them without evaluating the conversions.
        if center_square_coords in self._square_coords:
            return self._square_coords[center_square_coords]

        # If the square coordinates have not been visited before,
        # use the dictionary of letters and their numerical values to obtain the numerical value of the column letter
        column_letter = center_square_coords[0]
        column_number = self._LETTERS[column_letter]

        # Since the board is displayed with row 20 on the top and row 1 on the bottom,
        # the row number must be flipped in order to refer to the correct cell in the board list.
        # For example, cell 'r19' would by default show up as the 19th row (near the bottom of the board).
        # Subtracting the row value by 20 and taking the absolute value will get the corrected value.
        # To account for the bottom row containing the column labels, we add an additional 1 to this value row value.
        row_number = abs(int(center_square_coords[1:]) - 20) + 1

        # Save the coordinates in the dictionary for future reference, then return the coordinates
        self._square_coords[center_square_coords] = [column_number - 1, row_number - 1]
        return [column_number - 1, row_number - 1]

    def get_piece_from_square(self, center_square):
        """
        Takes a list of the column and row of a square on the Gess board square and returns the piece of that square.
        :param center_square: List of the row number and column number of a square on the Gess board.
        :return: A list of the contents of the squares in the piece of the provided center square.
        """
        [column_number, row_number] = center_square

        # Define the piece as a list
        # iterate over number of row + 1 to row number - 1
        # iterate over letter of column -1 to letter of column + 1
        # add each square to the list of values representing the piece.
        piece = []
        for row in range(row_number - 1,  row_number + 2):
            for column in range(column_number - 1, column_number + 2):
                piece.append(self._gess_board[row][column])

        return piece


class GessGame:
    """
    A GessGame object represents a game of Gess, a variant of the two board games Chess and Go.
    The GessGame interacts with the GessBoard class to create a Gess board in order to play a game.
    The GessGame object also interacts with the GessGUI class to send the current game build to the GUI.
    The GessGame allows each player to move a piece or resign the game.
    The GessGame also includes internal functions to display the current and waiting players.
    """
    def __init__(self):
        """
        Initiates the GessGame object.
        Has private data members representing the current game state, current player, and board.
        """
        self._game_state = 'UNFINISHED'
        self._current_player = "B"
        self._board = GessBoard()

    def get_gess_board(self):
        """
        Returns the current Gess board as a list of list values for use in the GessGUI class.
        :return: Returns a List of lists representing the rows and columns of the current Gess board.
        """
        return self._board.get_board()

    def display(self):
        """
        Displays the current state of the Gess Board as a series of print statements.
        :return: Returns True once the board has been displayed using print statements.
        """
        current_board = self._board.get_board()
        for row_index, row in enumerate(current_board):
            if row_index == 20:
                line = '|'.join([letter for letter in row])
            else:
                formatted_row = []
                for square in row:
                    square_format = f'\033[;4m{square}\033[0m'
                    if square == ' ':
                        square_format = f'\033[;37;4;43m{square}\033[0m'
                    if square == 'W':
                        square_format = '\033[;30;4;1;43mO\033[0m'
                    if square == 'B':
                        square_format = '\033[;4;37;1;43mO\033[0m' #●
                    formatted_row.append(square_format)
                line = '\033[;43;4;37m|\033[0m'.join([formatted_square for formatted_square in formatted_row])
            print(line)
        print('\n')
        return True

    def get_game_state(self):
        """
        Returns the value of the private data member representing the current game state of the GessGame object.
        :return: String representing the current game state
        """
        return self._game_state

    def set_game_state(self, game_state_to_set):
        """
        Sets the current game state to one of the three possible game status options
        :param game_state_to_set: String to set the game status
        :return: Returns True once the game state was changed successfully.
        """
        self._game_state = game_state_to_set
        return True

    def get_current_player(self):
        """
        Returns the token color of the current player of the Gess game.
        :return: Returns a character representing the the current player's token color: 'B' for Black and 'W' for White.
        """
        return self._current_player

    def get_waiting_player(self):
        """
        Returns whichever player is currently waiting for their turn.
        :return: Returns a character, either 'W' or 'B', representing the token color of the player who is waiting.
        """
        return 'W' if self.get_current_player() == 'B' else 'B'

    def set_current_player(self, player):
        """
        Sets the current player
        :param player: The character 'W' or 'B' representing the players with the Black and White tokens respectively.
        :return: Returns True once the current player has been set to a new value.
        """
        self._current_player = player
        return True

    def make_move(self, origin_square, destination_square):
        """
        Allows the current player to move a token from the origin square to the destination square.
        A legal move:
            - has a destination square within the bounds of columns b through s and rows 2 through 19 on the Gess board
            - cannot leave the current player without a ring
            - may not have an origin square whose piece contains squares of the opposing player
            - may only move the range and direction dictated by the tokens of the current piece
        :param origin_square: string of column letter and row number of a Gess board square
        whose the desired piece is being moved from
        :param destination_square: string of column letter and row number of a Gess board square
        where the desired piece is being moved to
        :return: Returns True if the move was made successfully. Returns False if the move was not allowed.
        """
        # When a move occurs, the current player has attempted to move a piece from the provided origin square to
        # the provided destination square.

        # To begin, we must confirm that the current game state is unfinished.
        # If the game is not unfinished (ie Black or White has already won), return False.
        # This is done in order to avoid additional invalid moves made after the game has concluded.
        if self.get_game_state() != 'UNFINISHED':
            return False

        # Basic validation of the coordinates received
        for coords in [origin_square, destination_square]:
            # separate the provided coordinates of the target square into a row and a column
            # check that the row value is within the range of 2 to 19 (inclusive), if it is not, return False
            # check that the column value is within the range of b to s (inclusive), if it is not, return False
            if coords[0] not in 'bcdefghijklmnopqrs' or int(coords[1:]) not in range(2, 20):
                return False

            # If the origin square is the same as the destination square, return False
            if origin_square == destination_square:
                return False

        # Initial set-up of the coordinates of each of the two squares involved
        origin_coords = self._board.get_square_from_coords(origin_square)
        destination_coords = self._board.get_square_from_coords(destination_square)

        # First, select the piece of the provided origin square (nine squares in total). Examine the contents.
        # If the current piece contains no tokens of the current player, then the move is invalid.
        # This is because the only thing the current player can move is their own tokens.
        # If the current piece contains any tokens of the waiting player, then the move is also invalid.
        # This is because a player cannot move another player's tokens.
        origin_piece = self._board.get_piece_from_square(origin_coords)
        if self.get_current_player() not in origin_piece or self.get_waiting_player() in origin_piece:
            return False

        # Next, examine the desired destination in comparison with the origin piece
        # We need to determine the direction the piece needs to move, and the distance between the squares.
        # First, obtain the column and row values at the origin and destination squares.
        # Calculate the desired change in each direction based on the current move.
        [origin_column, origin_row] = origin_coords
        [destination_column, destination_row] = destination_coords

        change_in_columns = destination_column - origin_column
        change_in_rows = destination_row - origin_row

        # Next, examine the tokens that make up the origin piece to determine which movements are possible.
        [up_left, up, up_right, left, center, right, down_left, down, down_right] = origin_piece

        # Each modification tuple is formatted as follows:
        #   (change in rows needed, change in columns needed, square token needed)
        # For example, if the change is rows is less than zero (first value)
        # and the change in columns is equal to zero (second value),
        # and the piece contains a piece in the left square (third value).
        direction_modifications = (
            (change_in_rows < 0, change_in_columns > 0, up_right),
            (change_in_rows < 0, change_in_columns < 0, up_left),
            (change_in_rows < 0, change_in_columns == 0, up),
            (change_in_rows > 0, change_in_columns > 0, down_right),
            (change_in_rows > 0, change_in_columns < 0, down_left),
            (change_in_rows > 0, change_in_columns == 0, down),
            (change_in_rows == 0, change_in_columns > 0, right),
            (change_in_rows == 0, change_in_columns < 0, left)
        )

        # Iterate over the modifications and find the needed movement direction.
        # Check to see if the piece contains the token in the square necessary for a move to made in that direction.
        # If the piece does not contain the necessary token, the move is invalid. Return False.
        # Otherwise, end the check.
        for modification in direction_modifications:
            if modification[0] and modification[1]:
                if modification[2] != self.get_current_player():
                    return False
                else:
                    break

        # Check to see if the move distance is greater than 3 but the piece does not contain a center token.
        # If so, then the move is invalid because the destination square is too far for the piece to move.
        # Without a center token, the piece can only move three squares. In this case, False is returned.
        if (abs(change_in_rows) > 3 or abs(change_in_columns) > 3) and center != self.get_current_player():
            return False

        # Determine the necessary movement in the x axis (along the columns).
        x_move = y_move = 0
        if change_in_columns != 0:
            y_move = change_in_columns / abs(change_in_columns)

        # Determine the necessary movement in the y axis (along the rows).
        if change_in_rows != 0:
            x_move = change_in_rows / abs(change_in_rows)

        # If the move is legal, lift the piece from the board.
        lifted = list(origin_piece)
        for row_value in range(origin_row - 1, origin_row + 2):
            for column_value in range(origin_column - 1, origin_column + 2):
                self._board.get_board()[row_value][column_value] = ' '

        # Create a function to iterate over squares in the provided piece and place the tokens in the provided location
        def place_piece(piece_to_place, row_to_place, column_to_place):
            """
            places a piece (up to nine tokens) at a designated center row and column, clearing the footprint below
            :param piece_to_place: List of the contents of nine squares on the board representing the piece.
            :param row_to_place: Integer of the desired row of the center square of the piece
            :param column_to_place: Integer of the desired column of the center square of the piece
            """
            piece_index = 0
            for row_of_piece in range(row_to_place - 1, row_to_place + 2):
                for column_of_piece in range(column_to_place - 1, column_to_place + 2):
                    self._board.get_board()[row_of_piece][column_of_piece] = piece_to_place[piece_index]
                    piece_index += 1

        # Check that by lifting this piece away, the current player has not broken their last remaining ring
        # If so, this is an invalid move. Place the piece back and Return False.
        if not self._board.has_rings(self.get_current_player()):
            place_piece(lifted, origin_row, origin_column)
            return False

        # Then, move the piece towards the destination square one square at a time in the desired direction.
        # While doing this, check for tokens of either player.
        # If any tokens of either player are encountered before the move is completed, return False as the move.
        # This is because the only valid move is one that claims a piece, not one that moves beyond a token.
        (current_row, current_column) = (origin_row, origin_column)
        while not (current_row == destination_row and current_column == destination_column):
            for square in self._board.get_piece_from_square([current_column, current_row]):
                if square != ' ':
                    # If we have encountered another obstruction piece here, place the lifted piece back
                    place_piece(lifted, origin_row, origin_column)
                    return False
            current_row += int(x_move)
            current_column += int(y_move)

        # If the path has been determined to be clear, check that the footprint will not overlap a ring
        lifted_destination = list(self._board.get_piece_from_square(destination_coords))
        for row_value in range(destination_row - 1, destination_row + 2):
            for column_value in range(destination_column - 1, destination_column + 2):
                self._board.get_board()[row_value][column_value] = ' '

        # Check that by lifting the tokens in the destination footprint, the current player still has a remaining ring
        # If they do not, this is an invalid move. Place the destination and origin pieces back, and Return False.
        if not self._board.has_rings(self.get_current_player()):
            place_piece(lifted_destination, destination_row, destination_column)
            place_piece(lifted, origin_row, origin_column)
            return False

        # If the path has been determined to be clear of obstructions, place the piece in the destination
        place_piece(lifted, destination_row, destination_column)

        # Clearing the boundary rows and columns
        # First, eliminate all tokens in the boundary rows (1 and 20)
        for row_number in [0, 19]:
            if len(set(self._board.get_board()[row_number])) != 2:
                for index, square in enumerate(self._board.get_board()[row_number]):
                    self._board.get_board()[row_number][index] = ' '

        # Then, eliminate all tokens in the boundary columns (a and t).
        for row_number in range(0, 20):
            for column_number in [0, 19]:
                self._board.get_board()[row_number][column_number] = ' '

        # At the end of a successful move, check to see if the current player has removed the opposing player's ring
        # If so, the current player has won and the game is over.
        if not self._board.has_rings(self.get_waiting_player()):
            self.set_game_state('WHITE_WON') if self.get_current_player() == 'W' else self.set_game_state('BLACK_WON')

        # If the move was successful and the game is still unfinished,
        # then switch the current player with the waiting player and return True.
        self.set_current_player(self.get_waiting_player())
        return True

    def resign_game(self):
        """
        Allows the current player to resign.
        This makes the waiting player the winner, changing the game state respectively and ending the game.
        :return: Returns False if the game has already finished.
        Returns True if the current player has successfully resigned.
        """
        # First, check that the game is unfinished. If it is not, return False.
        if self.get_game_state() != 'UNFINISHED':
            return False

        # Determine the current player, then set the other player as the winner.
        self.set_game_state('WHITE_WON' if self.get_current_player() == 'B' else 'BLACK_WON')
        return True


def main():
    """
    Allows for basic testing in case the GessGame.py file is called as a script.
    """
    gess = GessGame()
    gess.display()


if __name__ == '__main__':
    main()

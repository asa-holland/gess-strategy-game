# Author: Asa Holland
# Date: 05/30/2020
# Description: Unit testing to check validity of GessGame.py

import unittest

from GessGame import GessGame, GessBoard


class TestGess(unittest.TestCase):
    """
    Contains units tests for the GessGame and GessBoard classes
    """

    def test_scenario_1(self):
        """
        Tests that a legal move that does not capture any stones behaves as expected.
        """
        # In this test, Black will make a legal move that does not capture any stones.
        # First, we will check that both the origin square and the destination square are found on the board of play.
        # Next, we will check that the tokens in the squares of the origin piece belong to the current player.
        # Then, the squares will be checked to see if such a move is possible based on the components of black's piece.
        # Then the destination square will be updated to reflect the tokens that have moved.
        # The board will be updated, and White will become the current player.
        gess = GessGame()
        gess.make_move('c3', 'c5')
        self.assertEqual(gess.get_current_player(), 'W')
        print('Test Scenario 1: a legal move that does not capture a token.')
        gess.display()

    def test_scenario_2(self):
        """
        Tests that a legal move that captures one stone behaves as expected.
        """
        # In this test, Black will make a legal move that captures one black stone.
        # First, we will check that both the origin square and the destination square are found on the board of play.
        # Next, we will check that the tokens in the squares of the origin piece belong to the current player.
        # Then, the squares will be checked to see if such a move is possible based on the components of black's piece.
        # Then, the destination stone will be captured and removed from the board.
        # Then the destination square will be updated to reflect the tokens that have moved.
        # The board will be updated, and White will become the current player.
        gess = GessGame()
        gess.make_move('c3', 'c6')
        self.assertEqual(gess.get_current_player(), 'W')
        print('Test Scenario 2: a legal move that captures a token.')
        gess.display()

    def test_scenario_3(self):
        """
        Tests that a player cannot move the other player's piece.
        """
        # In this test, Black will attempt to move a piece containing only White's tokens.
        # Using the coordinates provided for the origin square, the origin square is located on the Gess board.
        # Then, the origin square and the eight squares around that origin square are examined to form a 'piece'.
        # The contents of the piece are searched for any tokens that do not belong to the current player.
        # When any tokens that do not belong to the current player are found, the move is determined to be invalid.
        # This will cause the make_move function to return False, and it will remain Black's turn.
        gess = GessGame()
        self.assertEqual(gess.make_move('r18', 'r16'), False)
        self.assertEqual(gess.get_current_player(), 'B')
        print('Test Scenario 3: an invalid move attempted by moving another player\'s piece.')
        gess.display()

    def test_scenario_4(self):
        """
        Tests that a player cannot move a legal 'piece' in an invalid direction.
        """
        # In this test, Black will attempt to move a legal piece in an invalid direction.
        # Using the coordinates provided for the origin square, the origin square is located on the Gess board.
        # Then, the origin square and the eight squares around that origin square are examined to form a 'piece'.
        # The contents of the piece are searched for any tokens that do not belong to the current player.
        # When the piece is determined to be 'legal', the destination square is examined in a similar fashion.
        # The origin row and destination row are compared, which determines whether the intended move will take
        # the piece towards a row value with a greater or lesser value than the current origin square.
        # The same comparison is made using the columns.
        # Then, based on those comparison values, we can determine which general direction the piece needs to move.
        # For example, the move could be asking the piece to move up, to the right, or down and to the left.
        # These directions can then be compared to the contents of the origin piece.
        # If the origin piece does not contain the necessary token to move in the intended direction,
        # then the move is invalid, the function will return False, and it will remain Black's turn.

        # Initiate the game
        gess = GessGame()

        # Test that Black's invalid move returns False.
        self.assertEqual(gess.make_move('r7', 'r10'), False)

        # Test that following the invalid move, the current player is still Black.
        self.assertEqual(gess.get_current_player(), 'B')
        print('Test Scenario 4: an invalid move that attempts to move a valid piece in an invalid direction.')
        gess.display()

    def test_scenario_5(self):
        """
        Tests that the resign function of GessGame behaves as expected.
        """
        # In this test, Black will resign on the first move.
        # When the resignation is called for, the current player is determined to be Black.
        # Since we know the current player is Black, that means that the waiting player is White.
        # In this scenario, White will be set as the winner of the game in the game status.

        # Initiate the game
        gess = GessGame()
        gess.resign_game()

        # Test that the expected value of get_game_state matches the actual output of the function
        self.assertEqual(gess.get_game_state(), 'WHITE_WON')
        print('Test Scenario 5: a scenario where Black resigns and it White has won the game.')
        gess.display()

    def test_initial_game_state(self):
        """
        Tests that the display function of GessGame behaves as expected
        """
        # Initiate the game
        gess = GessGame()

        # Test that the expected value of get_game_state matches the actual output of the function
        self.assertEqual(gess.get_game_state(), 'UNFINISHED')
        print('Test Initial Game State: Testing that the initial setup of the board is displayed as expected.')
        gess.display()

    def test_rings(self):
        """
        Tests that the test_rings function of GessBoard behaves as expected.
        This will confirm that at the start of the game, each player has a ring.
        """
        board = GessBoard()
        self.assertEqual(board.has_rings('W'), True)
        self.assertEqual(board.has_rings('B'), True)
        print('Test has_rings function: Testing that the initial setup of the board shows rings for both players.')

    def test_get_square(self):
        """
        Tests the get_square_from_coords function in the GessBoard class.
        """
        # Check to see the function appropraitely returns the integers of the row
        # and column in the Gess board referring to the given square
        board = GessBoard()

        # Create the expected location of square c8 (located in the 12th row and the 2nd column with index 0)
        expected_value = [2, 12]

        # Run the function to obtain the actual result
        actual_result = board.get_square_from_coords('c8')

        # Test that the expected value of get_square_from_coords matches the actual output of the function
        self.assertEqual(expected_value, actual_result)

    def test_get_piece(self):
        """
        Tests the get_piece_from_square function in the GessBoard class.
        """
        board = GessBoard()

        # Create the expected contents of the piece located square o18.
        # This piece is located in the 2nd row and the 17th column with index 0.
        expected_value = ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W']

        # Run the function to obtain the actual result
        square = board.get_square_from_coords('o18')
        actual_result = board.get_piece_from_square(square)

        # Test that the expected value of get_square_from_coords matches the actual output of the function
        self.assertEqual(expected_value, actual_result)

    def test_illegal_move_off_board(self):
        """
        Tests that attempting to move a piece off the board.
        """
        # In this test, Black will attempt an illegal move by trying to move a piece off the board.
        # As this is not a possible move, the move will return False and it will remain Black's turn.
        gess = GessGame()
        gess.make_move('r3', 'v3')
        self.assertEqual(gess.get_current_player(), 'B')
        print('Test invalid move off board: Testing handling of an invalid move of a piece off the board boundary.')
        gess.display()

    def test_illegal_move_of_piece_with_only_center_token(self):
        """
        Tests that attempting to move a piece with only a center token behaves as expected.
        """
        # In this test, Black will make an illegal move by trying to move a piece that only contains a center token.
        # As this is not a possible move, the move will return False and it will remain Black's turn.
        gess = GessGame()
        gess.make_move('c7', 'c10')
        self.assertEqual(gess.make_move('c7', 'c10'), False)
        self.assertEqual(gess.get_current_player(), 'B')
        print('Test invalid of a piece with only the center token: Testing handling of an invalid piece.')
        gess.display()

    def test_game_over(self):
        """
        Test that once a game is over, additional moves cannot be made and the other player cannot resign.
        """
        # In this test, black will resign the game.
        # Then White will attempt to make a move. This will not be possible as the game is already over.
        # Then White will attempt to resign. This will not be possible as the game is already over.
        gess = GessGame()
        gess.resign_game()
        self.assertEqual(gess.make_move('c3', 'f8'), False)
        self.assertEqual(gess.resign_game(), False)

    def test_obstruction_of_legal_move(self):
        """
        Tests that a legal move will be obstructed by a token in between the origin and destination of the piece.
        """
        # Black will make a legal move of piece r3 to r6, capturing a Black token.
        # White will make a legal move from e18 to e15, capturing a white token.
        # Then, Black will make a legal move of piece r6 to r17.
        # However, since White has a token in r14, the move will stop prematurely in r13, capturing the token in r14.
        gess = GessGame()
        gess.make_move('r3', 'r6')
        gess.make_move('e18', 'e15')
        gess.make_move('r6', 'r17')

        # Check that moving beyond an obstructed square returns False (as it is an invalid move)
        self.assertEqual(gess.make_move('r6', 'r17'), False)
        self.assertEqual(gess.get_current_player(), 'B')

        # Check that moving up to an obstructed square returns True and advances the turn
        self.assertEqual(gess.make_move('r6', 'r13'), True)
        self.assertEqual(gess.get_current_player(), 'W')
        print('Test obstruction handling: Testing behavior of a legal move that encounters an obstructing piece.')
        gess.display()

    def test_center_stone_movement(self):
        """
        Test that moving a piece with a center stone behaves as expected.
        """
        # In this test, Black will legally move the piece in p3 to p5.
        # Then, White will legally move the piece from i18 to i15, capturing the white token in i14
        # Then, Black will legally move p6 to i13, capturing the white tokens in h14, i14, and j14
        gess = GessGame()
        gess.make_move('p3', 'p5')
        gess.make_move('i18', 'i15')
        gess.make_move('p6', 'i13')
        self.assertEqual(gess.get_current_player(), 'W')
        print('Test center stone movement: Testing a legal move using the center token\'s expanded range.')
        gess.display()

    def test_break_ring_illegal_move(self):
        """
        Test that moving a piece that would cause a ring to break behaves as expected.
        """
        # In this test, Black will attempt an illegal move that would break Black's only ring.
        # The attempt will fail and it will remain Black's turn.
        gess = GessGame()
        gess.make_move('n3', 'o3')
        self.assertEqual(gess.get_current_player(), 'B')
        print('Test breaking ring: Testing that breaking a player\'s own ring is invalid.')
        gess.display()

    def test_tokens_cleared_from_bounds(self):
        """
        Test that tokens placed within the boundary column and row are removed as expected.
        """
        # In this test, Black will attempt a legal move that results in a Black token being removed from column t.
        # Then, White will attempt a legal move that results in a White token being removed from row 20.
        # Then, Black will attempt a legal move that results in a Black token being removed from row 1.
        # Finally, White will attempt a legal move that results in a White token being removed from column a.
        gess = GessGame()
        gess.make_move('r3', 's3')
        gess.make_move('c18', 'c19')
        gess.make_move('i3', 'i2')
        gess.make_move('c19', 'b19')
        self.assertEqual(gess.get_current_player(), 'B')
        print('Test boundary handling: Testing that boundary areas are cleared when tokens are placed there.')
        gess.display()

    def test_full_game(self):
        """
        Test that will go through multiple moves by each player, resulting in a conclusion of a game.
        """
        # In this test, Black and White will each make several legal moves, and Black will eventually win.
        # The game will conclude when Black wins by breaking the ring of White.
        gess = GessGame()
        gess.make_move('c3', 'c5')
        gess.make_move('r18', 'r16')
        gess.make_move('r3', 'r5')
        gess.make_move('r16', 'q16')
        gess.make_move('k6', 'n9')
        gess.make_move('m15', 'j12')
        gess.make_move('r5', 'r3')
        gess.make_move('j13', 'h15')
        gess.make_move('j7', 'h7')
        gess.make_move('j10', 'h12')
        gess.make_move('i3', 'i13')
        gess.make_move('c15', 'c12')
        gess.make_move('i13', 'l16')
        self.assertEqual(gess.get_game_state(), 'BLACK_WON')
        print('Test complete game: Testing that the game ends when a player breaks the opponent\'s last ring.')
        gess.display()


if __name__ == '__main__':
    unittest.main()

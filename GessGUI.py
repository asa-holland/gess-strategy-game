# Author: Asa Holland
# Date: 06/04/2020
# Description: A GUI implementation of the game of Gess using Kivy

from GessGame import GessGame
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.core.image import Image as CoreImage
from kivy.graphics import Line
from kivy import Config


# Set minimum size of the window to avoid texture problems
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '600')
Config.set('kivy', 'window_icon', None)

kv_string = """

<BackgroundColor@Widget>
    background_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos
            
<BackgroundLabel@Label+BackgroundColor>
    background_color: 0, 0, 1, 1

<GessGameGUI>:
    BoxLayout:
        orientation: 'vertical'
        BackgroundLabel:
            text: 'Current Player: Black'
            id: current_status_gui
            size_hint_y: None
            height: 25
            color: 0, 0, 0, 1
            background_color: 0.82, 0.64, 0.11, 1
        Label:
            text: ' '
            id: top_buffer
            size_hint_y: None
            height: 3
        BoxLayout:
            orientation: 'horizontal'
            id: central_area
            Label:
                text: ' '
                id: left_buffer
                size_hint_x: None
                width: 3 
            GridLayout:
                id: grid_layout
                canvas.before:
                    BorderImage:
                        source: '../gess-strategy-game/background.jpg'
                        pos: self.pos
                        size: self.size
                cols: 21 # Button insertion
            Label:
                text: ' '
                id: right_buffer
                size_hint_x: None
                width: 3
                # Right Buffer
        Label:
            text: ' '
            id: bottom_buffer
            size_hint_y: None
            height: 5 
        BoxLayout:
            orientation: 'horizontal'
            id: bottom_tabs
            size_hint_y: None
            height: 25
            Label:
                text: ' '
                size_hint_x: None
                width: 3
            Button:
                text: 'Resign Game'
                id: resign_btn
                size_hint_y: None
                height: 25
                on_press: root.press_resign_button()
            Button:
                text: 'Reset Game'
                id: reset_btn
                size_hint_y: None
                height: 25
                on_press: root.press_reset_button()
            Label:
                text: ' '
                size_hint_x: None
                width: 3
        Label:
            text: ' '
            size_hint_y: None
            height: 1 
"""

# Build a list of the names of the squares by iterating over the letters and numbers of the Gess Board
square_names = []

for digit in range(20, -1, -1):
    if digit != 0:
        for letter in 'abcdefghijklmnopqrstu':
            if letter != 'u':
                square_name_to_append = letter + str(digit)
            else:
                square_name_to_append = str(digit)
            square_names.append(square_name_to_append)
    else:
        for letter in 'abcdefghijklmnopqrst':
            square_names.append(letter)

# Define the non-playable squares on the board
non_playable_squares = [letter for letter in 'abcdefghijklmnopqrst'] + [str(i) for i in range(1, 21)] +\
                       ['a' + str(i) for i in range(1, 21)] + \
                       ['t' + str(i) for i in range(1, 21)] + \
                       ['u' + str(i) for i in range(1, 21)] + \
                       [letter + '20'for letter in 'abcdefghijklmnopqrst'] + \
                       [letter + '1' for letter in 'abcdefghijklmnopqrst']

# Define the playable squares on the board
just_playable_square_names = [name for name in square_names if name not in non_playable_squares]

# Utilize the existing list of square names on the Gess Board to add 21*21 buttons to the Gess Board
# Each button has an id that matches the given square name, defaults to text filled with a space character,
# is set to have no background color (transparent), assigned a square_coords value (that is the same as the ID).
# Additionally, set the font of the button to a unicode-friendly font in order to display tokens.
# Finally, bind a function to return the move using the selected button value as a reference.
button_text = ''
for btn_id in square_names:
    button_text += f'SquareButton:\n\t\t\t\t\tsquare_coords: \'{btn_id}\'' \
                   f'\n\t\t\t\t\ttext: \' \'\n\t\t\t\t\tbackground_color: 0, 0, 0, 0\n\t\t\t\t\t' \
                   f'font_name: "Arial.ttf"\n\t\t\t\t\tid: {btn_id}' \
                   f'\n\t\t\t\t\ton_press: root.attempt_move(self.square_coords)\n\t\t\t\t'

# Edit the existing kivy string to splice in the additional 21*21 buttons
temp_string = kv_string
index = temp_string.find(' # Button insertion')
modified_string = temp_string[:index] + '\n\t\t\t\t' + button_text + temp_string[index:]
kv_string = modified_string


# Define the SquareButton Class
class SquareButton(Button):
    """
    Creates a custom class inheriting from the kivy Button class, representing one of the squares on the board.
    """
    def on_size(self, square_coords='', *args):
        self.font_name = 'Arial.ttf'
        self.canvas.before.clear()
        with self.canvas.before:
            pass

        self.canvas.after.clear()
        with self.canvas.after:
            Color(0, 0, 0, 1)
            self.line = Line(width=1.2,
                             points=(self.x, self.y,
                                     self.x, self.y + self.height,
                                     self.x + self.width, self.y + self.height,
                                     self.x + self.width, self.y,
                                     self.x, self.y,), color=(0, 0, 0, 1))

        self.bind(x=self.update_line, y=self.update_line)


    def update_line(self, *args):
        self.canvas.after.clear()
        self.line = Line(width=2,
                         points=(self.x, self.y,
                                 self.x, self.y + self.height,
                                 self.x + self.width, self.y + self.height,
                                 self.x + self.width, self.y,
                                 self.x, self.y,))

# Run the modified kivy string, which will build the basic structure of the resulting App
Builder.load_string(kv_string)


class GessGameGUI(BoxLayout):
    """
    Define a GessGameGUI that holds the functions responsible for user-interaction.
    This inherits from the Kivy BoxLayout class, and serves various user functions.
    The GessGameGUI's primary function is to allow the players (both Black and White) to make moves on the Gess game
    by selecting pieces from the GUI and sending the attempted moves to the GessGame backend.
    If the move is successful, the GessGameGUI makes the move and updates the current GUI.
    After a move, the GessGameGUI updates the current status of the game (both in the GUI and in the backend).
    The GessGameGUI allows the user to press the resign and reset buttons, respectively resigning or resetting the game.
    The GessGameGUI provides highlights to selection (green for selected origin square and yellow for selected tokens).
    The GessGameGUI removes highlights from squares after a move has been made, whether valid or invalid.
    """

    def __init__(self, **kwargs):
        global kv_string
        super(GessGameGUI, self).__init__(**kwargs)

        Builder.load_string(kv_string)

        self._square_names = []
        self._gess_game = GessGame()
        self._status = 'WAITING_FOR_SELECTION'
        self._origin_square_selection = ''
        self._destination_square_selection = ''
        self.update_board()

    def press_resign_button(self):
        """
        When the 'Resign Game' button is pressed, updates the current game status in the back end and the GUI display.
        """
        # First, call the resign game function in the back end class. This effectively ends the game.
        self._gess_game.resign_game()
        # Then, update the current GUI to reflect that the game has ended and the appropriate player has won.
        self.update_current_status()

    def press_reset_button(self):
        """
        When the 'Reset Game' button is pressed, updates the current game status in the back end and the GUI display.
        """
        # First, reset the current back end class. This effectively resets the game.
        self._gess_game = GessGame()
        # Then, update the current GUI to reflect that the game has been reset.
        self.update_board()
        self.update_current_status()

    def get_gess_game(self):
        """
        Returns the backend of the current Gess Game.
        :return: Returns the backend of the current Gess Game.
        """
        return self._gess_game

    def highlight_green_square(self, coordinates):
        """
        Highlights a square at the given coordinates on the Gess Board in a green highlight.
        :param coordinates:  Takes a string representing the letter and number of a square on the Gess Board (f5 or o12)
        """
        self.ids[coordinates].background_color = (0, 1, 0, 1)

    def highlight_red_square(self, coordinates):
        """
        Highlights a square at the given coordinates on the Gess Board in a red highlight.
        :param coordinates:  Takes a string representing the letter and number of a square on the Gess Board (f5 or o12)
        """
        self.ids[coordinates].background_color = (1, 0, 0, 1)

    def highlight_yellow_square(self, coordinates):
        """
        Highlights a square at the given coordinates on the Gess Board in a yellow highlight.
        :param coordinates:  Takes a string representing the letter and number of a square on the Gess Board (f5 or o12)
        """
        self.ids[coordinates].background_color = (1, 1, 0, 1)

    def decolor_square(self, coordinates):
        """
        Removes the highlighted color from a square on the Gess Board GUI, returning the color to transparent.
        :param coordinates: Takes a string representing the letter and number of a square on the Gess Board (f5 or o12)
        """
        self.ids[coordinates].background_color = (0, 0, 0, 0)

    def attempt_move(self, square_coords):
        """
        Sends a coordinate from a square.
        :param square_coords:
        :return: Returns True if 1) the origin square has been selected or 2) a destination square has been selected
        and the move has been made. Otherwise, returns False.
        """

        # Initial test for validation of squares within the playable board
        # If the square coordinates received are not within the playable area, return False
        global square_names
        if square_coords not in just_playable_square_names:
            return False

        # If this is the first square selection made by the current player, set the selected square as the origin
        # Highlight the origin square green
        if self._status == 'WAITING_FOR_SELECTION':
            print(f'Origin selected: {square_coords}')
            self._origin_square_selection = square_coords
            self.highlight_green_square(square_coords)

            # Highlight the eight cells around the origin square in yellow color
            # Only highlight playable squares
            square_index = square_names.index(square_coords)
            for square in (square_index - 22, square_index - 21, square_index - 20,
                            square_index - 1, square_index + 1,
                           square_index + 20, square_index + 21, square_index + 22):

                # Highlight playable squares within the piece in yellow
                if square_names[square] not in non_playable_squares:
                    self.highlight_yellow_square(square_names[square])

                # Highlight non-playable squares (boundary boxes) within the piece in red
                elif square_names[square] in non_playable_squares and self.ids[square_names[square]].text == ' ':
                    self.highlight_red_square(square_names[square])

            # Record that the origin has been selected and return
            self._status = 'ORIGIN_SELECTED'
            return True

        # If this is the second square that a current player has selected, set the selected square as the destination
        if self._status == 'ORIGIN_SELECTED':
            print(f'Destination selected: {square_coords}')
            self._destination_square_selection = square_coords

            # Remove all highlights on squares on the board
            for square_name in square_names:
                self.decolor_square(square_name)

            # Attempt to make a move using the backend, passing the saved origin and destination locations as args
            # If the move is legal, update the board, set the game to waiting (for the other player).
            # Reset the origin and destination values and return True.
            if self._gess_game.make_move(self._origin_square_selection, self._destination_square_selection):
                print(f'Move from {self._origin_square_selection} to {self._destination_square_selection} successful.')
                self.update_board()
                self._status = 'WAITING_FOR_SELECTION'
                self._origin_square_selection = ''
                self._destination_square_selection = ''
                return True

            # If the attempt to move resulted in False, this means the backend determined the move to be invalid.
            # Clear the recorded values for origin and destination and wait for the current player to make a new move.
            else:
                print('Invalid move')
                self._status = 'WAITING_FOR_SELECTION'
                self._origin_square_selection = ''
                self._destination_square_selection = ''
                return False

    def update_current_status(self):
        """
        Updates the current status displayed in the game GUI based on the backend of the Gess game.
        :return: Returns None
        """
        if self._gess_game.get_game_state() == 'UNFINISHED':
            current_player = 'Black' if self._gess_game.get_current_player() == 'B' else 'White'
            self.ids['current_status_gui'].text = 'Current Player: ' + current_player
        else:
            winning_player = 'Black' if self._gess_game.get_game_state() == 'BLACK_WON' else 'White'
            self.ids['current_status_gui'].text = 'Game Over... ' + winning_player + ' Won!'

    def update_board(self):
        """
        Updates the current GUI board to reflect that of the backend board. Displays colored tokens and their locations.
        :return: Returns None.
        """
        # Obtain the names of the square coordinates
        global square_names

        # Obtain the current values of the Gess Game board
        current_contents = []
        for row in self._gess_game.get_gess_board():
            for contents in row:
                current_contents.append(contents)

        # Match these two lists (the names of square coordinates and the current values)
        # square_names is a list of the 'value' of each square on the display
        # formatted_contents is a list of the formatted contents of each square on the Gess board
        # For each match, set the resulting square of the GUI so that it's contents match the backend contents
        square_names_and_contents = zip(square_names, current_contents)
        for (square_name, square_contents) in square_names_and_contents:
            square = self.ids[square_name]

            # For squares with containing tokens, place the token (a unicode filled circle symbol) in the square center.
            if square_contents in {'W', 'B'}:
                square.text = u'\u25CF'
                square.font_size = 40
                square.bold = False
                square.text_size = (0, 38)

                # For squares with Black tokens, set the font color of the token to Black.
                if square_contents == 'B':
                    square.color = 0, 0, 0, 1

                # If the token is white, set the font color to White.
                else:
                    square.color = 1, 1, 1, 1

            # For squares without tokens, set the text format to black and normal font.
            else:
                square.text = square_contents
                square.color = 0, 0, 0, 1
                square.font_size = 16
                square.bold = True
                square.text_size = (None, None)

        # Update the current status displayed at the top of the board
        self.update_current_status()


class GessApp(App):
    """
    Runs an App and loads a fresh copy of the Gess Game GUI for the user to utilize.
    """
    def build(self):
        return GessGameGUI()


# Allows the Gess App to be run as a script.
if __name__ == '__main__':
    GessApp().run()

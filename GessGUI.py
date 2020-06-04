# Author: Asa Holland
# Date: 06/01/2020
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
from kivy.graphics import BorderImage
from kivy import Config

Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '600')

kv_string = """
<GessGameGUI>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Current Player: Black'
            id: top_buffer
            size_hint_y: None
            height: 25
        BoxLayout:
            orientation: 'horizontal'
            id: central_area
            Button:
                text: 'left_buffer'
                id: left_buffer
                size_hint_x: None
                width: 25  
            GridLayout:
                id: grid_layout
                canvas.before:
                    BorderImage:
                        source: '../gess-strategy-game/background.jpg'
                        pos: self.pos
                        size: self.size
                cols: 21 # Button insertion
            Button:
                text: 'right_buffer'
                id: right_buffer
                size_hint_x: None
                width: 25
                # Right Buffer
        Button:
            text: 'bottom_buffer'
            id: bottom_buffer
            size_hint_y: None
            height: 25 
        BoxLayout:
            orientation: 'horizontal'
            id: bottom_tabs
            size_hint_y: None
            height: 25
            Button:
                text: 'Resign'
                id: resign_btn
                size_hint_y: None
                height: 25
                on_press: root.press_resign_button()
"""
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

button_text = ''
print(square_names)
for btn_id in square_names:
    button_text += f'SquareButton:\n\t\t\t\t\tsquare_coords: \'{btn_id}\'' \
                   f'\n\t\t\t\t\ttext: \' \'\n\t\t\t\t\tbackground_color: 0, 0, 0, 0\n\t\t\t\t\t' \
                   f'font_name: "/usr/share/fonts/truetype/freefont/FreeSans.ttf"\n\t\t\t\t\tid: {btn_id}' \
                   f'\n\t\t\t\t\ton_press: root.attempt_move(self.square_coords)\n\t\t\t\t'

temp_string = kv_string
index = temp_string.find(' # Button insertion')
modified_string = temp_string[:index] + '\n\t\t\t\t' + button_text + temp_string[index:]
kv_string = modified_string


class SquareButton(Button):
    """
    Creates a custom class inheriting from the kivy Button class, representing one of the squares on the board.
    """

    def on_size(self, square_coords='', *args):
        self.font_name = 'Arial.ttf'
        self.canvas.before.clear()
        with self.canvas.before:
            pass
            #BorderImage(border=(1, 1, 1, 1), size=(self.width, self.height), pos=(self.x,  self.y))
            # Color(0, 0, 0, 0)


Builder.load_string(kv_string)


class GessGameGUI(BoxLayout):

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



    def get_gess_game(self):
        """
        Returns the backend of the current Gess Game.
        :return: Returns the backend of the current Gess Game.
        """
        return self._gess_game

    def highlight_green_square(self, coordinates):
        self.ids[coordinates].background_color = (0, 1, 0, 1)

    def highlight_yellow_square(self, coordinates):
        self.ids[coordinates].background_color = (1, 1, 0, 1)

    def decolor_square(self, coordinates):
        self.ids[coordinates].background_color = (0, 0, 0, 0)

    def attempt_move(self, square_coords):
        """
        Sends a coordinate from a square.
        :param square_coords:
        :return:
        """

        global square_names

        if self._status == 'WAITING_FOR_SELECTION':
            print(f'Origin selected: {square_coords}')
            self._origin_square_selection = square_coords
            self.highlight_green_square(square_coords)

            square_index = square_names.index(square_coords)

            for square in (square_index - 22, square_index - 21, square_index - 20,
                            square_index - 1, square_index + 1,
                           square_index + 20, square_index + 21, square_index + 22):
                self.highlight_yellow_square(square_names[square])

            self._status = 'ORIGIN_SELECTED'
            return True

        if self._status == 'ORIGIN_SELECTED':
            print(f'Destination selected: {square_coords}')
            self._destination_square_selection = square_coords

            self.decolor_square(self._origin_square_selection)

            for square_name in square_names:
                self.decolor_square(square_name)

            if self._gess_game.make_move(self._origin_square_selection, self._destination_square_selection):
                print(f'Move from {self._origin_square_selection} to {self._destination_square_selection} successful.')
                self.update_board()
                self._status = 'WAITING_FOR_SELECTION'
                self._origin_square_selection = ''
                self._destination_square_selection = ''
                return True
            else:
                print('Invalid move')
                self._status = 'WAITING_FOR_SELECTION'
                self._origin_square_selection = ''
                self._destination_square_selection = ''
                return False

    def update_square(self, square_name, new_value):
        pass
        # self.square_name.text = new_value

    def update_current_status(self):
        if self._gess_game.get_game_state() == 'UNFINISHED':
            current_player = 'Black' if self._gess_game.get_current_player() == 'B' else 'White'
            self.ids['top_buffer'].text = 'Current Player: ' + current_player
        else:
            winning_player = 'Black' if self._gess_game.get_game_state() == 'BLACK_WON' else 'White'
            self.ids['top_buffer'].text = 'Game Over... ' + winning_player + ' Won!'

    def update_board(self):

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
            if square_contents == 'W':
                self.ids[square_name].text = u'\u25CF'
                self.ids[square_name].color = 0, 0, 0, 1
                self.ids[square_name].font_size = 40
                self.ids[square_name].bold = False
                self.ids[square_name].text_size = (0, 38)
            elif square_contents == 'B':
                self.ids[square_name].text = u'\u25CF'
                self.ids[square_name].color = 1, 1, 1, 1
                self.ids[square_name].font_size = 40
                self.ids[square_name].bold = False
                self.ids[square_name].text_size = (0, 38)
            else:
                self.ids[square_name].text = square_contents
                self.ids[square_name].color = 0, 0, 0, 1
                self.ids[square_name].font_size = 16
                self.ids[square_name].bold = True
                self.ids[square_name].text_size = (None, None)


        # Update the current status displayed at the top of the board
        self.update_current_status()





class GessApp(App):
    def build(self):
        return GessGameGUI()


if __name__ == '__main__':
    GessApp().run()

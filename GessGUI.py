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
                on_press: root.get_gess_game().resign_game()
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
                   f'\n\t\t\t\t\ttext: \' \'\n\t\t\t\t\tbackground_color: 0, 0, 0, 0.2\n\t\t\t\t\tid: {btn_id}' \
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

    def get_gess_game(self):
        """
        Returns the backend of the current Gess Game.
        :return: Returns the backend of the current Gess Game.
        """
        return self._gess_game

    def highlight_square(self, coordinates):
        self.ids[coordinates].background_color = (0, 1, 0, 1)

    def decolor_square(self, coordinates):
        self.ids[coordinates].background_color = (0, 0, 0, 0.2)

    def attempt_move(self, square_coords):
        """
        Sends a coordinate from a square.
        :param square_coords:
        :return:
        """

        if self._status == 'WAITING_FOR_SELECTION':
            print(f'Origin selected: {square_coords}')
            self._origin_square_selection = square_coords
            self.highlight_square(square_coords)
            self._status = 'ORIGIN_SELECTED'
            return True

        if self._status == 'ORIGIN_SELECTED':
            print(f'Destination selected: {square_coords}')
            self._destination_square_selection = square_coords

            self.decolor_square(self._origin_square_selection)
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

    def update_board(self):
        global square_names
        current_contents = []
        for row in self._gess_game.get_gess_board():
            for contents in row:
                current_contents.append(contents)

        # square_names is a list of the 'value' of each square on the display
        # current_contents is a list of the contents of each square on the Gess board
        square_names_and_contents = zip(square_names, current_contents)
        for (square_name, square_contents) in square_names_and_contents:
            self.ids[square_name].text = square_contents

        current_player = 'Black' if self._gess_game.get_current_player() == 'B' else 'White'
        self.ids['top_buffer'].text = 'Current Player: ' + current_player



class GessApp(App):
    def build(self):
        return GessGameGUI()


if __name__ == '__main__':
    GessApp().run()

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



kv_string = """
<GessGameGUI>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'top_buffer'
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
    button_text += f'SquareButton:\n\t\t\t\t\tsquare_coords: \'{btn_id}\'\n\t\t\t\t\ttext: \' \'\n\t\t\t\t\ton_press: root.attempt_move(self.square_coords)\n\t\t\t\t'

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
            Color(1, 1, 1, 1)


Builder.load_string(kv_string)


class GessGameGUI(BoxLayout):

    def __init__(self, **kwargs):
        global kv_string
        super(GessGameGUI, self).__init__(**kwargs)

        Builder.load_string(kv_string)

        self._square_names = []

        # for digit in range(20, -1, -1):
        #     if digit != 0:
        #         for letter in 'abcdefghijklmnopqrstu':
        #             if letter != 'u':
        #                 square_name_to_append = letter + str(digit)
        #             else:
        #                 square_name_to_append = str(digit)
        #             self._square_names.append(square_name_to_append)
        #     else:
        #         for letter in 'abcdefghijklmnopqrst':
        #             self._square_names.append(letter)
        #
        # button_text = ''
        # for btn_id in self._square_names:
        #     button_text += f'Button:\n\t\t\t\t\tid: {btn_id}\n\t\t\t\t\ttext: \' \'\n\t\t\t\t'#on_press: root.attempt_move(self.id)'


        # for square_name in self._square_names:
        #     self.named_button = SquareButton(text=square_name, id=square_name)
        #     self.ids['grid_layout'].add_widget(self.named_button)
        #     self.named_button.square_value = square_name
        #     self.named_button.bind(on_press=attempt_move)

        temp_string = kv_string
        index = temp_string.find(' # Button insertion')
        modified_string = temp_string[:index] + '\n\t\t\t\t' + button_text + temp_string[index:]
        kv_string = modified_string
        print(kv_string)



        # self.update_board()

    def attempt_move(self, square_coords):
        """
        Sends a coordinate from a square.
        :param square_coords:
        :return:
        """
        print(f'Pressed {square_coords}')

    def update_square(self, square_name, new_value):
        pass
        # self.square_name.text = new_value

    def update_board(self):
        pass
        # current_values = []
        # for row in GessGame().get_gess_board():
        #     for contents in row:
        #         current_values.append(contents)
        #
        # for current_index, current_value in enumerate(current_values):
        #     square_name_at_index = self._square_names[current_index]
        #     self.update_square(square_name_at_index, current_value)


class GessApp(App):
    def build(self):
        return GessGameGUI()


if __name__ == '__main__':
    GessApp().run()

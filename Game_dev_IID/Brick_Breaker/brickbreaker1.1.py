from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Brick Breaker Game'))
        self.start_button = Button(text='Start Game')
        self.start_button.bind(on_release=self.start_game)
        self.add_widget(self.start_button)
        self.add_widget(Label(text='Dark Mode:'))
        self.dark_mode_switch = Switch(active=False)
        self.dark_mode_switch.bind(active=self.on_dark_mode_switch_active)
        self.add_widget(self.dark_mode_switch)

    def start_game(self, instance):
        # Here you would add the logic to start the game
        print('Start game')

    def on_dark_mode_switch_active(self, instance, value):
        if value:
            with self.canvas.before:
                Color(0, 0, 0, 1)  # set color to black
                self.rect = Rectangle(size=self.size, pos=self.pos)
        else:
            with self.canvas.before:
                Color(1, 1, 1, 1)  # set color to white
                self.rect = Rectangle(size=self.size, pos=self.pos)

class BrickBreakerApp(App):
    def build(self):
        return GameScreen()

if __name__ == '__main__':
    BrickBreakerApp().run()

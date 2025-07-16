from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

players = ["Player1", "Player2", "Player3"]
commands = ["speed", "money", "invisible", "tp", "heal", "kick", "reset", "visible"]

class HackPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.spinner = Spinner(text='Oyuncu Seç', values=players)
        self.add_widget(self.spinner)

        self.cmd_input = TextInput(hint_text='Komut yaz (örnek: speed)', multiline=False)
        self.add_widget(self.cmd_input)

        self.run_button = Button(text='Komutu Gönder')
        self.run_button.bind(on_press=self.send_command)
        self.add_widget(self.run_button)

        self.status_label = Label(text='Durum: Bekleniyor...')
        self.add_widget(self.status_label)

    def send_command(self, instance):
        player = self.spinner.text
        command = self.cmd_input.text.lower()
        if player not in players:
            self.status_label.text = "❌ Oyuncu seçilmedi!"
        elif command not in commands:
            self.status_label.text = f"❌ '{command}' geçerli değil!"
        else:
            self.status_label.text = f"✅ {player} oyuncusuna '{command}' gönderildi."

class RobloxHackApp(App):
    def build(self):
        return HackPanel()

if __name__ == '__main__':
    RobloxHackApp().run()

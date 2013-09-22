from kivy.app import App
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from jnius import autoclass
import csv
import datetime
import sys
import os


class BetterTextInput(TextInput):
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        self.hook()
        super(BetterTextInput, self)._keyboard_on_key_down(window, keycode, text, modifiers)

    def hook(self):        
        raise NotImplementedError


class MainApp(App):
    def build(self):
        self.hw = autoclass('org.renpy.android.Hardware')
        self.hw.accelerometerEnable(1)
        self.hw.orientationSensorEnable(1)
        Clock.schedule_interval(self.update, 0.2)
        self.intro = self.root.ids['intro']
        self.setpath()
        self.root.ids['path'].text = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'readings.csv')
        self.root.ids['path'].hook = self.stop
        self.root.ids['path'].bind(focus=self.setpath)
        self.progress = self.root.ids['progress']
        self.capture = False
        self.n = 0

    def start(self):
        self.root.ids['path'].focus = False
        now = str(datetime.datetime.utcnow())
        self.intro.text = "Started capture at %s\n\nFile: %s\n" % (now, self.path)
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow('Timestamp x y z yaw pitch roll'.split(' '))
        self.capture = True

    def stop(self):
        if self.capture:
            self.intro.text += "Ended capture at %s" % str(datetime.datetime.utcnow())
        self.capture = False

    def setpath(self, *args):
        self.n = 0
        self.path = self.root.ids['path'].text
        self.intro.text = "File path set to '%s'" % self.path

    def update(self, dt):
        if self.capture:
            x, y, z = self.hw.accelerometerReading()
            yaw, pitch, roll = self.hw.orientationSensorReading()
            with open(self.path, 'a') as f:
                writer = csv.writer(f)
                now = str(datetime.datetime.utcnow())
                writer.writerow([now, x, y, z, yaw, pitch, roll])
                self.n += 1
        self.progress.text = '(%i rows)' % self.n

    def quit(self, btn_instance):
        sys.exit(0)


if __name__ == '__main__':
    MainApp().run()

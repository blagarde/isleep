from kivy.app import App
from kivy.clock import Clock
from jnius import autoclass
import csv
import datetime
import sys


class MainApp(App):
    def build(self):
        self.hw = autoclass('org.renpy.android.Hardware')
        self.hw.accelerometerEnable(1)
        self.hw.orientationSensorEnable(1)
        Clock.schedule_interval(self.update, 0.2)
        self.intro = self.root.ids['intro']
        self.setpath()
        self.progress = self.root.ids['progress']
        self.capture = False
        self.n = 0

    def start(self):
        self.n = 0
        now = str(datetime.datetime.utcnow())
        self.intro.text = "Started capture at %s\n\nFile: %s\n" % (now, self.path)
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow('Timestamp x y z yaw pitch roll'.split(' '))
        self.capture = True

    def stop(self):
        self.capture = False

    def setpath(self):
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

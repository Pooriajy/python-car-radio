import threading
import time
import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication
from qt_material import apply_stylesheet
import sys
import os
import random
import vlc


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.main = uic.loadUi('main.ui', self)
        self.playbtn.clicked.connect(self.playbtnfunc)
        self.volume.valueChanged.connect(self.setvolume)
        self.stopbtn.clicked.connect(self.stopmusic)
        self.applytheme.clicked.connect(self.changetheme)
        self.stations.currentItemChanged.connect(self.changeradio)
        self.actionExit.triggered.connect(self.exit)
        self.isplaying = False
        self.themes = ['dark_red.xml',
                                   'dark_blue.xml',
                                   'dark_cyan.xml',
                                   'dark_lightgreen.xml',
                                   'dark_pink.xml',
                                   'dark_purple.xml',
                                   'dark_amber.xml',
                                   'dark_teal.xml',
                                   'dark_yellow.xml',
                                   'light_amber.xml',
                                   'light_blue.xml',
                                   'light_cyan.xml',
                                   'light_cyan_500.xml',
                                   'light_lightgreen.xml',
                                   'light_pink.xml',
                                   'light_purple.xml',
                                   'light_red.xml',
                                   'light_teal.xml',
                                   'light_yellow.xml']

        self.currenttime = 0
        self.p = vlc.MediaPlayer(self.musicadrs.text())
        self.p.audio_set_volume(70)
        self.volume.setValue(70)
        self.volperc.setText(str(self.volume.value())+"%")
        ##
        self.streaming = False
        threading.Thread(target=self.count).start()
        self.choosetheme.addItems(self.themes)
        apply_stylesheet(self.main, self.themes[random.randint(0,7)])#select between dark themes
        self.show()
        ##
        self.stations.addItems(['Radio Javan',
                                'Radio Farda',
                                'Radio Golchin LA',
                                'Radio Shadi',
                                'IRAN Intel National',
                                'Radio Mojahed',
                                '',

                              'PARTY VIBE MUSIC : ALL THE HITS ALL THE TIME',
                              'Florida',
                              'RADIO ESTILO LEBLON',
                              'Classic Hits Global HD',
                              'Dance UK Radio danceradiouk',
                              'MoveDaHouse',


                                ])



    def stopmusic(self):
        self.p.stop()
        self.isplaying = False
        self.streaming = False
        QCoreApplication.processEvents()

    def setvolume(self):
        self.p.audio_set_volume(self.volume.value())
        self.volperc.setText(str(self.volume.value()) + "%")

    def playbtnfunc(self):
        if self.isplaying == False:
            self.isplaying = True
            self.streaming = True
            self.p = vlc.MediaPlayer(self.musicadrs.text())
            self.p.play()
            QCoreApplication.processEvents()



    def count(self):
        while(True):
            if self.streaming:
                self.currenttime = self.currenttime + 1
                self.streamtimer.display(str(datetime.timedelta(seconds=int(self.currenttime))))
                time.sleep(1)

    def changeradio(self):
        txt = self.stations.currentItem().text()
        if txt == "Radio Javan":
            self.sr("http://74.115.215.36/")
        elif txt == "Florida":
            self.sr("https://us4.internet-radio.com/proxy/douglassinclair?mp=/stream")
        elif txt == "RADIO ESTILO LEBLON":
            self.sr("https://us4.internet-radio.com/proxy/radioestiloleblon?mp=/stream")
        elif txt == "Classic Hits Global HD":
            self.sr("https://us2.internet-radio.com/proxy/chglobal?mp=/stream") # got tired of typing so i created the setText function :)
        elif txt == "Dance UK Radio danceradiouk":
            self.sr("https://uk2.internet-radio.com/proxy/danceradiouk?mp=/stream")
        elif txt == "MoveDaHouse":
            self.sr("https://uk7.internet-radio.com/proxy/movedahouse?mp=/stream")
        elif txt == "PARTY VIBE MUSIC : ALL THE HITS ALL THE TIME":
            self.sr("https://uk6.internet-radio.com/proxy/pvradio?mp=/stream")
        elif txt == "Radio Farda":
            self.sr("https://n09.radiojar.com/cp13r2cpn3quv?rj-ttl=5&rj-tok=AAABfETSRHkARIIGrQfYDMazLQ")
        elif txt == "IRAN Intel National":
            self.sr("https://radio.iraninternational.app/iintl_c")
        elif txt == "Radio Golchin LA":
            self.sr("https://radiogolchin.out.airtime.pro/radiogolchin_a")
        elif txt == "Radio Shadi":
            self.sr("https://ice9.securenetsystems.net/SHADI")
        elif txt == "Radio Mojahed":
            self.sr("https://s2.radio.co/s830691c74/listen")

    def changetheme(self):
        apply_stylesheet(self.main ,self.choosetheme.currentText())
    def sr(self,txt):
        self.musicadrs.setText(txt)
        self.p.stop()
        self.isplaying = False
        self.playbtnfunc()

    def exit(self):
        os._exit(1)
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

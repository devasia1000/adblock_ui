#!/usr/bin/python
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
import sys
import socket
import os
import json
import thread

os.putenv('DISPLAY', ':0.0') # REQUIRED for startup on raspberry pi 
sys.path.insert(0, '/home/pi/zigbee_spi/')
from writer import init, set_led_on, set_led_off
from wink import setWinkLightbulbState

adblockStatus = False
cachingStatus = False
zigbeeStatus = False
    
adblockEnabledFile = '/etc/dnsmasq.d/dnsmasq.adlist.conf'
adblockDisabledFile = '/home/pi/dnsmasq.adlist.conf'

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(495, 300)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(self.centralWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.label_5 = QtGui.QLabel(self.centralWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dial = QtGui.QDial(self.centralWidget)
        self.dial.setObjectName(_fromUtf8("dial"))
        self.horizontalLayout.addWidget(self.dial)
        self.dial_2 = QtGui.QDial(self.centralWidget)
        self.dial_2.setObjectName(_fromUtf8("dial_2"))
        self.horizontalLayout.addWidget(self.dial_2)
        self.dial_3 = QtGui.QDial(self.centralWidget)
        self.dial_3.setObjectName(_fromUtf8("dial_3"))
        self.horizontalLayout.addWidget(self.dial_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 52))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 495, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuRouter_Interface = QtGui.QMenu(self.menuBar)
        self.menuRouter_Interface.setObjectName(_fromUtf8("menuRouter_Interface"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuRouter_Interface.addAction(self.actionExit)
        self.menuBar.addAction(self.menuRouter_Interface.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Adblock", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Page-caching", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Zigbee", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Adblock is ALWAYS enabled.\nThis dial has no effect", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Disabled", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Disabled", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRouter_Interface.setTitle(QtGui.QApplication.translate("MainWindow", "Router Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        
        # Disable Adblock dial
        self.dial.value = 100
        self.dial.setEnabled(False)
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", 'Enabled', None, QtGui.QApplication.UnicodeUTF8))

        # Track changes to dials
        self.dial_2.valueChanged.connect(self.movedPageCachingDial)
        self.dial_3.valueChanged.connect(self.movedZigbeeDial)

    def disableDnsAdblock(self):
        global adblockEnabledFile
        global adblockDisabledFile
        os.system('sudo rm /etc/dnsmasq.d/dnsmasq.adlist.conf')
        os.system('sudo service dnsmasq restart &')

    def enableDnsAdblock(self):
        global adblockEnabledFile
        global adblockDisabledFile
        os.system('sudo ln -s /etc/dnsmasq.adlist.conf /etc/dnsmasq.d/dnsmasq.adlist.conf')
        os.system('sudo service dnsmasq restart &')
        
    def sendDataToProxy(self, message):
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect(('localhost', 9000))
         s.send(message)
         s.close()

    def movedAdblockDial(self, pos):
        global adblockStatus
        label_str = ""

        #print 'Adblock slider has been moved to ', pos
        if pos >= 50:
            label_str = 'Enabled'
        elif pos < 50:
            label_str = 'Disabled'
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", label_str, None, QtGui.QApplication.UnicodeUTF8))
        
        if pos >= 50 and adblockStatus is False:
            adblockStatus = True
            self.enableDnsAdblock()
            self.sendDataToProxy('enableAdblock')
        elif pos < 50 and adblockStatus is True:
            adblockStatus = False
            self.disableDnsAdblock()
            self.sendDataToProxy('disableAdblock')

    def movedPageCachingDial(self, pos):
        global cachingStatus
        label_str = ""
        
        #print 'Page caching slider has been moved to ', pos
        if pos >= 50:
            label_str = 'Enabled'
        elif pos < 50:
            label_str = 'Disabled'
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", label_str, None, QtGui.QApplication.UnicodeUTF8))
        
        if pos >= 50 and cachingStatus is False:
            cachingStatus = True
            self.sendDataToProxy('enableCaching')
        elif pos < 50 and cachingStatus is True:
            cachingStatus = False
            self.sendDataToProxy('disableCaching')

    def movedZigbeeDial(self, pos):
        global zigbeeStatus
        label_str = ""
        
        #print 'Zigbee dial has been moved to ', pos
        if pos >= 50:
            label_str = 'Enabled'
        else:
            label_str = 'Disabled'
        self.label.setText(QtGui.QApplication.translate("MainWindow", label_str, None, QtGui.QApplication.UnicodeUTF8))    

        if pos >= 50 and zigbeeStatus is False:
            zigbeeStatus = True
        elif pos < 50 and zigbeeStatus is True:
            zigbeeStatus = False

def start_zigbee():
    spi = init()
  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('52.25.165.62', 80))
    print 'Connected to SmartThings endpoint'    
    
    global zigbeeStatus
    while True:
        message = client_socket.recv(4096)
        data = json.loads(message)
        
        if zigbeeStatus == False:
            print 'Ignoring Zigbee message since zigbee_status is', zigbeeStatus
            continue

        led = data['display_name']
        value = data['value']

        print led, 'is', value
        if led == 'LED #1':
            if value == 'on':
                set_led_on(spi)
                setWinkLightbulbState(False)
            if value == 'off':
                set_led_off(spi)
                setWinkLightbulbState(True)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.showMaximized()
    
    os.system('java -cp /home/pi/java_http_proxy/out/production/java_http_proxy/:/home/pi/java_http_proxy/out/production/java_http_proxy/* Main /home/pi/java_http_proxy/blocklist.txt 2>&1 | tee /home/pi/proxy_log.txt &')

    thread.start_new_thread(start_zigbee, ())
    sys.exit(app.exec_())

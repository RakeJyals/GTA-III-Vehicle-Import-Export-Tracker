from ReadWriteMemory import ReadWriteMemory
import copy
import math

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

#Note: Application will crash if gta3.exe is not open. Need to have exception that tries again later
rwm = ReadWriteMemory()
process = rwm.get_process_by_name("gta3.exe") #Note that this fails when GTA 3 is closed or restarted
process.open()

#Getting raw data, needs try loop until process is found
portland_garage_pt = process.get_pointer(0x8F295C)
portland_crane_pt = process.get_pointer(0x906540)
shoreside_garage_pt = process.get_pointer(0x8F2960)

port_garage_list = ["Securicar", "Moonbeam", "Coach", "Flatbed", "Linerunner", "Trashmaster", "Patriot", "Mr. Whoopee", \
    "Blista", "Mule", "Yankee", "Bobcat", "Dodo", "Bus", "Rumpo", "Pony"]

port_crane_list = ["Firetruck", "Ambulance", "Enforcer", "FBI Car", "Tank (End)", "Barracks OL (Shima)", "Copcar"]

shore_garage_list = ["Sentinel (4 Door Emblem)", "Cheetah", "Banshee", "Idaho (2 Door, 2 Color)", "Infernus (Spoiler)", "Taxi", "Kuruma", "Stretch", "Perennial", "Stinger (Yakuza Car)", \
    "Manana", "Landstalker (Wheel on Back)", "Stallion (Hood Holes)", "BF Injection (RTB)", "Cabbie", "Esperanto (2 Door, 1 Color)"]


global port_garage_remaining
global port_crane_remaining
global shore_garage_remaining
port_garage_remaining = copy.copy(port_garage_list)
port_crane_remaining = copy.copy(port_crane_list)
shore_garage_remaining = copy.copy(shore_garage_list)


global port_garage_cars
global port_crane_cars
global shore_garage_cars
port_garage_cars = process.read(portland_garage_pt)
port_crane_cars = process.read(portland_crane_pt)
shore_garage_cars = process.read(shoreside_garage_pt)



class InfoDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GTA 3 Car Collection Tracker")

        self.resize(1000, 500)
        self.move(4600,725)
        self.portGarage = QLabel()
        self.portGarage.setFont(QFont("Arial", 14))
        self.portCrane = QLabel()
        self.portCrane.setFont(QFont("Arial", 14))
        self.shoreGarage = QLabel()
        self.shoreGarage.setFont(QFont("Arial", 14))
        layout = QHBoxLayout()
        layout.addWidget(self.shoreGarage)
        layout.addWidget(self.portGarage)
        layout.addWidget(self.portCrane)
        self.setLayout(layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDisplay)
        
        self.timer.start(1000)


    def updateDisplay(self): #Loop goes here
        #Update data from RAM
        global port_garage_cars
        global port_crane_cars
        global shore_garage_cars
        global port_garage_remaining
        global port_crane_remaining
        global shore_garage_remaining
        port_garage_cars_old = port_garage_cars
        port_crane_cars_old = port_crane_cars
        shore_garage_cars_old = shore_garage_cars

        port_garage_cars = process.read(portland_garage_pt)
        port_crane_cars = process.read(portland_crane_pt)
        shore_garage_cars = process.read(shoreside_garage_pt)

        
        #Update lists of remaning cars
        if port_garage_cars == 0 and port_crane_cars == 0 and shore_garage_cars == 0: #Rework to support decrease from loading semi complete save file?
            port_garage_remaining = copy.copy(port_garage_list)
            port_crane_remaining = copy.copy(port_crane_list)
            shore_garage_remaining = copy.copy(shore_garage_list)


        if port_garage_cars > port_garage_cars_old:
            collected_car_bit = int(math.log(port_garage_cars - port_garage_cars_old, 2))
            port_garage_remaining.remove(port_garage_list[collected_car_bit])

        if port_crane_cars > port_crane_cars_old:
            collected_car_bit = int(math.log(port_crane_cars - port_crane_cars_old, 2))
            port_crane_remaining.remove(port_crane_list[collected_car_bit])

        if shore_garage_cars > shore_garage_cars_old:
            collected_car_bit = int(math.log(shore_garage_cars - shore_garage_cars_old, 2))
            shore_garage_remaining.remove(shore_garage_list[collected_car_bit])


        #Display: Using plaintext for portland (for now), HTML for shoreside vale
        port_garage_string = "Portland Garage:\n\n"
        for car in port_garage_remaining:
            port_garage_string += car + "\n"
        self.portGarage.setText(port_garage_string)

        port_crane_string = "Portland Crane:\n\n"
        for car in port_crane_remaining:
            port_crane_string += car + "\n"
        self.portCrane.setText(port_crane_string)

        shore_garage_string = "Shoreside Vale Garage:\n\n"
        for car in shore_garage_remaining:
            shore_garage_string += car + "\n"
        self.shoreGarage.setText(shore_garage_string)
        
        
        
        #self.portGarage.setText("<p><font color='blue'>Test</font></p><p>test2</p>") #Placeholder


app = QApplication(sys.argv)
win = InfoDisplay()
win.show()





#Should activate this on closing of window
app.exec()
process.close()
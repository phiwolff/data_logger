# -*- coding: utf-8 -*-
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
import numpy as np
import serial
import matplotlib as plt
import matplotlib.pyplot as plt
import threading
from datetime import datetime
import matplotlib.dates as md
import time
import csv

def update(frame):

    x_data, y_data1, y_data2, y_data3, y_data4, y_data5, y_data6 = values(x=None, y1=None, y2=None, y3=None, y4=None, y5=None, y6=None)      
    line2.set_data(x_data, y_data2)
    line3.set_data(x_data, y_data3)
    line4.set_data(x_data, y_data4)
    line5.set_data(x_data, y_data5)
    line6.set_data(x_data, y_data6)
    
    figure.gca().relim()
    figure.gca().autoscale_view()
 
    return line2, line3, line4, line5, line6


def thread_function():
    x_data = []
    y_data1 = []
    y_data2 = []
    y_data3 = []
    y_data4 = []
    y_data5 = []
    y_data6 = []
    counter = 0
    totalTime = 0
    

    while(True):
        
        response = ser.readline()
        response = response.decode().strip().split()
        if(len(response) > 0):
            
            if (counter == 0):
                pyplot.title('Software Versionsnummer: '+ str(response[0]))
                 
            response = list(map(int, response))
     
            if counter == 0:
                last_time = current_milli_time()
    
            this_time = current_milli_time()
            
            if counter != 0:
                difference = this_time - last_time
                totalTime += difference
            
            last_time = this_time
    
            counter += 1
    
            x_data.append(totalTime)
            # response[0] ist sw versionsnummer
            y_data1.append(response[0])
            y_data2.append(response[1])
            y_data3.append(response[2])
            y_data4.append(response[3])
            y_data5.append(response[4])
            y_data6.append(response[5])
    

    
            if counter == 1:
                
          
                
                with open('Log_Data.csv', 'w', newline='') as file:
        
                    writer = csv.writer(file)
                    kanal2neu = "Kanal 2 (Faktor: " + str(kanal2) + ")"
                    kanal3neu = "Kanal 3 (Faktor: " + str(kanal3) + ")"
                    kanal4neu = "Kanal 4 (Faktor: " + str(kanal4) + ")"
                    kanal5neu = "Kanal 5 (Faktor: " + str(kanal5) + ")"
                    kanal6neu = "Kanal 6 (Faktor: " + str(kanal6) + ")"
                    writer.writerow(["Zeit", kanal2neu,  kanal3neu,  kanal4neu,  kanal5neu,  kanal6neu])
                    writer.writerow([totalTime,  response[1],  response[2],  response[3],  response[4],  response[5]])
    
                    
            if counter > 1 :
                
                with open('Log_Data.csv', 'a', newline='') as file:
    
                    writer = csv.writer(file)
     
                    writer.writerow([totalTime,  response[1],  response[2],  response[3],  response[4],  response[5]])
    
                
            # setzte neue Werte
            values(x_data, y_data1, y_data2, y_data3, y_data4, y_data5, y_data6, True)

        
def values(x,y1,y2,y3,y4,y5,y6,check=False):

    global resX, resY1, resY2, resY3, resY4, resY5, resY6

    
    if(check):
        resX = x
        resY1 = y1
        resY2 = y2
        resY3 = y3
        resY4 = y4
        resY5 = y5
        resY6 = y6
        return resX,resY1,resY2,resY3,resY4,resY5,resY6
    else:
        return resX,resY1,resY2,resY3,resY4,resY5,resY6
            
def on_click(event):
    
    state = figure.canvas.manager.toolbar.mode
    # wenn kein tool ausgewählt ist und dann auf den canvas geklickt wird,
    # dann soll autoscale wieder eingeschaltet werden
    if state == '':
        print("no tool selected")
        plt.autoscale(True)
        
    # wemm Tool ausgewählt, soll das     
    if state == 'zoom rect':
        plt.autoscale(False)
    if state == 'pan/zoom':
        plt.autoscale(False)



if __name__ == "__main__":
    
    current_milli_time = lambda: int(round(time.time()))
    x_data, y_data1, y_data2, y_data3, y_data4, y_data5, y_data6 = values([],[],[],[],[],[],[],True)
    
    global kanal2,  kanal3,  kanal4,  kanal5,  kanal6
    
    kanal2 = input("Name Kanal 2 und Faktor: ")
    kanal3 = input("Name Kanal 3 und Faktor: ")
    kanal4 = input("Name Kanal 4 und Faktor: ")
    kanal5 = input("Name Kanal 5 und Faktor: ")
    kanal6 = input("Name Kanal 6 und Faktor: ")

    figure = pyplot.figure()
    line2, = pyplot.plot(x_data, y_data2, '-',  marker='o', label = 'Kanal2: ' + str(kanal2))
    line3, = pyplot.plot(x_data, y_data3, '-',  marker='o', label = 'Kanal3: ' + str(kanal3))
    line4, = pyplot.plot(x_data, y_data4, '-',  marker='o', label = 'Kanal4: ' + str(kanal4))
    line5, = pyplot.plot(x_data, y_data5, '-',  marker='o', label = 'Kanal5: ' + str(kanal5))
    line6, = pyplot.plot(x_data, y_data6, '-',  marker='o', label = 'Kanal6: ' + str(kanal6))
    
    plt.legend(loc="upper left")
    
    pyplot.title("")
    pyplot.xlabel("Zeit[s]")
    pyplot.ylabel("Wert")
    
    plt.axis([0,3,0,255])
    plt.axis('auto')

    port = "/dev/ttyUSB0"
      
    ser = serial.Serial()
    ser.baudrate = 1200
    ser.port = port
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    
    try:
        ser.open()
    except Exception as e:
        print('Error: ' +  str(e))
      
    
    x = threading.Thread(target=thread_function, args=())
    x.start()

    animation = FuncAnimation(figure, update, interval=1000)
    
    plt.connect('button_press_event', on_click)

    
    plt.grid(b=True, which='major', color='k', linestyle='-')
    plt.grid(b=True, which='minor', linewidth='2.', color='k', linestyle='-', alpha=0.2)
    plt.minorticks_on()
            
    pyplot.show()





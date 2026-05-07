#!/usr/bin/env python3
"""
<plugin key="BIOMAX970" name="BIOMAX970" version="1.0.1" author="Mircool">
    <params>
        <param field="SerialPort" label="Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="1" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""
import serial
import Domoticz
import time


class C14_RS485:
    def buildframe(ValueType, RecipientAddress, SenderAddress, ValueNumbers):
        bFrame = bytearray(30)
        bFrame[0] = 128 + RecipientAddress
        bFrame[1] = ord(ValueType)
        bFrame[3] = SenderAddress
        i=6
        for vanu in ValueNumbers:
            bFrame[i] = vanu
            i = i+4
        bFrame[29] = ord('#')
        bFrame[2] = (sum(bFrame) - bFrame[2]) & 0x7F # checksum
        return bFrame

    def readframe(bFrame):
        for i in range(10):
            ser= serial.Serial('/dev/ttyACM0', 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
            ser.write(bFrame)
            rFrame = ser.read(30)
            ser.close()
            time.sleep(1)
            if ((list(rFrame)[0]) == (bFrame)[3]+128):
               return rFrame

class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.serial = ""
        self.bFrames = 0
        self.bFrame = 0
        self.rFrame = 0
        return


    def onStart(self):
        devicecreated = []
        Domoticz.Log("BIOMAX970 plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1
        if 1 not in Devices:
            Domoticz.Device(Name="Temperatura zew,", Unit=1, Type=80, Subtype=5).Create()
            Domoticz.Device(Name="Temperatura kotła", Unit=2, Type=80, Subtype=5).Create()
            Domoticz.Device(Name="Temperatura CWU", Unit=3, Type=80, Subtype=5).Create()

        self.runInterval = int(Parameters["Mode3"]) * 6

    def onStop(self):
        Domoticz.Log("BIOMAX970 plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            bFrame =  C14_RS485.buildframe('T',1, 113, [1, 2, 3, 4, 43, 11])
            rFrame =  C14_RS485.readframe(bFrame)
            tempZew = round(((rFrame[7] * 128 + rFrame[8] - 2000) * 0.1), 2)
            Devices[1].Update(0,str(tempZew))
            tempKot = round(((rFrame[11] * 128 + rFrame[12] - 2000) * 0.1), 2)
            Devices[2].Update(0,str(tempKot))
            tempCwu = round(((rFrame[15] * 128 + rFrame[16] - 2000) * 0.1), 2)
            Devices[3].Update(0,str(tempCwu))
            #Domoticz.Log("BIOMAX970 ok")

            self.runInterval = int(Parameters["Mode3"]) * 6

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BioMax970 Plugin
#
# Author: mircolo
"""
<plugin key="BIOMAX970" name="BIOMAX 970" author="mircolo" version="1.0" wikilink="https://github.com/mircolo/biomax970">
    <params>
        <param field="Address" label="Port USB" width="100px" required="true" default="/dev/ttyUSB0"/>
        <param field="Mode1" label="Rejestry danych" width="400px" required="true" default="T;100;1;1,2,3,4"/>
        <param field="Mode2" label="Częstotliwość odczytu" width="30px" required="true" default="60"/>
        <param field="Mode3" label="Interwał między odczytami" width="30px" required="true" default="3"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import serial

@unique
class unit(IntEnum):
    """
        Device Unit numbers
        Define here your units numbers. These can be used to update your devices.
        Be sure the these have a unique number!
    """

    # INWENTERTEMP = 1
    temp_zewn = 1
    temp_piec = 2

class BasePlugin:

    __HEARTBEATS2MIN = 2
    __MINUTES = 1

    __UNITS = [
    [unit.temp_zewn, "Temperatura zewnętrzna", 80, 5, {"Custom": "0;Â°C"}, 1],
    [unit.temp_piec, "Temperatura pieca", 80, 5, {"Custom": "0;Â°C"}, 1],
        ]

    def __init__(self):
        self.__runAgain = 0

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)
        Domoticz.Debug("onStart called")
        # Validate parameters
        # --------------------------------------------------------------------------------
        # The provided images do, for some reason, conflit with Domoticz!!!
        # --------------------------------------------------------------------------------
        # Images
        # Check if images are in database
        # if "xfrpimonitor" not in Images:
        #     Domoticz.Image("xfrpimonitor.zip").Create()
        # image = Images["xfrpimonitor"].ID
        # Domoticz.Debug("Image created. ID: {}".format(image))
        #
        # Create devices
        for unit in self.__UNITS:
            if unit[0] not in Devices:
                Domoticz.Device(
                    Unit=unit[0],
                    Name=unit[1],
                    Type=unit[2],
                    Subtype=unit[3],
                    Options=unit[4],
                    Used=unit[5],
                    # Image=image,
                ).Create()
        # Log config
        DumpAllToLog()

    def onStop(self):
        Domoticz.Debug("onStop")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug(
            "onConnect {}={}:{} {}-{}".format(
                Connection.Name,
                Connection.Address,
                Connection.Port,
                Status,
                Description,
            )
        )

    def onMessage(self, Connection, Data):
        Domoticz.Debug(
            "onMessage {}={}:{}".format(
                Connection.Name, Connection.Address, Connection.Port
            )
        )

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand: {}, {}, {}, {}".format(unit, command, level, hue))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug(
            "onNotification: {}, {}, {}, {}, {}, {}, {}".format(
                name, subject, text, status, priority, sound, imagefile
            )
        )

    def onDisconnect(self, Connection):
        Domoticz.Debug(
            "onDisconnect {}={}:{}".format(
                Connection.Name, Connection.Address, Connection.Port
            )
        )

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat")
        self.__runAgain -= 1
        if self.__runAgain <= 0:
            self.__runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
            #
            fnumber = getCPUtemperature()
            #Domoticz.Debug("CPU temp ..........: {} Â°C".format(fnumber[151]))
            UpdateDevice(unit.atemp_zewn, int(0), str(fnumber[12]), TimedOut=0)
            UpdateDevice(unit.acemp_piec, int(0), str(fnumber[26]), TimedOut=0)

        else:
            Domoticz.Debug(
                "onHeartbeat called, run again in {} heartbeats.".format(
                    self.__runAgain
                )
            )

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

################################################################################
# Generic helper functions
################################################################################


def DumpDevicesToLog():
    # Show devices
    Domoticz.Debug("Device count.........: {}".format(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device...............: {} - {}".format(x, Devices[x]))
        Domoticz.Debug("Device Idx...........: {}".format(Devices[x].ID))
        Domoticz.Debug(
            "Device Type..........: {} / {}".format(Devices[x].Type, Devices[x].SubType)
        )
        Domoticz.Debug("Device Name..........: '{}'".format(Devices[x].Name))
        Domoticz.Debug("Device nValue........: {}".format(Devices[x].nValue))
        Domoticz.Debug("Device sValue........: '{}'".format(Devices[x].sValue))
        Domoticz.Debug("Device Options.......: '{}'".format(Devices[x].Options))
        Domoticz.Debug("Device Used..........: {}".format(Devices[x].Used))
        Domoticz.Debug("Device ID............: '{}'".format(Devices[x].DeviceID))
        Domoticz.Debug("Device LastLevel.....: {}".format(Devices[x].LastLevel))
        Domoticz.Debug("Device Image.........: {}".format(Devices[x].Image))


def DumpImagesToLog():
    # Show images
    Domoticz.Debug("Image count..........: {}".format((len(Images))))
    for x in Images:
        Domoticz.Debug("Image '{}'...: '{}'".format(x, Images[x]))


def DumpParametersToLog():
    # Show parameters
    Domoticz.Debug("Parameters count.....: {}".format(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter '{}'...: '{}'".format(x, Parameters[x]))


def DumpSettingsToLog():
    # Show settings
    Domoticz.Debug("Settings count.......: {}".format(len(Settings)))
    for x in Settings:
        Domoticz.Debug("Setting '{}'...: '{}'".format(x, Settings[x]))


def DumpAllToLog():
    DumpDevicesToLog()
    DumpImagesToLog()
    DumpParametersToLog()
    DumpSettingsToLog()


def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=True):
    if Unit in Devices:
        if (
            Devices[Unit].nValue != nValue
            or Devices[Unit].sValue != sValue
            or Devices[Unit].TimedOut != TimedOut
            or AlwaysUpdate
        ):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            # Domoticz.Debug("Update {}: {} - '{}'".format(Devices[Unit].Name, nValue, sValue))


def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        if Devices[Unit].Options != Options:
            Devices[Unit].Update(
                nValue=Devices[Unit].nValue,
                sValue=Devices[Unit].sValue,
                Options=Options,
            )
            # Domoticz.Debug(
            #     "Device Options update: {} = {}".format(Devices[Unit].Name, Options)
            # )

global _last_idle, _last_total
_last_idle = _last_total = 0


def getBits(value, start, length):
    return (value >> start) & 2 ** length - 1

def getCPUtemperature():
    try:
        # res = os.popen("mpp-solar -p /dev/hidraw0 -c QPIGS | grep inverter_heat_sink_temperature | awk '{sum=$2}; END {print sum}'").readline()
        res = os.popen("mpp-solar -p /dev/ttyUSB0 -P PI30MAX -c QPIGS").read().split()
    except:
        res = "0"
    return res

def getpvb():
    try:
        res = os.popen("mpp-solar -p /dev/ttyUSB0 -P PI30MAX -c QPIGS2").read().split()
    except:
        res = "0"
    return res

def getstatus():
    try:
        res = os.popen("mpp-solar -p /dev/ttyUSB0 -P PI30MAX -c QMOD | grep device_mode | awk '{sum=$2}; END {print sum}'").readline()
    except:
        res = "0"
    return res

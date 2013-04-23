""" Ambient Hue Lighting Controller Service
    Regularly sets a Phillips Hue light to the average screen colour
    Usage : python ambiservice.py install (or / then start, stop, remove)
"""

import win32service
import win32serviceutil
import win32api
import win32event
import servicemanager
from phue import Bridge
import ambihue

# Modify the follow two lines to fit your system
hubIP = "192.168.1.42"
lightID = 2


class hueService(win32serviceutil.ServiceFramework):
   
    _svc_name_ = "ambihue"
    _svc_display_name_ = "Ambient Hue Lighting"
    _svc_description_ = "Monitors screen colours to change the light of a Phillips Hue lamp"
    bridge = None
         
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.bridge = Bridge(hubIP)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        command = {'transitiontime': 25, 'on': False}
        self.bridge.set_light(lightID, command)
        win32event.SetEvent(self.hWaitStop)
         
    def SvcDoRun(self):
        # Leave a message in Event Viewer that the service has started
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))

        self.timeout = 500  # This is how long the service will wait to run / refresh itself


        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
            # Stop signal encountered
                servicemanager.LogInfoMsg("AmbiHue - STOPPED!")  #For Event Log
                break
            else:

                #Ok, here's the real money shot right here.
                #[actual service code between rests]
                r, g, b = ambihue.getAverageScreenColor()
                ambihue.turnLightToColor(self.bridge, lightID, r, g, b)
                #[actual service code between rests]


def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(hueService)

# Done! Lets go out and get some dinner, bitches!
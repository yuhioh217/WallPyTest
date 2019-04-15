import objc
import os
import socket
from access_points import get_scanner


class wifiScan():
  def __init__(self):
    wifi_scanner = get_scanner()
    wifi_scanner.get_access_points()
    self.result = wifi_scanner.get_access_points()

  def getWifiList(self):
    return self.result


class windows_wifiConnection():
  def __init__(self):
    self.ssid = ''

  def setWifiSSID(self, ssid):
    self.ssid = ssid


class linux_wifiConnection():
  def __init__(self):
    self.ssid = ''

  def setWifiSSID(self, ssid):
    self.ssid = ssid


class macOS_wifiConnection():
  def __init__(self):
    self.ssid = ''
    self.password = ''

  def setWifiSSID(self, ssid):
    self.ssid = ssid
  
  def setWifiPassword(self, password):
    self.password = password

  def wifi_connect(self):
    try:
      objc.loadBundle('CoreWLAN',
        bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
        module_globals=globals())
      iface = CWInterface.interface() # CWInterface is provided by MacOS system not in python module, get from CoreWLAN obect-C
      networks, scan_error = iface.scanForNetworksWithName_error_(self.ssid, None)
      network = networks.anyObject()
      connect_success, connect_error = iface.associateToNetwork_password_error_(network, self.password , None)
      if connect_success:
        print('Successful to connect wifi ' + self.ssid)
        hostname = socket.gethostname() 
        IPAddr = socket.gethostbyname(hostname)
        #print('curl --insecure --data "show_video_id:=BBB|http://' + IPAddr + ':8080/spain.mp4" -H "Content-Type:application/json" -X POST https://192.168.43.1:8080/command')
        a = os.popen('curl --insecure --data "show_video_id:=BBB|http://' + IPAddr + ':8080/spain.mp4" -H "Content-Type:application/json" -X POST https://192.168.43.1:8080/command').readlines()
        print(a)
      if connect_error:
        print('!!!! failed to connect wifi "' + self.ssid + '"')
    except Exception as e:
      print(e)



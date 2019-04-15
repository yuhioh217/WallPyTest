from access_points import get_scanner
from src.wifiScanning import wifiScan, macOS_wifiConnection, windows_wifiConnection

if __name__ == "__main__":
  # scanning the wifi and prepare the config file for testing
  scan = wifiScan()
  wifiList = scan.getWifiList()
  testAPArr = []
  for wifi in wifiList:
    if 'VAP' in wifi.ssid:
      testAPArr.append(wifi.ssid)
  
  # macOS connection version
  print(testAPArr)
  wifiController = macOS_wifiConnection()
  for testAP in testAPArr:
    wifiController.setWifiSSID(testAP)
    wifiController.setWifiPassword('Videri123')
    wifiController.wifi_connect()

  

  
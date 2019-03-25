import os
import sys
import json
import time
import requests

def control(argv):
  if len(argv.split('.')) == 4:
    result = os.popen("adb connect " + argv).read()
    fileList = []
    # print(result)
    if 'unable' in result:
      print('connection failed.')
    elif 'connected' in result:
      print('connection successful')
      list = os.popen("adb ls /sdcard/Android/data/swpc.wistron.com.wiwall.tv/files/logs/").read()
      for file in (list.split(' ')):
        if 'txt' in file:
          fileList.append(file.split('\n')[0])
      # print(fileList)
      time.sleep(2)
      os.popen("adb pull /sdcard/Android/data/swpc.wistron.com.wiwall.tv/files/logs/" + fileList[0] + " ./recordfile")
      time.sleep(4)
      os.rename('./recordfile/'+ fileList[0], './recordfile/' + argv + '_' + fileList[0])
      os.popen("adb shell \"su 0 rm -rf /sdcard/Android/data/swpc.wistron.com.wiwall.tv/files/logs/" + fileList[0] + "\"")
      os.popen("adb shell \"su 0 rm -rf /data/data/swpc.wistron.com.wiwall.tv/cache\"")
      os.popen("adb shell \"su 0 rm -rf /data/data/swpc.wistron.com.wiwall.tv/code_cache\"")
      os.popen("adb shell \"su 0 rm -rf /data/data/swpc.wistron.com.wiwall.tv/databases\"")
      os.popen("adb shell \"su 0 rm -rf /data/data/swpc.wistron.com.wiwall.tv/files\"")
      os.popen("adb shell \"su 0 rm -rf /data/data/swpc.wistron.com.wiwall.tv/shared_prefs\"")
      time.sleep(2)
      os.popen("adb shell \"su 0 rm -rf /sdcard/WiWall/Download\"")
      time.sleep(2)
      os.popen("adb reboot")
      os.popen("adb disconnect")
      time.sleep(1)
      return argv + '_' + fileList[0]
  else:
    print('Your ip address is invalid, please try again.')
    return "null"

def processTime(file):
  start_time = 0
  end_time = 0
  tempTime = ''
  f = open('./recordfile/' + file)
  for line in f:
    if "enque download" in line:
      tempTime = (line.split(' ')[1]).split('.')[0]
      start_time = int(tempTime.split(':')[0]) * 3600 + int(tempTime.split(':')[1]) * 60 + int(tempTime.split(':')[2])
    if "downloadComplete" in line:
      tempTime = (line.split(' ')[1]).split('.')[0]
      end_time = int(tempTime.split(':')[0]) * 3600 + int(tempTime.split(':')[1]) * 60 + int(tempTime.split(':')[2])
  return secondToDateString(end_time - start_time)

def timeStrToInt(timeStr):
  return int(timeStr.split(':')[0]) * 3600 + int(timeStr.split(':')[1]) * 60 + int(timeStr.split(':')[2])

def secondToDateString(value):
  hourInt = int(value/3600)
  minInt  = int((value - (hourInt*3600))/60)
  secInt  = int(value - hourInt*3600 - minInt*60)
  # print(str(hourInt) , ':' , str(minInt) , ':' , str(secInt))
  return str(hourInt) + ':' + str(minInt) + ':' + str(secInt)

def loadSetting():
  with open('config.json', 'r') as json_data_file:
    data = json.load(json_data_file)
  return data

def fetch_api_request(modelName):
  # api name https://7nqd4bdcal.execute-api.ap-northeast-1.amazonaws.com/test/checksplitting
  r = requests.post(
    'https://7nqd4bdcal.execute-api.ap-northeast-1.amazonaws.com/test/checksplitting',
    json = {'wall_name':modelName}
  )
  # print(r.json())
  return r.json()

def aws_lambda_timing(modelName):
  try:
    json_result = fetch_api_request(modelName)
    lambda_start_time = timeStrToInt((str((((json_result[0])["playlistData"])[0])["split_info"]["s_start_time"]).split('T')[1]).split('.')[0])
    lambda_end_time = timeStrToInt((str((((json_result[0])["playlistData"])[0])["split_info"]["s_update_time"]).split('T')[1]).split('.')[0])
    time1 = secondToDateString(lambda_end_time - lambda_start_time)
    print("AWS Lambda Splitting Cost Time : " + time1)
    return time1
  except:
    return "0:0:0"


if __name__ == "__main__":
  #control(sys.argv)
  #processTime("192.168.1.3_0322_200754.txt")
  config = loadSetting()
  ipArr = config["model"]["ip"]
  modelName = config["name"]
  #### process lambda log file ####
  aws_lambda_timing(modelName)
  #################################
  for ip in ipArr:
    print("============   " + ip + "   ==============")
    resultText = control(ip)
    time.sleep(2)
    time2 = processTime(resultText)
    #totalTime = secondToDateString(timeStrToInt(time1) + timeStrToInt(time2))
    totalTime = time2
    print("Android download cost : " + time2)
    print("Total Cost : " + totalTime)
    print("============================================")

import configparser
import serial
from serial.tools import list_ports
import time
import datetime
import csv

import inv

# 初期化処理
print("### Starting MPC Heat Test... ###")

# 再設定用リスト表示
print("[LOG] List of serial ports:")
ports = list_ports.comports()
devices = [info.device for info in ports]
for i in range(len(devices)):
  print("[LOG]   input %3d: open %s" % (i, devices[i]))

# 設定ファイル読み込み
print("[LOG] Loading settings.ini...")
inifile = configparser.ConfigParser()
inifile.read("settings.ini")
timeout = int(inifile.get("Proto1", "TIMEOUT"))
baudrate = int(inifile.get("Proto1", "BAUDRATE"))
arduino_port = inifile.get("Proto1", "ARDUINO_PORT")
msz = int(inifile.get("Proto1", "MATRIX_SIZE"))
max_itr = int(inifile.get("Proto1", "ITERATION"))
print("[LOG] Success.")

# Arduino接続
arduino_serial = serial.Serial(arduino_port, baudrate=baudrate, timeout=timeout)

# CSVファイル作成
datetime_string = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
with open('benchmark_' + "v1.0_" + datetime_string + '.csv', 'w') as f:
  writer = csv.writer(f)
  
  # CSVヘッダー
  writer.writerow(["経過時間", "セグメントあたり計算所要時間", "内部温度"])
  
  # ベンチマークテスト開始
  print("[LOG] Start a calculation.")
  time_base = time.time() # 基準時間
  # 初期状態出力
  start_line = arduino_serial.readline()
  start_temp = start_line.decode().replace("inner_temp", "")
  writer.writerow([time.time() - time_base, 0, start_temp])
  
  i = 0
  for i in max_itr:
    # 逆行列計算の実行時間を取得
    dtl = inv.cal_inv(msz)
    # 基準時間からの経過時刻を取得
    time_passed = time.time() - time_base
    # Arduinoから内部温度データ収集、フォーマット: inner_temp=[float]
    line = arduino_serial.readline()
    temp = line.decode().replace("inner_temp=", "")  
    # CSV書き込み
    writer.writerow([time_passed, dtl, temp])
    i = i + 1

arduino_serial.close()    

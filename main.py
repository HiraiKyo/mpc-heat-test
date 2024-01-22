import configparser
import serial
from serial.tools import list_ports
import time
import datetime
import csv
from threading import Thread

import inv
import temp

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
thread_arduino = Thread(target=temp.listen_temp, args=(arduino_port, baudrate, timeout))
thread_arduino.start()

# CSVファイル作成
datetime_string = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
with open('benchmark_' + "v1.0_" + datetime_string + '.csv', 'w') as f:
  writer = csv.writer(f)
  
  # CSVヘッダー
  writer.writerow(["経過時間", "イテレーションあたり計算所要時間", "内部温度"])
  
  # ベンチマークテスト開始
  print("[LOG] Start a calculation.")
  time_base = time.time() # 基準時間
  # 初期状態出力
  start_temp = temp.get_temp()
  writer.writerow([time.time() - time_base, 0, start_temp])
  
  i = 0
  for i in range(max_itr):
    print("[LOG] イテレーション", i, "回目...")
    # 逆行列計算の実行時間を取得
    dtl = inv.cal_inv(msz)
    # 基準時間からの経過時刻を取得
    time_passed = time.time() - time_base
    # Arduinoから内部温度取得
    temp_current = temp.get_temp()
    # CSV書き込み
    writer.writerow([time_passed, dtl, temp_current])
    
  temp.stop()
import subprocess
import os

def get_cpu_temp():
  temp = subprocess.run(['sensors'], stdout=subprocess.PIPE).stdout.decode('utf-8')
  lines = temp.split(os.linesep)
  cpus = []
  for i in range(8):
    cpus.append(lines[3+i].split()[2])
  return cpus

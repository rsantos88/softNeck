import sys,platform
import ctypes, ctypes.util
import yarp
import os
import time

pathLocate = "/home/humasoft/Escritorio/Py-C/softNeck/build"

if platform.system()== "Windows":
    path = ctypes.util.find_library("msvcrt")
else:
    path = ctypes.util.find_library(pathLocate + "/startMotors")


try:
    libc=ctypes.CDLL(path)
except OSError:
    print("Error no encuentra el path")
    sys.exit()

print("FUNCIONO BIENNNNN")
#libc.main()
os.system("/home/humasoft/Escritorio/Py-C/softNeck/build/setPosition 0 0")
time.sleep(3)
os.system("/home/humasoft/Escritorio/Py-C/softNeck/build/setPosition 20 0")
print("HE ACABADO SIN PETAR")




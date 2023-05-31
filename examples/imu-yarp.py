import yarp
import time

yarp.Network.init()
pin = yarp.BufferedPortBottle()
pout = yarp.BufferedPortBottle()

pin.open("/pin")
pout.open("/pout")

yarp.Network.connect("/pout", "/receiver")
yarp.Network.connect("/sender", "/pin" )

if not yarp.Network.isConnected("/pout", "/receiver"):
    print("Error connection witch /pout /receiver")
    exit()

if not yarp.Network.isConnected("/sender", "/pin"):
    print("Error connection witch /pin, /sender")
    exit()
for i in range(1):
    bout = yarp.Bottle()
    bout = pout.prepare()

    print(i)
    bout.addString("sendme")
    pout.write()
    print("Sending [%s]"%bout.toString())

    bin = yarp.Bottle()

    bin = pin.read()
    bout.clear()

    print(bin.toString())
    time.sleep(0.1)
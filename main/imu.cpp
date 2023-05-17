#include "imu3dmgx510.h"
#include <iostream>
#include <stdio.h>

#include <yarp/os/Bottle.h>
#include <yarp/os/Network.h>
#include <yarp/os/Port.h>

using yarp::os::Bottle;
using yarp::os::Network;
using yarp::os::Port;


class Sensor
{
    private:
        IMU3DMGX510 * imu;
        double pitch,roll, yaw;
    public:
        Sensor(double f);
        std::vector<double> read();
};

Sensor::Sensor(double f){
    imu = new IMU3DMGX510("/dev/ttyUSB0",f);
}

std::vector<double> Sensor::read(){
    imu->GetPitchRollYaw(pitch,roll,yaw);
    std::vector<double> result{pitch,roll};
    return result;
}

int main(){
    Network yarp;
    Port input, output;
    Bottle inBottle, outBottle;
    input.open("/receiver");
    output.open("/sender");
    Sensor s(50);

    while(1){
        input.read(inBottle);
        cout << inBottle.get(0).asString() << endl;
        if(inBottle.toString()=="sendme")
        {
            std::vector<double> value = s.read();
            printf("> %f %f\n", value[0], value[1]);
            outBottle.addFloat64(value[0]);
            outBottle.addFloat64(value[1]);
            sleep(0.1);
            output.write(outBottle);
            inBottle.clear();
            outBottle.clear();
        }
        if(inBottle.toString()=="exit")
            break;

    }
}



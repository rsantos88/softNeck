#include "imu3dmgx510.h"
#include <iostream>
#include <stdio.h>


class Sensor
{
    private:
        IMU3DMGX510 * imu;
        double freq;
        double pitch,roll, yaw;
    public:
        Sensor(double f);
        std::vector<double> read();
};

Sensor::Sensor(double f){
    imu = new IMU3DMGX510("/dev/ttyUSB0",f);
    for (double t=0;t<10;t+=1/f)
    {
       imu->GetPitchRollYaw(pitch,roll,yaw);
    }
    cout<<"Calibrated"<<endl;
}

std::vector<double> Sensor::read(){
    imu->GetPitchRollYaw(pitch,roll,yaw);
    std::vector<double> result{pitch,roll};
    return result;
}

int main(){
    Sensor s(0.02);
    std::vector<double> value = s.read();
}


#include "imu3dmgx510.h"
#include <iostream>
#include <stdio.h>


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
    //printf("Calibrando IMU..\n");

    //cout<<"Calibrated"<<endl;

}

std::vector<double> Sensor::read(){
    imu->GetPitchRollYaw(pitch,roll,yaw);
    std::vector<double> result{pitch,roll};
    return result;
}

int main(){
    Sensor s(50);
    std::vector<double> value = s.read();
    printf("%f %f\n", value[0], value[1]);
}



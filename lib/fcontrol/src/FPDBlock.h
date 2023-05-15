#ifndef FPDBLOCK_H
#define FPDBLOCK_H
//#include "fcontrol.h" //cant include because of compilation error: ‘FPDBlock’ has not been declared
#include "Block.h"
#include "FractionalController1DOF.h"

class FPDBlock : public BaseBlock
{
public:
//    FPDBlock();
    FPDBlock(double new_kp = 1, double new_kd = 1, double new_fex = 1, double new_dts = 0.001);

    double OutputUpdate(double new_input);
    long ParameterUpdate(vector<double> new_params);

    double GetState() const;

    long PrintParameters();
    long GetParameters(double &out_kp, double &out_kd, double &out_fex );

    long AntiWindup(double minPlantSaturation, double maxPlantSaturation);
private:
    double kp, kd, fex;
    double cp, cd, dci;
    double dts;

    double state, input, scaledInput;
    FractionalController1DOF s_e;
    double s_e_state;

    bool antiwindup;
    double minWindup,maxWindup;

};

#endif // FPDBLOCK_H

#Functions to perform standard calculations and provide constants relevant for fluid dynamics

import numpy as np

nue_air = 1.5e-05   #kinematic viscosity of air

def Re_kin(u,L,nue):    #calculate Re-Number
    #u: characteristic velocity
    #l: charcteristic length
    #nue: kinematic viscosity
    return (u * L) / nue

def turb_y_from_yplus(y_plus,u,nue):    #estimates the y necesarry to achiev a target y+ at a turbulent wall
    u_t = 0.05 * u
    return y_plus * nue / u_t


def cylinder_CD_fit(RE): #https://github.com/peterdsharpe/CylinderDragFits Can calculate the CD of a cylinder in a crossflow as a function of RE, Mach = 0 is assumed
    csigc = 5.5766722118597247
    csigh = 23.7460859935990563
    csub0 = -0.6989492360435040
    csub1 = 1.0465189382830078
    csub2 = 0.7044228755898569
    csub3 = 0.0846501115443938
    csup0 = -0.0823564417206403
    csupc = 6.8020230357616764
    csuph = 9.9999999999999787
    csupscl = -0.4570690347113859

    x = np.log10(RE)

    # First term
    term1_log_base = csub0 * x + csub1
    term1_inner_log = 10 ** term1_log_base + csub2 + csub3 * x
    term1 = np.log10(term1_inner_log) * (1 - 1 / (1 + np.exp(-csigh * (x - csigc))))

    # Second term
    term2_log_inner_exp = np.exp(csuph * (csupc - x)) + 1
    term2_log = csup0 + (csupscl / csuph) * np.log(term2_log_inner_exp)
    term2 = term2_log * (1 / (1 + np.exp(-csigh * (x - csigc))))

    # Final result
    result = term1 + term2
    return 10 ** result
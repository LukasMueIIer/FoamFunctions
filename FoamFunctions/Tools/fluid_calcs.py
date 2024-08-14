#Functions to perform standard calculations and provide constants relevant for fluid dynamics

nue_air = 1.5e-05   #kinematic viscosity of air

def Re_kin(u,L,nue):    #calculate Re-Number
    #u: characteristic velocity
    #l: charcteristic length
    #nue: kinematic viscosity
    return (u * L) / nue

def turb_y_from_yplus(y_plus,u,nue):    #estimates the y necesarry to achiev a target y+ at a turbulent wall
    u_t = 0.05 * u
    return y_plus * nue / u_t


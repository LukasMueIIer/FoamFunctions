## In this script the simulation is executed

#fixed imports
from FoamFunctions.Tools import general
from FoamFunctions.Solvers import Sim_Master
import os

#custom imports
from PyFoam.Execution.ParallelExecution import LAMMachine
#custom functions

def Simulation(dir_path):
    #dir_path is the path of the directory in which simulation will be done
    if not os.path.isdir(dir_path):
        print("Passed working directory path is NOT valid!")
        return 1
  
    sim_master = Sim_Master.sim_master(dir_path,4)  #general sim_master which is used to execute simulations

    #case specific code and simulation execution



    general.reconstruct(dir_path) #reconstruct case
    general.paraFoam(dir_path) #create paraFoam file

    return 0 #return 0 if ran sucessfully


#independent run
if __name__ == "__main__":
    print("Simulation running as standalone")

    #get working directory
    dir_path = general.get_start_path()
    sim_state = Simulation(dir_path)
    if(sim_state == 0):
        print("Simulation done sucessfully!")
    else:
        print("An Error occured with code: " + str(sim_state))
# class to make chaining and execting solvers easier
from PyFoam.Execution.ParallelExecution import LAMMachine

class sim_step:
    def __init__(self,solver,time = 1, writeInterval = 1, dT = 1) -> None:
        self.time = time #timeframe which is simulated
        self.writeInterval = writeInterval #at what interval results are written
        self.dT = dT    #timestep size (or initial size if addaptive timestep)
        self.solver = solver #String which matches the Foam Command to execute the solver
        
    def inverval_splitting(self,n): #sets the writeInterval, so that n files are written
        self.writeInterval = self.time / n



class sim_master:
    def __init__(self,dir_path,CPU_count) -> None:
        self.lam = LAMMachine(nr = CPU_count)
        self.solverEndtimes = []    #simulation time until which solver was executed
        self.solverExecutionTimes = [] #physical duration which solver took to be executed
        self.dir = dir_path #simulation directory

    def execute(sim: sim_step): #execute a simulation defined as sim_step class
        
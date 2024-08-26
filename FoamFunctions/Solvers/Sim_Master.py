# class to make chaining and execting solvers easier
from PyFoam.Execution.ParallelExecution import LAMMachine
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Execution.BasicRunner import BasicRunner
import time

class sim_step:
    def __init__(self,solver,time = 1, writeInterval = 1, dT = 1, silent=True, ddTSchemes = None) -> None:
        self.time = time #timeframe which is simulated
        self.writeInterval = writeInterval #at what interval results are written
        self.dT = dT    #timestep size (or initial size if addaptive timestep)
        self.solver = solver #String which matches the Foam Command to execute the solver
        self.silent = silent #If solver output is shown in console
        self.ddTSchemes = ddTSchemes    #to swap between time schemes before execution
        self.steady_state_solvers = ["simpleFoam", "buoyantSimpleFoam", "potentialFoam", "porousSimpleFoam"] #List of common steady state solvers

    def inverval_splitting(self,n): #sets the writeInterval, so that n files are written
        self.writeInterval = self.time / n



class sim_master:
    def __init__(self,dir_path,CPU_count) -> None:
        self.lam = LAMMachine(nr = CPU_count)
        self.solverEndtimes = []    #simulation time until which solver was executed
        self.solverExecutionTimes = [] #physical duration which solver took to be executed
        self.dir_path = dir_path #simulation directory

    def execute(self,sim: sim_step): #execute a simulation defined as sim_step class
        dire = SolutionDirectory(self.dir_path)
        cD_file = ParsedParameterFile(dire.systemDir() + "/controlDict")

        #write solver information to controlDict
        cD_file["application"] = sim.solver
        if(len(self.solverEndtimes == 0)):
            cD_file["endTime"]  = str(sim.time)
            self.solverEndtimes.append(sim.time)
        else:
            cD_file["endTime"]  = str(sim.time + self.solverEndtimes[-1])
            self.solverEndtimes.append(sim.time + self.solverEndtimes[-1])
        cD_file["writeInterval"] = sim.writeInterval
        cD_file["deltaT"] = sim.dT
        cD_file.writeFile()

        #change time scheme if required
        if sim.ddTSchemes is not None:
            fv_file = ParsedParameterFile(dire.systemDir() + "/fvSchemes")
            fv_file["ddtSchemes"]["default"] = sim.ddTSchemes
            fv_file.writeFile()

        #check if a steady state solver has a steady state ddT


        #run solver and measure time
        start_time = time.time()
        print("Executing " + sim.solver)
        runner = BasicRunner(argv=[sim.solver, "-case", self.dir_path], silent= sim.silent, lam=self.lam)
        runner.start()
        if runner.runOK():
            print(sim.solver + " ran successfully")
        else:
            print(sim.solver + " failed for case")
        exec_time = time.time() - start_time
        print(f"Execution time: {exec_time} seconds")
        
        #save information
        self.solverExecutionTimes.append(exec_time)
        



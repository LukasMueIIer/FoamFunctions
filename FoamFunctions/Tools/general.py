#generally helpfull tools that fit no specific category
import os
import inspect
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Execution.BasicRunner import BasicRunner
import shutil

def get_start_path():   
    #returns the path of the folder where the file that was used to start this current python process is located
    # Get the file path of the script that called this function
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    
    # Get the directory of the caller file
    start_path = os.path.dirname(os.path.realpath(caller_file))
    
    return start_path


def clean_parallel_and_postProcessing(dir_path):
    #cleans up a case that was run in parallel and also removes the postProcessing dictionary

    dire = SolutionDirectory(dir_path,parallel=True)
    dire.clearResults(removeProcs=True)
    dire = SolutionDirectory(dir_path) #this weird thing is needed to remove the proccessor directories
    #delete PostProcessingResults
    post_processing_dir = os.path.join(dir_path, "postProcessing")
    if os.path.exists(post_processing_dir):
        print(f"Removing postProcessing directory: {post_processing_dir}")
        shutil.rmtree(post_processing_dir)

def run_Blockmesh(dir_path,silent=True): #basic BlockMesh execution with no addons
    bm_runner = BasicRunner(argv=["blockMesh","-case",dir_path],silent=silent)
    bm_runner.start()
    if bm_runner.runOK():
        print(f"blockMesh ran successfully")
    else:
        print(f"blockMesh failed for case")

def renumber_Mesh(dir_path,silent=True):    #basic renumber mesh 
    rm_runner = BasicRunner(argv=["renumberMesh","-case",dir_path,"-overwrite"],silent=False)
    rm_runner.start()
    if rm_runner.runOK():
        print(f"renumberMesh ran successfully")
    else:
        print(f"renumberMesh failed for case")

def paraFoam(dir_path,silent=True,vtk=True):    #basic paraFoam runner that touches and uses vtk (if activated)
    if(vtk):
        pf_runner = BasicRunner(argv=["paraFoam","-case",dir_path,"-touch","-vtk"],silent=silent)
        pf_runner.start()
        if pf_runner.runOK():
            print(f"paraFoam ran successfully")
        else:
            print(f"paraFoam failed for case")
    else:
        pf_runner = BasicRunner(argv=["paraFoam","-case",dir_path,"-touch"],silent=silent)
        pf_runner.start()
        if pf_runner.runOK():
            print(f"paraFoam ran successfully")
        else:
            print(f"paraFoam failed for case")
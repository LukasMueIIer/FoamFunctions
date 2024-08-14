#generally helpfull tools that fit no specific category
import os
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
import shutil

def get_start_path():   
    #returns the path of the folder where the file that was used to start this current python process is located
    return os.path.dirname(os.path.realpath(__file__))

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
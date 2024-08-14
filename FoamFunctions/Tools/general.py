#generally helpfull tools that fit no specific category
import os

def get_start_path():   
    #returns the path of the folder where the file that was used to start this current python process is located
    return os.path.dirname(os.path.realpath(__file__))
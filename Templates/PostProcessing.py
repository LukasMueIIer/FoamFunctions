##In this script all PostProcessing is done

#fixed imports
from FoamFunctions.Tools import general
import os

#custom imports

#custom functions

def PostProcessing(dir_path):    
    #dir_path is the path of the directory in which simulation will be done
    if not os.path.isdir(dir_path):
        print("Passed working directory path is NOT valid!")
        return 1

    #case specific code


    return 0 #return 0 if ran sucessfully


#independent run
if __name__ == "__main__":
    print("PostProcessing running as standalone")

    #get working directory
    dir_path = general.get_start_path()
    pp_state = PostProcessing(dir_path)
    if(pp_state == 0):
        print("PostProcessing done sucessfully!")
    else:
        print("An Error occured with code: " + str(pp_state))

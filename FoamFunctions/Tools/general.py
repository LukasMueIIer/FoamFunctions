#generally helpfull tools that fit no specific category
import os
import inspect
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
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
    dire.clearResults(removeProcs=True,after=0)
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

def run_topoSet(dir_path,silent=True):
    ts_runner = BasicRunner(argv=["topoSet","-case",dir_path],silent=silent)
    ts_runner.start()
    if ts_runner.runOK():
        print(f"topoSet ran successfully")
    else:
        print(f"topoSet failed for case")

def run_subsetMesh(dir_path,setName,overwrite = True,silent=True):
    if(overwrite):
        sM_runner = BasicRunner(argv=["subsetMesh","-case",dir_path,"-overwrite",str(setName)],silent=silent)
    else:
        sM_runner = BasicRunner(argv=["subsetMesh","-case",dir_path,str(setName)],silent=silent)
    sM_runner.start()
    if sM_runner.runOK():
        print(f"subsetMesh ran successfully")
    else:
        print(f"subsetMesh failed for case")

def renumber_Mesh(dir_path,silent=True):    #basic renumber mesh 
    rm_runner = BasicRunner(argv=["renumberMesh","-case",dir_path,"-overwrite"],silent=False)
    rm_runner.start()
    if rm_runner.runOK():
        print(f"renumberMesh ran successfully")
    else:
        print(f"renumberMesh failed for case")

def change_type_in_all_files(subDirectoryPath,boundaryName,newType):
    #this can be used to change the type of a boundary in all fields contained in a timestep
    def get_top_level_files(directory_path):
        """
        Returns a list of absolute file paths for all files in the top level of the given directory.

        Parameters:
            directory_path (str): The path to the directory.

        Returns:
            list: A list of absolute file paths.
        """
        try:
            # Ensure the input is a valid directory
            if not os.path.isdir(directory_path):
                raise ValueError(f"{directory_path} is not a valid directory.")

            # List comprehension to filter only files at the top level
            top_level_files = [
                os.path.abspath(os.path.join(directory_path, file))
                for file in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, file))
            ]

            return top_level_files

        except Exception as e:
            print(f"Error: {e}")
            return []
        
    files = get_top_level_files(subDirectoryPath)
    for file in files:
        paramFile = ParsedParameterFile(file)
        paramFile["boundaryField"][boundaryName]["type"] = newType
        paramFile.writeFile()

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

def decompose(dir_path,core_count,silent=True,copyZero = False):    #basic case decomposer that adapts the decomposePar file as well
    #modify file
    dire = SolutionDirectory(dir_path)
    dP_file = ParsedParameterFile(dire.systemDir() + "/decomposeParDict")
    dP_file["numberOfSubdomains"] = str(core_count)
    dP_file.writeFile()
    #execite decomposition
    if(copyZero):
        decompose_runner = BasicRunner(argv=["decomposePar", "-case", dir_path, "-force","-copyZero"], silent=silent)
    else:
        decompose_runner = BasicRunner(argv=["decomposePar", "-case", dir_path, "-force"], silent=silent)
    decompose_runner.start()
    if decompose_runner.runOK():
        print("decomposePar completed successfully.")
    else:
        print("decomposePar failed.")

def reconstruct(dir_path,silent=True):  #basic reconstruction of a parallel case
    print("Reconstructing the Mesh")
    reconstruct_runner = BasicRunner(argv=["reconstructParMesh", "-case", dir_path], silent=False)
    reconstruct_runner.start()
    if reconstruct_runner.runOK():
        print("reconstructParMesh ran successfully")
    else:
        print("reconstructParMesh failed for case")    

    print("Reconstructing the case")
    reconstruct_runner = BasicRunner(argv=["reconstructPar", "-case", dir_path], silent=False)
    reconstruct_runner.start()
    if reconstruct_runner.runOK():
        print("reconstructPar ran successfully")
    else:
        print("reconstructPar failed for case")    

def find_largest_numbered_directory(dir_path):
    #finds the directory with the largest numerical value in the dir_path folder

    # List all folders in the directory
    folders = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]

    # Filter out non-integer folder names and convert to integers
    folder_numbers = [int(f) for f in folders if f.isdigit()]

    # Initialize largest_folder_path to None in case no valid folder is found
    largest_folder_path = None

    # Find the folder with the largest number
    if folder_numbers:
        largest_folder = str(max(folder_numbers))

        # Construct the path to the largest numbered folder
        largest_folder_path = os.path.join(dir_path, largest_folder)
    else:
        print("No folders with integer names found.")

    return largest_folder_path

def copy_and_renumber(dir_path,source : str,target : str): #coppies the timestep with name source and renames to to target
    # Define source and destination paths
    src_folder = os.path.join(dir_path, source)
    dest_folder = os.path.join(dir_path, target)

    # Copy the folder and rename it
    if os.path.exists(dest_folder):
        # If it exists, delete it
        shutil.rmtree(dest_folder)
    # Copy the source folder to the destination

    shutil.copytree(src_folder, dest_folder)

    print(f'Folder {source} has been copied and renamed to {target} in {dir_path}.')

def run_setExprFields(dir_path,silent=True,exclude_0 = True): #basic setExprFields execution with no addons
    #exclude_0 means that the 0 timestep will not be overwritten
    EF_runner = BasicRunner(argv=["setExprFields","-case",dir_path],silent=silent)
    if(exclude_0):
        EF_runner = BasicRunner(argv=["setExprFields","-case",dir_path,"-noZero"],silent=silent)
    EF_runner.start()
    if EF_runner.runOK():
        print(f"setExprFields ran successfully")
    else:
        print(f"setExprFields failed for case")

def remove_PyFoam_Logs(dir_path): #removes all files that start with "PyFoam" in the top level off dir path
    # List all files in the top-level of dir_path
    for filename in os.listdir(dir_path):
        # Construct the full file path
        file_path = os.path.join(dir_path, filename)
        
        # Check if it's a file (not a directory) and starts with "PyFoam"
        if os.path.isfile(file_path) and filename.startswith("PyFoam"):
            os.remove(file_path)  # Delete the file
            print(f'Deleted: {file_path}')


def fix_setField_variable_syntax(file_path):
    """
    Corrects the setExprFields dict after it is written with pyFoam. Removes the wrong ' in the variable line
    Reads a file, removes single quotes around the variables line, and writes the corrected content back.
    
    Args:
        file_path (str): Path to the file to be fixed.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Modify the specific line containing 'variables'
        for i, line in enumerate(lines):
            if line.strip().startswith("variables '(") and line.strip().endswith(")';"):
                # Replace single quotes in this specific line
                lines[i] = line.replace("variables '(", "variables (").replace(")';", ");")
                break
        
        # Write back the updated lines to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
        
        print("File updated successfully.")
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_time_folders(directory_path):
    """
    Deletes all folders in the specified directory whose names are valid float numbers and do not contain any letters.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        None
    """
    # Ensure the provided path is a directory
    if not os.path.isdir(directory_path):
        print(f"Error: The path {directory_path} is not a valid directory.")
        return

    # Iterate through the items in the directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Check if the folder name is a float and contains no letters
            try:
                if item.replace('.', '', 1).isdigit() and not any(char.isalpha() for char in item):
                    # Delete the folder
                    shutil.rmtree(item_path)
                    print(f"Deleted folder: {item}")
            except ValueError:
                pass

def copy_field_files(target_directory, source_directory, file_list, overwrite=False):
    """
    Copies specified files from the source directory to the target directory.

    Args:
        target_directory (str): Path to the target directory.
        source_directory (str): Path to the source directory.
        file_list (list): List of file names to copy.
        overwrite (bool): If True, overwrite files in the target directory if they already exist.

    Returns:
        None
    """
    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created target directory: {target_directory}")

    # Iterate over the file list and copy files
    for file_name in file_list:
        source_path = os.path.join(source_directory, file_name)
        target_path = os.path.join(target_directory, file_name)

        # Check if the file exists in the source directory
        if not os.path.exists(source_path):
            print(f"File not found in source directory: {source_path}")
            continue

        # Copy the file, handling overwriting if necessary
        if not os.path.exists(target_path) or overwrite:
            shutil.copy2(source_path, target_path)
            print(f"Copied file: {file_name} to {target_directory}")
        else:
            print(f"File already exists and overwrite is set to False: {file_name}")

#Remove all Processor Directories, and decompose again
def delete_processor_folders(directory_path):
    """
    Deletes all folders that start with "processor" in the specified directory.

    Parameters:
        directory_path (str): Path to the directory where folders will be deleted.

    Returns:
        None
    """
    try:
        # Check if the provided directory path exists
        if not os.path.exists(directory_path):
            print(f"The directory {directory_path} does not exist.")
            return

        # Iterate through items in the directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Check if the item is a folder and starts with "processor"
            if os.path.isdir(item_path) and item.startswith("processor"):
                print(f"Deleting folder: {item_path}")
                shutil.rmtree(item_path)  # Delete the folder and its contents

        print("Completed deletion of processor folders.")

    except Exception as e:
        print(f"An error occurred: {e}")
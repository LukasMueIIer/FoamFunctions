#Collection of functions that read Foam created data into python 

def readCD_last(file_path):
    #function to read the result file of the forces function objective
    #extracts the last written value usefull for steady state simulations
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("The file is empty")
            
            last_line = lines[-1].strip()  # Get the last line and strip any whitespace
            values = last_line.split()  # Split the line into values
            
            if len(values) < 2:
                raise ValueError("The last line does not contain enough values")
            
            second_value = float(values[1])  # Convert the second value to float
            return second_value
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def readCD_all(file_path,start_at = 14):
    #function to read the result file of the forces function objective
    #reads all values after start_at and writes them into an array that is returned
    #for openFoam v2406 starting at line 14 excludes only the file header

    # List to store the extracted Cd values
    cd_values = []

    # Open the file and process it line by line
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # Skip the header lines and start from line 14
            if i >= start_at:
                # Split the line into components based on whitespace
                parts = line.split()
                # The second number (index 1) is the Cd value
                if len(parts) > 1:  # Checking to make sure there's a number to extract
                    cd = float(parts[1])  # Convert the string to a float
                    cd_values.append(cd)
    
    return cd_values

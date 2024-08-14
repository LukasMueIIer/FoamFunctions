#collection of functions that can process data

import numpy as np

def find_lokalPeaks(data, window = 1):
    #function that finds indices of local maximas in the provided data.
    #A local maxima is defined such that the values in the range +/- window must be smaller
    #usefull f.e. to find the St-Number of an oscilating cylinder based on the drag as function of time
    #returns the indexes of the array elements that are local maxima
    #WARNING: the first i<window values are excluded same with the last |window| values

    if not isinstance(data, np.ndarray):    #convert data to numpy array if it isn't one already
        data = np.array(data)
        
    local_maxima_indices = []
    for i in range(window, len(data) - window):
        # Check if the current value is greater than all its neighbors within the window
        if np.all(data[i] > data[i-window:i]) and np.all(data[i] > data[i+1:i+1+window]):
            local_maxima_indices.append(i)
    
    return np.array(local_maxima_indices)
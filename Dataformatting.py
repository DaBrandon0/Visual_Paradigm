from scipy import stats
import scipy
import numpy as np
import matplotlib.pyplot as plt
import pickle
# Load the .mat file

mat_data = scipy.io.loadmat('preprocessed.mat', simplify_cells = True)['combined_export']
EEG1sec_FCZ_err = []
EEG1sec_CZ_err = []
EEG1sec_FCZ_valid = []
EEG1sec_CZ_valid = []
EEG_FCZ = [sublist[9] for sublist in mat_data['filtered_data']]
EEG_CZ = [sublist[14] for sublist in mat_data['filtered_data']]
erroneous_event_code = [3002]
valid_event_code = [3001]
error_indices = [index for index, value in enumerate(mat_data['triggers'][0]) if value in erroneous_event_code]
valid_indices = [index for index, value in enumerate(mat_data['triggers'][0]) if value in valid_event_code]
EEG_indices_err = []
EEG_indices_valid = []
for i in error_indices:
    EEG_indices_err.append(mat_data['trigger_index'][i])
for i in valid_indices:
    EEG_indices_valid.append(mat_data['trigger_index'][i])
for i in EEG_indices_err:
    list_FCZ = np.array(EEG_FCZ)[i-1:i+511]
    list_CZ = np.array(EEG_CZ)[i-1:i+511]
    EEG1sec_CZ_err.append(list_CZ)
    EEG1sec_FCZ_err.append(list_FCZ)
for i in EEG_indices_valid:
    list_FCZ = np.array(EEG_FCZ)[i-1:i+511]
    list_CZ = np.array(EEG_CZ)[i-1:i+511]
    EEG1sec_CZ_valid.append(list_CZ)
    EEG1sec_FCZ_valid.append(list_FCZ)

with open('EEG1sec_CZ_err.pkl', 'wb') as file:
    pickle.dump(EEG1sec_CZ_err, file)
with open('EEG1sec_FCZ_err.pkl', 'wb') as file:
    pickle.dump(EEG1sec_FCZ_err, file)
with open('EEG1sec_CZ_valid.pkl', 'wb') as file:
    pickle.dump(EEG1sec_CZ_valid, file)
with open('EEG1sec_FCZ_valid.pkl', 'wb') as file:
    pickle.dump(EEG1sec_FCZ_valid, file)

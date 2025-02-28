from scipy import stats
import scipy
import numpy as np
import matplotlib.pyplot as plt
import pickle
from BaselineRemoval import BaselineRemoval
# Load the .mat file

mat_data = scipy.io.loadmat(r"C:\Users\Brandon\Documents\2025 Fall\EEG_Analysis\mat_py_in\NathanVisual2_27_1.mat", simplify_cells = True)['combined_export']
EEG1sec_FZ_err = []
EEG1sec_CZ_err = []
EEG1sec_FZ_valid = []
EEG1sec_CZ_valid = []
EEG_FZ = [sublist[5] for sublist in mat_data['filtered_data']]
EEG_CZ = [sublist[15] for sublist in mat_data['filtered_data']]
startindex = mat_data['trigger_index'][0] #index of start of experiment
endindex = mat_data['trigger_index'][-1]
EEG_FZ = EEG_FZ[startindex:endindex] #select data between start and stop of experiment
EEG_CZ = EEG_CZ[startindex:endindex]
'''
#Ttest plots
x = list(range(len(EEG_FZ)))
plt.plot(x, EEG_FZ, label='not removed', marker='s')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.show()
'''
'''

FZ_base_obj = BaselineRemoval(EEG_FZ) #
CZ_base_obj = BaselineRemoval(EEG_CZ)
removed1 = FZ_base_obj.ModPoly(2)
removed2 = CZ_base_obj.ModPoly(2)



x = list(range(len(EEG_FZ)))

#Ttest plots
plt.plot(x, removed1, label='removed', marker='o')
plt.plot(x, EEG_FZ, label='not removed', marker='s')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('t-test')
plt.legend()
plt.show()

EEG_FZ = removed1
EEG_CZ = removed2
'''
both = [3002,3001]
erroneous_event_code = [3002]
valid_event_code = [3001]
start_code = [6000]


error_indices = [index for index, value in enumerate(mat_data['triggers'][0]) if value in erroneous_event_code] 
valid_indices = [index for index, value in enumerate(mat_data['triggers'][0]) if value in valid_event_code]
start_indices = [index for index, value in enumerate(mat_data['triggers'][0]) if value in start_code]
all_indices = [index for index, value in enumerate(mat_data['triggers'][0]) if value in both]
EEG_indices_err = []
EEG_indices_valid = []
EEG_indices_all = []
indices_start = []
for i in all_indices:
    EEG_indices_all.append(mat_data['trigger_index'][i])
for i in error_indices:
    if(mat_data['triggers'][0][i+1] == 4002):
        EEG_indices_err.append(mat_data['trigger_index'][i])
for i in valid_indices:
    if(mat_data['triggers'][0][i+1] == 4001):
        EEG_indices_valid.append(mat_data['trigger_index'][i])
for i in start_indices:
    indices_start.append(mat_data['trigger_index'][i])
for i in indices_start:
    #sorry
    base_avg_FZ = np.mean(np.array(EEG_FZ)[i-startindex-103:i-startindex])
    base_avg_CZ = np.mean(np.array(EEG_CZ)[i-startindex-103:i-startindex])
    to_scale_FZ = np.array(EEG_FZ)[EEG_indices_all[indices_start.index(i)]-1-startindex:EEG_indices_all[indices_start.index(i)]+511-startindex]
    to_scale_CZ = np.array(EEG_CZ)[EEG_indices_all[indices_start.index(i)]-1-startindex:EEG_indices_all[indices_start.index(i)]+511-startindex]
    scaled_FZ = [x - base_avg_FZ for x in to_scale_FZ]
    scaled_CZ = [x - base_avg_CZ for x in to_scale_CZ]
    EEG_FZ[EEG_indices_all[indices_start.index(i)]-1-startindex:EEG_indices_all[indices_start.index(i)]+511-startindex] = scaled_FZ
    EEG_CZ[EEG_indices_all[indices_start.index(i)]-1-startindex:EEG_indices_all[indices_start.index(i)]+511-startindex] = scaled_CZ


for i in EEG_indices_err:
    list_FZ = np.array(EEG_FZ)[i-1-startindex:i+511-startindex]
    list_CZ = np.array(EEG_CZ)[i-1-startindex:i+511-startindex]
    if(min(list_CZ)> -100 and max(list_CZ) < 100):
        EEG1sec_CZ_err.append(list_CZ)
    if(min(list_FZ)> -100 or max(list_FZ) < 100):
        EEG1sec_FZ_err.append(list_FZ)
for i in EEG_indices_valid:
    list_FZ = np.array(EEG_FZ)[i-1-startindex:i+511-startindex]
    list_CZ = np.array(EEG_CZ)[i-1-startindex:i+511-startindex]
    if(min(list_CZ)> -100 and max(list_CZ) < 100):
        EEG1sec_CZ_valid.append(list_CZ)
    if(min(list_FZ)> -100 or max(list_FZ) < 100):
        EEG1sec_FZ_valid.append(list_FZ)

with open('EEG1sec_CZ_err.pkl', 'wb') as file:
    pickle.dump(EEG1sec_CZ_err, file)
with open('EEG1sec_FZ_err.pkl', 'wb') as file:
    pickle.dump(EEG1sec_FZ_err, file)
with open('EEG1sec_CZ_valid.pkl', 'wb') as file:
    pickle.dump(EEG1sec_CZ_valid, file)
with open('EEG1sec_FZ_valid.pkl', 'wb') as file:
    pickle.dump(EEG1sec_FZ_valid, file)

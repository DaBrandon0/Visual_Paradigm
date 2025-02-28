from scipy import stats
import scipy
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import make_interp_spline

#open formatted files containing 1 second of eeg data after stimuli
with open('EEG1sec_CZ_err.pkl', 'rb') as file:
    EEG1sec_CZ_err = pickle.load(file)
with open('EEG1sec_FZ_err.pkl', 'rb') as file:
    EEG1sec_FZ_err = pickle.load(file)
with open('EEG1sec_CZ_valid.pkl', 'rb') as file:
    EEG1sec_CZ_valid = pickle.load(file) 
with open('EEG1sec_FZ_valid.pkl', 'rb') as file:
    EEG1sec_FZ_valid = pickle.load(file)     

dist_FZ_err = []
dist_CZ_err = []
dist_FZ_valid = []
dist_CZ_valid = []

#extracting distributions for each sampling point

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_FZ_err)):
        dist.append(EEG1sec_FZ_err[j][i])
    dist_FZ_err.append(dist)

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_CZ_err)):
        dist.append(EEG1sec_CZ_err[j][i])
    dist_CZ_err.append(dist)

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_FZ_valid)):
        dist.append(EEG1sec_FZ_valid[j][i])
    dist_FZ_valid.append(dist)

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_CZ_valid)):
        dist.append(EEG1sec_CZ_valid[j][i])
    dist_CZ_valid.append(dist)
'''
 #Histogram
plt.hist(dist_FZ_err[0], bins=50, alpha=0.5, label='List 1', color='blue')
plt.hist(dist_FZ_valid[0], bins=50, alpha=0.5, label='List 2', color='orange')
plt.show()
'''
##Ttest
average_t_FZ = []
average_t_CZ = []

for i in range(512):
    average_t_FZ.append(stats.ttest_ind(dist_FZ_err[i], dist_FZ_valid[i]).pvalue)
    average_t_CZ.append(stats.ttest_ind(dist_CZ_err[i], dist_CZ_valid[i]).pvalue)

'''
print(np.mean(average_t_FZ))
print(np.mean(average_t_CZ))
'''

CZ_valid_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_CZ_valid)]
CZ_err_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_CZ_err)]
FZ_valid_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_FZ_valid)]
FZ_err_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_FZ_err)]


x = np.array(list(range(512)))
x_smooth = np.linspace(x.min(), x.max(), 5120)

spline_CZ_e = make_interp_spline(x, CZ_err_averages, k=3)  # Cubic spline interpolation
spline_CZ_v = make_interp_spline(x, CZ_valid_averages, k=3)  # Cubic spline interpolation
smooth_CZ_e = spline_CZ_e(x_smooth)
smooth_CZ_v = spline_CZ_v(x_smooth)

spline_FZ_e = make_interp_spline(x, FZ_err_averages, k=3)  # Cubic spline interpolation
spline_FZ_v = make_interp_spline(x, FZ_valid_averages, k=3)  # Cubic spline interpolation
smooth_FZ_e = spline_FZ_e(x_smooth)
smooth_FZ_v = spline_FZ_v(x_smooth)


#Ttest plots
plt.plot(x, average_t_FZ, label='FZ')
plt.plot(x, average_t_CZ, label='CZ')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Time series distribution t-test')
plt.legend()
#Grand average CZ plot
plt.figure()
plt.plot(x_smooth, smooth_CZ_v, label='valid')
plt.plot(x_smooth, smooth_CZ_e, label='error')
plt.xlabel('1 second of samples at 512 Hz sampling rate after stimuli')
plt.ylabel('μV')
plt.title('Grand Average CZ plot')
plt.legend()
#Grand average FZ plot
plt.figure()
plt.plot(x_smooth, smooth_FZ_v, label='valid')
plt.plot(x_smooth, smooth_FZ_e, label='error')
plt.xlabel('1 second of samples at 512 Hz sampling rate after stimuli')
plt.ylabel('μV')
plt.title('Grand Average FZ plot')
plt.legend()
plt.show()

debugpoint = []
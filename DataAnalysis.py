from scipy import stats
import scipy
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import make_interp_spline

#open formatted files containing 1 second of eeg data after stimuli
with open('EEG1sec_CZ_err.pkl', 'rb') as file:
    EEG1sec_CZ_err = pickle.load(file)
with open('EEG1sec_FCZ_err.pkl', 'rb') as file:
    EEG1sec_FCZ_err = pickle.load(file)
with open('EEG1sec_CZ_valid.pkl', 'rb') as file:
    EEG1sec_CZ_valid = pickle.load(file) 
with open('EEG1sec_FCZ_valid.pkl', 'rb') as file:
    EEG1sec_FCZ_valid = pickle.load(file)     

dist_FCZ_err = []
dist_CZ_err = []
dist_FCZ_valid = []
dist_CZ_valid = []

#extracting distributions for each sampling point

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_FCZ_err)):
        dist.append(EEG1sec_FCZ_err[j][i])
    dist_FCZ_err.append(dist)

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_CZ_err)):
        dist.append(EEG1sec_CZ_err[j][i])
    dist_CZ_err.append(dist)

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_FCZ_valid)):
        dist.append(EEG1sec_FCZ_valid[j][i])
    dist_FCZ_valid.append(dist)

for i in range(512):
    dist = []
    for j in range(len(EEG1sec_CZ_valid)):
        dist.append(EEG1sec_CZ_valid[j][i])
    dist_CZ_valid.append(dist)
'''
 #Histogram
plt.hist(dist_FCZ_err[0], bins=50, alpha=0.5, label='List 1', color='blue')
plt.hist(dist_FCZ_valid[0], bins=50, alpha=0.5, label='List 2', color='orange')
plt.show()
'''
##Ttest
average_t_FCZ = []
average_t_CZ = []

for i in range(512):
    average_t_FCZ.append(stats.ttest_ind(dist_FCZ_err[i], dist_FCZ_valid[i]).pvalue)
    average_t_CZ.append(stats.ttest_ind(dist_CZ_err[i], dist_CZ_valid[i]).pvalue)

'''
print(np.mean(average_t_FCZ))
print(np.mean(average_t_CZ))
'''

CZ_valid_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_CZ_valid)]
CZ_err_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_CZ_err)]
FCZ_valid_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_FCZ_valid)]
FCZ_err_averages = [sum(elements) / len(elements) for elements in zip(*EEG1sec_FCZ_err)]


x = np.array(list(range(512)))
x_smooth = np.linspace(x.min(), x.max(), 5120)

spline_CZ_e = make_interp_spline(x, CZ_err_averages, k=3)  # Cubic spline interpolation
spline_CZ_v = make_interp_spline(x, CZ_valid_averages, k=3)  # Cubic spline interpolation
smooth_CZ_e = spline_CZ_e(x_smooth)
smooth_CZ_v = spline_CZ_v(x_smooth)

spline_FCZ_e = make_interp_spline(x, FCZ_err_averages, k=3)  # Cubic spline interpolation
spline_FCZ_v = make_interp_spline(x, FCZ_valid_averages, k=3)  # Cubic spline interpolation
smooth_FCZ_e = spline_FCZ_e(x_smooth)
smooth_FCZ_v = spline_FCZ_v(x_smooth)


#Ttest plots
plt.plot(x, average_t_FCZ, label='FCZ')
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
#Grand average FCZ plot
plt.figure()
plt.plot(x_smooth, smooth_FCZ_v, label='valid')
plt.plot(x_smooth, smooth_FCZ_e, label='error')
plt.xlabel('1 second of samples at 512 Hz sampling rate after stimuli')
plt.ylabel('μV')
plt.title('Grand Average FCZ plot')
plt.legend()
plt.show()

debugpoint = []
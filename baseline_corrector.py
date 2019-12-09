''' 
Baseline Corrector
------------------

From the paper "Efficient and Effective Baseline Correction Algorithm for Raman Spectra" by Yung-Sheng Chen & Yu Hsu

'''

import numpy as np


### Basis Functions ###

#an integer
window_size = 3 

# Returns minimum of a graph in a window around a point
def WMIN(idx,datapoints,ws = window_size):	
	num_datapoints = len(datapoints)	
	wstart = max(idx - ws,0)
	wend = min(idx + ws, num_datapoints) 
	return min(datapoints[wstart:wend])

def WMEAN(idx,datapoints,ws = window_size):
	num_datapoints = len(datapoints)
	wstart = max(idx - ws,0)
	wend = min(idx + ws, num_datapoints) 
	NOM = 0
	for i in range(wstart,wend):
		NOM += WMIN(i,datapoints,ws)
	# correct extreme edge values
	multiplier = 2*ws/(wend - wstart)
	NOM *= multiplier
	return NOM/(2*ws + 1)

def W4MEAN(idx,datapoints,ws = window_size):
	num_datapoints = len(datapoints)
	wstart = max(idx - ws*4,0)
	wend = min(idx + ws*4, num_datapoints) 
	NOM = 0
	for i in range(wstart,wend):
		NOM += WMEAN(i,datapoints,ws)
	# correct extreme edge values
	multiplier = 2*ws/(wend - wstart)
	NOM *= multiplier
	return NOM/(8*ws + 1)

def WAVG(idx,datapoints,ws = window_size): 
	return (WMEAN(idx,datapoints,ws) + W4MEAN(idx,datapoints,ws))/2

# Minima Smoother

def SMOOTH(datapoints,ws = window_size):
	num_datapoints = len(datapoints)
	f_min = [WMEAN(i,datapoints,ws) for i in range(num_datapoints)]
	f_min = np.array(f_min)
	f_avg = [WAVG(i,datapoints,ws) for i in range(num_datapoints)]
	f_avg = np.array(f_avg)	
	return (f_avg,f_min)


### Negative Signal Removal ###

def comp3(a,b,c):
	if b < c: 
		return c
	else: 
		return a

def NEGSIGNAL(P_in,P_ref,ws = window_size):
	assert len(P_in) == len(P_ref)
	num_datapoints = len(P_in)
	M_in = [WMEAN(i,P_in,ws) for i in range(num_datapoints)]
	M_in = np.array(M_in)
	M_ref = [WMEAN(i,P_ref,ws) for i in range(num_datapoints)]
	M_ref = np.array(M_ref)
	OUT = list(map(comp3,P_in, M_in,M_ref))
	return OUT

### Baseline Removal ###

def baseline_removal(datapoints,ws=window_size):
	## stage 1	
	Y_in = datapoints
	Y_ref, _ = SMOOTH(Y_in,ws)
	Y_out = NEGSIGNAL(Y_in, Y_ref,ws)
	## stage 2
	Y_in_2 = Y_out
	Y_ref_2, _ = SMOOTH(Y_out)  	
	ws_2 = max(0,int(ws/3))
	Y_out_2 = NEGSIGNAL(Y_in_2,Y_ref_2,ws_2)
	## stage 3
	_,Y_out = SMOOTH(Y_out_2)

	Y_corrected = Y_in - Y_out
	return Y_corrected

##########################
if __name__ == '__main__':
	pass

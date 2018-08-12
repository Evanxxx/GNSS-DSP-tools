#!/usr/bin/env python

import sys
import os
import numpy as np
import scipy.signal
import scipy.fftpack as fft

import gnsstools.galileo.e1c as e1c
import gnsstools.nco as nco
import gnsstools.io as io

#
# Acquisition search
#

def search(x,prn):
  fs = 8192000.0
  n = 32768                                        # 4 ms coherent integration
  incr = float(e1c.code_length)/n
  c = e1c.code(prn,0,0,incr,n)                     # obtain samples of the E1-C code
  boc = nco.boc11(0,0,incr,n)
  c = fft.fft(np.concatenate((c*boc,np.zeros(n))))
  m_metric,m_code,m_doppler = 0,0,0
  for doppler in np.arange(-9000,9000,50):         # doppler bins
    q = np.zeros(2*n)
    w = nco.nco(-doppler/fs,0,2*n)
    for block in range(20):                        # 20 incoherent sums
      b = x[(block*n):((block+2)*n)]
      b = b*w
      r = fft.ifft(c*np.conj(fft.fft(b)))
      q = q + np.absolute(r)
    idx = np.argmax(q)
    if q[idx]>m_metric:
      m_metric = q[idx]
      m_code = e1c.code_length*(float(idx)/n)
      m_doppler = doppler
  m_code = m_code%e1c.code_length
  return m_metric,m_code,m_doppler

#
# main program
#

# parse command-line arguments
# example:
#   ./acquire-galileo-e1c.py data/gps-5001-l1_a.dat 68873142.857 -8662285.714

filename = sys.argv[1]        # input data, raw file, i/q interleaved, 8 bit signed (two's complement)
fs = float(sys.argv[2])       # sampling rate, Hz
coffset = float(sys.argv[3])  # offset to E1 Galileo carrier, Hz (positive or negative)

# read first 85 ms of file

n = int(fs*0.085)
fp = open(filename,"rb")
x = io.get_samples_complex(fp,n)

# resample to 8.192 MHz

fsr = 8192000.0/fs
nco.mix(x,-coffset/fs,0)
h = scipy.signal.firwin(161,4e6/(fs/2),window='hanning')
x = scipy.signal.filtfilt(h,[1],x)
xr = np.interp((1/fsr)*np.arange(85*8192),np.arange(len(x)),np.real(x))
xi = np.interp((1/fsr)*np.arange(85*8192),np.arange(len(x)),np.imag(x))
x = xr+(1j)*xi

# iterate (in parallel) over PRNs of interest

def worker(p):
  x,prn = p
  metric,code,doppler = search(x,prn)
  return 'prn %2d doppler % 7.1f metric % 7.1f code_offset %6.1f' % (prn,doppler,metric,code)

import multiprocessing as mp

prns = list(range(1,51))
cpus = mp.cpu_count()
results = mp.Pool(cpus).map(worker, map(lambda prn: (x,prn),prns))

for r in results:
  print(r)

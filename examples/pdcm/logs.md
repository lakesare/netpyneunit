// All results calculated from 60-sec simulations and approximately 1850 neurons.

// Unbalanced Poisson, 10%, running for 1s (took me 10 minutes)
my sim      paper
L2e : 0.852 0.75
L2i : 4.244 3.28
L4e : 4.180 4.76
L4i : 5.313 6.20
L5e : 5.672 6.55
L5i : 8.019 8.97
L6e : 0.079 1.10
L6i : 6.129 1.10

// Balanced Poisson, 10%, running for 1s (took me 10 minutes)
paper        my sim
L2e: 0.75    L2e: 0.733 Hz
L2i: 3.28    L2i: 3.250 Hz
L4e: 4.76    L4e: 4.665 Hz
L4i: 6.20    L4i: 6.174 Hz
L5e: 6.55    L5e: 6.726 Hz
L5i: 8.97    L5i: 8.868 Hz
L6e: 1.10    L6e: 1.150 Hz
L6i: 1.10    L6i: 8.044 Hz

// Balanced Poisson, 10%, running for 60s
paper        my 1s sim           my 60s sim
L2e: 0.75    L2e: 0.733 Hz    L2e : 0.747 Hz  
L2i: 3.28    L2i: 3.250 Hz    L2i : 3.277 Hz  
L4e: 4.76    L4e: 4.665 Hz    L4e : 4.756 Hz  
L4i: 6.20    L4i: 6.174 Hz    L4i : 6.204 Hz  
L5e: 6.55    L5e: 6.726 Hz    L5e : 6.595 Hz  
L5i: 8.97    L5i: 8.868 Hz    L5i : 8.964 Hz  
L6e: 1.10    L6e: 1.150 Hz    L6e : 1.102 Hz  
L6i: 1.10    L6i: 8.044 Hz    L6i : 8.055 Hz  


// Balanced Poisson, 1% and 2%, running for 1s
              L2e            L2i           L4e           L4i
2%  0.68 (24.13%)  3.83 (36.70%)  4.05 (7.79%)  5.88 (3.17%)
1%  0.69 (23.06%)  3.79 (35.47%)  4.32 (1.65%)  5.86 (2.85%)
// It does reasonably match the paper (Salvador runs them for 60s!)


// Balanced DC, 10%, running for 1s
L2e : 0.798 Hz
L2i : 3.046 Hz
L4e : 4.312 Hz
L4i : 5.488 Hz
L5e : 6.734 Hz
L5i : 8.217 Hz
L6e : 0.813 Hz
L6i : 7.190 Hz

     L2e
10%  0.80 (...)

It's 0.87 in the paper.

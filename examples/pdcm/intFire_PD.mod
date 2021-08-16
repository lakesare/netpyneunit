NEURON {
  : ARTIFICIAL_CELL means
  
  ARTIFICIAL_CELL IntFire_PD
  RANGE m, Iext, i
  : m plays the role of voltage
}

PARAMETER {
  :Membrane time constant
  taum = 10 (ms)
  :Absolute refractory period
  tauref =2 (ms) 
  :Postsynaptic current time constant
  tausyn = 0.5 (ms) :0.5
  :Reset potential
  Vreset = -65 (mV) : -49 (mV) :
  :Fixed firing threshold
  Vteta  = -50 (mV)
  :Membrane capacity
  Cm   = 250 (pF)
  Iext = 0(pA)
}

: Specify units that have physiological interpretations (NB: ms is already declared)
UNITS {
  (mV) = (millivolt)
  (pF) = (picofarad)
  (pA) = (picoamps)
}


ASSIGNED {
  m(mV)
  i(pA)
  t0(ms)
  refractory
}

FUNCTION M() {

}

FUNCTION I() {

}


INITIAL {
  t0 = t
  refractory = 0 : 0-integrates input, 1-refractory
}

NET_RECEIVE (w) {
  if (refractory == 0) { : inputs integrated only when excitable
    
    :6.5
    i=i-(i/tausyn)*(t-t0)
    i=i+w
    m=m+(((Vreset-m)/taum)+((i+Iext)/Cm))*(t-t0)
    
    
    :7.5
    :i=i+w
    :m=m+(((Vreset-m)/taum)+((i+Iext)/Cm))*(t-t0)
    :i=i-(i/tausyn)*(t-t0)
    
    :6.7
    :m=m+(((Vreset-m)/taum)+((i+Iext)/Cm))*(t-t0)
    :i=i+w
    :i=i-(i/tausyn)*(t-t0)
    t0 = t

    if (m > Vteta) {
      refractory = 1
      :m = Vreset
      m = Vreset+30
      net_send(tauref, refractory)
      net_event(t)
    }
  }else if (flag == 1) { : ready to integrate again
    t0 = t
    refractory = 0
    m = Vreset
  }
}

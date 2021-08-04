
In the play repo


This initSim() introduces:
  NEURON: syntax error
   near line 1
   append={}
          ^
errors in the last two tests:
  gaba  nmda gaba2 nmda2 gaba3 nmda3
  Pass  Pass  Pass  Pass  Fail  Fail


  def initSim(self):
    netParams = specs.NetParams({
      'popParams': {
        'population1': {
          'numCells': 10,
          'cellType': 'PYR',
          'cellModel': 'HH'
        }
      },

      'cellParams': {
        'PYR': {
          'conds': {'cellModel':'HH', 'cellType': 'PYR'},
          'secs': {
            'soma': {
              'geom': {'diam': 18.8, 'L': 18.8, 'Ra': 123.0},
              'mechs': {
                'hh': {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}
              },
              'vinit': -71
            }
          }
        }
      },

      'synMechParams': {
        'AMPA': {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 1.0, 'e': 0},
        'NMDA': {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0},
        'GABA': {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -75}
      },

      'connParams': {
        'population1->population1_AMPA': {
          'preConds': {'pop': 'population1'}, 
          'postConds': {'pop': 'population1'},
          'weight': 0.1,       
          'delay': '0.2+normal(13.0,1.4)',
          'synMech': 'AMPA'
        },
        'population1->population1_NMDA': {
          'preConds': {'pop': 'population1'}, 
          'postConds': {'pop': 'population1'},
          'weight': self.default_nmda_weight,
          'delay': '0.2+normal(13.0,1.4)',
          'synMech': 'NMDA'
        },
        'population1->population1_GABA': {
          'preConds': {'pop': 'population1'}, 
          'postConds': {'pop': 'population1'},
          'weight': self.default_gaba_weight,  
          'delay': 5,    
          'synMech': 'GABA'
        }
      },

      'stimSourceParams': {
        'background': {
          'type': 'NetStim',
          'rate': 30,
          'noise': 0.5,
          'start': 1
        }
      },

      'stimTargetParams': {
        'background->population1': {
          'source': 'background', 
          'conds': {'pop': 'population1'}, 
          'weight': 0.1, 
          'delay': 'uniform(1,2)'
        }
      }
    })

    simConfig = specs.SimConfig({
      'duration': .5*1e3,
      'dt': 0.025,
      'seeds': {'conn': 1, 'stim': 1, 'loc': 1},
      'timing': False,
      'hParams': {'v_init': -75},
      'recordCells': [],
      'recordTraces': {'Vsoma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}},
      'recordStim': True,
      'recordStep': 0.1
    })

    sim.create(netParams=netParams, simConfig=simConfig)



This doesn't:


  def initSim(self):
    netParams=specs.NetParams()
    simConfig=specs.SimConfig()

    ### Set the network paramters ###

    # Population parameters
    # _______________USED to be 200!
    netParams.popParams['population1']={
      # Original n of cells is 200, however each run takes 137s then.
      # 10 cells approximates the results well.
      'numCells': 10, # population1 comprises 200 
      'cellType':'PYR', # pyramidal cells
      'cellModel':'HH'
    }  # of the hodgkyn-huxley model, which is native to netpyne

    # Cell parameters

    ## The cell properties

    # First, we create a dict of cell rules. The conds refer to the cell's conditions
    # and the secs refers to its sections 
    cellRule={'conds':{'cellModel':'HH', 'cellType': 'PYR'},  'secs': {}} 
    cellRule['secs']['soma']={'geom': {}, 'mechs': {}}  


    cellRule['secs']['soma']['geom']={'diam': 18.8, 'L': 18.8, 'Ra': 123.0} # The soma's geomtry  
    cellRule['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} # The soma's hh mechanism
    cellRule['secs']['soma']['vinit']=-71 # the initial cell's electric potential

    netParams.cellParams['PYR']=cellRule  # add rule dictionary to the cell params


    # Synaptic mechanism parameters

    # Exp2Syn is a two state kinetic scheme synapse where
    # the rise time is set by tau1 and the decay time by tau2.
    # the reversal potential is e.

    netParams.synMechParams['AMPA']={'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 1.0, 'e': 0}
    netParams.synMechParams['NMDA']={'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0} 
    netParams.synMechParams['GABA']={'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -75}

    # Connectivity parameters
    # AMPA synapses
    netParams.connParams['population1->population1_AMPA'] = {
      'preConds': {'pop': 'population1'}, 
      'postConds': {'pop': 'population1'},
      'weight': 0.1,       
      'delay': '0.2+normal(13.0,1.4)',     # delay min=0.2, mean=13.0, var = 1.4
      'synMech': 'AMPA'
    }    

    # NMDA synapses
    netParams.connParams['population1->population1_NMDA'] = {
      'preConds': {'pop': 'population1'}, 
      'postConds': {'pop': 'population1'},
      'weight': self.default_nmda_weight,
      'delay': '0.2+normal(13.0,1.4)',     # delay min=0.2, mean=13.0, var = 1.4
      'synMech': 'NMDA'
    }  

    # GABA synapses
    netParams.connParams['population1->population1_GABA'] = {
      'preConds': {'pop': 'population1'}, 
      'postConds': {'pop': 'population1'},
      'weight': self.default_gaba_weight,  
      'delay': 5,    
      'synMech': 'GABA'
    }


    # Stimulation parameters
    netParams.stimSourceParams['background'] = {
      'type': 'NetStim', # network stimuli
      'rate': 30, # of 30 hz
      'noise': 0.5,
      'start': 1
    }

    netParams.stimTargetParams['background->population1'] = {
      'source': 'background', 
      'conds': {'pop': 'population1'}, 
      'weight': 0.1, 
      'delay': 'uniform(1,2)'
    }

    ### Set the simulation ###

    # Simulation parameters
    simConfig.duration = .5*1e3 # Duration of the simulation, in ms
    simConfig.dt = 0.025 # Internal integration timestep to use
    simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
    simConfig.verbose = False  # show detailed messages 
    simConfig.hParams = {'v_init': -75}

    # Recording 
    simConfig.recordCells = []  # which cells to record from
    simConfig.recordTraces = {'Vsoma':{'sec':'soma','loc':0.5,'var':'v'}}
    simConfig.recordStim = True  # record spikes of cell stims
    simConfig.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)

    sim.create(netParams=netParams, simConfig=simConfig)



In the netpyneunit repo, however, both produce the neuron error!




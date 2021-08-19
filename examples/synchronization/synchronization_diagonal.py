import os
import sys

from netpyne import specs, sim
import sciunit
from netpyneunit.models import NetpyneModel
from netpyneunit.models.backends import NetpyneBackend

import logging
logging.getLogger('netpyne').setLevel(logging.WARNING)

class ProducesSyncMeasure(sciunit.Capability): 
  def produce_sync_measure(self):
    self.unimplemented()

from sciunit.models.backends import register_backends
register_backends({"Netpyne": NetpyneBackend})

class NeuromodulatorModel(NetpyneModel, ProducesSyncMeasure):

  def __init__(self, name, nmda_weight=0.7, gaba_weight=0.005):
    super().__init__(name=name, backend=("Netpyne", { "use_memory_cache": False, "use_disk_cache": False }))
    self.nmda_weight = nmda_weight
    self.gaba_weight = gaba_weight

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
          'weight': self.nmda_weight,
          'delay': '0.2+normal(13.0,1.4)',
          'synMech': 'NMDA'
        },
        'population1->population1_GABA': {
          'preConds': {'pop': 'population1'}, 
          'postConds': {'pop': 'population1'},
          'weight': self.gaba_weight,  
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
      'verbose': False,
      'hParams': {'v_init': -75},
      'recordCells': [],
      'recordTraces': {'Vsoma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}},
      'recordStim': True,
      'recordStep': 0.1
    })
    
    sim.initialize(netParams=netParams, simConfig=simConfig)
    sim.net.createPops()
    sim.net.createCells()

  def produce_sync_measure(self):
    return sim.analysis.syncMeasure()

class SynchronyTest(sciunit.Test):
  required_capabilities = (ProducesSyncMeasure, )
  score_type = sciunit.scores.BooleanScore

  def generate_prediction(self, model):
    model.run()
    return model.produce_sync_measure()

  def compute_score(self, observation, prediction):
    score = self.score_type(observation['value'] == prediction)
    return score

model_by_default = NeuromodulatorModel("Default model")
model_with_nmda_antagonist = NeuromodulatorModel("With nmda antagonist", nmda_weight=0)
model_with_gaba_agonist = NeuromodulatorModel("With gaba agonist", gaba_weight=0.5)

default_test = SynchronyTest({'value': 0.896}, name="default")
# Synchronization decreases (from the default), as it should
nmda_test = SynchronyTest({'value': 0.808}, name="nmda")
# Synchronization increases (from the default), as it should
gaba_test = SynchronyTest({'value': 0.954}, name="gaba")

neuromodulators_suite = sciunit.TestSuite([default_test, gaba_test, nmda_test], name="Neuromodulators test suite")
score_matrix = neuromodulators_suite.judge([model_by_default, model_with_gaba_agonist, model_with_nmda_antagonist])
print(score_matrix)

import os
import sys

from netpyne import specs, sim
import sciunit
from netpyneunit.models import NetpyneModel
from netpyneunit.models.backends import NetpyneBackend

import logging
# (The default logging level in NetPyNE is logging.INFO)
logging.getLogger('netpyne').setLevel(logging.WARNING)

class ProducesSyncMeasure(sciunit.Capability): 
  def produce_sync_measure(self):
    self.unimplemented()

class AddsGabaAgonist(sciunit.Capability):
  def add_gaba_agonist(self):
    self.unimplemented()

  def revert_add_gaba_agonist(self):
    self.unimplemented()

class AddsNmdaAntagonist(sciunit.Capability):
  def add_nmda_antagonist(self):
    self.unimplemented()

  def revert_add_nmda_antagonist(self):
    self.unimplemented()

class NeuromodulatorModel(NetpyneModel,
  AddsGabaAgonist, AddsNmdaAntagonist, ProducesSyncMeasure):

  default_nmda_weight = 0.7
  default_gaba_weight = 0.005

  def __init__(self):
    super().__init__(name="Neuromodulator Model")
    with suppress_stdout():
      self.initSim()

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

  def produce_sync_measure(self):
    return sim.analysis.syncMeasure()

  def add_gaba_agonist(self):
    sim.net.modifyConns({'conds': {'label': 'population1->population1_GABA'}, 'weight': 0.5})

  def revert_add_gaba_agonist(self):
    sim.net.modifyConns({'conds': {'label': 'population1->population1_GABA'}, 'weight': self.default_gaba_weight})

  def add_nmda_antagonist(self):
    sim.net.modifyConns({'conds': {'label': 'population1->population1_NMDA'}, 'weight': 0})

  def revert_add_nmda_antagonist(self):
    sim.net.modifyConns({'conds': {'label': 'population1->population1_NMDA'}, 'weight': self.default_nmda_weight})

class GabaAgonistTest(sciunit.Test):
  required_capabilities = (ProducesSyncMeasure, AddsGabaAgonist)
  score_type = sciunit.scores.BooleanScore

  def generate_prediction(self, model):
    model.add_gaba_agonist()
    model.run()
    model.revert_add_gaba_agonist()
    return model.produce_sync_measure()

  def compute_score(self, observation, prediction):
    score = self.score_type(observation['value'] == prediction)
    return score

class NmdaAntagonistTest(sciunit.Test):
  required_capabilities = (ProducesSyncMeasure, AddsNmdaAntagonist)
  score_type = sciunit.scores.BooleanScore

  def generate_prediction(self, model):
    model.add_nmda_antagonist()
    model.run()
    model.revert_add_nmda_antagonist()
    return model.produce_sync_measure()

  def compute_score(self, observation, prediction):
    score = self.score_type(observation['value'] == prediction)
    return score

neuromodulator_model = NeuromodulatorModel()

gaba_test = GabaAgonistTest({'value': 0.954}, name='gaba')
gaba_test_2 = GabaAgonistTest({'value': 0.954}, name='gaba2')
nmda_test = NmdaAntagonistTest({'value': 0.808}, name='nmda')

neuromodulators_suite = sciunit.TestSuite([gaba_test, nmda_test, gaba_test_2], name="Neuromodulators test suite")
score_matrix = neuromodulators_suite.judge([neuromodulator_model])
print(score_matrix)

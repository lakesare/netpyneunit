import os
import sys
from netpyne import sim
from sciunit.models.backends import Backend

class NetpyneBackend(Backend):
  # From sim.load()
  def cache_to_results(self, cache):
    sim.initialize()
    sim.loadSimCfg(None, data=cache)
    sim.cfg.createNEURONObj = True
    sim.loadNetParams(None, data=cache)
    sim.loadNet(None, data=cache, compactConnFormat=sim.cfg.compactConnFormat)
    sim.loadSimData(None, data=cache)

  # From sim.saveData()
  def results_to_cache(self, results):
    cache = {
      'netpyne_version': sim.version(show=False),
      'netpyne_changeset': sim.gitChangeset(show=False),
      'net': {
        'params': sim.replaceFuncObj(sim.net.params.__dict__),
        'cells': sim.net.allCells,
        'pops': sim.net.allPops,
      },
      'simConfig': sim.cfg.__dict__,

      # Results
      'simData': sim.allSimData
    }

    if 'LFP' in cache['simData']['allSimData']:
      cache['simData']['allSimData']['LFP'] = cache['simData']['allSimData']['LFP'].tolist()

    # This line changes the first result (remember the colab bug)
    # cache = sim.replaceDictODict(cache)

    return cache

  # A final get_sim_hash()!
  def get_sim_hash(self):
    net = {}
    # net['params'] = sim.replaceFuncObj(sim.net.params.__dict__)
    net['simConfig'] = sim.cfg.__dict__
    # print(sim.cfg.__dict__)
    # net['netpyne_version'] = sim.version(show=False)
    return net

  def backend_run(self):
    self.model.initSim()
    sim_hash = self.get_sim_hash()
    # I think sciunit is doing something bad to run_params.
    # And then NEURON complains.
    self.model.set_run_params(sim_hash=sim_hash)

    # Checks whether we have cache, and runs it (with _backend_run) if we don't.
    super().backend_run()

  def _backend_run(self):
    # Identical to sim.create():
    #
    # 1. We leave these up to the user:
    #    sim.initialize(netParams, simConfig)
    #    sim.net.createPops()
    #    sim.net.createCells()

    # 2. And we run these ourselves.
    #    The user can override _backend_run if they want to!
    sim.net.connectCells()
    sim.net.addStims()
    sim.net.addRxD()
    sim.setupRecording()

    # Identical to sim.simulate():
    sim.runSim()
    sim.gatherData()

    # Identical to sim.analyze():
    sim.saveData()
    sim.analysis.plotData()
    return sim

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
      'simData': sim.allSimData
    }

    if 'LFP' in cache['simData']['allSimData']:
      cache['simData']['allSimData']['LFP'] = cache['simData']['allSimData']['LFP'].tolist()

    cache = sim.replaceDictODict(cache)

    return cache

  def get_sim_hash(self):
    """
      Used to determine whether the sim we want to run is already cached.

      Does NOT react to sim.net.modifyConns, modifyStims, and other similar methods.
      If we want to differentiate between the sims on which `sim.net.modifyConns` was or wasn't called, we want to cache:
        net['cells'] = sim.net.allCells
        net['pops'] = sim.net.allPops
      additionally.
      However, these can be huge objects, and we might want to consider other options:
      1. Do we even need to account for `sim.net.modifyConns`? Is this frequently used in papers?
      2. Instead of looking at sim.net.allCells, every time we change something, we might change the attribute of the NetpyneModel.
    """
    net = {}
    net['params'] = sim.replaceFuncObj(sim.net.params.__dict__)
    net['simConfig'] = sim.cfg.__dict__
    net['netpyne_version'] = sim.version(show=False)
    return net

  def backend_run(self):
    self.model.initSim()
    sim_hash = self.get_sim_hash()
    self.model.set_run_params(sim_hash=sim_hash)
    # Checks whether we have cache, and runs it (with _backend_run) if we don't.
    super().backend_run()

  def _backend_run(self):
    # Identical to sim.create():
    #
    # 1. We leave these up to the user (they implement it in initSim()):
    #    ATTENTION: it's prettier to only leave sim.initialize() to the user.
    #    The reason I also left .createPops() and .createCells() to the user
    #    is because the PdcmModel randomizes the input AFTER it creates pops & cells.
    #    When we implement more models it will be more clear what we want
    #    the user to have in initSim(), and what we want to run for them.
    #
    #    sim.initialize(netParams, simConfig)
    #    sim.net.createPops()
    #    sim.net.createCells()
    #
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

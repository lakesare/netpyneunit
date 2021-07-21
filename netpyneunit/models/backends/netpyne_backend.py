import os
import sys
from netpyne import sim
from sciunit.models.backends import Backend

from contextlib import contextmanager
@contextmanager
def suppress_stdout():
  with open(os.devnull, "w") as devnull:
    old_stdout = sys.stdout
    sys.stdout = devnull
    try:  
      yield
    finally:
      sys.stdout = old_stdout


class NetpyneBackend(Backend):
  # From sim.load()
  def cache_to_results(self, cache):
    # Create network object and set cfg and net params
    sim.initialize()

    sim.loadSimCfg( None, data=cache)
    sim.loadSimData(None, data=cache)
    # I think we only need loadSimCfg() and loadSimData().
    # However, some analysis utils (or graphs) might requires these two too.
    sim.loadNetParams(None, data=cache)
    sim.loadNet(      None, data=cache, instantiate=False, compactConnFormat=sim.cfg.compactConnFormat)

  # From sim.saveData()
  def results_to_cache(self, results):
    sim.gatherData()

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

    cache = sim.replaceDictODict(cache)

    return cache

  # A final get_sim_hash()!
  def get_sim_hash(self):
    net = {}
    net['params'] = sim.replaceFuncObj(sim.net.params.__dict__)
    net['cells'] = sim.net.allCells
    net['pops'] = sim.net.allPops
    net['simConfig'] = sim.cfg.__dict__
    net['netpyne_version'] = sim.version(show=False)

    return net

  def _backend_run(self):
    # Populates .allCells and .allPops,
    # makes sure .modifyConns() affects the `net` dictionary
    with suppress_stdout():
      sim.gatherData()

    sim_hash = self.get_sim_hash()
    self.model.set_run_params(sim_hash=sim_hash)

    with suppress_stdout():
      sim.runSim()
      sim.gatherData()
    return sim

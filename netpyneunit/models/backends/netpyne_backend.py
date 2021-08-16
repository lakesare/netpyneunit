import os
import sys
from netpyne import sim
from sciunit.models.backends import Backend

class NetpyneBackend(Backend):
  # From sim.load()
  def cache_to_results(self, cache):
    # BOTH of these make the first successful run after the cache fetch fail!
    # Test with [gaba_test, gaba_test_2, gaba_test_3]
    # Should fail with the NEURON error.
    #
    # Create network object and set cfg and net params
    # sim.initialize()
    # sim.loadSimCfg( None, data=cache)

    sim.loadSimData(None, data=cache)
    # # I think we only need loadSimCfg() and loadSimData().
    # # However, some analysis utils (or graphs) might requires these two too.
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

    # This line changes the first result (remember the colab bug)
    # cache = sim.replaceDictODict(cache)

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

  # This may not be the best place to .set_run_params -
  # For example, self.print_run_params won't print them out.
  # However, the only other option is moving the get_sim_hash() generation
  # to the model, which I wouldn't very much like, I enjoy having all caching-related functionality in one place.
  def backend_run(self):
    # Populates .allCells and .allPops,
    # makes sure .modifyConns() affects the `net` dictionary
    #
    # Attention: sim.gatherData() clears sim.analysis.popAvgRates()! (we don't want this to happen)
    #
    sim.gatherData()

    print('Setting run_params=sim_hash')
    sim_hash = self.get_sim_hash()
    self.model.set_run_params(sim_hash=sim_hash)

    super().backend_run()

  def _backend_run(self):
    # Identical to sim.create():
    #
    # 1. We leave these up to the user:
    # sim.initialize(netParams, simConfig)
    # sim.net.createPops()
    # sim.net.createCells()
    #
    # 2. And we run these ourselves, because we need to run these every time to get the proper analysis.
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

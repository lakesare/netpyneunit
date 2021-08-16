from netpyne import specs, sim
from neuron import h
import sciunit
from netpyneunit.models import NetpyneModel
from netpyneunit.models.backends import NetpyneBackend
import numpy as np

class ProducesMeanFiringRate(sciunit.Capability): 
  def produce_mean_firing_rate(self):
    self.unimplemented()

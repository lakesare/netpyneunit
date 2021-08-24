import sciunit
from PdcmModel import PdcmModel
from tests import PopulationMeanFiringRateTest

import logging
# This relies on https://github.com/Neurosim-lab/netpyne/pull/623.
logging.getLogger('netpyne').setLevel(logging.WARNING)

def table_a1():
  model_80 = PdcmModel(name="80%", scale=0.8, ext_input="balanced_poisson")
  model_60 = PdcmModel(name="60%", scale=0.6, ext_input="balanced_poisson")
  model_50 = PdcmModel(name="50%", scale=0.5, ext_input="balanced_poisson")
  model_40 = PdcmModel(name="40%", scale=0.4, ext_input="balanced_poisson")
  model_30 = PdcmModel(name="30%", scale=0.3, ext_input="balanced_poisson")
  model_20 = PdcmModel(name="20%", scale=0.2, ext_input="balanced_poisson")
  model_10 = PdcmModel(name="10%", scale=0.1, ext_input="balanced_poisson")
  model_5  = PdcmModel(name="5%", scale=0.05, ext_input="balanced_poisson")
  model_2  = PdcmModel(name="2%", scale=0.02, ext_input="balanced_poisson")
  model_1  = PdcmModel(name="1%", scale=0.01, ext_input="balanced_poisson")

  test_L2e = PopulationMeanFiringRateTest({ 'value': 0.90, 'layer': 'L2e' }, name='L2e')
  test_L2i = PopulationMeanFiringRateTest({ 'value': 2.80, 'layer': 'L2i' }, name='L2i')
  test_L4e = PopulationMeanFiringRateTest({ 'value': 4.39, 'layer': 'L4e' }, name='L4e')
  test_L4i = PopulationMeanFiringRateTest({ 'value': 5.70, 'layer': 'L4i' }, name='L4i')
  test_L5e = PopulationMeanFiringRateTest({ 'value': 6.80, 'layer': 'L5e' }, name='L5e')
  test_L5i = PopulationMeanFiringRateTest({ 'value': 8.22, 'layer': 'L5i' }, name='L5i')
  test_L6e = PopulationMeanFiringRateTest({ 'value': 1.14, 'layer': 'L6e' }, name='L6e')
  test_L6i = PopulationMeanFiringRateTest({ 'value': 7.60, 'layer': 'L6i' }, name='L6i')

  suite = sciunit.TestSuite(
    [test_L2e, test_L2i, test_L4e, test_L4i, test_L5e, test_L5i, test_L6e, test_L6i],
    name="Population Mean Firing Rate: Balanced Poisson"
  )
  table = suite.judge(
    [model_80, model_60, model_50, model_40, model_30, model_20, model_10, model_5, model_2, model_1]
  )
  print(table)

def table_a2():
  model_80 = PdcmModel(name="80%", scale=0.8, ext_input="balanced_dc")
  model_60 = PdcmModel(name="60%", scale=0.6, ext_input="balanced_dc")
  model_50 = PdcmModel(name="50%", scale=0.5, ext_input="balanced_dc")
  model_40 = PdcmModel(name="40%", scale=0.4, ext_input="balanced_dc")
  model_30 = PdcmModel(name="30%", scale=0.3, ext_input="balanced_dc")
  model_20 = PdcmModel(name="20%", scale=0.2, ext_input="balanced_dc")
  model_10 = PdcmModel(name="10%", scale=0.1, ext_input="balanced_dc")

  test_L2e = PopulationMeanFiringRateTest({ 'value': 1.02, 'layer': 'L2e' }, name='L2e')
  test_L2i = PopulationMeanFiringRateTest({ 'value': 2.89, 'layer': 'L2i' }, name='L2i')
  test_L4e = PopulationMeanFiringRateTest({ 'value': 4.32, 'layer': 'L4e' }, name='L4e')
  test_L4i = PopulationMeanFiringRateTest({ 'value': 5.60, 'layer': 'L4i' }, name='L4i')
  test_L5e = PopulationMeanFiringRateTest({ 'value': 7.02, 'layer': 'L5e' }, name='L5e')
  test_L5i = PopulationMeanFiringRateTest({ 'value': 8.20, 'layer': 'L5i' }, name='L5i')
  test_L6e = PopulationMeanFiringRateTest({ 'value': 0.90, 'layer': 'L6e' }, name='L6e')
  test_L6i = PopulationMeanFiringRateTest({ 'value': 7.46, 'layer': 'L6i' }, name='L6i')

  suite = sciunit.TestSuite(
    [test_L2e, test_L2i, test_L4e, test_L4i, test_L5e, test_L5i, test_L6e, test_L6i],
    name="Population Mean Firing Rate: Balanced Direct Current"
  )
  table = suite.judge(
    [model_80, model_60, model_50, model_40, model_30, model_20, model_10]
  )
  print(table)

def fast_example_please():
  model_2  = PdcmModel(name="2%", scale=0.02, ext_input="balanced_poisson", duration=1*1e3)
  model_1  = PdcmModel(name="1%", scale=0.01, ext_input="balanced_poisson", duration=1*1e3)

  test_L2e = PopulationMeanFiringRateTest({ 'value': 0.90, 'layer': 'L2e' }, name='L2e')
  test_L2i = PopulationMeanFiringRateTest({ 'value': 2.80, 'layer': 'L2i' }, name='L2i')
  test_L4e = PopulationMeanFiringRateTest({ 'value': 4.39, 'layer': 'L4e' }, name='L4e')
  test_L4i = PopulationMeanFiringRateTest({ 'value': 5.70, 'layer': 'L4i' }, name='L4i')
  test_L5e = PopulationMeanFiringRateTest({ 'value': 6.80, 'layer': 'L5e' }, name='L5e')
  test_L5i = PopulationMeanFiringRateTest({ 'value': 8.22, 'layer': 'L5i' }, name='L5i')
  test_L6e = PopulationMeanFiringRateTest({ 'value': 1.14, 'layer': 'L6e' }, name='L6e')
  test_L6i = PopulationMeanFiringRateTest({ 'value': 7.60, 'layer': 'L6i' }, name='L6i')

  suite = sciunit.TestSuite(
    [test_L2e, test_L2i, test_L4e, test_L4i, test_L5e, test_L5i, test_L6e, test_L6i],
    name="Population Mean Firing Rate: Balanced Poisson"
  )
  table = suite.judge(
    [model_2, model_1]
  )
  print(table)

# A quick reproduction of the table_a1 for 1% and 2% models
# Unlike Table A1, however, this uses duration=1*1e3 instead of duration=60*1e3 to save the time.
fast_example_please()

# Comment out these lines if you'd like a full reproduction of the PDCM paper.
# Careful, this might take many hours to run!
# (E.g., on a single core
# the 1% PDCM model runs for a couple of seconds, while
# the 10% PDCM model runs for 10 minutes)
#
# table_a1()
# table_a2()

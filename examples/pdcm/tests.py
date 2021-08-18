import sciunit
from capabilities import ProducesMeanFiringRate

class MyRelativeDifferenceScore(sciunit.scores.RelativeDifferenceScore):
  def __str__(self):
    return f"{self.prediction[self.observation['layer']]:.2f} ({self.score * 100:.2f}%)"

class PopulationMeanFiringRateTest(sciunit.Test):
  required_capabilities = (ProducesMeanFiringRate, )
  score_type = MyRelativeDifferenceScore

  def generate_prediction(self, model):
    model.run() 
    return model.produce_mean_firing_rate()

  def compute_score(self, observation, prediction):
    pred = prediction[observation['layer']]
    obs = observation['value']

    score = MyRelativeDifferenceScore.compute(obs, pred, scale=obs)
    return score

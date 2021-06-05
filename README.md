# netpyneunit
## SciUnit Tests that work with NetPyne Models

Goals:
- We would like to be able to test neuron and neural circuit models built using NetPyNE.  
- Ideally, a very large fracton of models that are possible to build in NetPyNE (or that people are building) would be testable.  
- The tests themselves should be large in number and diverse.  Examples from NeuronUnit, NetworkUnit, HippoUnit, etc. may be starting points.  
- The SciUnit models themselves will essentially wrap the NetPyNE models, e.g.:
  - `from netpyneunit import NetPyneModel`
  - `my_netpynemodel = NetPyneModel(actual_netpyne_model)  # actual_netpyne_model is an object built in NetPyNE itself`
- `NetPyneModel` will have as its base classes `sciunit.Model` and some number of sciunit `Capability` classes that we will build to provide an interface to netpyne calls.
- There may ultimately be many subclasses of `NetPyneModel` to do different things, some of of which implement capabilities in different ways depending on the model type. Most of the work will be in figuring these last two things out.
- Then we verify that some suites of tests we would like to use can successfully be run against these models, and return scores that make sense.  
- Finally, we should check that we can serialize these scores for use in the SciDash API (this should be easy and possible work automatically).
- An absolute starting point might involve tests that do trivial things (like count the number of neurons), to verify that we can successfully implement capabilities that call netpyne methods and interpret their results correctly.  This assumes that a NetPyNE model can already be built and run successfully (which is an outcome of going through the NetPyNE tutorials).

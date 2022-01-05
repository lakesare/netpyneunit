
<h1 align="center">
  NetpyneUnit:  SciUnit Tests for NetPyNE Models
</h1> 
<p align="center">
  <img alt="GitHub" src="https://img.shields.io/github/issues/lakesare/netpyneunit.svg">
  <img alt="GitHub" src="https://img.shields.io/github/issues-closed/lakesare/netpyneunit.svg">
  <img alt="GitHub" src="https://img.shields.io/github/commit-activity/m/lakesare/netpyneunit.svg">
</p>

<!--   <img alt="GitHub" src="https://github.com/lakesare/netpyneunit/workflows/CI/badge.svg"> -->

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Getting-Started">Getting started</a> •
  <a href="#Examples">Examples</a> •
  <a href="#Functionality">Functionality</a> •
  <a href="#Next-steps">Next steps</a> •
  <a href="#Other">Other</a> 

</p>

## Overview

Check out [google colab](https://colab.research.google.com/github/russelljjarvis/netpyneunit/blob/main/docs/PDCM_example.ipyn) to see **NetpyneUnit** in action.

## Getting Started

<details>
  <summary> Getting Started Steps </summary>

# Install the Python module
1. `git clone https://github.com/lakesare/netpyneunit.git`
2. `pip install sciunit netpyne neuron`  
3. `cd netpyneunit`
4. `pip install -e .` (this will install **NetpyneUnit** locally as if it's a real remote package, and you'll be able to import it from anywhere)
5. `python examples/synchronization/synchronization_diagonal.py`

If you get **3 Passes** on the **diagonal** (and fails everywhere else) - then you ran it successfully!
  
</details>

## Examples

Please read the `README.md` in each subfolder of `/examples`.

## Functionality

<details>
  <summary>Currently, the chief role of the `NetpyneBackend`</summary>

Currently, the chief role of the `NetpyneBackend` is to **run** the simulation in the NetPyNE-specific way, and to **cache** the results of our simulation run.  

Caching is necessary for **NetpyneUnit**:
- if we add a new model to our suite, we don't want to rerun every other simulation (which can well take hours)
- each test separately reruns the simulation by design, even if we just ran it for another test.

**Richard Gerkin** puts it well:
> I am enthusiastic about the caching option because it solves a problem that comes up in validation testing where the same model is run many times (maybe tens or even hundreds of times) under an identical configuration, but different parts of the results are encoded in each test outcome.
> 
> The alternative solution, which would be to specifically organize the tests to "know" when they are likely to produce the same simulation output and have them share it, is impractical for a few reasons: this would violate the "separate the interface from the implementation" principle behind testing generally and SciUnit specifically, would require a big rewrite of the testing logic in SciUnit, and also I'm not sure it’s even possible to compute in advance exactly what any arbitrary test will do to a model.

**Things to keep in mind**:
- You will see the `NEURON: syntax error`  - do not worry about this, this is merely a warning (explained down below).
- Our caching layer won't understand that you changed your model via `sim.net.modifyConns()` - try to be changing the model simply visa updating the instance variables.

</details>

## Next steps

<details>
  <summary>Caching within **NetpyneUnit** works</summary>

Caching within **NetpyneUnit** works, however we believe the caching layer belongs to **NetPyNE**.
Please follow the following issue in **NetPyNE**: [https://github.com/Neurosim-lab/netpyne/issues/624](https://github.com/Neurosim-lab/netpyne/issues/624) to see whether **NetPyNE** folks agree.
If **NetPyNE** implements internal caching, then we'll be able to remove the caching code from `NetpyneBackend` and `NetpyneModel`.
If **NetPyNE** decides against it, we should improve **NetpyneUnit** caching. Following points describe the necessary improvements.

</details>

<details>
  <summary> 1. Deal with the cryptic NEURON warning   </summary>
 
   With caching enabled, you'll be sure to stumble upon the following **NEURON** error:
```
NEURON: syntax error
 near line 1
 __dict__={}
          ^
```
  
Do not fret! This is merely a warning, and it shouldn't affect the results of your sim run.
This happens because our `jsonpickle.encode(self)` slightly mutates our `simConfig` (and probably `netParams`) when it creates the hash of the model: it inserts undesirable attributes into every object, e.g. `__dict__` and `__getnewargs__`. 
**NEURON** doesn't recognize these attributes, and raises the aforementioned warning.

We should create a **custom jsonpickle handler** (place it along our other handlers) that will remove these foreign attrs.

</details>

<details>
  <summary>  2. Decide what to do with sim.net.modifyConns() </summary>

Salvador raised the concern that calculating the model hash with `sim.net.allPops` and `sim.net.allCells` might be a bad idea - what if we have 80k cells, will this perform reasonably well?
Further more, if we have randomization, `allCells`  might be catching the attributes we don't want to cache.

#### 3. Walk through `sim.load()` and `sim.saveData()`

Walk through **NetPyNE**'s `sim.load()` and `sim.saveData()` to make sure that **NetpyneUnit**'s' `cache_to_results` and `results_to_cache()` aren't missing any code of importance.

</details>


<details>
  <summary> Logging </summary>
  
By default, **NetPyNE** outputs a ton of logs on each run, and, with many sims per the program run, the **NetPyNE** output becomes incomprehensible, and the **SciUnit** output gets hard to find.  
To deal with this, I created the logging PR to **NetPyNE**, and hopefully they should merge it soon ([https://github.com/Neurosim-lab/netpyne/pull/623](https://github.com/Neurosim-lab/netpyne/pull/623)).

Please follow the logging PR [https://github.com/Neurosim-lab/netpyne/pull/623](https://github.com/Neurosim-lab/netpyne/pull/623) - we expect question answer and a PR review from **NetPyNE**, and we want this PR merged.

If you want to control the **NetPyNE** logs already - clone their repo, switch to the `lakesare:switch_to_logging` branch, and run `pip install -e .`.
Then, in your code, run:
```
import logging
logging.getLogger('netpyne').setLevel(logging.WARNING)
```
  
</details>


<details>
  <summary> ResizeSuite </summary>

Continue with the **PCDM model example** (`/examples/pdcm`), and try to generalize it.
Find a paper similar to [https://direct.mit.edu/neco/article-pdf/33/7/1993/1925382/neco_a_01400.pdf](https://direct.mit.edu/neco/article-pdf/33/7/1993/1925382/neco_a_01400.pdf) - some paper that tries to rescale the **NetPyNE** model while keeping its statistics intact, and convert it to the language of **SciUnit**.
After this is done, we should be able to see a better (if any exists!) way to structure our `NetpyneBackend`/`NetpyneFrontend`, and potentially create a `ResizeSuite`.

</details>

<details>
  <summary> SciDash </summary>

We should check that we can serialize the scores for use in the **SciDash API** (this should be easy and possible work automatically).

</details>

### Other

<details>
  <summary> Generality of Approach used here </summary>
    
Almost any paper describing a **NetPyNE** network should be able to benefit from **SciUnit**.
Our role with **NetpyneUnit** is to standardize widespread tests, and to implement logic common to a lot of papers.

For this to be possible, we should go from the ground up - read the paper, wrap the **NetPyNE** model into **SciUnit**, and see whether anything should be abstracted into a **NetpyneModel** subclass or a new **sciunit.Test**.

It may also be useful to take hints from other similar libraries - examples from **NeuronUnit**, **NetworkUnit**, **HippoUnit**, etc. can be starting points.  
    
</details>


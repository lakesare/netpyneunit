# Synchronization of the network depending on the neuromodulators

### Origin
Comes from **Gili Karni**'s excellent medium post:
[https://medium.com/@gili.karni/simulating-biological-neural-networks-with-netpyne-d1744c1f4a02](https://medium.com/@gili.karni/simulating-biological-neural-networks-with-netpyne-d1744c1f4a02).

### Description
Gili reviews multiple studies, and expects our **NetPyNE** network to have a particular behavior:
- **NMDA antagonist** should **decrease the synchrony**
- **GABA agonist** should **increase the synchrony**  

The only difference betweeen hers and our model is the number of neurons - she used **200** (see `'numCells'`), and we used **10** to speed up the model (hers runs for 10 minutes, ours for a few seconds).
Additionally, our model is beautified - if you'd like to read the proper description of the model and see the comments in code, please head to her post.

### Goal
This is a simplistic, fast model with an easy to predict behaviour - we use it to test caching in our `NetpyneBackend`, to show various ways to encode the same model, and to make sure everything is properly installed in our environment.

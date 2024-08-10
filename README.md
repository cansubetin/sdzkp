# SDZKP: A zero-knowledge proof using subgroup distance problem

We present a new zero-knowledge identification scheme rooted in the complexity of the subgroup distance problem within the Hamming metric. The proposed protocol, called the Subgroup Distance Zero Knowledge Proof (SDZKP), incorporates a cryptographically secure pseudorandom number generator to obscure secrets and employs a Stern-type algorithm to ensure strong security features.

## Installation

Create a project folder, in that folder preferably create a virtual environment:
```python3 -m venv venv```
```source venv/bin/activate```


### Prerequisites
SDZKP is an interactive zero-knowledge protocols and we use gRPC.
```pip install grpcio```
```pip install protobuf```

### SDZKP package
Install the latest SDZKP package
```pip install sdzkp```

You can then copy sdzkp_verifier.py and sdzkp_prover.py from **[GitHub](https://github.com/cansubetin/sdzkp)** and run them in two terminals (do not forget to `source venv/bin/activate` in both terminals).

## Acknowledgement
This work is partially supported by the NLnet foundation under the MoU number 2021-12-510.
# Introduction

Zero-knowledge proof (ZKP) systems help principals to verify the
veracity of a piece of information without sharing the data. They are
widely used to preserve confidentiality and ownership of data. ZKP can
be seen as a reusable building block for making the future internet
trustworthy and secure. In this project (0KNOW) we aimed to develop a
lightweight group-theoretic zero-knowledge proof system that can be
employed as a cryptographic primitive in many security protocols such as
identification, authentication, or credential ownership.

In 0KNOW, we have studied NP group-theoretic problems and selected the
search version of the subgroup distance problem within the Hamming
metric. Breifly, for given distance $k$, given element $g$, given
subgroup H from the symmeric group of degree $n$ ($S_n$), problem asks
to find an element h from the subgroup H which is at most $k$ distance
from $g$. Our choice as platform subgroup is an elementary abelian
subgroup. We have designed a novel black-box 3-round statistical zero
knowledge proof of knowledge protocol called the Subgroup Distance Zero
Knowledge Proof (SDZKP). It can be seen as a Stern-type protocol. It has
3-special-soundness property which assures knowledge soundness with
error $\frac{2}{3}$.

All in all, we present a new zero-knowledge identification scheme rooted
in the complexity of the subgroup distance problem within the Hamming
metric. SDZKP incorporates a cryptographically secure pseudorandom
number generator to obscure secrets and employs a Stern-type algorithm
to ensure strong security features.

## Articles

-   Cansu Betin Onur, \`\`Intractable Group-theoretic Problems Around
    Zero-knowledge Proofs,'' [arXiv:2206.13350
    \[cs.CR\]](https://arxiv.org/abs/2206.13350)
    [@onur2023intractablegrouptheoreticproblemszeroknowledge]
-   Cansu Betin Onur, \`\`A Zero-Knowledge Proof of Knowledge for
    Subgroup Distance Problem,'' [arXiv:2408.00395
    \[cs.CR\]](https://arxiv.org/abs/2408.00395)
    [@onur2024zeroknowledgeproofknowledgesubgroup]

## Acknowledgement

This work is partially supported by the NLnet foundation under the MoU
number 2021-12-510.

# Installation

We present the details for installing SDZKP using pypi package or using
the source code.

## Installation (Package)

Create a project folder, in that folder preferably create a virtual
environment:

`python3 -m venv venv`

`source venv/bin/activate`

### Prerequisites

SDZKP is an interactive zero-knowledge protocols and we use gRPC.

`pip install grpcio`

`pip install protobuf`

You can easily install the required packages by
`pip install -r requirements.txt`.

### SDZKP package

Install the latest SDZKP package

`pip install sdzkp`

You can then copy sdzkp_verifier.py and sdzkp_prover.py from
[GitHub](https://github.com/cansubetin/sdzkp) and run them in two
terminals (do not forget to `source venv/bin/activate` in both
terminals).

## Installation (from source)

To install sdzkp from source, checkout the latest version from
[GitHub](https://github.com/cansubetin/sdzkp) by

    git clone https://github.com/cansubetin/sdzkp
    cd sdzkp
    pip install -e .

If you change the gRPC proto definitions, `sdzkp/api/sdzkp.proto` then
under root project folder, run

    pip install grpcio-tools
    ./compile_api.sh


In this document, we present the abstract model of zero-knowledge proof (ZKP) schemes, the security requirements, design choices, performance metrics, adversary model and threat analysis that will be used to evaluate the ZKP proposal that we develop in this project.

# Abstract Model

In a ZKP scheme, the statements (claims) are formally represented as a relation $R$ between instances denoted as $x$ and witnesses represented as $w$. $R$ defines the acceptable $(x,w)$ pairs; i.e., $R$ consists of the pairs $(x,w)$. Then, the language $L$ defines $x$ that have an associated $w \in R$; i.e., $L=\{  x | \ (x,w)\in R \text{ for some } w   \}$. Here, $L$ is the set of instances induced by $R.$ An instance is a commonly known input in an interactive proof scheme and a witness is a private information known by the prover. A membership claim can then be defined in the form of $x \in L$ and a knowledge claim can be defined in the statement form of "Considering $R$, I know the witness $w$ associated with the instance $x$.\" In both types, the statements can be represented as software pieces or Boolean/Arithmetic circuits consisting of input nodes, output nodes and computation gates. The literature considers mostly the depth of the circuit $d$, or circuit size $C$ (i.e., the number of gates in the circuit) or the size of the input given to the circuit $n=|x|$ where $x \in L.$

A zero-knowledge proof facilitates proving that a statement is true while preserving some secret (and privacy-sensitive) information. The claims about privacy-sensitive data can be defined as statements. For instance, the claim, 'I am older than 18 years old\" is a **statement** that is to be proven. An identity card (e.g., TCKK) is an **instance** of this statement. The birth date and personal information of the person signed by the government is the **witness** of this instance. A general claim (statement) is substantiated by the instance. The association between the instance and the secret information (or private information such as the actual age in this example) is called the witness. Claim (statement) and sometimes the instances are known to both of the principals (parties taking part in a protocol).

Zero knowledge proof schemes are seen in two types. A proof to assure that a statement is true or a proof of knowledge of an hidden information. The principals in a ZKP scheme are the prover (Alice or $P$) and the verifier (Bob or $V$) as shown in Figure [1](#fig:zkparch){reference-type="ref" reference="fig:zkparch"}
that depicts the overall architecture of a ZKP scheme. In an abstract ZKP scheme as shown in Figure [1](#fig:zkparch){reference-type="ref"
reference="fig:zkparch"}, the prover generates a proof of the statement and send it to the verifier. This step is called as the commit ($a$, witness) phase. Subsequently, the verifier challenges the prover by posing some questions such as sending a binary sequence back to the prover; this phase is called as the challenge ($c$) phase. The prover prepares adequate response to the challenge and send it to the verifier (response, $z$ phase). Finally the verifier accepts or rejects the claim without being able to reveal any confidential information.

A $\Sigma$-protocol shown in Figure [1](#fig:zkparch){reference-type="ref" reference="fig:zkparch"} is a three move (commit $a$, challenge $c$, response $z$) special honest verifier zero knowledge proof protocol which has special soundness [@damgaard2002sigma]. Security requirements completeness, soundness and zero-knowledge properties are given in Section [2](#sec:securityreq){reference-type="ref" reference="sec:securityreq"} with their variants. A $\Sigma$-protocol can be converted to a non-interactive mode by employing the Fiat-Shamir transformation [@fiat1986prove]. To employ this transformation, the prover runs the first step and produces the commitment $a$. Then, instead of expecting a challenge from the verifier, the prover computes a (random) challenge by using a random oracle that accepts $a$ and the statement circuit ($x$) as input. Using this challenge, the prover produces the response in step 3.

![The general architecture of a ZKP protocol. This scheme is called as
the $\Sigma$-protocol in
literature [@damgaard2002sigma].](figures/zkparch.png){#fig:zkparch
width="\\linewidth"}

Let us give a mathematical example initially presented by Tompa and Woll[@tompa1987zero; @tompa1987random]. The set of integers between $1$ and $n$ that are relatively prime with $n$ is denoted by $Z_n^*.$ A number $a \in  Z_n^*$ is said to be a quadratic residue mod $n$ if there exits $x \in  Z_n^*$ such that $a=x^2.$ Say $n=q_1q_2$ for distinct primes $q_1$ and $q_2.$ If the factorization of $n$ is not known, then the problem whether $a$ is a quadratic residue modulo $n$ is known to be computationally hard. Alice wants to prove that she knows an element $c \in  Z_n^*$ such that $a=c^2.$ Then, the steps of the ZKP scheme are:


Step 1 (commit phase): Alice (prover, $P$) chooses a random element $k \in  Z_n^*$ and computes $K=k^2$ mod $n.$ She sends $K$ to Bob (verifier, $V$).

Step 2 (challenge phase): Bob chooses $b \in    \{0,1 \}$ uniform randomly and sends it to Alice.

Step 3 (response phase): Alice computes $C=c^bk$ and sends it to Bob.

Step 4 (verification): Bob verifies $C^2=a^bK$ mod $n.$


This protocol should be repeated sufficiently many times. If it is applied only once, Alice can cheat Bob with probability at most $\frac{1}{2} .$ If it is repeated $m$ times, then this probability is reduced to $\frac{1}{2^m} .$

# Security Requirements {#sec:securityreq}


An interactive proof scheme (IP) is a two-party protocol between a prover and a verifier (turing machines) that must meet the conditions of completeness and soundness. Completeness property means that if the statement is true, the prover can convince the verifier. Soundness property means, if the statement is false, a dishonest prover cannot mislead the verifier, except with negligable probability. {cite:p}``

In a formal interactive proof system, the prover (P) has infinite computational power, while the verifier (V) operates within polynomial time. The system satisfies:

Completeness: The probability that the verifier accepts a true statement is high.
Soundness: The probability that the verifier accepts a false statement is low.
These probabilities are determined by the verifier’s coin tosses. Repeating the protocol can reduce error probability.

Some IP protocols may require an initial trusted setup phase, potentially involving a trusted third party (TTP) or secure multi-computing, using a common reference string (CRS) known to both parties.

A zero-knowledge proof (ZKP) is an IP where the verifier learns nothing beyond the truth of the statement. If the prover convinces the verifier with just one message, the proof is non-interactive. Non-interactive ZKPs (NIZKP) can be achieved through a CRS or the Fiat–Shamir heuristic.

The zero-knowledge property is modeled using a simulator, ensuring the verifier gains no additional information, making the simulator’s output indistinguishable from the verifier’s.

























Informally, an interactive proof scheme (IP) is a two party protocol between a prover and a verifier such that the requirements **completeness** and **soundness** are satisfied. Completeness is whenever the statement is TRUE, a prover can convince the verifier. Soundness means whenever the statement is FALSE, a dishonest prover cannot convince the verifier. More formally, an *interactive proof system* [^goldwasser1989knowledge]  for a language $L$ over $\{0,1 \}^*$ is a protocol between an interactive pair of Turing machines $(P,V)$ where $P ,$ called the prover, has infinite power and $V ,$ called the verifier, has polynomial time computation power. An interactive proof system should satisfy the properties:

-   Completeness: $Pr[V(x)=Accept \ | \ x\in L ] \geq 1-\frac{1}{n^k}$

-   Soundness: $Pr[V(x)=Accept \ | \ x\notin L ] \leq \frac{1}{n^k}$

where the probabilities are taken over fair coin tosses; $n=|x|$ is the sufficiently large input length and $k$ is a positive constant. The proof system $(P, V )$ is named **public coin**, a.k.a **Arthur-Merlin game**, if $V$ sends each coin tosses. General approach in an IP is reducing the probability error by repeating the protocol many times. 

Some protocols may require an initial phase called trusted setup. The setup phase can be executed by a trusted third party (TTP) or by employing a secure multi-computing technique in a distributed fashion. Apart from the (instance, witness) pair, some private/common inputs can be assigned to the participants of the protocol, e.g., by a trusted third party (TTP). A common component known by both parties is generally called by common reference string (CRS).

A zero knowledge proof system is an interactive protocol reinforced with the **zero knowledge property**; the verifier will not learn anything from the proof procedure other than the fact that the statement is true. If in a proof system the prover convinces the verifier by sending only a single message, then this system is said to be **non-interactive**. By its very nature, originally defined ZKP is a highly repetitive interactive protocol. On the other hand via a CRS or a random oracle model one may achieve (computational) non-interactive zero-knowledge (NIZKP). A common method to achive a NIZKP is transform an interactive protocol to non-interactive by Fiat--Shamir heuristic.

The zero knowledge property, the verifier will not gain any extra information from the interaction, is formulated by means of a simulator (a probabilistic polynomial-time algorithm). The simulation paradigm [@oded2001foundations] postulates that "whatever a party can do by itself cannot be considered a gain from interaction with the outside.\" The simulator's output and the verifier's output are expected to be indistinguishable.

Formally, let $(P,V)$ be an interactive proof system and $x$ be an input. All messages between $P$ and $V$ during the execution of the protocol on $x$ is called the view of $V$ on $x$ and denoted by $View_V[ P(x) \leftrightarrow V(x)].$ A proof system $(P,V)$ is said to be zero knowledge proof if, for every efficient (PPT) verifier $V^*$, there exists an efficient simulator $S_{V^*}$ such that for every true statement $x,$ $View_{V^*}[ P(x) \leftrightarrow V^*(x)]=S_{V^*}(x).$ In this definition, verifier may not follow the specified protocol and he can cheat. If we restrict ourselves to honest verifier, than the protocol is called **honest verifier zero knowledge proof**.

For practical purposes, the definition of zero knowledge is relaxed by allowing the simulator to fail. Mainly there are three variants of zero knowledge property. **Perfect zero knowledge** means no information is leaked. The two distributions are identical as given in the definition. **Statistical zero knowledge** means some information is leaked to the verifier but it is a negligible amount regardless of the computational resources the verifier. The two distributions are not identical but have negligible statistical distance Lastly, a zero knowledge is said to be **computational** if the amount of information leaked is negligible for
a probabilistic polynomial-time verifier. That is; a polynomial time Turing machine can not distinguish samples from the two distributions.

To sum up, in perfect and statistical (a.k.a., almost-perfect) zero knowledge, it is not possible to notice the difference in outputs of the verifier and the simulator in information-theoretic sense. On the other
hand, in computational zero-knowledge although this distinction can be done theoretically, it is not possible by any computationally efficient procedure. A zero-knowledge protocol without any of these adjectives is used for the most general class computational zero-knowledge.

Relaxation can be done also on the soundness condition. Recall that a protocol is sound if the statement $x$ is false, a cheating prover $P^*$ can not convince $V$. For a computationally unbounded $P^*,$ **perfect soundness** is referred to no success of $P^*$ while **statistical soundness** is referred $P^*$ to has negligible probability of cheating the verifier. If $P^*$ is PPT and has negligible probability of success in cheating the verifier then the protocol is said to have **computational soundness.**

Zero knowledge systems with computational soundness also called as **arguments** by Brassard, Chaum and Crepeau [@brassard1988minimum]. In summary, zero-knowledge proofs satisfies the soundness requirements
under the assumption of computationally unbounded provers whereas the zero-knowledge arguments satisfies this requirement under the assumption of computationally-bounded provers. Although there is a distinction between zero-knowledge proofs and arguments, we use the term proof in this project for simplifying the presentation.

Special Soundness: A three round (commit, challenge, response) protocol for a relation $R$ is said to have special soundness if there exists an efficient extractor $A$ which computes a $w$ satisfying $(x,w)\in R$ for
any $x$ and any pair of transcripts $(a,c,z),(a,c',z')$ with $c\not=c'.$

Special honest verifier zero knowledge property: A three round (commit, challenge, response) protocol for a relation $R$ is said to have special honest verifier zero knowledge property if there exists an efficient simulator $S$ which outputs an accepting transcript $(a,c,z)$ with distribution just like the real transcript for any given any $x$ and $c.$

All in all, the ZKP implementations can be compared based on the
following design choices [@zkproof2022]:

1.  Types of supported statements: a ZKP of knowledge or a ZKP of membership.

2.  Whether or not a trusted setup is required: When existing ZKP protocols are analyzed, the following possibilities for the trusted setup phase emerge:

    1.  No setup: In this case, the ZKP scheme does not require any trusted setup phase; e.g., a copy of the security parameter is the only information required for initializing the ZKP scheme. For instance, bulletproof does not require any setup phase.

    2.  Uniform random string (public coin): If the messages produced by the verifier are uniform random strings, and if those messages are independent of the prover's messages, then we say that the setup phase employs public coins. All parties have access to an output of a uniform random number generator.

    3.  Common reference string (CRS): When the setup phase employs a publicly known information called as CRS known to everybody. This is the generalization of the public coins. In CRS, the information does not have to be uniform random.

    4.  Designated verifier setup: When the CSR is known only to a designated verifier, the setup phase is called as designated verifier setup. In this approach, the setup algorithm executed by the prover is correlated with the setup algorithm executed by the verifier; and this requires a trust to the setup phase.

    5.  Random oracle model: The setup phase defines a common cryptographically secure hash function that acts as a random oracle to produce nonces (numbers used once and never repeated) that are never used in the past invocations of the algorithm.

3.  Interactive or not.

4.  Assumptions about the underlying intractable problem: Most of the works in the literature using group theoretic approach allocates DLP.

# Metrics for Comparing ZKP Schemes

The efficiency of ZKP implementations can be compared based on the following performance metrics [@zkproof2022]. Here, we list the most-commonly used metrics.

1.  Proof size (succinctness): the size of the proof in comparison to the circuit size ($C$) representing the statement.

    1.  Fully succinct: $\mathcal{O}(1)$

    2.  Polylog succinct: e.g., $\mathcal{O}(\log^2 C)$

    3.  Sqare root succinct: $\mathcal{O}(\sqrt{C})$

    4.  Depth-succinct: e.g., $\mathcal{O}(d \log C)$ assuming that the
        depth of the verification circuit is $d.$

    5.  Non-succinct: the proof is not sublinear in $C$.

2.  The time complexity for the trusted setup (if exists)

3.  The time complexity of the tasks executed by the prover $P:$ efficiency of the proof generation

4.  The time complexity of the tasks executed by the verifier $V$: efficiency of the proof verification

In addition to these metrics, round complexity, parallelizability, batching, memory consumption, number of operations in the algorithms, memory consumption, disk and storage requirements can be considered as additional performance metrics for comparing various ZKP proposals [@zkproof2022].

Zero-Knowledge Succinct Non-Interactive ARgument of Knowledge (zk-SNARK) is a non-interactive ZKP protocol initially proposed by Bitansky et al. in 2011. They showed that if there exist extractable collision-resistant hash functions (ECRHs) and an appropriate private information retrieval scheme, then there exist SNARKs for NP. Also in this work, they propose candidates for ECRH constructions. One of these is based on the hardness of discrete logarithm problem and the two others are based on hard problems on lattices namely, knapsack (subset-sum) problems. In 2016, Groth constructed an efficient zk-SNARK for Quadratic Arithmetic Programs where he used bilinear groups. Zcash uses Groth's construction. A downside of zk-SNARK is it uses non-public randomness in its setup phase. In other words, zk-SNARK requires a trusted setup. Also, it is not quantum-safe. A remedy to these problem is zk-STARK.

Scalable Transparent Zero-knowledge Argument of Knowledge (zk-STARK) introduced by Ben-Sasson et al. in 2018. It is an Interactive Oracle Proofs (IOP) system. zk-STARK is more transparent, i.e., it needs no trusted set-up. zk-STARKS rely on collision-resistant hash functions. The zk-STARK-friendly hash function [@ben2020stark; @canteaut2020report] is the focus of extensive research campaign. Relying on hash functions,
it is quantum resistant. A major disadvantage of zk-STARKS is the proof size compared to zk-SNARKS. There are some recent works that try to reduce the proof length.

Zk-SNARK's algorithmic complexity for prover $\mathcal{O}(C\log(C))$ and verifier $\mathcal{O}(1)$ are lower compared to zk-STARK's complexity that is $\mathcal{O}(C \text{polylog}(C))$ and $\mathcal{O}(\text{polylog}(C))$, respectively. The proof size of zk-SNARK is $\mathcal{O}(1)$ whereas it is $\mathcal{O}(\text{polylog}(C))$ for zk-STARK.

Aurora [@ben2019aurora] is a Zk-SNARK proposed by Ben-Sasson et al. in 2019. They developed the protocol for Rank-1 Constraint Satisfaction (R1CS) which is an NP-complete language. Aurora employs a public (transparent) setup phase. It is lightweight and quantum-safe. For the same number of constraints defined in R1CS, they accomplished reducing the proof size to 20 times shorter than the previous Zk-SNARK proposals. Aurora uses an interactive oracle proof for solving univariate version of the sumcheck problem [@lund1992algebraic].

Hyrax [@wahby2018doubly] is another Zk-SNARK variant proposed by Wahby et al. in 2017. They convert an interactive proof of arithmetic circuit (AC) satisfiability to a ZKP scheme. Hyrax's proofs are sublinear in
circuit size (succinct), does not require a trusted setup phase, secure under the discrete log assumption.

Ligero is a zero knowledge argument based on a chosen collision-resistant hash function. By making it non-interactive in the random oracle model, an efficient zk-SNARKs can be obtained that do not require a trusted setup or public-key encryption.

Bulletproof is a short zero-knowledge proof depending on the hardness of discrete logarithm problem and has no trusted setup. It uses Pedersen vector commitment and has very short the proof size by groundbreaking
method inner product algorithm. It can be non-interactive using Fiat-Shamir heuristic. One disadvantage of Bulletproof is, it takes more time to verify a bulletproof than to verify a SNARK proof.

Libra [@cryptoeprint:2019/317] is zero-knowledge proof scheme that has both optimal prover time with a succinct proof size and $\mathcal{O}(d \log C)$ verification time. Different from the other proposals, Libra employs a one-time setup phase that does not have to be repeated per statement. It relies on the GKR protocol
[@goldwasser2015delegating].

# Adversary Model and Threat Analysis

An adversary is a (malicious) attacker carrying out an attack on the protocol and an adversary model is the formal definition of the attacker in a security protocol. Depending on the level of formalization, it may
be a set of statements about the capabilities (skill sets, advantages, assumptions, and also limitations) of the attacker and its goal. An adversary model can be an algorithm having some computation power. Adversary models are generally used to prove the security of the protocol. A widely used model is the Dolev-Yao model
[@dolev1983security]. In the Dolev--Yao model, the adversary can listen to communication between the principals and can send data/messages to principals. It may act as a man in the middle.

An adversary model usually defines

1.  the assumptions about the attacker

    1.  assumptions about the environment: whether the adversary is an insider or outsider. Connectivity of the adversary to the protocol infrastructure can also be evaluated here.

    2.  intellectual resources: the intellectual resources of the adversary based on competence and knowledgeability.

    3.  capabilities: the privileges of the adversary and whether or not it is active

    4.  computational resources; e.g., number of CPUs, memory, etc.

    5.  amount of accessible data

2.  the goal(s) of the adversary.

While designing a zero knowledge protocol, the main security concerns are whether or not completeness, soundness and zero knowledge properties are satisfied. However, when zero-knowledge proofs are employed in
applications such as identification or authentication, additional attacks can be implemented by an adversary. Below we briefly define the attack vectors and the associated adversary models are presented in
Table [1](#tab:adversary){reference-type="ref"mreference="tab:adversary"}
[@major2020authentication; @walshe2019non; @grassi2021poseidon; @pathak2021secure; @Dwork2004; @UMAR2021102374].

1.  Impersonation attacks (masquerading as prover)

2.  Mutual impersonation: person-in-the-middle attack

3.  Replay attacks

    1.  General replay attacks (resending previously captured messages)

    2.  Interleaving attack (a selective combination of information from previous protocol executions is used to attack the protocol)

    3.  Reflection attack (some messages are replayed back to the sender)

    4.  Delay attack (some messages are delayed by an active adversary)

4.  Integrity attack (some messages are intelligently modified by an active adversary)

5.  Brute force attack (all possible combinations to solve the intractable problem are tried)

6.  Quantum attack (whether or not the protocol is quantum-safe?)

7.  Redundancy information attack (a passive adversary listens to all messages on the channel and tries to derive useful information)

8.  Timing attack (a passive adversary has access to system clocks and can measure how much time it takes for algorithms to run.)
    [@Dwork2004]

::: {#tab:adversary}
  -------------------------------------------------------------------------------------------
  **Attack**       **Goal(s)**      **Location**   **Passive   **Resources**   **Accessible
                                                   Active**                    data**
  ---------------- ---------------- -------------- ----------- --------------- --------------
  Impersonate as   Break soundness, Insider        Active      Bounded         Some $(x,w)$
  prover           cheat verifier   outsider                                   pairs

  Mutual           Break            Insider        Active      Bounded         Public data
  impersonation    completeness and outsider                                   
  (person in the   soundness                                                   
  middle)                                                                      

  Replay attacks                    Insider        Active      Bounded         Public data
  (interleaving,                    outsider                                   
  reflection,                                                                  
  delay)                                                                       

  Integrity attack Modify messages  Insider        Active      Bounded         Public data
                   to break                                                    and previously
                   soundness                                                   captured
                                                                               messages

  Brtute force     Break            Outsider       Passive     Bounded         Public data
  attack           zero-knowledge                              Unbounded       

  Quantum attacks  Break            Outsider       Passive     Quantum         Messages on
                   zero-knowledge                              computer        channel

  Redundancy       Break            Outsider       Passive     Unbounded       Messages on
  information      zero-knowledge                                              channel
  attack           by eavesdropping                                            
                   messages or by                                              
                   analyzing public                                            
                   data                                                        

  Timing attacks   Reveal secret    Insider        Passive     Bounded         System clocks
                   information                                                 
  -------------------------------------------------------------------------------------------

  : Potential attacks and the adversary model.
:::

# Conclusion

This report presents a comprehensive analysis of Zero-Knowledge Proof (ZKP) schemes, focusing on their abstract models, security requirements, design choices, and performance metrics. The study highlights the
fundamental principles of ZKP, distinguishing between proofs of membership and proofs of knowledge. It also delves into the essential security properties of completeness, soundness, and zero-knowledge, outlining their formal definitions and practical implications.

Moreover, the report categorizes ZKP schemes based on their need for a trusted setup, interaction patterns, and underlying cryptographic assumptions. Notable ZKP implementations such as zk-SNARKs and zk-STARKs are compared in terms of proof size, computational complexity, and security features. The analysis extends to newer protocols like Aurora and Bulletproof, discussing their unique advantages and limitations.

The adversary model and threat analysis section provides a detailed account of potential attacks and the corresponding adversarial capabilities, emphasizing the importance of robust security measures in ZKP protocols. By understanding these aspects, researchers and practitioners can make informed decisions about the most suitable ZKP schemes for their specific applications, ensuring both efficiency and security in cryptographic implementations.


[^goldwasser1989knowledge]: S. Goldwasser, .... ``The knowledge ...'' 
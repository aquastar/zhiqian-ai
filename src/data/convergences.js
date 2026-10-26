// Built 2026-10-26. Cases: each paper checked against Crossref (title, venue, DOI,
// citation count); ranked by citations per year since publication. Topics: each
// joins named papers from three or more fields. See convergences.astro.
export const convergences = {
 "built": "2026-10-26",
 "cases": [
  {
   "id": "esteva",
   "idea": "Transfer learning",
   "src": "Computer vision",
   "dst": "Dermatology",
   "fa": "ai",
   "fb": "biomed",
   "home": "A network trained on 1.28 million everyday photos (ImageNet) to tell dogs from cats, cars from boats.",
   "how": "The authors took Google's Inception v3, already trained on ImageNet, replaced its last layer, and retrained it on 129,450 clinical photos of skin covering 2,032 diseases. They then tested it against 21 board-certified dermatologists on biopsy-proven images: carcinoma versus benign growths, and melanoma versus moles.",
   "map": [
    [
     "edges and textures that separate a dog from a cat",
     "the borders and colour patterns that separate a melanoma from a mole"
    ]
   ],
   "result": "The network matched the dermatologists on both tasks, and showed that a model trained on ordinary photos can be repurposed for medicine with a modest labelled set.",
   "paper": {
    "authors": "Esteva et al.",
    "year": 2017,
    "title": "Dermatologist-level classification of skin cancer with deep neural networks",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/nature21056",
    "cites": 12857
   },
   "perYear": 1429
  },
  {
   "id": "smallworld",
   "idea": "Small-world networks (\"six degrees of separation\")",
   "src": "Sociology",
   "dst": "Neuroscience, power grids",
   "fa": "netsci",
   "fb": "neuro",
   "home": "Milgram's 1960s letter-passing experiments suggested any two Americans are linked by about six acquaintances, but nobody had a model of why.",
   "how": "Watts and Strogatz started from a ring where each node links only to its neighbours, then rewired each link to a random node with a small probability. A handful of random shortcuts made paths short while neighbourhoods stayed tightly knit. They then measured three real networks with the same two numbers: the 282-neuron nervous system of the worm C. elegans, the 4,941-node power grid of the western United States, and film actors who appeared together.",
   "map": [
    [
     "acquaintances",
     "synapses between neurons, transmission lines between substations"
    ],
    [
     "a friend of a friend",
     "a short path through the network"
    ]
   ],
   "result": "All three were small worlds. The paper founded network science and is the reason brain connectomes are now described as small-world networks.",
   "paper": {
    "authors": "Watts & Strogatz",
    "year": 1998,
    "title": "Collective dynamics of 'small-world' networks",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/30918",
    "cites": 34987
   },
   "perYear": 1250
  },
  {
   "id": "annealing",
   "idea": "Annealing",
   "src": "Metallurgy and statistical physics",
   "dst": "Chip design",
   "fa": "physics",
   "fb": "eda",
   "home": "Metalworkers cool hot metal slowly so its atoms settle into a strong, low-energy crystal; physicists simulated this with the Metropolis algorithm.",
   "how": "Kirkpatrick, Gelatt and Vecchi, at IBM, treated the cost of a chip layout, total wire length and congestion, as energy. At a high \"temperature\" the algorithm accepts moves that make the layout worse, with a probability that shrinks as the temperature is lowered step by step, so it escapes poor local layouts. They used it to partition and place circuits for IBM computers and on travelling-salesman routes through thousands of cities.",
   "map": [
    [
     "atoms",
     "logic gates on the chip"
    ],
    [
     "energy",
     "wire length and congestion"
    ],
    [
     "slow cooling",
     "gradually refusing worse layouts"
    ]
   ],
   "result": "A general-purpose optimiser that became a standard method for placing circuits on chips.",
   "paper": {
    "authors": "Kirkpatrick et al.",
    "year": 1983,
    "title": "Optimization by Simulated Annealing",
    "venue": "Science",
    "url": "https://doi.org/10.1126/science.220.4598.671",
    "cites": 35255
   },
   "perYear": 820
  },
  {
   "id": "esm",
   "idea": "Language modelling (fill in the masked word)",
   "src": "Natural language processing",
   "dst": "Protein biology",
   "fa": "ai",
   "fb": "biomed",
   "home": "Models such as BERT learn language by hiding words in sentences and predicting them.",
   "how": "Rives and colleagues treated each of 250 million protein sequences as a sentence and each amino acid as a letter, and trained a transformer to predict hidden amino acids. No structures or functions were given. Afterwards they probed the model's internal representations.",
   "map": [
    [
     "words",
     "amino acids"
    ],
    [
     "grammar",
     "which amino acids can sit next to, or touch, each other in the folded protein"
    ]
   ],
   "result": "The representations encoded secondary structure, which residues touch in 3D, and the effect of mutations. The work led to the ESM family used for protein structure prediction and design.",
   "paper": {
    "authors": "Rives et al.",
    "year": 2021,
    "title": "Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences",
    "venue": "PNAS",
    "url": "https://doi.org/10.1073/pnas.2016239118",
    "cites": 3342
   },
   "perYear": 668
  },
  {
   "id": "graphcast",
   "idea": "Graph neural networks",
   "src": "Machine learning",
   "dst": "Weather forecasting",
   "fa": "ai",
   "fb": "physics",
   "home": "Networks that pass messages along the links of a graph, developed for molecules and physics simulations.",
   "how": "Lam and colleagues covered the Earth with a multi-resolution mesh of triangles, mapped the atmosphere's state on a 0.25° grid onto it, and trained a graph neural network on 39 years of ECMWF reanalysis data to predict the state six hours ahead. Repeating the step gives a 10-day forecast.",
   "map": [
    [
     "nodes and messages",
     "points on the globe exchanging wind, pressure and humidity with neighbours"
    ]
   ],
   "result": "It beat ECMWF's operational forecast on 90% of 1,380 verification targets and produced a 10-day forecast in under a minute on one machine.",
   "paper": {
    "authors": "Lam et al.",
    "year": 2023,
    "title": "Learning skillful medium-range global weather forecasting",
    "venue": "Science",
    "url": "https://doi.org/10.1126/science.adi2336",
    "cites": 1486
   },
   "perYear": 495
  },
  {
   "id": "blackscholes",
   "idea": "The heat equation",
   "src": "Physics",
   "dst": "Finance",
   "fa": "physics",
   "fb": "ts",
   "home": "The equation that describes how heat spreads through a metal bar, solved in the 19th century.",
   "how": "Black and Scholes built a portfolio of a stock and an option on it that is riskless over a short time, and derived the equation the option's price must obey. A change of variables turned it into the heat equation, whose solution was already known, giving a closed-form price from the stock price, strike, time to expiry, interest rate and volatility.",
   "map": [
    [
     "temperature",
     "option price"
    ],
    [
     "heat spreading out",
     "uncertainty about the stock price growing with time"
    ]
   ],
   "result": "The formula became the basis of the options market; Scholes and Merton received the 1997 Nobel prize in economics.",
   "paper": {
    "authors": "Black & Scholes",
    "year": 1973,
    "title": "The Pricing of Options and Corporate Liabilities",
    "venue": "Journal of Political Economy",
    "url": "https://doi.org/10.1086/260062",
    "cites": 20311
   },
   "perYear": 383
  },
  {
   "id": "hopfield",
   "idea": "Spin glasses (disordered magnets)",
   "src": "Physics",
   "dst": "Neural computation",
   "fa": "physics",
   "fb": "neuro",
   "home": "Models of magnets in which atoms point up or down and pull on each other with mixed strengths, settling into stable low-energy states.",
   "how": "Hopfield treated neurons as up or down spins and set the connections between them by Hebb's rule so that chosen patterns became low-energy states. He proved the network has an energy that never increases, so a partial or noisy pattern rolls downhill to the nearest stored memory.",
   "map": [
    [
     "spins",
     "neurons firing or silent"
    ],
    [
     "stable low-energy states",
     "stored memories"
    ],
    [
     "settling",
     "recalling from a partial cue"
    ]
   ],
   "result": "A physical theory of associative memory that helped revive neural networks; Hopfield shared the 2024 Nobel prize in physics.",
   "paper": {
    "authors": "Hopfield",
    "year": 1982,
    "title": "Neural networks and physical systems with emergent collective computational abilities.",
    "venue": "PNAS",
    "url": "https://doi.org/10.1073/pnas.79.8.2554",
    "cites": 15149
   },
   "perYear": 344
  },
  {
   "id": "pagerank",
   "idea": "Citation analysis",
   "src": "Bibliometrics",
   "dst": "Web search",
   "fa": "netsci",
   "fb": "ai",
   "home": "Scientometricians ranked journals by citations, weighting a citation by the importance of the citing journal.",
   "how": "Brin and Page treated hyperlinks as citations. PageRank is the long-run share of time a random surfer spends on each page when following links and sometimes jumping anywhere. They computed it over a crawl of about 24 million pages and combined it with text matching in the Google prototype.",
   "map": [
    [
     "a paper cited by important papers",
     "a page linked from important pages"
    ]
   ],
   "result": "Google. The idea later travelled again: Allesina and Pascual (2009) used PageRank on food webs to find the species whose loss collapses the most others.",
   "paper": {
    "authors": "Brin & Page",
    "year": 1998,
    "title": "The anatomy of a large-scale hypertextual Web search engine",
    "venue": "Computer Networks and ISDN Systems",
    "url": "https://doi.org/10.1016/s0169-7552(98)00110-x",
    "cites": 9343
   },
   "perYear": 334
  },
  {
   "id": "sparsemri",
   "idea": "Compressed sensing",
   "src": "Applied mathematics",
   "dst": "Medical imaging",
   "fa": "amath",
   "fb": "biomed",
   "home": "Theorems from 2006 showing that a signal that is sparse in some basis can be recovered exactly from far fewer measurements than classical sampling requires.",
   "how": "Lustig, Donoho and Pauly noted that MR images are sparse in a wavelet basis and that an MRI scanner measures the image's frequencies one line at a time. They sampled only a random fraction of those lines and reconstructed the image by L1 minimisation, which favours the sparsest image consistent with the data.",
   "map": [
    [
     "a sparse signal",
     "an MR image in wavelet form"
    ],
    [
     "few random measurements",
     "a fraction of the frequency lines, so a shorter scan"
    ]
   ],
   "result": "Several-fold faster scans; compressed-sensing MRI reached commercial scanners cleared by the FDA from 2017.",
   "paper": {
    "authors": "Lustig et al.",
    "year": 2007,
    "title": "Sparse MRI: The application of compressed sensing for rapid MR imaging",
    "venue": "Magnetic Resonance in Medicine",
    "url": "https://doi.org/10.1002/mrm.21391",
    "cites": 6032
   },
   "perYear": 317
  },
  {
   "id": "geman",
   "idea": "Gibbs distributions and annealing",
   "src": "Statistical physics",
   "dst": "Computer vision",
   "fa": "physics",
   "fb": "vis",
   "home": "The Ising model, in which each atom's state depends only on its neighbours, and the Gibbs distribution over all such configurations.",
   "how": "The Gemans modelled an image as a lattice of pixels whose values depend on their neighbours, a Markov random field. Restoring a noisy image became finding the most probable clean configuration. They updated one pixel at a time by drawing from its distribution given its neighbours, the Gibbs sampler, while slowly lowering a temperature.",
   "map": [
    [
     "atoms in a lattice",
     "pixels"
    ],
    [
     "low-energy states",
     "clean, smooth images with sharp edges"
    ]
   ],
   "result": "Image restoration, and the Gibbs sampler, which became a workhorse of Bayesian statistics.",
   "paper": {
    "authors": "Geman & Geman",
    "year": 1984,
    "title": "Stochastic Relaxation, Gibbs Distributions, and the Bayesian Restoration of Images",
    "venue": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "url": "https://doi.org/10.1109/tpami.1984.4767596",
    "cites": 13224
   },
   "perYear": 315
  }
 ],
 "more": [
  {
   "id": "dopamine",
   "idea": "Temporal-difference learning",
   "src": "Computer science",
   "dst": "Neuroscience",
   "text": "Dopamine neurons fire to the difference between expected and received reward, the exact error signal of a reinforcement-learning algorithm.",
   "paper": {
    "authors": "Schultz et al.",
    "year": 1997,
    "title": "A Neural Substrate of Prediction and Reward",
    "venue": "Science",
    "url": "https://doi.org/10.1126/science.275.5306.1593",
    "cites": 8074
   }
  },
  {
   "id": "checklist",
   "idea": "Pre-flight checklists",
   "src": "Aviation",
   "dst": "Surgery",
   "text": "A 19-item checklist used in eight hospitals cut deaths after surgery from 1.5% to 0.8%.",
   "paper": {
    "authors": "Haynes et al.",
    "year": 2009,
    "title": "A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population",
    "venue": "New England Journal of Medicine",
    "url": "https://doi.org/10.1056/NEJMsa0810119",
    "cites": 4646
   }
  },
  {
   "id": "ego",
   "idea": "Kriging",
   "src": "Mining geostatistics",
   "dst": "Engineering design",
   "text": "The method for guessing ore grades between boreholes became efficient global optimisation of expensive simulations, today's Bayesian optimisation.",
   "paper": {
    "authors": "Jones et al.",
    "year": 1998,
    "title": "Efficient Global Optimization of Expensive Black-Box Functions",
    "venue": "Journal of Global Optimization",
    "url": "https://doi.org/10.1023/a:1008306431147",
    "cites": 7251
   }
  },
  {
   "id": "mendelian",
   "idea": "Instrumental variables",
   "src": "Econometrics",
   "dst": "Epidemiology",
   "text": "Genes are handed out at random at conception, so they can stand in for a randomised trial of what they influence (Mendelian randomisation).",
   "paper": {
    "authors": "Davey Smith & Ebrahim",
    "year": 2003,
    "title": "'Mendelian randomization': can genetic epidemiology contribute to understanding environmental determinants of disease?*",
    "venue": "International Journal of Epidemiology",
    "url": "https://doi.org/10.1093/ije/dyg070",
    "cites": 5437
   }
  },
  {
   "id": "matword2vec",
   "idea": "Word embeddings",
   "src": "Natural language processing",
   "dst": "Materials science",
   "text": "Word2vec trained on 3.3 million materials abstracts pointed to thermoelectric materials years before they were reported.",
   "paper": {
    "authors": "Tshitoyan et al.",
    "year": 2019,
    "title": "Unsupervised word embeddings capture latent knowledge from materials science literature",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/s41586-019-1335-8",
    "cites": 1042
   }
  },
  {
   "id": "waddingtonot",
   "idea": "Optimal transport",
   "src": "Mathematics",
   "dst": "Cell biology",
   "text": "The mathematics of moving piles of earth at least cost traced cells across time points in about 315,000 single-cell profiles of reprogramming.",
   "paper": {
    "authors": "Schiebinger et al.",
    "year": 2019,
    "title": "Optimal-Transport Analysis of Single-Cell Gene Expression Identifies Developmental Trajectories in Reprogramming",
    "venue": "Cell",
    "url": "https://doi.org/10.1016/j.cell.2019.01.006",
    "cites": 818
   }
  },
  {
   "id": "kalmanmotor",
   "idea": "The Kalman filter",
   "src": "Control engineering",
   "dst": "Neuroscience",
   "text": "People estimating where their unseen hand is make the errors a Kalman filter combining a movement model with feedback would make.",
   "paper": {
    "authors": "Wolpert et al.",
    "year": 1995,
    "title": "An Internal Model for Sensorimotor Integration",
    "venue": "Science",
    "url": "https://doi.org/10.1126/science.7569931",
    "cites": 2991
   }
  },
  {
   "id": "animalconflict",
   "idea": "Game theory",
   "src": "Economics",
   "dst": "Evolutionary biology",
   "text": "An evolutionarily stable strategy explains why animal fights are mostly ritual displays rather than fights to the death.",
   "paper": {
    "authors": "Maynard Smith & Price",
    "year": 1973,
    "title": "The Logic of Animal Conflict",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/246015a0",
    "cites": 5075
   }
  },
  {
   "id": "banking",
   "idea": "Ecosystem stability",
   "src": "Ecology",
   "dst": "Finance",
   "text": "Models of how food webs collapse were used to analyse how bank failures spread through the network of loans.",
   "paper": {
    "authors": "Haldane & May",
    "year": 2011,
    "title": "Systemic risk in banking ecosystems",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/nature09659",
    "cites": 1164
   }
  },
  {
   "id": "ising",
   "idea": "The Ising model",
   "src": "Physics",
   "dst": "Neuroscience",
   "text": "A model with only pairwise interactions, from magnetism, captured the collective firing patterns of groups of retinal neurons.",
   "paper": {
    "authors": "Schneidman et al.",
    "year": 2006,
    "title": "Weak pairwise correlations imply strongly correlated network states in a neural population",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/nature04701",
    "cites": 1540
   }
  },
  {
   "id": "flu-abm",
   "idea": "Agent-based simulation",
   "src": "Complex systems",
   "dst": "Epidemiology",
   "text": "A simulation of 85 million people in Thailand and its neighbours showed an emerging flu pandemic could be contained with targeted antivirals.",
   "paper": {
    "authors": "Ferguson et al.",
    "year": 2005,
    "title": "Strategies for containing an emerging influenza pandemic in Southeast Asia",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/nature04017",
    "cites": 1497
   }
  },
  {
   "id": "afib",
   "idea": "Patient-specific digital twins",
   "src": "Engineering simulation",
   "dst": "Cardiology",
   "text": "Heart models built from each patient's MRI chose where to ablate for persistent atrial fibrillation, tested in 10 patients.",
   "paper": {
    "authors": "Boyle et al.",
    "year": 2019,
    "title": "Computationally guided personalized targeted ablation of persistent atrial fibrillation",
    "venue": "Nature Biomedical Engineering",
    "url": "https://doi.org/10.1038/s41551-019-0437-9",
    "cites": 301
   }
  },
  {
   "id": "tdgammon",
   "idea": "Temporal-difference learning",
   "src": "Animal-learning theory",
   "dst": "Game playing",
   "text": "A network that learned backgammon from self-play by predicting its own future evaluations reached the level of top human players.",
   "paper": {
    "authors": "Tesauro",
    "year": 1995,
    "title": "Temporal difference learning and TD-Gammon",
    "venue": "Communications of the ACM",
    "url": "https://doi.org/10.1145/203330.203343",
    "cites": 1062
   }
  },
  {
   "id": "indoeuropean",
   "idea": "Bayesian phylogenetics",
   "src": "Evolutionary biology",
   "dst": "Linguistics",
   "text": "Gene-tree software dated the Indo-European family from 87 languages to 7,800 to 9,800 years ago, supporting an origin in Anatolia.",
   "paper": {
    "authors": "Gray & Atkinson",
    "year": 2003,
    "title": "Language-tree divergence times support the Anatolian theory of Indo-European origin",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/nature02029",
    "cites": 553
   }
  },
  {
   "id": "laughlin",
   "idea": "Information theory",
   "src": "Communications engineering",
   "dst": "Neuroscience",
   "text": "A fly's photoreceptor responds to contrast in the way that maximises the information it can carry, given the contrasts found in nature.",
   "paper": {
    "authors": "Laughlin",
    "year": 1981,
    "title": "A Simple Coding Procedure Enhances a Neuron's Information Capacity",
    "venue": "Zeitschrift für Naturforschung C",
    "url": "https://doi.org/10.1515/znc-1981-9-1040",
    "cites": 822
   }
  },
  {
   "id": "rumours",
   "idea": "The epidemic model",
   "src": "Epidemiology",
   "dst": "Social science",
   "text": "Infected, susceptible and recovered became spreaders, ignorants and stiflers in a model of how rumours spread.",
   "paper": {
    "authors": "Daley & Kendall",
    "year": 1964,
    "title": "Epidemics and Rumours",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/2041118a0",
    "cites": 807
   }
  },
  {
   "id": "virus",
   "idea": "Epidemic models",
   "src": "Epidemiology",
   "dst": "Computer security",
   "text": "Disease spread on directed graphs predicted how computer viruses spread and when they die out.",
   "paper": {
    "authors": "Kephart & White",
    "year": 1991,
    "title": "Directed-graph epidemiological models of computer viruses",
    "venue": "IEEE Symposium on Security and Privacy",
    "url": "https://doi.org/10.1109/risp.1991.130801",
    "cites": 427
   }
  },
  {
   "id": "canterbury",
   "idea": "Phylogenetic trees",
   "src": "Evolutionary biology",
   "dst": "Literary studies",
   "text": "Software for building family trees of species reconstructed how 58 manuscripts of a Canterbury Tales prologue were copied from one another.",
   "paper": {
    "authors": "Barbrook et al.",
    "year": 1998,
    "title": "The phylogeny of The Canterbury Tales",
    "venue": "Nature",
    "url": "https://doi.org/10.1038/29667",
    "cites": 99
   }
  },
  {
   "id": "federalist",
   "idea": "Bayesian inference",
   "src": "Statistics",
   "dst": "History",
   "text": "Word frequencies attributed the 12 disputed Federalist Papers to Madison rather than Hamilton.",
   "paper": {
    "authors": "Mosteller & Wallace",
    "year": 1963,
    "title": "Inference in an Authorship Problem",
    "venue": "Journal of the American Statistical Association",
    "url": "https://doi.org/10.2307/2283270",
    "cites": 78
   }
  }
 ],
 "topics": [
  {
   "id": "cyber-health",
   "fields": [
    "security",
    "epi",
    "biomed"
   ],
   "title": "Measure phishing training the way flu vaccines are measured, and rotate malware detectors the way hospitals rotate antibiotics",
   "setting": {
    "field": "security",
    "paper": {
     "authors": "Lain, Kostiainen & Čapkun",
     "year": 2022,
     "title": "Phishing in Organizations: Findings from a Large-Scale and Long-Term Study",
     "venue": "IEEE S&P",
     "url": "https://doi.org/10.1109/sp46214.2022.9833766"
    },
    "text": "A 15-month study at a company of more than 14,000 employees, with simulated phishing and a button to report suspicious email. It could not cleanly say whether training helps."
   },
   "ideas": [
    {
     "field": "epi",
     "paper": {
      "authors": "Jackson & Nelson",
      "year": 2013,
      "title": "The test-negative design for estimating influenza vaccine effectiveness",
      "venue": "Vaccine",
      "url": "https://doi.org/10.1016/j.vaccine.2013.02.053"
     },
     "text": "Flu-vaccine studies take only people who came in with symptoms and were tested, then compare how many of those who tested positive and negative were vaccinated. Because everyone in the study chose to seek care, that bias cancels."
    },
    {
     "field": "biomed",
     "paper": {
      "authors": "Bergstrom, Lo & Lipsitch",
      "year": 2004,
      "title": "Ecological theory suggests that antimicrobial cycling will not reduce antimicrobial resistance in hospitals",
      "venue": "PNAS",
      "url": "https://doi.org/10.1073/pnas.0402298101"
     },
     "text": "A model showing that switching a whole hospital from one antibiotic to the next on a schedule (\"cycling\") slows resistance no better than giving each patient a randomly chosen drug (\"mixing\"), and often worse."
    }
   ],
   "steps": [
    "Take every email the security team investigated because an employee reported it or clicked it: these are the \"tested\" people.",
    "Label real attacks positive and harmless emails negative, and compare the share of trained employees in each group. One minus the odds ratio is the training's effectiveness, read exactly as vaccine effectiveness is.",
    "Separately, simulate an attacker that adapts to whichever detector it meets, and compare rotating one detector at a time with sending each file to a random detector, the cycling-versus-mixing test."
   ],
   "gives": "A training effect measured from data companies already have, and an evidence-based rule for deploying detectors.",
   "status": "Neither idea has been applied to security. Epidemic models of how worms spread are old, but they answer a different question.",
   "marks": [
    8,
    8,
    9,
    8
   ],
   "score": 8.25
  },
  {
   "id": "decoders",
   "fields": [
    "quantum",
    "power",
    "epi",
    "netsci"
   ],
   "title": "Use a quantum error-correction decoder to locate grid faults and reconstruct infection chains",
   "setting": {
    "field": "power",
    "paper": {
     "authors": "Kersting",
     "year": 1991,
     "title": "Radial distribution test feeders",
     "venue": "IEEE Transactions on Power Systems",
     "url": "https://doi.org/10.1109/59.119237"
    },
    "text": "The IEEE test feeders: standard models of local distribution grids, used to compare fault-location methods."
   },
   "ideas": [
    {
     "field": "quantum",
     "paper": {
      "authors": "Higgott",
      "year": 2022,
      "title": "PyMatching: A Python Package for Decoding Quantum Codes with Minimum-Weight Perfect Matching",
      "venue": "ACM Transactions on Quantum Computing",
      "url": "https://doi.org/10.1145/3505637"
     },
     "text": "Open-source software that takes a graph and the list of checks that fired, and returns the most likely set of hidden errors, fast enough for real-time quantum hardware."
    },
    {
     "field": "epi",
     "paper": {
      "authors": "Didelot et al.",
      "year": 2017,
      "title": "Genomic infectious disease epidemiology in partially sampled and ongoing outbreaks",
      "venue": "Molecular Biology and Evolution",
      "url": "https://doi.org/10.1093/molbev/msw275"
     },
     "text": "TransPhylo, the standard tool for inferring who infected whom from pathogen genomes. It is accurate but samples slowly."
    }
   ],
   "steps": [
    "Grid: draw the feeder as a graph, mark each protection relay or fault indicator that tripped as a fired check, weight each line by how likely it is to fail, and run PyMatching. Compare with impedance-based fault location on simulated faults.",
    "Outbreak: put positive cases on the contact graph as fired checks, weight each contact by minus the log probability of transmission, and let the decoder pair cases into likely chains. Compare accuracy and speed with TransPhylo on its own simulated outbreaks.",
    "The research problem: matching pairs up endpoints, while faults can be multiple and infection trees branch, so the decoder must be extended (hypergraph decoders are the candidate)."
   ],
   "gives": "One fast inference engine for any network where you see symptoms and must infer hidden failures.",
   "status": "No paper joins quantum decoders with grids or epidemics (searched in Semantic Scholar, Europe PMC and OpenAlex).",
   "marks": [
    9,
    9,
    8,
    6
   ],
   "score": 8.0
  },
  {
   "id": "sleep-coach",
   "fields": [
    "sleep",
    "control",
    "amath"
   ],
   "title": "Replace the 15-minute rule of insomnia therapy with a predictive controller, and put a safety filter on sleep-deepening sound",
   "setting": {
    "field": "sleep",
    "paper": {
     "authors": "Spielman, Saskin & Thorpy",
     "year": 1987,
     "title": "Treatment of Chronic Insomnia by Restriction of Time in Bed",
     "venue": "Sleep",
     "url": "https://doi.org/10.1093/sleep/10.1.45"
    },
    "text": "The origin of sleep restriction therapy: cut time in bed to the time actually slept, then lengthen it by 15 minutes after a week of efficient sleep. The same rule is still used for everyone."
   },
   "ideas": [
    {
     "field": "amath",
     "paper": {
      "authors": "Borbély",
      "year": 2022,
      "title": "The two-process model of sleep regulation: Beginnings and outlook",
      "venue": "Journal of Sleep Research",
      "url": "https://doi.org/10.1111/jsr.13598"
     },
     "text": "Two equations: sleep pressure that builds while awake and drains during sleep, and a 24-hour body clock that opens and closes the gate to sleep."
    },
    {
     "field": "control",
     "paper": {
      "authors": "Ames et al.",
      "year": 2017,
      "title": "Control Barrier Function Based Quadratic Programs for Safety Critical Systems",
      "venue": "IEEE Transactions on Automatic Control",
      "url": "https://doi.org/10.1109/tac.2016.2638961"
     },
     "text": "A filter that changes a controller's command as little as possible so the system provably stays out of a forbidden region, used in self-driving cars."
    }
   ],
   "steps": [
    "Fit the two-process model to each patient's sleep diary and watch data.",
    "Each week, choose the next bedtime window by model predictive control: simulate candidate windows with the fitted model and pick the one with the best predicted sleep, subject to limits such as at least five hours in bed.",
    "For clicks timed to slow brain waves, which deepen sleep and improve memory (Ngo et al., Neuron 2013), pass each click through the barrier-function filter so predicted arousal never crosses the waking threshold."
   ],
   "gives": "Personal insomnia treatment that adapts weekly, and stimulation as strong as each sleeper tolerates with a stated safety guarantee.",
   "status": "A 2026 preprint models one person's insomnia as a dynamical system, but nobody closes the loop with a controller or a safety filter.",
   "marks": [
    7,
    7,
    9,
    8
   ],
   "score": 7.75
  },
  {
   "id": "leak-survey",
   "fields": [
    "epi",
    "ai",
    "uq"
   ],
   "title": "Estimate how much of a benchmark leaked into a model's training data, corrected the way antibody surveys are",
   "setting": {
    "field": "ai",
    "paper": {
     "authors": "Shi et al.",
     "year": 2024,
     "title": "Detecting Pretraining Data from Large Language Models",
     "venue": "ICLR",
     "url": "https://arxiv.org/abs/2310.16789"
    },
    "text": "Min-K% Prob, a detector that guesses whether a text was in a model's training data, with the WikiMIA benchmark of texts known to be in or out. Like any test, it misses some leaks and flags some clean items."
   },
   "ideas": [
    {
     "field": "epi",
     "paper": {
      "authors": "Rogan & Gladen",
      "year": 1978,
      "title": "Estimating prevalence from the results of a screening test",
      "venue": "American Journal of Epidemiology",
      "url": "https://doi.org/10.1093/oxfordjournals.aje.a112510"
     },
     "text": "The formula for true prevalence from an imperfect test: (share testing positive + specificity − 1) ÷ (sensitivity + specificity − 1)."
    },
    {
     "field": "uq",
     "paper": {
      "authors": "Gelman & Carpenter",
      "year": 2020,
      "title": "Bayesian Analysis of Tests with Unknown Specificity and Sensitivity",
      "venue": "JRSS Series C",
      "url": "https://doi.org/10.1111/rssc.12435"
     },
     "text": "The Bayesian version, written for COVID antibody surveys, that carries the uncertainty in the test's own error rates into the final interval."
    }
   ],
   "steps": [
    "Measure Min-K%'s sensitivity and specificity for the model in question on texts known to be in or out of its training data, as WikiMIA does.",
    "Run the detector on every item of a benchmark and record the share flagged.",
    "Correct that share with Rogan–Gladen and report a Gelman–Carpenter interval: \"an estimated 12% of this benchmark leaked, 95% interval 6–19%.\""
   ],
   "gives": "A leak estimate with honest error bars for every benchmark score, instead of a raw detector count.",
   "status": "A 2026 audit paper notes the Rogan–Gladen link in passing; nobody has carried out the correction with measured error rates.",
   "marks": [
    7,
    7,
    8,
    8
   ],
   "score": 7.5
  },
  {
   "id": "meter",
   "fields": [
    "power",
    "epi",
    "sleep"
   ],
   "title": "Read flu waves and sleep timing from household smart meters, and schedule grid requests around people's sleep",
   "setting": {
    "field": "power",
    "paper": {
     "authors": "Ferrando et al.",
     "year": 2023,
     "title": "Changes in energy use profiles derived from electricity smart meter readings",
     "venue": "Sustainable Cities and Society",
     "url": "https://doi.org/10.1016/j.scs.2023.104876"
    },
    "text": "Smart-meter readings showing how household power use changed when people stayed home during COVID lockdowns."
   },
   "ideas": [
    {
     "field": "sleep",
     "paper": {
      "authors": "Roenneberg, Wirz-Justice & Merrow",
      "year": 2003,
      "title": "Life between Clocks: Daily Temporal Patterns of Human Chronotypes",
      "venue": "Journal of Biological Rhythms",
      "url": "https://doi.org/10.1177/0748730402239679"
     },
     "text": "The Munich ChronoType Questionnaire: a person's chronotype is the midpoint of their sleep on free days, corrected for sleep debt."
    },
    {
     "field": "epi",
     "paper": null,
     "text": "CDC's ILINet: weekly counts of influenza-like illness from outpatient clinics, the benchmark any new flu signal is judged against."
    }
   ],
   "steps": [
    "For each home, find the quietest stretch of night-time load on weekends; its midpoint is an \"electric sleep midpoint\". Check it against the chronotype questionnaire in a small survey.",
    "Aggregate unusual weekday daytime load by postcode and compare it, week by week, with ILINet flu counts to see whether it rises earlier.",
    "Schedule each home's peak-hour requests outside its sleep window and measure whether fewer homes opt out."
   ],
   "gives": "A free early flu signal and grid programmes that fewer households quit.",
   "status": "Floated for flu in a 2016 trade column and never tested; never joined with sleep.",
   "marks": [
    8,
    8,
    6,
    7
   ],
   "score": 7.25
  },
  {
   "id": "ai-power",
   "fields": [
    "ai",
    "opt",
    "ts",
    "power"
   ],
   "title": "Batch AI chatbot requests with paper-mill cutting methods, and forecast the power swings with finance's volatility models",
   "setting": {
    "field": "ai",
    "paper": {
     "authors": "Kwon et al.",
     "year": 2023,
     "title": "Efficient Memory Management for Large Language Model Serving with PagedAttention",
     "venue": "SOSP",
     "url": "https://doi.org/10.1145/3600006.3613165"
    },
    "text": "vLLM stores each conversation's working memory in fixed-size blocks, which almost removed wasted memory. Which requests to run together is still decided by simple first-come rules, and the GPUs' power draw swings with each batch."
   },
   "ideas": [
    {
     "field": "opt",
     "paper": {
      "authors": "Gilmore & Gomory",
      "year": 1961,
      "title": "A Linear Programming Approach to the Cutting-Stock Problem",
      "venue": "Operations Research",
      "url": "https://doi.org/10.1287/opre.9.6.849"
     },
     "text": "Column generation: cut paper rolls into orders of many widths with least waste, handling astronomically many cutting patterns without listing them, and proving how close a plan is to the best."
    },
    {
     "field": "ts",
     "paper": {
      "authors": "Engle",
      "year": 1982,
      "title": "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation",
      "venue": "Econometrica",
      "url": "https://doi.org/10.2307/1912773"
     },
     "text": "ARCH, the model of volatility that comes in clusters, built for inflation and now standard for stock prices."
    }
   ],
   "steps": [
    "Treat each batch as a \"roll\" of GPU memory and each request as an \"order\" of a given length; choose batches by column generation to fill memory with the least idle space.",
    "Record the GPUs' power draw under each batching policy and fit an ARCH-type model to its swings.",
    "Use the volatility forecast to size the battery or grid contract the data centre needs, and compare policies by cost."
   ],
   "gives": "More requests per GPU, smoother power, and smaller batteries for the same AI service.",
   "status": "GPU power swings and serving schedulers are each studied; nobody has used cutting-stock batching or volatility models on them.",
   "marks": [
    7,
    6,
    7,
    8
   ],
   "score": 7.0
  },
  {
   "id": "religion-ai",
   "fields": [
    "religion",
    "psych",
    "ai"
   ],
   "title": "Show AI vision models the moving-triangles film, and a random version, to test the theory that belief in spirits comes from over-detecting agents",
   "setting": {
    "field": "psych",
    "paper": {
     "authors": "Heider & Simmel",
     "year": 1944,
     "title": "An Experimental Study of Apparent Behavior",
     "venue": "American Journal of Psychology",
     "url": "https://doi.org/10.2307/1416950"
    },
    "text": "A short film of two triangles and a circle moving around a box. Almost every viewer describes them as characters with intentions: chasing, bullying, hiding."
   },
   "ideas": [
    {
     "field": "religion",
     "paper": {
      "authors": "Barrett",
      "year": 2000,
      "title": "Exploring the natural foundations of religion",
      "venue": "Trends in Cognitive Sciences",
      "url": "https://doi.org/10.1016/s1364-6613(99)01419-9"
     },
     "text": "The \"hyperactive agency detection\" account: minds evolved to see agents too readily, and belief in unseen agents grows from that."
    },
    {
     "field": "ai",
     "paper": {
      "authors": "Acerbi & Stubbersfield",
      "year": 2023,
      "title": "Large language models show human-like content biases in transmission chain experiments",
      "venue": "PNAS",
      "url": "https://doi.org/10.1073/pnas.2313790120"
     },
     "text": "Evidence that language models reproduce human biases from cognitive-science experiments, so they can serve as test subjects."
    }
   ],
   "steps": [
    "Show vision-language models the original film and versions where the same shapes move at random.",
    "Count words of intention in their descriptions, scored the way human studies score them. Intention seen in random motion is over-detection.",
    "Compare models trained mostly on text with models trained on video: if text-trained models over-detect more, the bias may travel in language rather than in an evolved detector."
   ],
   "gives": "A new test of a central theory in the cognitive science of religion, and a measure of whether AI reads intent into accidents.",
   "status": "Vision-language models have been tested on understanding the film (the TriangleCOPA benchmark, 2024); nobody has tested over-detection in random motion or tied it to the religion theory.",
   "marks": [
    7,
    9,
    6,
    6
   ],
   "score": 7.0
  },
  {
   "id": "microscopy",
   "fields": [
    "biomed",
    "materials",
    "ai"
   ],
   "title": "Segment metal micrographs with an AI model trained on cancer slides",
   "setting": {
    "field": "materials",
    "paper": {
     "authors": "Stuckner et al.",
     "year": 2022,
     "title": "Microstructure segmentation with deep learning encoders pre-trained on a large microscopy dataset",
     "venue": "npj Computational Materials",
     "url": "https://doi.org/10.1038/s41524-022-00878-5"
    },
    "text": "MicroNet: over 100,000 micrographs used to pretrain encoders for segmenting grains and phases, with labelled benchmarks of superalloys and coatings. More pretraining data helped."
   },
   "ideas": [
    {
     "field": "biomed",
     "paper": {
      "authors": "Chen et al.",
      "year": 2024,
      "title": "Towards a general-purpose foundation model for computational pathology",
      "venue": "Nature Medicine",
      "url": "https://doi.org/10.1038/s41591-024-02857-3"
     },
     "text": "UNI, a vision model pretrained on more than 100 million tissue patches from about 100,000 slides."
    }
   ],
   "steps": [
    "Freeze UNI and train only a small segmentation head on MicroNet's labelled benchmarks.",
    "Compare with MicroNet-pretrained and ImageNet-pretrained encoders when only 1, 5 or 20 labelled images are available.",
    "Check which image features carry over (grain boundaries, inclusions) and which mislead."
   ],
   "gives": "A stronger starting model for materials images at almost no cost, and a test of how general pathology models are.",
   "status": "No study applies pathology foundation models to metal micrographs.",
   "marks": [
    8,
    5,
    6,
    6
   ],
   "score": 6.25
  },
  {
   "id": "guarantee",
   "fields": [
    "philosophy",
    "uq",
    "biomed"
   ],
   "title": "When does a 90% conformal guarantee justify a doctor's belief about this patient?",
   "setting": {
    "field": "biomed",
    "paper": {
     "authors": "Lu et al.",
     "year": 2022,
     "title": "Fair Conformal Predictors for Applications in Medical Imaging",
     "venue": "AAAI",
     "url": "https://doi.org/10.1609/aaai.v36i11.21459"
    },
    "text": "Conformal predictors for medical images that met their coverage guarantee overall but covered some patient groups less well than others."
   },
   "ideas": [
    {
     "field": "uq",
     "paper": {
      "authors": "Angelopoulos & Bates",
      "year": 2023,
      "title": "Conformal Prediction: A Gentle Introduction",
      "venue": "Foundations and Trends in Machine Learning",
      "url": "https://doi.org/10.1561/2200000101"
     },
     "text": "The guarantee: the prediction set contains the truth for 90% of patients on average, not for 90% of every kind of patient."
    },
    {
     "field": "philosophy",
     "paper": {
      "authors": "Conee & Feldman",
      "year": 2004,
      "title": "The Generality Problem for Reliabilism",
      "venue": "Evidentialism (Oxford)",
      "url": "https://doi.org/10.1093/0199253722.003.0007"
     },
     "text": "Reliabilism says a belief is justified if it comes from a reliable process; the generality problem is that a process is reliable or not depending on how broadly you describe it."
    }
   ],
   "steps": [
    "Lay out Lu et al.'s result as a case: the same tool is reliable described as \"this tool\" and unreliable described as \"this tool on this group\".",
    "Argue which description fixes justification for a clinician, and what that demands of the guarantee: overall, per group, or per patient.",
    "Turn the answer into a reporting rule for clinical AI and check it on the paper's datasets."
   ],
   "gives": "A principled answer to what such guarantees let a clinician conclude, and a rule for how they should be reported.",
   "status": "No paper joins conformal guarantees with theories of justification.",
   "marks": [
    8,
    6,
    5,
    6
   ],
   "score": 6.25
  },
  {
   "id": "learning-limit",
   "fields": [
    "psych",
    "ai",
    "theory"
   ],
   "title": "Put babies, small language models and the optimal learner on the same two-minute speech stream",
   "setting": {
    "field": "psych",
    "paper": {
     "authors": "Saffran, Aslin & Newport",
     "year": 1996,
     "title": "Statistical Learning by 8-Month-Old Infants",
     "venue": "Science",
     "url": "https://doi.org/10.1126/science.274.5294.1926"
    },
    "text": "After two minutes of a continuous stream of made-up syllables, 8-month-olds told its \"words\" from other syllable sequences, using only how often syllables follow each other."
   },
   "ideas": [
    {
     "field": "theory",
     "paper": {
      "authors": "Goldwater, Griffiths & Johnson",
      "year": 2009,
      "title": "A Bayesian framework for word segmentation: Exploring the effects of context",
      "venue": "Cognition",
      "url": "https://doi.org/10.1016/j.cognition.2009.03.008"
     },
     "text": "An ideal Bayesian learner for finding words in unsegmented speech, which sets the best that can be done with the input alone."
    },
    {
     "field": "ai",
     "paper": {
      "authors": "Warstadt et al.",
      "year": 2023,
      "title": "Findings of the BabyLM Challenge: Sample-Efficient Pretraining on Developmentally Plausible Corpora",
      "venue": "CoNLL BabyLM",
      "url": "https://doi.org/10.18653/v1/2023.conll-babylm.1"
     },
     "text": "A shared task training language models on child-sized amounts of text, to measure how data-hungry they are."
    }
   ],
   "steps": [
    "Recreate Saffran's stream and find how many exposures the ideal learner needs to reach the infants' level of discrimination.",
    "Train BabyLM-style models on the same stream and count the exposures they need.",
    "Place the three on one scale: infants near the ideal learner means efficient use of the input; infants beyond it means built-in knowledge."
   ],
   "gives": "A number for how far AI is from human learning efficiency, and how much infants bring with them.",
   "status": "Older models have been run on Saffran-style streams, but not modern small language models alongside the ideal learner and the infant data.",
   "marks": [
    5,
    7,
    7,
    6
   ],
   "score": 6.25
  }
 ]
};

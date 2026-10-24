// Generated from the convergences screen and hand verification, 2026-10-24.
// See src/pages/conferences/convergences.astro for how it is shown.
export const convergences = {
 "built": "2026-10-24",
 "screenedOpen": 77,
 "verified": 48,
 "top": [
  {
   "rank": 1,
   "id": "tnd-phish",
   "fa": "epi",
   "fb": "security",
   "title": "Test-negative design for measuring security-awareness training",
   "gap": "Estimate how much phishing training cuts compromise using the test-negative design that vaccine-effectiveness studies use, with reported-suspicious emails as the 'tested' population.",
   "bridge": "Both problems estimate how well a protection works from people who come forward, not from a random sample. The test-negative design compares positives and negatives among those who sought a test, which cancels out who chooses to seek one. Reported emails carry the same bias, so the design carries over almost unchanged.",
   "nearest": [
    {
     "t": "Are You at Risk? Profiling Organizations and Individuals Subject to Targeted Attacks (Thonnard et al.)",
     "u": "https://library.cyentia.com/report/report_002219.html",
     "note": "Case-control epidemiology for targeted attack risk factors; not test-negative, not training effect."
    },
    {
     "t": "Understanding the Efficacy of Phishing Training in Practice (2025)",
     "u": "https://www.csail-live-2025.csail.mit.edu/node/14000",
     "note": "Large field RCT of training efficacy; randomized, not test-negative design."
    }
   ],
   "verdict": "OPEN",
   "joint": 1,
   "qa": "test-negative design",
   "qb": "phishing",
   "score": 8.5,
   "parts": {
    "gap": 9,
    "distance": 8,
    "depth": 9,
    "payoff": 8
   }
  },
  {
   "rank": 2,
   "id": "qec-fault",
   "fa": "quantum",
   "fb": "power",
   "title": "Syndrome decoding for fault location from sparse grid alarms",
   "gap": "Locate distribution-grid faults from sparse relay and PMU alarms with the graph decoders used in quantum error correction.",
   "bridge": "A fault trips a pattern of protection alarms, and the task is to infer the most likely set of faults that explains it. That is the syndrome decoding problem on a graph. Matching and union-find decoders solve it in near-linear time with known optimality conditions.",
   "nearest": [
    {
     "t": "Sparse Blossom: correcting a million errors per core second with minimum-weight matching (2023)",
     "u": "https://arxiv.org/abs/2303.15933",
     "note": "QEC matching decoder side only; no grid application."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "syndrome decoding",
   "qb": "fault location",
   "score": 8.0,
   "parts": {
    "gap": 9,
    "distance": 8,
    "depth": 8,
    "payoff": 7
   }
  },
  {
   "rank": 3,
   "id": "cbf-sleep",
   "fa": "control",
   "fb": "sleep",
   "title": "Control barrier functions for closed-loop acoustic sleep stimulation",
   "gap": "Keep closed-loop auditory stimulation of slow oscillations inside a no-arousal safe set with a control barrier function, rather than fixed volume rules.",
   "bridge": "Closed-loop stimulation already reads the EEG in real time, and its failure mode is a hard constraint: waking the sleeper. A control barrier function turns 'never cross into arousal' into a filter on every stimulus, which is what CBFs do for robots near obstacles.",
   "nearest": [
    {
     "t": "Driving Sleep Slow Oscillations by Auditory Closed-Loop Stimulation - A Self-Limiting Process (2015)",
     "u": "https://research.uni-luebeck.de/en/publications/driving-sleep-slow-oscillations-by-auditory-closed-loop-stimulati/",
     "note": "CLAS with intrinsic self-limiting dynamics; no formal safety controller."
    },
    {
     "t": "Closed-loop auditory stimulation of sleep slow oscillations: Basic principles and best practices (2023)",
     "u": "https://pubmed.ncbi.nlm.nih.gov/37660843/",
     "note": "CLAS review; fixed rule-based volume/timing, no barrier functions."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "control barrier function",
   "qb": "slow oscillation",
   "score": 8.0,
   "parts": {
    "gap": 9,
    "distance": 7,
    "depth": 8,
    "payoff": 8
   }
  },
  {
   "rank": 4,
   "id": "qec-contact",
   "fa": "quantum",
   "fb": "epi",
   "title": "Surface-code decoders for inferring hidden infection chains",
   "gap": "Read positive tests as syndromes and infection chains as error strings, and use minimum-weight perfect matching decoders to reconstruct unobserved transmission.",
   "bridge": "A surface-code decoder sees only the endpoints of error chains and infers the chains between them. Testing sees only positive cases and must infer the hidden transmission that links them. Minimum-weight matching on a contact graph is a direct, fast counterpart to the slow Bayesian tree samplers in use now.",
   "nearest": [
    {
     "t": "Experimentally Informed Decoding of Stabilizer Codes Based on Syndrome Correlations (2025)",
     "u": "https://arxiv.org/abs/2502.17722",
     "note": "Explains MWPM over syndrome defects; quantum side only, no epidemiology."
    },
    {
     "t": "Novel Decoding Algorithm for Noiseless Non-Adaptive Group Testing (2026)",
     "u": "https://arxiv.org/abs/2601.07388",
     "note": "Closest epidemiology-side decoding: infers positives from pooled tests, not transmission chains or matching."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "minimum weight perfect matching",
   "qb": "contact tracing",
   "score": 7.75,
   "parts": {
    "gap": 9,
    "distance": 9,
    "depth": 7,
    "payoff": 6
   }
  },
  {
   "rank": 5,
   "id": "mpc-cbti",
   "fa": "control",
   "fb": "sleep",
   "title": "Model predictive control of sleep-restriction therapy",
   "gap": "Titrate the time-in-bed window in CBT-I with MPC over a two-process sleep model fitted to each patient's diary, instead of the fixed 15-minute rule.",
   "bridge": "Sleep-restriction therapy is already a feedback loop: diary in, time-in-bed window out, adjusted weekly by a fixed rule. MPC replaces the rule with a model-based optimiser that respects constraints, for example a minimum of five hours in bed, and personalises the pace.",
   "nearest": [
    {
     "t": "SYSTEM AND METHOD FOR PERSONALIZATION OF SLEEP RESTRICTION THERAPY (patent application US20220110582)",
     "u": "https://patents.justia.com/patent/20220110582",
     "note": "Derives personalized target in-bed duration from sleep data; no MPC or two-process model described."
    },
    {
     "t": "Optimization of light exposure and sleep schedule for circadian rhythm entrainment (2021)",
     "u": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8186815/",
     "note": "Optimal control of sleep schedule over two-process model, for jet lag not insomnia."
    }
   ],
   "verdict": "OPEN",
   "joint": 14,
   "qa": "model predictive control",
   "qb": "insomnia",
   "score": 7.75,
   "parts": {
    "gap": 8,
    "distance": 7,
    "depth": 8,
    "payoff": 8
   }
  },
  {
   "rank": 6,
   "id": "serosurvey-contam",
   "fa": "epi",
   "fb": "ai",
   "title": "Serosurvey statistics for benchmark contamination prevalence",
   "gap": "A 2026 audit paper notes in passing that Rogan-Gladen correction is the population version of its estimator, but no study measures detector sensitivity and specificity and reports corrected contamination prevalence with intervals, as serosurveys do.",
   "bridge": "Contamination detectors misfire in both directions, just as antibody assays do. Serosurveys solved exactly this: correct raw positive rates for known sensitivity and specificity, with honest intervals. Benchmark audits currently report raw detector rates.",
   "nearest": [
    {
     "t": "When Is Benchmark Contamination Detectable? Information Limits and Power-Calibrated Audits (2026)",
     "u": "https://arxiv.org/abs/2608.07914",
     "note": "Lower-bound certificate on contaminated fraction; explicitly calls Rogan-Gladen the population version of its ratio."
    },
    {
     "t": "Correcting test set contamination by spiking the training data (2026)",
     "u": "https://arxiv.org/abs/2605.24818",
     "note": "Calibrates MIA/memorization predictors via spiked data to correct inflated scores, not prevalence."
    }
   ],
   "verdict": "PARTIAL",
   "joint": 0,
   "qa": "Rogan-Gladen",
   "qb": "data contamination",
   "score": 7.75,
   "parts": {
    "gap": 6,
    "distance": 8,
    "depth": 9,
    "payoff": 8
   }
  },
  {
   "rank": 7,
   "id": "chrono-dr",
   "fa": "sleep",
   "fb": "power",
   "title": "Chronotype-aware residential demand response",
   "gap": "Schedule demand-response events using household chronotype and sleep timing to cut comfort loss and opt-outs.",
   "bridge": "Demand response asks households to shift load at set hours, and people opt out when those hours clash with their sleep. Chronotype is measurable with short questionnaires or from meter data. Scheduling around it targets the comfort cost that drives opt-outs.",
   "nearest": [
    {
     "t": "Assessing thermal comfort and participation in residential demand flexibility programs (PNNL, 2026)",
     "u": "https://www.pnnl.gov/publications/assessing-thermal-comfort-and-participation-residential-demand-flexibility-programs",
     "note": "Comfort and participation in DR events; no chronotype or sleep timing"
    },
    {
     "t": "Nambiar 2024 residential DR case studies (CBE Berkeley)",
     "u": "https://cbe.berkeley.edu/wp-content/uploads/2024/11/Nambiar-2024-residential-DR-case-studies.pdf",
     "note": "Residential DR comfort/opt-out case studies; no chronotype"
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "chronotype",
   "qb": "demand response",
   "score": 7.5,
   "parts": {
    "gap": 9,
    "distance": 8,
    "depth": 6,
    "payoff": 7
   }
  },
  {
   "rank": 8,
   "id": "smartmeter-flu",
   "fa": "power",
   "fb": "epi",
   "title": "Smart-meter load as an influenza surveillance signal",
   "gap": "A 2016 trade column floated the idea and COVID-era studies tied load to lockdown behaviour, but no study validates household load as an influenza signal against ILINet.",
   "bridge": "Sick people stay home, and homes draw more power on weekdays when they do. Meter data is near-real-time and covers whole communities, unlike clinic visits. It could give influenza surveillance a lead of days.",
   "nearest": [
    {
     "t": "Tracking the Bugs with Smart Meter Data (Public Utilities Fortnightly column, 2016)",
     "u": "https://www.fortnightly.com/node/23571",
     "note": "Opinion column reporting a group claims to track flu spread from real-time electricity use; no study"
    },
    {
     "t": "Electricity consumption reveals proactive community response to COVID-19 progression (NUS, 2021)",
     "u": "https://news.nus.edu.sg/electricity-consumption-proactive-community-response-covid-19-progression/",
     "note": "Household smart-meter load tracks pandemic behaviour, not illness incidence"
    }
   ],
   "verdict": "PARTIAL",
   "joint": 0,
   "qa": "smart meter",
   "qb": "influenza surveillance",
   "score": 7.5,
   "parts": {
    "gap": 7,
    "distance": 8,
    "depth": 7,
    "payoff": 8
   }
  },
  {
   "rank": 9,
   "id": "gsadf-hype",
   "fa": "ts",
   "fb": "netsci",
   "title": "Explosive-root bubble tests for research-hype detection",
   "gap": "Apply the Phillips GSADF bubble test, built for asset prices, to keyword publication counts to date the start and collapse of research fads.",
   "bridge": "The GSADF test detects when a series grows faster than any stable process would, and dates when the episode starts and ends. Publication counts in a hot topic look like asset prices in a bubble. The test would give research hype a formal start date and collapse date.",
   "nearest": [
    {
     "t": "Examining the Relationship between Scientific Publishing Activity and Hype-Driven Financial Bubbles: A Comparison of the Dot-Com and AI Eras (2025)",
     "u": "https://arxiv.org/abs/2509.11982",
     "note": "Links publishing to market bubbles with LSTM/ARX/GARCH, not explosive-root tests on counts."
    },
    {
     "t": "Limited Diffusion of Scientific Knowledge Forecasts Collapse (2023)",
     "u": "https://arxiv.org/pdf/2304.07468",
     "note": "Predicts collapse of scientific bubbles from diffusion, not GSADF."
    }
   ],
   "verdict": "OPEN",
   "joint": 1,
   "qa": "explosive behavior",
   "qb": "research topics",
   "score": 7.25,
   "parts": {
    "gap": 9,
    "distance": 6,
    "depth": 8,
    "payoff": 6
   }
  },
  {
   "rank": 10,
   "id": "sample-infant",
   "fa": "theory",
   "fb": "psych",
   "title": "Sample-complexity bounds as a yardstick for infant statistical learning",
   "gap": "Compare how many exposures infants need to segment words with PAC sample-complexity lower bounds for the same task.",
   "bridge": "Learning theory gives the minimum number of examples any learner needs for a task. Infant studies measure how many exposures babies actually need. Putting the two side by side says whether infants are near-optimal learners or rely on priors the task does not supply.",
   "nearest": [
    {
     "t": "Grammatical inference and first language acquisition (Clark, 2004)",
     "u": "https://sites.socsci.uci.edu/~lpearl/colareadinggroup/readings/Clark2004_GramInference.pdf",
     "note": "Argues PAC variant formalizes language learnability; no infant segmentation data comparison."
    },
    {
     "t": "Testing the limits of statistical learning for word segmentation (Johnson & Tyler, 2010)",
     "u": "https://sites.socsci.uci.edu/~lpearl/courses/readings/JohnsonTyler2010_LimitsStatLearningWordSeg.pdf",
     "note": "Infant segmentation experiment side only; no sample-complexity bound."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "sample complexity",
   "qb": "statistical learning infants",
   "score": 7.25,
   "parts": {
    "gap": 8,
    "distance": 8,
    "depth": 7,
    "payoff": 6
   }
  },
  {
   "rank": 11,
   "id": "amr-malware",
   "fa": "epi",
   "fb": "security",
   "title": "Antimicrobial-resistance evolution models for malware-classifier evasion",
   "gap": "Model how heavy deployment of one detector selects for evasive malware with the selection-pressure and stewardship models used for antimicrobial resistance.",
   "bridge": "Overusing one antibiotic breeds resistance, and overusing one detector breeds evasion. AMR science has quantitative models of selection pressure and of stewardship policies that rotate or restrict drugs. Detector deployment has no such models yet.",
   "nearest": [
    {
     "t": "MalTree: Tracing Malware Evolution from Embeddings at Scale (2026)",
     "u": "https://arxiv.org/pdf/2606.06570",
     "note": "Notes defences exert selective pressure akin to biology; lineage tracing, no AMR model."
    },
    {
     "t": "Measuring the Speed of the Red Queen's Race; Adaption and Evasion in Malware (Sophos talk)",
     "u": "https://ai.sophos.com/presentations/measuring-the-speed-of-the-red-queens-race-adaption-and-evasion-in-malware",
     "note": "Measures malware adaptation rate under detector pressure; no resistance/stewardship modelling."
    }
   ],
   "verdict": "OPEN",
   "joint": 1,
   "qa": "antimicrobial resistance",
   "qb": "malware detection",
   "score": 7.25,
   "parts": {
    "gap": 8,
    "distance": 8,
    "depth": 7,
    "payoff": 6
   }
  },
  {
   "rank": 12,
   "id": "hadd-llm",
   "fa": "religion",
   "fb": "ai",
   "title": "Hyperactive agency detection in language models",
   "gap": "Only an unpublished thesis tests a neighbouring bias (teleology) in LLMs; no study gives LLMs agency-detection vignettes to test intent over-attribution.",
   "bridge": "The cognitive science of religion explains belief in unseen agents by an agency detector tuned to over-fire. LLMs trained on human text are a new kind of subject for that claim: if they over-attribute intent in the same vignettes, the bias may live in language itself.",
   "nearest": [
    {
     "t": "Praca licencjacka [Univ. Warsaw bachelor thesis on teleological bias in Gemini models]",
     "u": "https://repozytorium.uw.edu.pl//entities/publication/9b953ca8-8741-4387-b080-c524e9321dca",
     "note": "Tests whether LLMs reproduce human teleological bias (CSR-adjacent); found mechanistic preference. Not HADD."
    },
    {
     "t": "The Double-Edged Sword of Anthropomorphism in LLMs (Reinecke et al., 2025)",
     "u": "https://www.psych.ox.ac.uk/publications/2093324/modal",
     "note": "Applies HADD to humans anthropomorphizing chatbots; LLMs not subjects."
    }
   ],
   "verdict": "PARTIAL",
   "joint": 2,
   "qa": "agency detection",
   "qb": "large language model",
   "score": 7.25,
   "parts": {
    "gap": 7,
    "distance": 9,
    "depth": 7,
    "payoff": 6
   }
  },
  {
   "rank": 13,
   "id": "farrington-drift",
   "fa": "epi",
   "fb": "ai",
   "title": "Syndromic-surveillance outbreak detectors for model drift",
   "gap": "Deployed models are monitored with CUSUM and thresholds, but nobody has run Farrington or EARS outbreak detectors, built for seasonal weekly counts, on model error counts.",
   "bridge": "Public-health agencies have decades of tested algorithms that flag unusual weekly counts while allowing for seasonality and trend. Error counts from a deployed model are the same kind of data. Today they are monitored with ad-hoc thresholds or CUSUM.",
   "nearest": [
    {
     "t": "Detecting and Monitoring Bias for Subgroups in Breast Cancer Detection AI (2025)",
     "u": "https://arxiv.org/pdf/2502.10562",
     "note": "CUSUM control-chart surveillance of deployed AI performance drift; SPC, not outbreak algorithms."
    },
    {
     "t": "Monitoring Machine Learning Models: Online Detection of Relevant Deviations (2023)",
     "u": "https://arxiv.org/pdf/2309.15187",
     "note": "Sequential CUSUM-style monitoring of deployed ML error; no seasonal count-surveillance methods."
    }
   ],
   "verdict": "PARTIAL",
   "joint": 0,
   "qa": "Farrington algorithm",
   "qb": "concept drift",
   "score": 7.25,
   "parts": {
    "gap": 6,
    "distance": 8,
    "depth": 8,
    "payoff": 7
   }
  },
  {
   "rank": 14,
   "id": "rna-velocity",
   "fa": "neuro",
   "fb": "ai",
   "title": "RNA velocity for predicting neuron fate during model training",
   "gap": "Borrow RNA-velocity estimation from single-cell biology to predict which units of a network are about to specialise or die, from checkpoint pairs.",
   "bridge": "RNA velocity infers where a cell is heading from two snapshots of its state, the spliced and unspliced transcripts. Pairs of nearby checkpoints offer a similar two-state reading for each unit of a network. It could predict which units will specialise or die before it happens.",
   "nearest": [
    {
     "t": "The Early Phase of Neural Network Training (2020)",
     "u": "https://iclr.cc/virtual/2020/poster/1934",
     "note": "Early training weight dynamics carry structure; no per-unit fate prediction via velocity."
    }
   ],
   "verdict": "OPEN",
   "joint": 8,
   "qa": "RNA velocity",
   "qb": "neural network training",
   "score": 7.0,
   "parts": {
    "gap": 9,
    "distance": 7,
    "depth": 6,
    "payoff": 6
   }
  },
  {
   "rank": 15,
   "id": "pathfm-metal",
   "fa": "biomed",
   "fb": "materials",
   "title": "Pathology foundation models for metallographic micrographs",
   "gap": "Transfer whole-slide-image foundation models (UNI, Virchow) to optical and SEM micrographs of alloys for phase and defect segmentation.",
   "bridge": "Pathology foundation models are trained on millions of stained tissue images whose texture statistics, grains, boundaries and inclusions, resemble etched metal micrographs. Materials science has few labelled micrographs, so borrowing a strong visual prior is cheap to test.",
   "nearest": [
    {
     "t": "Machine Learning Models Pre-trained on MicroNet Show Improved Segmentation and Microstructure Quantification (IMAT 2023)",
     "u": "https://asm.confex.com/asm/imat2023/webprogram/Paper59137.html",
     "note": "Materials-micrograph pretrained encoders for segmentation; not pathology foundation models"
    },
    {
     "t": "Addressing materials' microstructure diversity using transfer learning (2021)",
     "u": "https://arxiv.org/abs/2107.13841",
     "note": "Domain adaptation for steel SEM segmentation; no histopathology transfer"
    }
   ],
   "verdict": "OPEN",
   "joint": 3,
   "qa": "pathology foundation model",
   "qb": "microstructure",
   "score": 7.0,
   "parts": {
    "gap": 9,
    "distance": 6,
    "depth": 6,
    "payoff": 7
   }
  },
  {
   "rank": 16,
   "id": "sublinear-sleep",
   "fa": "theory",
   "fb": "sleep",
   "title": "Sublinear-time sampling for overnight EEG screening",
   "gap": "Decide sleep-apnea severity from property-testing style samples of a night without reading the whole record.",
   "bridge": "Property testing decides whether data has a property by reading only a small random sample, with guaranteed error rates. Apnea severity is a threshold on an event rate over a night. A tester could cut scoring time with a stated bound on misclassification.",
   "nearest": [
    {
     "t": "Polysomnography scoring for sleep apnea: use of a sampling method",
     "u": "https://experts.arizona.edu/en/publications/polysomnography-scoring-for-sleep-apnea-use-of-a-sampling-method/",
     "note": "Scores 10-50% of epochs to estimate AHI category; empirical subsampling, no testing theory."
    },
    {
     "t": "Prerau lab AHI uncertainty tools",
     "u": "https://prerau.bwh.harvard.edu/ahi/",
     "note": "Statistical uncertainty of sleep-disordered-breathing metrics; relevant framework, not sublinear sampling."
    }
   ],
   "verdict": "PARTIAL",
   "joint": 0,
   "qa": "property testing",
   "qb": "sleep apnea",
   "score": 7.0,
   "parts": {
    "gap": 7,
    "distance": 8,
    "depth": 7,
    "payoff": 6
   }
  },
  {
   "rank": 17,
   "id": "flatband-net",
   "fa": "physics",
   "fb": "netsci",
   "title": "Flat-band compact localised states in social networks",
   "gap": "Find compact localised eigenstates of network Laplacians, known from flat-band lattices, and test whether they trap information spread.",
   "bridge": "Flat-band lattices host eigenstates confined to a few sites by destructive interference. Some network Laplacians may hold the same compact states. If so, diffusion started there stays trapped, a structural explanation for messages that never spread.",
   "nearest": [
    {
     "t": "Localization Phenomena in Large-Scale Networked Systems: Robustness and Fragility of Dynamics (2024)",
     "u": "https://arxiv.org/abs/2412.00252",
     "note": "Laplacian eigenvector localization in networks and its effect on dynamics; not flat-band CLS."
    },
    {
     "t": "Compact localized states and flatband generators in one dimension (2016)",
     "u": "https://arxiv.org/abs/1610.02970",
     "note": "Flat-band CLS theory for lattices only."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "compact localized states",
   "qb": "social network",
   "score": 6.75,
   "parts": {
    "gap": 9,
    "distance": 6,
    "depth": 7,
    "payoff": 5
   }
  },
  {
   "rank": 18,
   "id": "conformal-reliab",
   "fa": "philosophy",
   "fb": "uq",
   "title": "Reliabilist epistemology of conformal prediction",
   "gap": "Argue whether coverage-guaranteed prediction sets meet process-reliabilist criteria for justified belief, and where they fail.",
   "bridge": "Process reliabilism says a belief is justified if it comes from a reliable process. Conformal prediction is a process with a proven reliability guarantee, but only on average, not for each case. That marginal-versus-conditional gap maps onto reliabilism's generality problem.",
   "nearest": [
    {
     "t": "Beyond Accuracy: Epistemic Justification in Trustworthy Machine Learning (2026, ICML)",
     "u": "https://icml.cc/virtual/2026/77485",
     "note": "Epistemic justification vs accuracy in ML; not conformal prediction or process reliabilism."
    },
    {
     "t": "When is a Prediction Knowledge? (2019)",
     "u": "https://arxiv.org/abs/1904.09024",
     "note": "Gettier-style analysis of ML predictions; no conformal coverage."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "conformal prediction",
   "qb": "reliabilism",
   "score": 6.75,
   "parts": {
    "gap": 8,
    "distance": 8,
    "depth": 6,
    "payoff": 5
   }
  },
  {
   "rank": 19,
   "id": "pinn-sleep",
   "fa": "amath",
   "fb": "sleep",
   "title": "Physics-informed neural networks for the two-process sleep model",
   "gap": "Fit personal circadian and homeostatic parameters from wearable data with a PINN that embeds the Borbely two-process equations.",
   "bridge": "The two-process model is a pair of simple differential equations. Wearables give noisy, gappy sleep-wake and activity data. A physics-informed network fits the personal parameters while honouring the equations, where current fits use least squares on clean diaries.",
   "nearest": [
    {
     "t": "Sleep timing estimation from smartphone context information (Wahl & Amft)",
     "u": "https://www.cdh.med.fau.de/?p=1335",
     "note": "Hybrid data classifiers feeding a two-process expert model; not a PINN, smartphone not wearable."
    },
    {
     "t": "A method for characterizing daily physiology from widely used wearables (2021)",
     "u": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8462795/",
     "note": "Fits personal circadian parameters from wearable heart rate statistically, no PINN or Process S."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "physics-informed neural network",
   "qb": "two-process model",
   "score": 6.75,
   "parts": {
    "gap": 8,
    "distance": 7,
    "depth": 6,
    "payoff": 6
   }
  },
  {
   "rank": 20,
   "id": "colgen-kv",
   "fa": "opt",
   "fb": "eda",
   "title": "Column generation for KV-cache packing in LLM serving",
   "gap": "Formulate KV-cache memory packing across batched requests as a cutting-stock problem solved by column generation.",
   "bridge": "Packing variable-length KV caches into fixed GPU memory blocks is a cutting-stock problem, the classic home of column generation. Column generation handles the huge number of packing patterns implicitly and gives a lower bound on waste to compare heuristics against.",
   "nearest": [
    {
     "t": "Online Scheduling for LLM Inference with KV Cache Constraints (2025)",
     "u": "https://arxiv.org/abs/2502.07115v4",
     "note": "Integer program for batching under KV memory constraints; benchmark only, no column generation."
    },
    {
     "t": "Robust KV Cache Management for LLM Serving (2026)",
     "u": "https://www.alphaxiv.org/abs/2607.16892.md",
     "note": "Mixed-integer DRO KV reservation solved by block coordinate descent, not cutting stock."
    }
   ],
   "verdict": "OPEN",
   "joint": 0,
   "qa": "column generation",
   "qb": "KV cache",
   "score": 6.75,
   "parts": {
    "gap": 8,
    "distance": 4,
    "depth": 8,
    "payoff": 7
   }
  }
 ],
 "pool": [
  {
   "id": "tnd-phish",
   "fa": "epi",
   "fb": "security",
   "title": "Test-negative design for measuring security-awareness training",
   "joint": 1,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "serosurvey-contam",
   "fa": "epi",
   "fb": "ai",
   "title": "Serosurvey statistics for benchmark contamination prevalence",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "farrington-drift",
   "fa": "epi",
   "fb": "ai",
   "title": "Syndromic-surveillance outbreak detectors for model drift",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "amr-malware",
   "fa": "epi",
   "fb": "security",
   "title": "Antimicrobial-resistance evolution models for malware-classifier evasion",
   "joint": 1,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "smartmeter-flu",
   "fa": "power",
   "fb": "epi",
   "title": "Smart-meter load as an influenza surveillance signal",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "qec-contact",
   "fa": "quantum",
   "fb": "epi",
   "title": "Surface-code decoders for inferring hidden infection chains",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "qec-fault",
   "fa": "quantum",
   "fb": "power",
   "title": "Syndrome decoding for fault location from sparse grid alarms",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "cbf-sleep",
   "fa": "control",
   "fb": "sleep",
   "title": "Control barrier functions for closed-loop acoustic sleep stimulation",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "mpc-cbti",
   "fa": "control",
   "fb": "sleep",
   "title": "Model predictive control of sleep-restriction therapy",
   "joint": 14,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "string-agents",
   "fa": "complex",
   "fb": "ai",
   "title": "String stability of LLM agent pipelines",
   "joint": 1,
   "outcome": "open",
   "note": "partly done: Error growth along LLM agent chains is measured and some system-theoretic stability analysis exists, but nobody applies the platoon string-stability criterion or designs gains to bound it."
  },
  {
   "id": "cascade-agents",
   "fa": "power",
   "fb": "ai",
   "title": "Power-grid cascade models for failure propagation in multi-agent LLM systems",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Failure cascades in multi-agent LLM systems are actively modeled (contagion, topology, hubs), but nobody imports OPA or load-redistribution overload cascade models from grid reliability."
  },
  {
   "id": "csd-spikes",
   "fa": "dynsys",
   "fb": "ai",
   "title": "Critical slowing down as an early warning for LLM loss spikes",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Loss-spike early warning exists (TIC, mechanism-driven monitors) and CSD early warnings exist for training phase transitions, but no study tests classic rising-variance/lag-1 autocorrelation indicators before LLM pretraining loss spikes."
  },
  {
   "id": "csd-grok",
   "fa": "dynsys",
   "fb": "ai",
   "title": "Tipping-point indicators before grokking",
   "joint": 2,
   "outcome": "done",
   "note": "CSD framing and CSD-based early warnings for grokking exist, plus other precursors (commutator defect, oscillations); a direct test of classic variance/autocorrelation indicators of a saddle-node transition before grokking is not clearly done."
  },
  {
   "id": "hopf-repeat",
   "fa": "dynsys",
   "fb": "ai",
   "title": "Hopf bifurcation account of repetition loops in LLM decoding",
   "joint": 1,
   "outcome": "open",
   "note": "partly done: Attractor/critical-temperature accounts of LLM repetition exist, but no work models decoding loops as limit cycles born at a Hopf bifurcation in temperature or penalty parameters."
  },
  {
   "id": "multistab-persona",
   "fa": "dynsys",
   "fb": "ai",
   "title": "Multistability and hysteresis in LLM persona switching",
   "joint": 4,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "kuramoto-debate",
   "fa": "dynsys",
   "fb": "ai",
   "title": "Kuramoto synchronisation model of multi-agent LLM debate",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Kuramoto framing of agents and physics models of debate consensus both exist; fitting coupled-oscillator models to actual debate answer trajectories to predict lock-in vs split is not found."
  },
  {
   "id": "rna-velocity",
   "fa": "neuro",
   "fb": "ai",
   "title": "RNA velocity for predicting neuron fate during model training",
   "joint": 8,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "pseudotime-ckpt",
   "fa": "neuro",
   "fb": "ai",
   "title": "Pseudotime trajectory inference across training checkpoints",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Feature-lineage tracking across checkpoints exists, but nobody uses single-cell pseudotime/trajectory tools (Monocle, PAGA) to order neurons or features."
  },
  {
   "id": "microglia-prune",
   "fa": "neuro",
   "fb": "ai",
   "title": "Microglial complement-tagging rules as a pruning algorithm",
   "joint": 29,
   "outcome": "dropped",
   "note": "29 papers already join the two"
  },
  {
   "id": "hadd-llm",
   "fa": "religion",
   "fb": "ai",
   "title": "Hyperactive agency detection in language models",
   "joint": 2,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "csr-transmission",
   "fa": "religion",
   "fb": "ai",
   "title": "Minimally counterintuitive concepts in LLM transmission chains",
   "joint": 0,
   "outcome": "done",
   "note": "Acerbi and Stubbersfield already tested counterintuitive-content bias in LLM transmission chains; only extensions remain (MCI vs maximally-counterintuitive curve, newer models, LLM-to-LLM chains)."
  },
  {
   "id": "pathfm-metal",
   "fa": "biomed",
   "fb": "materials",
   "title": "Pathology foundation models for metallographic micrographs",
   "joint": 3,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "xvector-nilm",
   "fa": "audio",
   "fb": "power",
   "title": "Speaker-verification embeddings for appliance and inverter identification",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Verification-style embedding/enrollment for appliances exists via Siamese networks, but no work transfers x-vector/ECAPA-TDNN speaker-verification recipes to current waveforms or to identifying individual inverters."
  },
  {
   "id": "wav2vec-ae",
   "fa": "audio",
   "fb": "materials",
   "title": "Self-supervised speech models for acoustic-emission crack monitoring",
   "joint": 1,
   "outcome": "open",
   "note": "partly done: Self-supervised and contrastive AE methods exist, but large-scale wav2vec-style pretraining on raw unlabeled AE streams with crack-growth fine-tuning was not found."
  },
  {
   "id": "gsadf-hype",
   "fa": "ts",
   "fb": "netsci",
   "title": "Explosive-root bubble tests for research-hype detection",
   "joint": 1,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "sample-infant",
   "fa": "theory",
   "fb": "psych",
   "title": "Sample-complexity bounds as a yardstick for infant statistical learning",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "query-search",
   "fa": "theory",
   "fb": "psych",
   "title": "Query-complexity lower bounds for human visual search",
   "joint": 1,
   "outcome": "open",
   "note": "partly done: Human fixation counts are routinely benchmarked against Bayesian ideal-searcher and information-gain models, but not against formal query-complexity (noisy 20-questions) lower bounds per display."
  },
  {
   "id": "colgen-kv",
   "fa": "opt",
   "fb": "eda",
   "title": "Column generation for KV-cache packing in LLM serving",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "bnb-reason",
   "fa": "opt",
   "fb": "ai",
   "title": "Branch-and-bound with LLM-generated bounds for reasoning search",
   "joint": 1,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "pod-kv",
   "fa": "amath",
   "fb": "ai",
   "title": "Proper orthogonal decomposition with DEIM for KV-cache compression",
   "joint": 19,
   "outcome": "dropped",
   "note": "19 papers already join the two"
  },
  {
   "id": "amr-context",
   "fa": "amath",
   "fb": "ai",
   "title": "Adaptive mesh refinement for long-context token budgets",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Error-bound-driven coarse-to-fine refinement of long-context attention exists (CEDAR), so what remains is a genuine AMR formulation with a posteriori estimators, nested refinement levels and conservation-style guarantees."
  },
  {
   "id": "ch-opinion",
   "fa": "amath",
   "fb": "netsci",
   "title": "Cahn-Hilliard coarsening of opinion domains on social networks",
   "joint": 2,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "pinn-sleep",
   "fa": "amath",
   "fb": "sleep",
   "title": "Physics-informed neural networks for the two-process sleep model",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "flatband-net",
   "fa": "physics",
   "fb": "netsci",
   "title": "Flat-band compact localised states in social networks",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "berry-train",
   "fa": "physics",
   "fb": "ai",
   "title": "Berry phase of training trajectories under cyclic learning rates",
   "joint": 3,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "mips-traffic",
   "fa": "physics",
   "fb": "complex",
   "title": "Motility-induced phase separation theory for mixed-autonomy traffic jams",
   "joint": 11,
   "outcome": "dropped",
   "note": "11 papers already join the two"
  },
  {
   "id": "tmr-agent",
   "fa": "eda",
   "fb": "ai",
   "title": "Triple modular redundancy with voters for LLM agent actions",
   "joint": 2,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "dse-connectome",
   "fa": "eda",
   "fb": "neuro",
   "title": "Design-space exploration of connectome wiring trade-offs",
   "joint": 1,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "iss-llmloop",
   "fa": "control",
   "fb": "ai",
   "title": "Input-to-state stability of LLM-in-the-loop controllers",
   "joint": 2,
   "outcome": "open",
   "note": "partly done: The ISS-with-bounded-LLM-error framing is sketched in a survey, but no paper gives actual ISS certificates for an LLM proposing control actions."
  },
  {
   "id": "cbf-dp",
   "fa": "control",
   "fb": "security",
   "title": "Control barrier functions for privacy-budget spending",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Privacy filters already enforce cumulative-loss budgets adaptively; a CBF formulation that adapts noise online to keep loss in a safe set is not published."
  },
  {
   "id": "chrono-dr",
   "fa": "sleep",
   "fb": "power",
   "title": "Chronotype-aware residential demand response",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "sleep-replay-llm",
   "fa": "sleep",
   "fb": "ai",
   "title": "NREM/REM alternation schedules for continual LLM fine-tuning",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Consolidation-plus-dreaming sleep phases for continual LLM learning exist; what is missing is alternating them in human-sleep-cycle ratio/order (multiple cycles, NREM-heavy early, REM-heavy late) and testing that schedule."
  },
  {
   "id": "bo-tes",
   "fa": "uq",
   "fb": "sleep",
   "title": "Bayesian optimisation of closed-loop auditory stimulation parameters",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: BO has been applied to sleep-stimulation detector settings (thesis) and auditory timing in BCIs, but no peer-reviewed work optimizes CLAS volume and phase timing per person across nights for slow-wave enhancement."
  },
  {
   "id": "conformal-reliab",
   "fa": "philosophy",
   "fb": "uq",
   "title": "Reliabilist epistemology of conformal prediction",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "fdr-leader",
   "fa": "uq",
   "fb": "ai",
   "title": "False-discovery-rate control for leaderboard rank claims",
   "joint": 52,
   "outcome": "dropped",
   "note": "52 papers already join the two"
  },
  {
   "id": "rr-fl",
   "fa": "epi",
   "fb": "security",
   "title": "Ring vaccination strategy for patch rollout in federated fleets",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Ring vaccination on networks and epidemic patch-control for malware both exist (plus an 'I-ring' P2P immunization strategy), but no head-to-head neighbour-first vs blanket patch rollout for fleets."
  },
  {
   "id": "r0-promptworm",
   "fa": "epi",
   "fb": "security",
   "title": "Reproduction number of prompt-injection worms among LLM agents",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Simple R0 / branching definitions appear in worm papers and Mind Viruses (2026) studies spread factors, but systematic R0 estimation and herd-immunity thresholds across email/RAG agent networks are not done."
  },
  {
   "id": "tte-copilot",
   "fa": "epi",
   "fb": "ai",
   "title": "Target-trial emulation for AI coding-assistant effects",
   "joint": 3,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "seasonal-bench",
   "fa": "epi",
   "fb": "ai",
   "title": "Nowcasting reporting delays for benchmark result streams",
   "joint": 410,
   "outcome": "dropped",
   "note": "410 papers already join the two"
  },
  {
   "id": "ddm-llm",
   "fa": "psych",
   "fb": "ai",
   "title": "Drift-diffusion modelling of LLM token decisions",
   "joint": 8,
   "outcome": "dropped",
   "note": "8 papers already join the two"
  },
  {
   "id": "metacog-sleep",
   "fa": "psych",
   "fb": "sleep",
   "title": "Metacognitive accuracy after sleep deprivation in human-AI teaming",
   "joint": 7,
   "outcome": "dropped",
   "note": "7 papers already join the two"
  },
  {
   "id": "presence-dream",
   "fa": "vis",
   "fb": "sleep",
   "title": "VR presence measures for lucid-dream realism",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Dreaming is framed theoretically as a presence analogue and lucidity scales rate realism, but no study administers validated VR presence questionnaires or behavioural presence probes to lucid dreamers."
  },
  {
   "id": "3dgs-micro",
   "fa": "vis",
   "fb": "materials",
   "title": "Gaussian splatting for 3D microstructure reconstruction from sparse tomography",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Gaussian splatting for sparse-view X-ray tomography is established (R2-Gaussian, GR-Gaussian, LamiGauss, DenZa-Gaussian for electron tomography); application and evaluation on grain/pore microstructure quantification from few projections is not found."
  },
  {
   "id": "netvis-patristic",
   "fa": "vis",
   "fb": "theology",
   "title": "Visual analytics of patristic citation networks",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Scripture-citation networks exist for single Fathers (Origen), but a multi-Father network mapped onto Christological controversies over time was not found."
  },
  {
   "id": "align-theology",
   "fa": "theology",
   "fb": "ai",
   "title": "Analogia entis as a formal account of LLM analogical reasoning",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "hermeneutic-rag",
   "fa": "theology",
   "fb": "ai",
   "title": "Hermeneutic-circle retrieval for long-document question answering",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "ritual-kuramoto",
   "fa": "religion",
   "fb": "complex",
   "title": "Coupled-oscillator models of synchrony in collective ritual",
   "joint": 14,
   "outcome": "dropped",
   "note": "14 papers already join the two"
  },
  {
   "id": "secular-perc",
   "fa": "religion",
   "fb": "netsci",
   "title": "Complex-contagion models of secularisation on friendship networks",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Simulations and longitudinal peer-influence studies exist, but no empirical test of disaffiliation as threshold complex contagion on longitudinal network surveys was found."
  },
  {
   "id": "costly-fl",
   "fa": "religion",
   "fb": "security",
   "title": "Costly-signalling theory for Sybil resistance in federated learning",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "evo-game-review",
   "fa": "complex",
   "fb": "ai",
   "title": "Evolutionary game model of reviewer effort at AI conferences",
   "joint": 230,
   "outcome": "dropped",
   "note": "230 papers already join the two"
  },
  {
   "id": "percolation-supply",
   "fa": "netsci",
   "fb": "eda",
   "title": "Percolation analysis of the chip-design IP supply network",
   "joint": 1,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "homophily-moe",
   "fa": "netsci",
   "fb": "ai",
   "title": "Homophily measures for expert routing in mixture-of-experts",
   "joint": 5,
   "outcome": "dropped",
   "note": "5 papers already join the two"
  },
  {
   "id": "bipartite-review",
   "fa": "netsci",
   "fb": "ai",
   "title": "Bipartite nestedness of reviewer-paper assignments",
   "joint": 1,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "hoi-lora",
   "fa": "complex",
   "fb": "ai",
   "title": "Higher-order interaction measures for LoRA adapter merging",
   "joint": 2,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "evac-dc",
   "fa": "complex",
   "fb": "power",
   "title": "Crowd-evacuation models for datacenter load shedding",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "traffic-tokens",
   "fa": "complex",
   "fb": "eda",
   "title": "LWR traffic-flow model for on-chip network congestion under LLM inference",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "garch-gpu",
   "fa": "ts",
   "fb": "power",
   "title": "GARCH volatility forecasting of AI-training power swings",
   "joint": 0,
   "outcome": "open",
   "note": "GARCH is used for general electricity load and AI-training power swings are studied for storage sizing, but no work fits GARCH-type volatility models to GPU-cluster power."
  },
  {
   "id": "emh-openreview",
   "fa": "ts",
   "fb": "ai",
   "title": "Market-efficiency tests on OpenReview score revisions",
   "joint": 33,
   "outcome": "dropped",
   "note": "33 papers already join the two"
  },
  {
   "id": "var-bench",
   "fa": "ts",
   "fb": "ai",
   "title": "Value-at-risk for tail failures of LLM deployments",
   "joint": 0,
   "outcome": "done",
   "note": "Nitsure et al. already propose tail-risk (TVaR/expected shortfall) metrics instead of mean scores for choosing LLMs under risk; only the exact per-query accuracy-loss framing for deployment differs."
  },
  {
   "id": "factor-sleep",
   "fa": "ts",
   "fb": "sleep",
   "title": "Dynamic factor models for multi-night wearable sleep data",
   "joint": 8,
   "outcome": "dropped",
   "note": "8 papers already join the two"
  },
  {
   "id": "changepoint-theology",
   "fa": "ts",
   "fb": "theology",
   "title": "Change-point detection in doctrinal vocabulary across councils",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "dro-epi",
   "fa": "opt",
   "fb": "epi",
   "title": "Wasserstein DRO for antiviral stockpile allocation",
   "joint": 9,
   "outcome": "dropped",
   "note": "9 papers already join the two"
  },
  {
   "id": "online-lockdown",
   "fa": "opt",
   "fb": "epi",
   "title": "Competitive-ratio guarantees for intervention timing",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "vrp-cbti",
   "fa": "opt",
   "fb": "sleep",
   "title": "Shift scheduling with circadian-phase constraints from wearables",
   "joint": 1,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "facility-conf",
   "fa": "opt",
   "fb": "netsci",
   "title": "Facility location for carbon-minimal conference siting",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "mlip-ree",
   "fa": "materials",
   "fb": "ai",
   "title": "Interatomic-potential uncertainty methods for LLM hallucination detection",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Ensemble-disagreement and latent-distance hallucination detectors already exist in NLP; an explicit transfer of MLIP machinery (LLPR, calibrated committees, active-learning loops) is not published."
  },
  {
   "id": "hardening-plast",
   "fa": "materials",
   "fb": "ai",
   "title": "Strain-hardening laws for loss of plasticity in continual learning",
   "joint": 14,
   "outcome": "dropped",
   "note": "14 papers already join the two"
  },
  {
   "id": "gb-merge",
   "fa": "materials",
   "fb": "ai",
   "title": "Grain-boundary energy models for model-merging interference",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "phasefield-tumor",
   "fa": "materials",
   "fb": "biomed",
   "title": "Phase-field fracture models for tumour invasion fronts",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Phase-field tumour models with damage and phase-field fracture of soft tissue exist separately, but no work uses a phase-field fracture (crack) formulation for invasion fronts fitted to histology."
  },
  {
   "id": "battery-sleep",
   "fa": "power",
   "fb": "sleep",
   "title": "Battery state-of-health estimators for sleep-pressure tracking",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "inverter-brain",
   "fa": "power",
   "fb": "neuro",
   "title": "Grid-forming inverter control as a model of thalamic pacemaking",
   "joint": 2,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "bilevel-review",
   "fa": "power",
   "fb": "ai",
   "title": "Bilevel optimisation of conference reviewer incentives",
   "joint": 19,
   "outcome": "dropped",
   "note": "19 papers already join the two"
  },
  {
   "id": "qfi-psych",
   "fa": "quantum",
   "fb": "psych",
   "title": "Quantum Fisher information as a bound on perceptual precision",
   "joint": 3,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "qnet-epi",
   "fa": "quantum",
   "fb": "epi",
   "title": "Entanglement-routing algorithms for vaccine cold-chain logistics",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "decoh-llm",
   "fa": "quantum",
   "fb": "ai",
   "title": "Decoherence models for context decay in long LLM conversations",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "treewidth-theo",
   "fa": "theory",
   "fb": "theology",
   "title": "Treewidth of argument graphs in scholastic disputations",
   "joint": 5,
   "outcome": "dropped",
   "note": "5 papers already join the two"
  },
  {
   "id": "proof-justif",
   "fa": "theory",
   "fb": "philosophy",
   "title": "Proof complexity as a measure of epistemic justification cost",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "sublinear-sleep",
   "fa": "theory",
   "fb": "sleep",
   "title": "Sublinear-time sampling for overnight EEG screening",
   "joint": 0,
   "outcome": "top",
   "note": ""
  },
  {
   "id": "hausdorff-dream",
   "fa": "math",
   "fb": "sleep",
   "title": "Fractal dimension of dream-report semantic trajectories",
   "joint": 4,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "cluster-merge",
   "fa": "math",
   "fb": "ai",
   "title": "Cluster-algebra mutation as a model of weight-space symmetry moves",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "ricci-gene",
   "fa": "math",
   "fb": "neuro",
   "title": "Discrete Ricci flow on single-cell similarity graphs for cell-state transitions",
   "joint": 4,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "dg-theology",
   "fa": "amath",
   "fb": "theology",
   "title": "Inverse-problem methods for dating biblical manuscript layers",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "cons-misinfo",
   "fa": "amath",
   "fb": "netsci",
   "title": "Hyperbolic conservation laws for misinformation shock fronts",
   "joint": 2,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "vit-theology",
   "fa": "biomed",
   "fb": "theology",
   "title": "Medical-image segmentation models for palimpsest recovery",
   "joint": 0,
   "outcome": "done",
   "note": "Deep segmentation and U-Net-based (biomedical-origin) networks are already used for palimpsest undertext; only explicit transfer of medical segmentation models/weights (e.g. nnU-Net) on multispectral stacks is unreported, so this is close to done."
  },
  {
   "id": "ehr-religion",
   "fa": "biomed",
   "fb": "religion",
   "title": "Religious-practice signals in EHR for end-of-life care prediction",
   "joint": 56,
   "outcome": "dropped",
   "note": "56 papers already join the two"
  },
  {
   "id": "fl-sleep",
   "fa": "security",
   "fb": "sleep",
   "title": "Federated learning across sleep clinics with polysomnography heterogeneity",
   "joint": 94,
   "outcome": "dropped",
   "note": "94 papers already join the two"
  },
  {
   "id": "sidechannel-sleep",
   "fa": "security",
   "fb": "sleep",
   "title": "Smart-speaker side channels revealing sleep disorders",
   "joint": 11,
   "outcome": "dropped",
   "note": "11 papers already join the two"
  },
  {
   "id": "backdoor-ptsd",
   "fa": "security",
   "fb": "psych",
   "title": "Backdoor-trigger models of intrusive memory",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "dp-census-relig",
   "fa": "security",
   "fb": "religion",
   "title": "Differential privacy impact on religious-minority statistics",
   "joint": 2,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  },
  {
   "id": "cultural-oss",
   "fa": "religion",
   "fb": "ai",
   "title": "Cultural-evolution models of open-weight model lineages",
   "joint": 0,
   "outcome": "open",
   "note": "partly done: Model phylogenies with evolutionary analysis exist (Laufer et al.), but fitting cultural-transmission models (neutral drift, conformity, prestige bias) to their spread is undone."
  },
  {
   "id": "dmn-idle",
   "fa": "neuro",
   "fb": "ai",
   "title": "Default-mode-network analogues in idle LLM agents",
   "joint": 136,
   "outcome": "dropped",
   "note": "136 papers already join the two"
  },
  {
   "id": "gut-brain-graph",
   "fa": "neuro",
   "fb": "netsci",
   "title": "Multilayer network of the gut-brain axis",
   "joint": 10,
   "outcome": "dropped",
   "note": "10 papers already join the two"
  },
  {
   "id": "aging-reservoir",
   "fa": "neuro",
   "fb": "dynsys",
   "title": "Reservoir-computing capacity of the aging connectome",
   "joint": 0,
   "outcome": "dropped",
   "note": "link judged too loose to pursue"
  }
 ],
 "method": [
  "103 pairs were proposed by joining a top topic, method or object of one field with a specific problem in another, drawn from the 27 fields on the conference pages and their most published topics.",
  "Each pair was screened by counting papers whose title or abstract contains both of its key phrases, in Semantic Scholar and Europe PMC.",
  "48 pairs with almost no such papers, and a link that works as a mechanism rather than a metaphor, were checked by hand: two to five web and arXiv searches each, with different wordings, looking for the closest prior work.",
  "Each surviving pair was scored 0 to 10 on four parts: gap (how empty the search came back), distance (how far apart the fields are), depth (a method or mechanism carried across, not 'apply ML to X') and payoff (what it would give either field). The novelty score is their mean.",
  "Being undone is not the same as being new. A pair can be empty because nobody cares; the depth and payoff parts are there to push those down."
 ]
};

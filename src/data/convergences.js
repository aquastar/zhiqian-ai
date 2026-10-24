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
   "title": "Does phishing training work? Measure it the way flu-vaccine studies do",
   "problem": "Companies spend heavily on anti-phishing training but cannot tell whether it helps. Comparing trained with untrained staff misleads, because the people who report suspicious emails are already the careful ones.",
   "idea": "Flu-vaccine studies face the same trap: people who get tested differ from people who do not. Their fix, the test-negative design, compares only people who came in for a test: among those who tested positive and those who tested negative, how many were vaccinated? Do the same with the emails staff report: among reported emails that were real attacks and those that were harmless, how many reporters had been trained?",
   "payoff": "A cheap, routine estimate of how much training cuts successful attacks, from data security teams already collect.",
   "status": "Not done. Studies of phishing training use randomised trials or click rates on fake phishing emails; none uses this design.",
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
   "title": "Find power-grid faults with the error-finding algorithms of quantum computers",
   "problem": "When a line in a local power grid fails, only a few sensors and protection switches raise alarms. Operators must work out from this sparse, sometimes misleading pattern where the fault is, and in large networks that is slow.",
   "idea": "Quantum computers face the same puzzle. Their errors are invisible and only some check points light up, so engineers built decoders that find the most likely errors from those lights, on graphs with millions of nodes, in a fraction of a second.",
   "payoff": "Faster, more reliable fault location from the alarms grids already have, with known conditions under which the answer is the best possible.",
   "status": "Not done. Grid fault location uses state estimation and machine learning; nobody has tried quantum decoders.",
   "nearest": [
    {
     "t": "Sparse Blossom: correcting a million errors per core second with minimum-weight matching (2023)",
     "u": "https://arxiv.org/abs/2303.15933",
     "note": "QEC matching decoder side only; no grid application."
    }
   ],
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
   "title": "Sound pulses that deepen sleep, with a guarantee against waking the sleeper",
   "problem": "Soft clicks timed to the brain's slow waves during deep sleep can strengthen it and improve memory; the technique is being tested in older adults and patients. The main risk is waking the person, and devices handle it with fixed volume rules.",
   "idea": "Robots and self-driving cars use control barrier functions: a mathematical filter that checks every action and blocks any that would push the system into a forbidden zone, such as hitting an obstacle. Here the forbidden zone is waking up, read from the live brain signal.",
   "payoff": "Stimulation as strong as each person tolerates, which may give more benefit, backed by a guarantee instead of a rule of thumb.",
   "status": "Not done. Current systems use fixed or simple adaptive volume rules.",
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
   "title": "Reconstruct hidden chains of infection with quantum error-correction decoders",
   "problem": "In an outbreak, health officials see only the people who test positive. Who infected whom, through which unseen people, stays hidden, and the tools that infer it are accurate but slow.",
   "idea": "Quantum decoders solve a look-alike problem: they see only the two ends of each chain of errors and must infer the chain in between, fast. Positive tests play the visible ends; the contact network plays the chip's layout.",
   "payoff": "Near-instant estimates of likely transmission routes on large contact networks, to decide whom to trace first.",
   "status": "Not done. Transmission-tree inference uses slow Bayesian sampling; nobody has tried quantum decoders.",
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
   "title": "Personalise the bedtime schedule in insomnia therapy with the controller that runs chemical plants",
   "problem": "The most effective insomnia treatment first limits time in bed, then extends it by a fixed 15 minutes a week if sleep improves. Everyone gets the same schedule, so some patients progress too slowly and others give up.",
   "idea": "Model predictive control, used in chemical plants and building climate systems, looks a few steps ahead with a model of the system and picks the best next move within set limits. The model here is the standard one of sleep pressure and body clock, fitted to each patient's sleep diary; a limit is, for example, at least five hours in bed.",
   "payoff": "A schedule tuned to each patient's response, which could shorten treatment and cut dropouts.",
   "status": "Not done. A patent and a few studies personalise the schedule with rules, not with a predictive controller.",
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
   "title": "Estimate how many AI test questions leaked into training data, the way antibody surveys do",
   "problem": "An AI benchmark means something only if the model never saw the test questions in training. The tools that detect such leaks err in both directions, so reported leak rates are biased and come without honest error bars.",
   "idea": "Antibody surveys have the same issue: blood tests miss some past infections and flag some people who were never infected. Epidemiologists correct the raw positive rate with the test's known error rates, using a standard formula, and report a confidence interval.",
   "payoff": "Corrected, comparable leak estimates for each benchmark, so readers know how far a score can be trusted.",
   "status": "One 2026 paper mentions the formula in passing; nobody has measured the detectors' error rates and applied the correction.",
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
   "title": "Ask night owls and early birds differently when the grid needs people to use less power",
   "problem": "Utilities pay households to use less power at peak hours. Many households opt out because the requested hours clash with their routine, especially their sleep.",
   "idea": "Sleep science measures chronotype, whether someone is a morning or an evening person, with a short questionnaire, and it may also show in meter data. Schedule each household's requests around its chronotype.",
   "payoff": "Fewer opt-outs and less discomfort for the same relief to the grid.",
   "status": "Not done. Studies look at comfort and daily routines in general, not at chronotype.",
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
   "title": "Spot flu waves early from household electricity use",
   "problem": "Flu surveillance relies on doctor visits and lab tests, which lag the real spread by one to two weeks.",
   "idea": "Sick people stay home on weekdays, so daytime electricity use rises. Smart meters record this every 15 minutes for whole towns.",
   "payoff": "A free, near-real-time signal that could warn of flu waves days before clinics do.",
   "status": "Floated in a 2016 trade column and linked to COVID lockdowns, but never checked against official flu data.",
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
   "title": "Date the rise and burst of research hype with the test economists use for stock bubbles",
   "problem": "Research topics go in and out of fashion, but hype is called by gut feeling, usually after the fact.",
   "idea": "Economists have a statistical test (GSADF) that tells when a price grows faster than any normal process would, and dates when the bubble began and when it burst. Apply it to the yearly number of papers on a topic.",
   "payoff": "An objective, early flag for overheated topics, useful to funders, editors and young researchers choosing a direction.",
   "status": "Not done. The test has been applied to AI stocks, not to publication counts.",
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
   "title": "Are babies near-perfect learners? Compare them with the theoretical minimum",
   "problem": "Psychologists measure how many repetitions infants need to pick words out of a stream of speech, but have no yardstick for whether that number is impressive.",
   "idea": "Learning theory in computer science proves the minimum number of examples any learner, human or machine, needs for a given task. Work out that minimum for the same word-finding tasks used in infant experiments.",
   "payoff": "If babies come close to the minimum, they learn near-optimally; if they need fewer examples than it allows, they must bring built-in knowledge. That puts numbers on a long nature-versus-nurture argument.",
   "status": "Not done.",
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
   "title": "Manage malware detectors the way hospitals manage antibiotics",
   "problem": "When one malware detector is used everywhere, attackers learn to slip past it and it loses power over time. Security teams have no model of how fast this happens or how to slow it.",
   "idea": "Overusing an antibiotic breeds resistant bacteria in the same way. Medicine has numerical models of how fast resistance grows with use, and of stewardship policies, such as rotating or restricting drugs, that slow it.",
   "payoff": "A way to plan how detectors are deployed so they stay effective for longer.",
   "status": "The analogy is made informally; nobody has fitted resistance models to malware data.",
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
   "title": "Do AI language models see intention where there is none, as people do?",
   "problem": "A leading theory of why people believe in unseen spirits says our minds over-detect agents: we hear a rustle and assume someone is there. It is hard to test, because every person's upbringing and culture are mixed in.",
   "idea": "Give large language models the standard story-based tests psychologists use for this bias. The models learned only from human text, with no body and no survival instinct.",
   "payoff": "If models show the same bias, the bias may travel in language itself rather than in evolved instinct, a new test of a major theory. AI builders also learn whether their models read intent into accidents.",
   "status": "Only an unpublished thesis tests a related bias; this test has not been run.",
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
   "title": "Watch AI models in use with the alarm systems built for disease outbreaks",
   "problem": "AI models in use slowly get worse as the world changes. Companies watch error counts with simple thresholds, which either raise false alarms over normal weekly and seasonal ups and downs or react late.",
   "idea": "Public-health agencies have algorithms, tested for decades, that flag unusual weekly case counts while allowing for seasons and trends. A model's error counts are the same kind of data.",
   "payoff": "Fewer false alarms and earlier real ones, using methods agencies already trust.",
   "status": "Monitoring uses simpler tools; nobody has applied these outbreak detectors.",
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
   "title": "Predict which parts of a neural network will specialise or go dead during training, with a tool from cell biology",
   "problem": "During training, some units of a network become specialised and others go dead. Usually we see this only afterwards.",
   "idea": "Biologists can tell what a cell is turning into from a single snapshot, by comparing its newly made and its mature RNA (RNA velocity). Two nearby training checkpoints give the same kind of before-and-after reading for each unit.",
   "payoff": "Early warning of dead units and a map of how features form, useful for cheaper training and for understanding models.",
   "status": "Not done.",
   "nearest": [
    {
     "t": "The Early Phase of Neural Network Training (2020)",
     "u": "https://iclr.cc/virtual/2020/poster/1934",
     "note": "Early training weight dynamics carry structure; no per-unit fate prediction via velocity."
    }
   ],
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
   "title": "Reuse AI models trained on cancer slides to analyse metal under the microscope",
   "problem": "Engineers judge metal quality from microscope images of grains, boundaries and defects, but labelled images are scarce, so AI tools for them are weak.",
   "idea": "Very large AI models have been trained on millions of stained tissue slides, and tissue and etched metal look surprisingly alike under a microscope: grains, boundaries, inclusions.",
   "payoff": "A strong starting model for materials images, and almost free to try.",
   "status": "Not done. Materials AI starts from everyday photos or its own small datasets.",
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
   "title": "Diagnose sleep apnea from a sample of the night, with a guaranteed error rate",
   "problem": "Diagnosing sleep apnea needs a technician to score a whole night of recordings. It takes hours and causes long waiting lists.",
   "idea": "A branch of computer science, property testing, decides whether data has a property by reading only a small random sample, with a proven bound on the chance of being wrong.",
   "payoff": "Faster screening with a stated error guarantee, rather than a hope that the sample is typical.",
   "status": "Scoring only part of the night has been tried, but without any guarantee.",
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
   "title": "Find the spots in a social network where information gets trapped, with a trick from physics",
   "problem": "Some messages never spread beyond a small group, even in a well-connected network. This is usually blamed on the content or on people's interests.",
   "idea": "In certain crystal lattices physicists found waves trapped on a handful of sites, because they cancel out everywhere else. The same mathematics may apply to the shape of a social network.",
   "payoff": "An explanation for stuck information that comes from the network's structure, not its content, and a way to find those spots in advance.",
   "status": "Not done.",
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
   "title": "When does an AI prediction with a guarantee count as justified belief?",
   "problem": "A popular AI method, conformal prediction, promises that its answers are right, say, 90% of the time. Users read this as trustworthiness for each case, but the promise holds only on average.",
   "idea": "Philosophers hold that a belief is justified if it comes from a reliable process, and they know the theory's weak spot: what counts as reliable depends on how cases are grouped. That weak spot is exactly the gap between an on-average and a per-case guarantee.",
   "payoff": "A clear account of what such guarantees do and do not license, for philosophers and for people using them in medicine or law.",
   "status": "Not done.",
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
   "title": "Read your body clock from a smartwatch with an AI that obeys the sleep equations",
   "problem": "Sleep science has a classic model: sleep pressure builds while you are awake, and a body clock opens and closes the gate to sleep. Fitting it to one person needs clean sleep diaries; smartwatch data is noisy and full of gaps.",
   "idea": "Physics-informed neural networks learn from data while being forced to obey known equations, which lets them cope with noisy, patchy measurements.",
   "payoff": "Personal estimates of sleep pressure and body-clock timing from everyday wearables, for shift planning or jet-lag advice.",
   "status": "Not done. Current fits use classical statistics.",
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
   "title": "Pack chatbot memory on GPUs with the method paper mills use to cut rolls",
   "problem": "AI chat services keep a working memory for every conversation on the GPU. Conversations differ in length, so memory fragments and goes to waste, which limits how many users one GPU can serve.",
   "idea": "Paper mills cut big rolls into orders of different widths with as little waste as possible. The classic method, column generation, copes with astronomically many cutting patterns and says how far a plan is from the best possible.",
   "payoff": "Less wasted memory, more users per GPU, and a benchmark for judging the rules of thumb in use today.",
   "status": "Not done. Current systems use rules of thumb and simple integer programs.",
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
   "id": "string-agents",
   "fa": "complex",
   "fb": "ai",
   "text": "Stop errors growing along a chain of AI agents with the rule that keeps a convoy of self-driving trucks from amplifying each other's braking.",
   "status": "Error growth is measured; this rule is not applied.",
   "outcome": "open",
   "score": 6.75
  },
  {
   "id": "cascade-agents",
   "fa": "power",
   "fb": "ai",
   "text": "Predict how one failing AI agent can bring down a team of agents, with the models used for blackouts spreading across a grid.",
   "status": "Error cascades are studied with other models.",
   "outcome": "open",
   "score": 5.75
  },
  {
   "id": "csd-spikes",
   "fa": "dynsys",
   "fb": "ai",
   "text": "Predict sudden failures when training large AI models from the warning signs that come before ecosystem tipping points: slower recovery, bigger wobbles.",
   "status": "Other early-warning signals are already studied.",
   "outcome": "open",
   "score": 6.25
  },
  {
   "id": "csd-grok",
   "fa": "dynsys",
   "fb": "ai",
   "text": "Look for tipping-point warning signs before an AI suddenly 'gets' a task after long training.",
   "status": "Mostly done.",
   "outcome": "done",
   "score": null
  },
  {
   "id": "hopf-repeat",
   "fa": "dynsys",
   "fb": "ai",
   "text": "Explain why AI text generators get stuck repeating themselves with the mathematics of how steady systems start to oscillate.",
   "status": "Other dynamical explanations exist.",
   "outcome": "open",
   "score": 5.75
  },
  {
   "id": "multistab-persona",
   "fa": "dynsys",
   "fb": "ai",
   "text": "Check whether an AI stays stuck in a persona once pushed into it, a sign of hidden stable states.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "kuramoto-debate",
   "fa": "dynsys",
   "fb": "ai",
   "text": "Use the mathematics of fireflies flashing in sync to predict when AI agents debating a question will agree or split.",
   "status": "Related ideas exist; never fitted to real debates.",
   "outcome": "open",
   "score": 5.5
  },
  {
   "id": "pseudotime-ckpt",
   "fa": "neuro",
   "fb": "ai",
   "text": "Use the tools biologists use to order cells along a development path to trace how features form inside a language model during training.",
   "status": "Features are tracked, but not with these tools.",
   "outcome": "open",
   "score": 6.5
  },
  {
   "id": "microglia-prune",
   "fa": "neuro",
   "fb": "ai",
   "text": "Trim neural networks with the rules brain immune cells use to prune unused connections.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "csr-transmission",
   "fa": "religion",
   "fb": "ai",
   "text": "Test whether AI, like people, best remembers stories that are only slightly supernatural.",
   "status": "Done: PNAS 2023 (Acerbi and Stubbersfield).",
   "outcome": "done",
   "score": null
  },
  {
   "id": "xvector-nilm",
   "fa": "audio",
   "fb": "power",
   "text": "Recognise each appliance or solar inverter by its electrical 'voice', with the AI that recognises a speaker's voice.",
   "status": "Similar methods exist.",
   "outcome": "open",
   "score": 6.5
  },
  {
   "id": "wav2vec-ae",
   "fa": "audio",
   "fb": "materials",
   "text": "Pretrain a speech-style AI on hours of unlabelled crackling sounds from stressed metal and concrete, then use it to detect growing cracks.",
   "status": "Smaller versions exist.",
   "outcome": "open",
   "score": 5.5
  },
  {
   "id": "query-search",
   "fa": "theory",
   "fb": "psych",
   "text": "Compare how many glances people need to find an object with the theoretical minimum number of yes-or-no questions.",
   "status": "Already compared with other ideal models.",
   "outcome": "open",
   "score": 6.25
  },
  {
   "id": "bnb-reason",
   "fa": "opt",
   "fb": "ai",
   "text": "Search AI reasoning steps with a classic optimisation method that safely skips hopeless branches.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "pod-kv",
   "fa": "amath",
   "fb": "ai",
   "text": "Compress a chatbot's working memory with the data-reduction method engineers use to speed up simulations.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "amr-context",
   "fa": "amath",
   "fb": "ai",
   "text": "Let an AI read long documents in detail only where it matters, as simulations refine their grid only where things happen.",
   "status": "A close method appeared in 2026.",
   "outcome": "open",
   "score": 5.5
  },
  {
   "id": "ch-opinion",
   "fa": "amath",
   "fb": "netsci",
   "text": "Model how opinion groups online slowly merge with the equation for oil and water separating.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "berry-train",
   "fa": "physics",
   "fb": "ai",
   "text": "Measure a geometric 'twist' that network weights pick up when the learning rate is cycled up and down.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "mips-traffic",
   "fa": "physics",
   "fb": "complex",
   "text": "Explain jams in mixed self-driving and human traffic with the physics of self-propelled particles clumping.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "tmr-agent",
   "fa": "eda",
   "fb": "ai",
   "text": "Have three AI agents vote on each action, as spacecraft computers do, and measure the gain in reliability.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "dse-connectome",
   "fa": "eda",
   "fb": "neuro",
   "text": "Use chip-design trade-off tools to ask whether brain wiring balances cost against performance.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "iss-llmloop",
   "fa": "control",
   "fb": "ai",
   "text": "Prove that a control system stays stable even when a language model that sometimes errs proposes its actions.",
   "status": "Sketched in a survey; no proofs yet.",
   "outcome": "open",
   "score": 6.25
  },
  {
   "id": "cbf-dp",
   "fa": "control",
   "fb": "security",
   "text": "Use a safety filter from robotics to stop a dataset's privacy budget being overspent as queries arrive.",
   "status": "Existing privacy filters already do most of this.",
   "outcome": "open",
   "score": 5.5
  },
  {
   "id": "sleep-replay-llm",
   "fa": "sleep",
   "fb": "ai",
   "text": "Train AI on new material in cycles that copy human sleep: more review early in the night, more 'dreaming' later.",
   "status": "Sleep-like phases tried; not the human schedule.",
   "outcome": "open",
   "score": 5.5
  },
  {
   "id": "bo-tes",
   "fa": "uq",
   "fb": "sleep",
   "text": "Tune sleep-deepening sound pulses to each person over a few nights with the search method used to tune AI models.",
   "status": "Only a master's thesis so far.",
   "outcome": "open",
   "score": 5.75
  },
  {
   "id": "fdr-leader",
   "fa": "uq",
   "fb": "ai",
   "text": "Correct AI leaderboards for the many 'A beats B' claims they make at once, so the lucky ones are not taken as real.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "rr-fl",
   "fa": "epi",
   "fb": "security",
   "text": "Patch the devices next to a hacked one first, as ring vaccination does around a smallpox case, and compare with patching everyone in turn.",
   "status": "Close variants exist.",
   "outcome": "open",
   "score": 6.25
  },
  {
   "id": "r0-promptworm",
   "fa": "epi",
   "fb": "security",
   "text": "Estimate how fast self-copying malicious prompts would spread among AI email assistants, and what share must be protected to stop them, like an epidemic's R number.",
   "status": "Partly done.",
   "outcome": "open",
   "score": 6.75
  },
  {
   "id": "tte-copilot",
   "fa": "epi",
   "fb": "ai",
   "text": "Estimate whether AI coding assistants cause more or fewer bugs by imitating a randomised trial from project histories.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "seasonal-bench",
   "fa": "epi",
   "fb": "ai",
   "text": "Correct recent AI benchmark trends for results not yet published, as epidemiologists correct for late case reports.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "ddm-llm",
   "fa": "psych",
   "fb": "ai",
   "text": "Model an AI's choice of word as evidence piling up to a threshold, the standard model of human decisions.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "metacog-sleep",
   "fa": "psych",
   "fb": "sleep",
   "text": "Test whether sleep-deprived people misjudge when to trust an AI's advice.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "presence-dream",
   "fa": "vis",
   "fb": "sleep",
   "text": "Measure how real lucid dreams feel with the questionnaires that measure 'being there' in virtual reality.",
   "status": "Proposed in theory only.",
   "outcome": "open",
   "score": 6.0
  },
  {
   "id": "3dgs-micro",
   "fa": "vis",
   "fb": "materials",
   "text": "Rebuild the 3D inside of a material from a few X-ray shots with the new graphics technique behind photo-real 3D scenes.",
   "status": "Used for X-rays already, not tested on materials.",
   "outcome": "open",
   "score": 5.75
  },
  {
   "id": "netvis-patristic",
   "fa": "vis",
   "fb": "theology",
   "text": "Map which Bible verses each early Church Father quoted, and how the map shifted during the debates over the nature of Christ.",
   "status": "Done for one author, Origen.",
   "outcome": "open",
   "score": 6.25
  },
  {
   "id": "align-theology",
   "fa": "theology",
   "fb": "ai",
   "text": "Grade the analogies AI models make with Thomas Aquinas's types of analogy.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "hermeneutic-rag",
   "fa": "theology",
   "fb": "ai",
   "text": "Let AI read long documents by moving back and forth between the parts and the whole, as interpreters of texts do.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "ritual-kuramoto",
   "fa": "religion",
   "fb": "complex",
   "text": "Measure whether people who move in sync during rituals bond more, with the mathematics of synchronising oscillators.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "secular-perc",
   "fa": "religion",
   "fb": "netsci",
   "text": "Test whether people leave religion the way they take up a habit only after several friends have, using surveys that follow friendships over years.",
   "status": "Simulated, not tested on real data.",
   "outcome": "open",
   "score": 6.5
  },
  {
   "id": "costly-fl",
   "fa": "religion",
   "fb": "security",
   "text": "Keep fake participants out of shared AI training by demanding costly contributions, as costly rituals prove religious commitment.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "evo-game-review",
   "fa": "complex",
   "fb": "ai",
   "text": "Model reviewer effort and AI-written reviews at AI conferences as strategies competing over time.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "percolation-supply",
   "fa": "netsci",
   "fb": "eda",
   "text": "Work out how many failures it takes to break the chip-design supply chain.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "homophily-moe",
   "fa": "netsci",
   "fb": "ai",
   "text": "Check whether similar words are sent to the same 'expert' inside mixture-of-experts AI models, and what that does to the load balance.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "bipartite-review",
   "fa": "netsci",
   "fb": "ai",
   "text": "Test whether reviewer-paper assignments have the nested shape of ecosystems, which would make them robust to reviewers dropping out.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "hoi-lora",
   "fa": "complex",
   "fb": "ai",
   "text": "Predict which add-on modules for AI models combine well by looking at groups of them, not pairs.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "evac-dc",
   "fa": "complex",
   "fb": "power",
   "text": "Plan moving jobs out of a failing data centre with crowd-evacuation models.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "traffic-tokens",
   "fa": "complex",
   "fb": "eda",
   "text": "Model congestion in the wiring inside AI chips with the equations for highway traffic.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "garch-gpu",
   "fa": "ts",
   "fb": "power",
   "text": "Forecast the swings in power use of AI training clusters with the volatility models used for stock prices, to size backup batteries.",
   "status": "Not done, but a routine transfer.",
   "outcome": "open",
   "score": 6.5
  },
  {
   "id": "emh-openreview",
   "fa": "ts",
   "fb": "ai",
   "text": "Test whether reviewers' score changes after author rebuttals can be predicted, as markets are tested for efficiency.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "var-bench",
   "fa": "ts",
   "fb": "ai",
   "text": "Choose AI models by how badly they fail in the worst cases, with financial risk measures, rather than by average score.",
   "status": "Done: ICML 2024 (Nitsure et al.).",
   "outcome": "done",
   "score": null
  },
  {
   "id": "factor-sleep",
   "fa": "ts",
   "fb": "sleep",
   "text": "Pull a few common sleep patterns out of many nights of wearable data with the models economists use for many indicators.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "changepoint-theology",
   "fa": "ts",
   "fb": "theology",
   "text": "Find the moments when theological vocabulary changed sharply across church councils.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "dro-epi",
   "fa": "opt",
   "fb": "epi",
   "text": "Allocate antiviral stockpiles so they hold up under the worst plausible epidemic curves.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "online-lockdown",
   "fa": "opt",
   "fb": "epi",
   "text": "Decide when to start and end lockdowns with guarantees that hold however the epidemic unfolds.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "vrp-cbti",
   "fa": "opt",
   "fb": "sleep",
   "text": "Schedule nurses' shifts around each nurse's body-clock timing, measured by a wearable.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "facility-conf",
   "fa": "opt",
   "fb": "netsci",
   "text": "Pick conference cities that minimise total flight emissions.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "mlip-ree",
   "fa": "materials",
   "fb": "ai",
   "text": "Detect AI hallucinations with the tricks chemists use to tell when an atom-level simulation is out of its depth.",
   "status": "Similar detectors already exist in AI.",
   "outcome": "open",
   "score": 6.0
  },
  {
   "id": "hardening-plast",
   "fa": "materials",
   "fb": "ai",
   "text": "Describe how AI models lose the ability to learn new things with the laws for metal hardening as it is bent.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "gb-merge",
   "fa": "materials",
   "fb": "ai",
   "text": "Model clashes when merging AI models with the energy at boundaries between grains in a metal.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "phasefield-tumor",
   "fa": "materials",
   "fb": "biomed",
   "text": "Model a tumour's invading edge as a crack running through tissue, with the mathematics of fracture in materials.",
   "status": "Related tumour models exist.",
   "outcome": "open",
   "score": 6.25
  },
  {
   "id": "battery-sleep",
   "fa": "power",
   "fb": "sleep",
   "text": "Track sleep pressure like a battery's charge, with the estimators in electric-car battery systems.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "inverter-brain",
   "fa": "power",
   "fb": "neuro",
   "text": "Compare how solar inverters keep the grid in rhythm with how the brain's thalamus sets its rhythms.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "bilevel-review",
   "fa": "power",
   "fb": "ai",
   "text": "Design conference reviewer incentives as a leader-and-follower optimisation.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "qfi-psych",
   "fa": "quantum",
   "fb": "psych",
   "text": "Compare how well people detect very dim light with the quantum limit for the same light.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "qnet-epi",
   "fa": "quantum",
   "fb": "epi",
   "text": "Route vaccine deliveries that spoil over time with algorithms for routing fragile quantum links.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "decoh-llm",
   "fa": "quantum",
   "fb": "ai",
   "text": "Model how chatbots forget instructions in long chats as quantum states losing coherence.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "treewidth-theo",
   "fa": "theory",
   "fb": "theology",
   "text": "Measure how tangled the arguments in Aquinas's Summa are with a graph measure from computer science.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "proof-justif",
   "fa": "theory",
   "fb": "philosophy",
   "text": "Use the length of the shortest proof as a measure of how costly a belief is to justify.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "hausdorff-dream",
   "fa": "math",
   "fb": "sleep",
   "text": "Measure how jagged dream stories are compared with waking stories, using fractal dimension.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "cluster-merge",
   "fa": "math",
   "fb": "ai",
   "text": "Describe the ways to rearrange a network without changing what it computes with a branch of algebra, to help merge models.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "ricci-gene",
   "fa": "math",
   "fb": "neuro",
   "text": "Find bottlenecks in how brain cells develop with a geometric flow from mathematics.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "dg-theology",
   "fa": "amath",
   "fb": "theology",
   "text": "Date the editing layers of biblical manuscripts as an inverse problem, like sharpening a blurred image.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "cons-misinfo",
   "fa": "amath",
   "fb": "netsci",
   "text": "Model sudden surges of misinformation as shock waves travelling through a network.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "vit-theology",
   "fa": "biomed",
   "fb": "theology",
   "text": "Use medical-image AI to read erased text under rewritten medieval manuscripts.",
   "status": "Mostly done with similar networks.",
   "outcome": "done",
   "score": null
  },
  {
   "id": "ehr-religion",
   "fa": "biomed",
   "fb": "religion",
   "text": "Use religious preference and chaplains' notes in medical records to predict end-of-life care choices.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "fl-sleep",
   "fa": "security",
   "fb": "sleep",
   "text": "Train sleep-scoring AI across clinics without sharing patient data, despite their different equipment.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "sidechannel-sleep",
   "fa": "security",
   "fb": "sleep",
   "text": "Show that encrypted traffic from bedroom smart devices can reveal sleep disorders.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "backdoor-ptsd",
   "fa": "security",
   "fb": "psych",
   "text": "Use hidden-trigger attacks on AI as a model of traumatic memories set off by cues.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "dp-census-relig",
   "fa": "security",
   "fb": "religion",
   "text": "Measure how privacy noise in census data distorts counts of small religious groups.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "cultural-oss",
   "fa": "religion",
   "fb": "ai",
   "text": "Treat the family tree of open AI models, copied and fine-tuned by others, like cultural traits passed between people, and test what makes some spread.",
   "status": "Family trees exist; the cultural-evolution test does not.",
   "outcome": "open",
   "score": 6.75
  },
  {
   "id": "dmn-idle",
   "fa": "neuro",
   "fb": "ai",
   "text": "Look for the brain's daydreaming-network pattern in AI agents left with nothing to do.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "gut-brain-graph",
   "fa": "neuro",
   "fb": "netsci",
   "text": "Build a layered network linking gut microbes, the chemicals they make and brain regions.",
   "status": "Already studied",
   "outcome": "dropped",
   "score": null
  },
  {
   "id": "aging-reservoir",
   "fa": "neuro",
   "fb": "dynsys",
   "text": "Compare the memory capacity of young and old brains' wiring when each is used as a simple computer.",
   "status": "Analogy, not a method",
   "outcome": "dropped",
   "score": null
  }
 ],
 "method": [
  "I paired a method, tool or finding from one field with a concrete problem in another, 103 pairs in all, drawn from the 27 fields on the conference pages.",
  "For each pair I counted papers whose title or abstract names both sides, in Semantic Scholar and Europe PMC. Pairs that were already well studied, or where the link was only a loose analogy, stopped here.",
  "The 48 that remained were searched by hand, two to five searches each in different wordings, to find the closest existing work.",
  "Each surviving idea got four marks out of 10: how untouched it is, how far apart the two fields are, whether a real method carries over (not just a metaphor), and how much it would give. The score is their average. An idea can be untouched because it is pointless; the last two marks push those down."
 ]
};

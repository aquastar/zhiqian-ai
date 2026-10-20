// The fields this page covers, by hand. Each one says how it is best shown,
// because the fields do not share a shape: AI is a race of ranked, selective
// conferences with published acceptance rates; neuroscience is a calendar of
// abstract meetings where the journal is the paper; control sits between.
//
// format   'table'  ranked, reviewed conferences, one row each
//          'cards'  meetings that take abstracts, one card each
// rank     'ccf'    CCF, CORE and CSRankings are the ranking (AI only)
//          'field'  the field's own tiers first, CCF / CORE beside them
//                   where they exist
//          'none'   the field has no ranking worth a column
// notes    how the field publishes, in three lines
export const GROUPS = [
  { id: 'computing', label: 'Computing' },
  { id: 'math', label: 'Math' },
  { id: 'science', label: 'Science & engineering' },
  { id: 'mind', label: 'Mind & brain' },
  { id: 'health', label: 'Health' },
];

export const DOMAINS = [
  {
    id: 'ai', label: 'AI · ML · Data Mining', group: 'computing', icon: 'fa-brain', hue: '#6d28d9',
    format: 'table', rank: 'ccf', scholar: 'eng_artificialintelligence',
    notes: [
      'Conferences lead. A journal paper is usually the long version of one.',
      'JMLR and TMLR review on a rolling basis, with no deadline to hit.',
      'TACL papers are presented at ACL conferences; TMLR has a route to ICLR and NeurIPS.',
    ],
  },
  {
    id: 'security', label: 'Security', group: 'computing', icon: 'fa-shield-halved', hue: '#b91c1c',
    format: 'table', rank: 'field', scholar: 'eng_computersecuritycryptography', cycles: true,
    notes: [
      'The Big Four conferences outrank every security journal.',
      'Each runs two or more cycles a year, and major revision is a formal outcome, so the calendar matters more than any one date.',
      'TDSC and TIFS are where extended conference papers usually go.',
    ],
  },
  {
    id: 'eda', label: 'Hardware & EDA', group: 'computing', icon: 'fa-microchip', hue: '#0369a1',
    format: 'table', rank: 'field', scholar: 'eng_computerhardwaredesign',
    notes: [
      'DAC and ICCAD are the two EDA venues everyone means; DATE and ASP-DAC are their European and Asian counterparts.',
      'Architecture has its own four: ISCA, MICRO, HPCA and ASPLOS.',
      'TCAD is the journal of record, and long versions of DAC and ICCAD papers go there.',
    ],
  },
  {
    id: 'theory', label: 'Theoretical CS', group: 'computing', icon: 'fa-sitemap', hue: '#3730a3',
    format: 'table', rank: 'field', scholar: 'eng_theoreticalcomputerscience',
    notes: [
      'STOC and FOCS are the top two, and SODA leads algorithms; a paper at any of them counts like a top journal paper.',
      'Submissions are full papers with proofs, often in an appendix, refereed by a program committee.',
      'The long version goes to JACM, SICOMP or TheoretiCS, often years after the conference paper.',
    ],
  },
  {
    id: 'quantum', label: 'Quantum computing', group: 'computing', icon: 'fa-wave-square', hue: '#0891b2',
    format: 'table', rank: 'field', scholar: '',
    notes: [
      'QIP is the top meeting, and it accepts talks rather than papers: the submission is judged, and the paper goes to a journal or stays on arXiv.',
      'TQC is the one with archival proceedings; IEEE Quantum Week is the large engineering meeting.',
      'Quantum and PRX Quantum are the journals people aim for, and nearly everything is on arXiv first.',
    ],
  },
  {
    id: 'audio', label: 'Music & Audio', group: 'computing', icon: 'fa-music', hue: '#be185d',
    format: 'table', rank: 'field', scholar: 'eng_signalprocessing',
    notes: [
      'ISMIR is the music-information-retrieval community in one room, and its papers are short: six pages plus references.',
      'ICASSP and Interspeech are the large signal-processing and speech meetings, four-page papers.',
      'TISMIR is ISMIR’s own journal; TASLP is where audio work goes long.',
    ],
  },
  {
    id: 'ts', label: 'Time series', group: 'computing', icon: 'fa-chart-line', hue: '#0f766e',
    format: 'cards', rank: 'none', scholar: '', topic: 'time series',
    notes: [
      'There is no top time-series conference. Methods papers go to the ML and data-mining venues under AI.',
      'Forecasting is its own community, with the International Institute of Forecasters, its symposium and IJF.',
      'The statistics side publishes in journals, JTSA among them.',
    ],
  },
  {
    id: 'control', label: 'Control', group: 'science', icon: 'fa-sliders', hue: '#b45309',
    format: 'table', rank: 'field', scholar: 'eng_automationcontroltheory',
    notes: [
      'Journals carry the weight. TAC and Automatica outrank any conference.',
      'CDC and ACC papers are six pages, reviewed and archived, often an early form of a journal paper.',
      'An L-CSS letter can be presented at CDC or ACC, on the joint deadline.',
    ],
  },
  {
    id: 'math', label: 'Mathematics', group: 'math', icon: 'fa-shapes', hue: '#1f2937',
    format: 'cards', rank: 'none', scholar: 'phy_pureappliedmathematics',
    notes: [
      'Mathematics is a journal field. Talks are invited or short contributed ones, and a paper is judged by where it is published.',
      'The top five (Annals, Acta, Inventiones, JAMS and Publications de l\u2019IH\u00c9S) are what hiring committees read first.',
      'The ICM, every four years, is the field\u2019s congress, where the Fields Medals are awarded.',
    ],
  },
  {
    id: 'dynsys', label: 'Dynamical systems', group: 'math', icon: 'fa-infinity', hue: '#7c3aed',
    format: 'cards', rank: 'none', scholar: 'phy_nonlinearscience',
    notes: [
      'A mathematics field: the paper is the journal paper, the meeting is where you talk about it.',
      'SIAM DS runs every other year and is the big one; Dynamics Days is a single-track meeting on each side of the Atlantic.',
      'SIADS, Chaos and Physica D cover most of it.',
    ],
  },
  {
    id: 'physics', label: 'Physics', group: 'science', icon: 'fa-magnet', hue: '#0c4a6e',
    format: 'cards', rank: 'none', scholar: 'phy_phygeneral',
    notes: [
      'Physics publishes in journals. The APS meetings take short talks on a one-paragraph abstract, and nothing there is refereed.',
      'PRL is the short, fast, selective letter journal; Nature Physics and PRX are the broad selective ones.',
      'Almost everything is on arXiv before it is submitted.',
    ],
  },
  {
    id: 'complex', label: 'Complex systems', group: 'science', icon: 'fa-circle-nodes', hue: '#0e7490',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'Overlaps network science, statistical physics and artificial life, and draws from all three.',
      'Meetings take one-page abstracts; the work is published in physics and interdisciplinary journals.',
      'Physical Review E is the usual home for the physics side.',
    ],
  },
  {
    id: 'netsci', label: 'Network science', group: 'science', icon: 'fa-diagram-project', hue: '#1d4ed8',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'NetSci is the flagship. Talks are chosen from one-page abstracts; nothing is archived.',
      'Complex Networks and CompleNet are the two meetings that publish papers, in Springer volumes.',
      'Sunbelt and IC2S2 are the social-science side of the same graphs.',
    ],
  },
  {
    id: 'uq', label: 'UQ & statistics', group: 'math', icon: 'fa-dice', hue: '#4d7c0f',
    format: 'cards', rank: 'none', scholar: 'phy_probabilitystatistics',
    notes: [
      'Uncertainty quantification sits between applied mathematics, statistics and engineering, and has a meeting in each.',
      'SIAM UQ runs every other year with the ASA; UNCECOMP is the engineering side, with optional full papers.',
      'JUQ is the joint SIAM and ASA journal.',
    ],
  },
  {
    id: 'opt', label: 'Optimization & OR', group: 'math', icon: 'fa-route', hue: '#9a3412',
    format: 'cards', rank: 'none', scholar: 'phy_mathematicaloptimization',
    notes: [
      'Journals are the record; meetings are abstracts and one talk each.',
      'ISMP, every three years, is the whole of mathematical optimization in one place.',
      'Mathematical Programming and SIOPT on the theory side, Operations Research on the applied.',
    ],
  },
  {
    id: 'amath', label: 'Applied math', group: 'math', icon: 'fa-square-root-variable', hue: '#475569',
    format: 'cards', rank: 'none', scholar: 'phy_computationalmathematics',
    notes: [
      'Minisymposia are how these meetings work: organise a session of four talks and invite the speakers.',
      'ICIAM runs every four years; in 2027 it takes the place of the SIAM Annual Meeting, which returns in 2028.',
      'SIAM Review and SISC are the broad journals.',
    ],
  },
  {
    id: 'neuro', label: 'Cognitive neuroscience', group: 'mind', icon: 'fa-head-side-virus', hue: '#7e22ce',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'Every meeting here takes abstracts. A poster is the normal outcome, and presenting does not spend the paper.',
      'COSYNE and CCN are the two where machine learning and neuroscience meet.',
      'The journal is what counts: Neuron and Nature Neuroscience at the top, J. Cogn. Neurosci. for the field itself.',
    ],
  },
  {
    id: 'psych', label: 'Psychology', group: 'mind', icon: 'fa-user-group', hue: '#a21caf',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'Psychology publishes in journals; conferences are for talks and posters.',
      'CogSci is the exception, with full papers in an archival proceedings, and the closest to computing.',
      'Psychological Science and Psychological Review for the broad audience, Cognition for the cognitive side.',
    ],
  },
  {
    id: 'sleep', label: 'Sleep & dreams', group: 'mind', icon: 'fa-moon', hue: '#4338ca',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'Sleep medicine and dream research are two communities: SLEEP and World Sleep for the first, IASD for the second.',
      'SLEEP abstracts are published in a supplement of the journal SLEEP.',
      'Dreaming and IJoDR are the dream-research journals.',
    ],
  },
  {
    id: 'biomed', label: 'Biomedical', group: 'health', icon: 'fa-heart-pulse', hue: '#0f766e',
    format: 'table', rank: 'field', scholar: 'med_medicalinformatics',
    notes: [
      'Clinical readers read journals: JAMIA or npj Digital Medicine counts for more than a conference.',
      'MICCAI is the imaging conference; MIDL and ISBI are its smaller neighbours.',
      'CHIL and ML4H are the machine-learning-for-health venues, both archival in PMLR.',
    ],
  },
  {
    id: 'epi', label: 'Epidemics', group: 'health', icon: 'fa-virus', hue: '#c2410c',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'Epidemic modelling is a journal field with two meetings: Epidemics for modellers, ESCAIDE for public-health practice.',
      'Both take abstracts; nothing is archived as a paper.',
      'The journal Epidemics and PLOS Computational Biology carry most modelling papers.',
    ],
  },
  {
    id: 'materials', label: 'Materials', group: 'science', icon: 'fa-atom', hue: '#57534e',
    format: 'cards', rank: 'none', scholar: '',
    notes: [
      'MRS and TMS are huge abstract meetings, organised as dozens of parallel symposia.',
      'AI for materials has its own workshop at NeurIPS.',
      'npj Computational Materials and Digital Discovery are where machine-learning work lands.',
    ],
  },
  {
    id: 'power', label: 'Power & energy', group: 'science', icon: 'fa-bolt', hue: '#a16207',
    format: 'table', rank: 'field', scholar: 'eng_powerengineering',
    notes: [
      'TPWRS and TSG are the journals that count; conference papers are short and fast.',
      'PSCC, every two years, is the selective conference, with full papers published in a journal.',
      'The PES General Meeting is the large annual gathering.',
    ],
  },
];

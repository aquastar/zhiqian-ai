// Deadlines, Sep 2026 - Feb 2027. `kind` drives the colour and follows the
// source legend: NSF grant, NIH grant, other grant, paper, review/report.
export const deadlines = [
  { month: 'Sep 2026', y: 2026, m: 8, items: [
    { d: 15, name: 'Sony Research Award (FRA)', kind: 'other' },
    { d: 18, name: 'ICLR 2027 abstract registration (mandatory)', kind: 'paper' },
    { d: 21, name: 'eBay 2027 eRUPT Academic Research Grants', kind: 'other' },
    { d: 25, name: 'ICLR 2027 full paper', kind: 'paper' },
    { d: 25, name: 'Grammy Museum Scientific Research LOI', kind: 'other' },
    { d: 28, name: 'NIH R16 SuRE', kind: 'nih' },
  ]},
  { month: 'Oct 2026', y: 2026, m: 9, items: [
    { d: 9, name: 'NSF MFAI', kind: 'nsf' },
    { d: 9, name: 'Air Force YIP FY2027 white paper', kind: 'other' },
    { d: 12, name: 'NAACL 2027 (main)', kind: 'paper' },
    { d: 12, name: 'COLING 2027 (main)', kind: 'paper' },
    { d: 14, name: 'IEEE BigData reviews due', kind: 'review' },
    { d: 15, name: 'WSDM 2027 demo', kind: 'paper' },
    { d: 16, name: 'NIH R21 new (standing date)', kind: 'nih' },
    { d: 18, name: 'WebConf abstract (research + industry)', kind: 'paper' },
    { d: 25, name: 'WebConf full paper', kind: 'paper' },
    { d: 26, name: 'NIH R15 AREA new (Oct 25 shift)', kind: 'nih' },
    { d: 29, name: 'NSF CIRC final + outcomes report', kind: 'review' },
    { d: 30, name: 'RIT Global Seed', kind: 'other' },
    { d: 30, name: 'ONR YIP', kind: 'other' },
  ]},
  { month: 'Nov 2026', y: 2026, m: 10, items: [
    { d: 4, name: 'NSF AI Datasets', kind: 'nsf' },
    { d: 4, name: 'NSF SBIR/STTR', kind: 'nsf' },
    { d: 7, name: 'CVPR 2027 abstract', kind: 'paper', est: true },
    { d: 9, name: 'WebConf short abstract', kind: 'paper' },
    { d: 9, name: 'Web4Good abstract', kind: 'paper' },
    { d: 13, name: 'CVPR 2027 main paper', kind: 'paper', est: true },
    { d: 16, name: 'WebConf short paper', kind: 'paper' },
    { d: 16, name: 'Web4Good full paper', kind: 'paper' },
    { d: 16, name: 'WebConf demo paper', kind: 'paper' },
    { d: 17, name: 'WSDM 2027 short paper', kind: 'paper' },
    { d: 17, name: 'NSF TTP', kind: 'nsf' },
  ]},
  { month: 'Dec 2026', y: 2026, m: 11, items: [
    { d: 1, name: 'Simons Empire AI (noon ET)', kind: 'other' },
    { d: 2, name: 'NSF Expeditions preliminary proposal', kind: 'nsf' },
  ]},
  { month: 'Jan 2027', y: 2027, m: 0, items: [
    { d: 20, name: 'NSF CICI', kind: 'nsf' },
    { d: 31, name: 'NSF CISE Core eligible again', kind: 'nsf' },
  ]},
  { month: 'Feb 2027', y: 2027, m: 1, items: [
    { d: 3, name: 'NIH R35 MIRA for ESIs', kind: 'nih' },
    { d: 8, name: 'NSF GCR', kind: 'nsf' },
    { d: 15, name: 'NeuroArts Fleming (mid Feb)', kind: 'other', est: true },
    { d: 16, name: 'NIH R21 new (standing date)', kind: 'nih' },
    { d: 25, name: 'NIH R15 AREA new (standing date)', kind: 'nih' },
  ]},
];

export const kindLabels = {
  nsf: 'NSF grant',
  nih: 'NIH grant',
  other: 'Other grant',
  paper: 'Paper',
  review: 'Review / report',
};

export const openCalls = [
  { heading: 'Submit anytime (no fixed deadline)', items: ['NSF BIO Core', 'NSF CMMI / IIDS (NSF 26-515)', 'NSF CMMI / EME', 'NSF TTP-E', 'NSF CISE Core — 2 per rolling 12 months; next slot opens Jan 31, 2027'] },
  { heading: 'Date not announced', items: ['ARPA-H EHI (call not yet announced)', 'CVPR 2027 demo (historically spring)', 'NeuroArts Fleming (mid Feb 2027)'] },
  { heading: 'NIH due dates (new applications)', items: ['R35 MIRA for ESIs: Feb 3, 2027 (Feb and Oct cycles)', 'R21: Feb 16 / Jun 16 / Oct 16', 'R15 AREA: Feb 25 / Jun 25 / Oct 25'] },
];

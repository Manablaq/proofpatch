export const PROOFPATCH = {
  network: {
    name: "Bradbury Testnet",
    rpc: "https://rpc-bradbury.genlayer.com",
    explorer: "https://explorer-bradbury.genlayer.com",
    chainId: 4221,
    symbol: "GEN",
  },
  governor: "0x20a14189cb68d1878eaA9253b14983ace1684aA6",
  target: "0x7e22B7c72B196e0db60785344570Fb558bD3b33A",
  owner: "0x1f87Ae197af539253978d435aD45cCf28Fb95024",
  proposalId: 1,
  parentVersion: "1.0.0",
  parentCodeHash:
    "7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19",
  candidateVersion: "2.0.0",
  candidateCodeHash:
    "013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea",
  policyFingerprint:
    "18c5d7e9852799896fb7fe3ee11ce8abc1104122adbb4afcee22e163fb424e50",
  evidenceSetHash:
    "bb4f2a6092e32f9ec67c2508f243a09036bfd1ad1d4b505f26766df65250cb5d",
  releaseLabel: "ProtectedTarget/v2-safe",
  productName: "ProofPatch Protected Target",
  protectedValue: "proofpatch-bradbury-baseline-v1",
  transactions: {
    registrationParent:
      "0xa0b19fe09cb2faed06d02c48b4b47e661f2c73f1585538cf1ec5f094e1fc09ae",
    proposalCreate:
      "0x1c32f5beb67fad804eea8c79f061c11ca16d402d119ea133e1a59e34541e801c",
    reviewParent:
      "0x0a6b3c9275dc12fb9f98f7ceb52cc165db74444b4c27de10dcdd235ca338e34b",
    upgradeChild:
      "0xd196ac64c42e48e944f6ca85b79ab0a74fcc6100235e8b6e3015a604a57e5e59",
    confirmationChild:
      "0xdd8118477147a0d8a9b65442b87d31ec0f8916e116e8ca89804901828a1462a5",
  },
  evidence: {
    finalAuditSha256:
      "4f0cf58ad0f8a76c74fadb0aa90870e407c0b749983cf7437930e8aa7e94005d",
  },
} as const;


export const PROOFPATCH_V3 = {
  network: {
    name: "Bradbury Testnet",
    rpc: "https://rpc-bradbury.genlayer.com",
    explorer: "https://explorer-bradbury.genlayer.com",
    chainId: 4221,
    symbol: "GEN",
  },
  facade: "0x46eE236d3812A4c71F09eBdf641963bFc6ea8c6D",
  target: "0x9e8ACf20747B8d18D54b3c45e0510003029BCf4f",
  owner: "0x1f87Ae197af539253978d435aD45cCf28Fb95024",
  version: "2.0.0",
  codeHash:
    "9da36f69837321c9688e6ec338dbdfbfd085a9f387361e7bb2c37037f353c9fe",
  policyFingerprint:
    "d090b20e2eb4deeff39cc295c703b431fb7631bfb64941d80405b37c85963607",
  kernelHash:
    "8a5f9c864d80aa10fdcd8f2878cf5bcd3ff28e0cdb62ab11043668e215e7a930",
  rootReleaseId: "root-9da36f69837321c9",
  releaseStatus: "REGISTERED_PARENT",
  releaseMode: "ACTIVE",
  proposalCount: 0,
  activeProposal: 0,
  registrationChain: {
    parent:
      "0xf01abff0c3f27998c0da2e212a51931ad4422ab5d4cd5ffec0b837f21d1befe9",
    registerTarget:
      "0x266f30fb932aafbccb5891ca26478baea1cc0826c587a2ab8bb25facdac511ad",
    registrationEngine:
      "0x93493791c5a6c1b4f2c61844d25cacd8e87f39ac5889d3d8758f1e13c045ec70",
    applyPolicyResult:
      "0xa1ce343c1688372527b94e0806eed01150be88de993a3380aef6091ab038b084",
    confirmation:
      "0x35824ed9d44dda5c25d778c009c77854b0d580e37378aa0e156dec2b2ddccfe4",
  },
} as const;

export const APP_NAV = [
  { id: "overview", label: "Overview" },
  { id: "finality", label: "Finality proof" },
  { id: "evidence", label: "Evidence" },
  { id: "policy", label: "Policy" },
  { id: "transactions", label: "Transactions" },
] as const;

export const SECURITY_GATES = [
  {
    title: "Publisher-bound evidence",
    detail:
      "Source, CI and independent audit authorities are policy-bound before a proposal can influence execution.",
  },
  {
    title: "Immutable/versioned records",
    detail:
      "Candidate and evidence URLs must resolve through approved immutable repository prefixes.",
  },
  {
    title: "Freshness + replay resistance",
    detail:
      "Evidence carries publication/expiry rules and scoped identifiers that cannot be reused for the same authority and target.",
  },
  {
    title: "Repairable evidence failures",
    detail:
      "Correctable fetch, parse and hash failures move the proposal into a repair state instead of forcing an unsafe terminal path.",
  },
  {
    title: "Exact consequential agreement",
    detail:
      "The candidate hash and authorization-driving semantic result are exact values, never fuzzy confidence thresholds.",
  },
  {
    title: "Finality before consequence",
    detail:
      "The upgrade message is finality-bound; acceptance alone cannot replace the protected target code.",
  },
] as const;

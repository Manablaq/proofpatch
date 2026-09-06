export const PROOFPATCH = {
  network: {
    name: "Bradbury Testnet",
    rpc: "https://rpc-bradbury.genlayer.com",
    explorer: "https://explorer-bradbury.genlayer.com",
    chainId: 4221,
    symbol: "GEN",
  },
  governor: "0xc0100eFD567CD9dCcC8b9D17E381774fC4113ade",
  target: "0xe7165dEA0F712E3161ADa773c41755d79F1e696B",
  owner: "0x1f87Ae197af539253978d435aD45cCf28Fb95024",
  proposalId: 1,
  parentVersion: "1.0.0",
  parentCodeHash:
    "7607cce754d8f7905eed629b0e8af0f3ce51bd405b3b4ba9db19e5d831209f19",
  candidateVersion: "2.0.0",
  candidateCodeHash:
    "013f8ae10b9f38aaad7689168b94335a514a9c30882f4a03daa3eb546cda83ea",
  policyFingerprint:
    "0f30dea3a111d4d6ba13b68bb667338618c963ea5258049303a2492be73fc1ab",
  evidenceSetHash:
    "c252fd77fb2209cf65a5d47fbb3079218c6d1d196461c6f72573b3fcdd046ec5",
  releaseLabel: "ProtectedTarget/v2-safe",
  productName: "ProofPatch Protected Target",
  protectedValue: "proofpatch-bradbury-baseline-v1",
  transactions: {
    registrationParent:
      "0xac7f7997622ea75a0330dd9027349a6cadd3e9cc36ad787939c85e651d9f8153",
    registrationChild:
      "0x1599b7bfdcb569f84e423ae8cb051d6884a6a295b42d59e623bd8b0d9484e92d",
    reviewOuter:
      "0x4ff466bf5ea4c29123b92ccd98fb28777f0124b700a3b2dee7479f9b197de97e",
    reviewParent:
      "0xdaf2daf536913570bb7b2b9a81b6a05f85cc5e8fde38e95519bfae1a38891345",
    upgradeChild:
      "0x12296f35e3e570d4c828022a769dc32c9c4d18ca5bb2c1a736a5f01ffdbcdb33",
    confirmationChild:
      "0x9715daa0308bffc9a7b439f99ddcf9337eae186b16564c93570f7174cf17b475",
  },
  evidence: {
    finalAuditSha256:
      "1270ae8e13fc8877613bde4c674ffbb7e1b1628db8d8e085fb93dbb6b5baa176",
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

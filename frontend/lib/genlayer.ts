"use client";

import { createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";
import { TransactionHashVariant } from "genlayer-js/types";
import { PROOFPATCH } from "@/lib/constants";

type HexAddress = `0x${string}`;
type HexHash = `0x${string}`;

export type ProofPatchLiveState = {
  proposalStatus: string;
  candidateHash: string;
  evidenceSetHash: string;
  policyFingerprint: string;
  currentCodeHash: string;
  currentVersion: string;
  activeProposal: string;
  proposalSummary: Record<string, unknown> | null;
  installedProposalId: string;
  installedCandidateHash: string;
  releaseLabel: string;
  owner: string;
  governor: string;
  productName: string;
  protectedValue: string;
};

export type ChainTransactionSnapshot = {
  hash: string;
  status: string;
  execution: string;
  lifecycle: string;
};

export const publicClient = createClient({
  chain: testnetBradbury,
});

function text(value: unknown): string {
  if (typeof value === "bigint") return value.toString();
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  if (value === null || value === undefined) return "";
  return String(value);
}

let finalizedReadTail: Promise<void> = Promise.resolve();

async function readFinal(
  address: string,
  functionName: string,
  args: unknown[] = [],
): Promise<unknown> {
  const previous = finalizedReadTail;
  let release!: () => void;
  finalizedReadTail = new Promise<void>((resolve) => {
    release = resolve;
  });

  await previous;
  try {
    return await publicClient.readContract({
      address: address as HexAddress,
      functionName,
      args: args as never[],
      transactionHashVariant: TransactionHashVariant.LATEST_FINAL,
    } as never);
  } finally {
    await new Promise((resolve) => setTimeout(resolve, 160));
    release();
  }
}

export async function getProofPatchLiveState(): Promise<ProofPatchLiveState> {
  const governor = PROOFPATCH.governor;
  const target = PROOFPATCH.target;
  const proposal = PROOFPATCH.proposalId;

  const pause = () => new Promise((resolve) => setTimeout(resolve, 140));

  const serialRead = async (
    address: string,
    functionName: string,
    args: unknown[] = [],
  ) => {
    const value = await readFinal(address, functionName, args);
    await pause();
    return value;
  };

  const proposalStatus = await serialRead(governor, "get_proposal_status", [proposal]);
  const candidateHash = await serialRead(governor, "get_candidate_hash", [proposal]);
  const evidenceSetHash = await serialRead(governor, "get_evidence_set_hash", [proposal]);
  const policyFingerprint = await serialRead(governor, "get_policy_fingerprint", [target]);
  const currentCodeHash = await serialRead(governor, "get_current_code_hash", [target]);
  const currentVersion = await serialRead(governor, "get_current_version", [target]);
  const activeProposal = await serialRead(governor, "get_active_proposal", [target]);
  const proposalSummaryRaw = await serialRead(governor, "get_proposal_summary", [proposal]);

  const installedProposalId = await serialRead(
    target,
    "proofpatch_installed_proposal_id",
  );
  const installedCandidateHash = await serialRead(
    target,
    "proofpatch_installed_candidate_hash",
  );
  const releaseLabel = await serialRead(target, "get_release_label");
  const owner = await serialRead(target, "get_owner");
  const targetGovernor = await serialRead(target, "get_proofpatch_governor");
  const productName = await serialRead(target, "get_product_name");
  const protectedValue = await readFinal(target, "get_protected_value");

  let proposalSummary: Record<string, unknown> | null = null;
  try {
    const raw = text(proposalSummaryRaw);
    proposalSummary = raw ? (JSON.parse(raw) as Record<string, unknown>) : null;
  } catch {
    proposalSummary = null;
  }

  return {
    proposalStatus: text(proposalStatus),
    candidateHash: text(candidateHash),
    evidenceSetHash: text(evidenceSetHash),
    policyFingerprint: text(policyFingerprint),
    currentCodeHash: text(currentCodeHash),
    currentVersion: text(currentVersion),
    activeProposal: text(activeProposal),
    proposalSummary,
    installedProposalId: text(installedProposalId),
    installedCandidateHash: text(installedCandidateHash),
    releaseLabel: text(releaseLabel),
    owner: text(owner),
    governor: text(targetGovernor),
    productName: text(productName),
    protectedValue: text(protectedValue),
  };
}

export async function getTransactionSnapshot(
  hash: string,
): Promise<ChainTransactionSnapshot> {
  const transaction = (await publicClient.getTransaction({
    hash: hash as HexHash,
  } as never)) as unknown as Record<string, unknown>;

  return {
    hash,
    status: text(
      transaction.statusName ??
        transaction.status ??
        transaction.consensusStatus ??
        "Unknown",
    ),
    execution: text(
      transaction.txExecutionResultName ??
        transaction.executionResult ??
        transaction.result ??
        "Unknown",
    ),
    lifecycle: text(transaction.lifecycle ?? ""),
  };
}

export async function getCanonicalFinalityChain() {
  const entries = [
    {
      label: "Review consensus",
      hash: PROOFPATCH.transactions.reviewParent,
    },
    {
      label: "Finality-triggered upgrade",
      hash: PROOFPATCH.transactions.upgradeChild,
    },
    {
      label: "Post-install confirmation",
      hash: PROOFPATCH.transactions.confirmationChild,
    },
  ];

  return Promise.all(
    entries.map(async (entry) => {
      try {
        return {
          ...entry,
          ...(await getTransactionSnapshot(entry.hash)),
          available: true,
        };
      } catch {
        return {
          ...entry,
          status: "Unavailable",
          execution: "",
          lifecycle: "",
          available: false,
        };
      }
    }),
  );
}

export type BrowserProvider = {
  request: (args: {
    method: string;
    params?: unknown[] | Record<string, unknown>;
  }) => Promise<unknown>;
  on?: (event: string, listener: (...args: unknown[]) => void) => void;
  removeListener?: (
    event: string,
    listener: (...args: unknown[]) => void,
  ) => void;
};

declare global {
  interface Window {
    ethereum?: BrowserProvider;
  }
}

export async function connectBradburyWallet(): Promise<string> {
  if (typeof window === "undefined" || !window.ethereum) {
    throw new Error(
      "No browser wallet detected. Install MetaMask or another EIP-1193 wallet.",
    );
  }

  const accounts = (await window.ethereum.request({
    method: "eth_requestAccounts",
  })) as string[];

  const address = accounts?.[0];
  if (!address) {
    throw new Error("The wallet did not return an account.");
  }

  const walletClient = createClient({
    chain: testnetBradbury,
    account: address as HexAddress,
    provider: window.ethereum as never,
  });

  await walletClient.connect("testnetBradbury");
  return address;
}

export type ProposalSummary = {
  proposal_id?: number | string;
  target?: string;
  parent_version?: string;
  parent_code_hash?: string;
  candidate_version?: string;
  candidate_code_hash?: string;
  policy_fingerprint?: string;
  evidence_set_hash?: string;
  status?: string;
  last_review_code?: string;
  created_at?: number | string;
  expires_at?: number | string;
  reviewed_at?: number | string;
  execution_deadline?: number | string;
  [key: string]: unknown;
};

export type ProposalWorkspaceState = {
  proposalCount: number;
  activeProposal: string;
  proposals: ProposalSummary[];
};

function parseProposalSummary(value: unknown): ProposalSummary | null {
  try {
    const raw = text(value);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as unknown;
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    return parsed as ProposalSummary;
  } catch {
    return null;
  }
}

export async function getProposalWorkspaceState(): Promise<ProposalWorkspaceState> {
  const countRaw = await readFinal(PROOFPATCH.governor, "get_proposal_count");
  const activeRaw = await readFinal(PROOFPATCH.governor, "get_active_proposal", [
    PROOFPATCH.target,
  ]);
  const proposalCount = Number(text(countRaw) || "0");
  const proposals: ProposalSummary[] = [];
  const first = Math.max(1, proposalCount - 7);

  for (let id = proposalCount; id >= first; id -= 1) {
    const raw = await readFinal(PROOFPATCH.governor, "get_proposal_summary", [id]);
    const summary = parseProposalSummary(raw);
    if (summary) proposals.push(summary);
  }

  return {
    proposalCount,
    activeProposal: text(activeRaw),
    proposals,
  };
}

async function getBradburyWriteClient(address: string) {
  if (typeof window === "undefined" || !window.ethereum) {
    throw new Error("No browser wallet detected.");
  }

  const client = createClient({
    chain: testnetBradbury,
    account: address as HexAddress,
    provider: window.ethereum as never,
  });

  await client.connect("testnetBradbury");
  return client;
}

export async function createProofPatchProposal(
  draft: import("@/lib/proposal-workflow").ProposalDraft,
  address: string,
): Promise<string> {
  const client = await getBradburyWriteClient(address);
  const candidateBytes = new TextEncoder().encode(draft.candidateCode);

  await client.simulateWriteContract({
    address: PROOFPATCH.governor as HexAddress,
    functionName: "create_proposal",
    args: [
      PROOFPATCH.target,
      draft.candidateVersion,
      draft.candidateSourceUrl,
      candidateBytes,
      draft.ciEvidenceUrl,
      draft.ciEvidenceId,
      draft.auditEvidenceUrl,
      draft.auditEvidenceId,
    ] as never[],
    transactionHashVariant: TransactionHashVariant.LATEST_FINAL,
  } as never);

  return (await client.writeContract({
    address: PROOFPATCH.governor as HexAddress,
    functionName: "create_proposal",
    args: [
      PROOFPATCH.target,
      draft.candidateVersion,
      draft.candidateSourceUrl,
      candidateBytes,
      draft.ciEvidenceUrl,
      draft.ciEvidenceId,
      draft.auditEvidenceUrl,
      draft.auditEvidenceId,
    ] as never[],
  } as never)) as string;
}

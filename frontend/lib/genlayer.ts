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

async function readFinal(
  address: string,
  functionName: string,
  args: unknown[] = [],
): Promise<unknown> {
  return publicClient.readContract({
    address: address as HexAddress,
    functionName,
    args: args as never[],
    transactionHashVariant: TransactionHashVariant.LATEST_FINAL,
  } as never);
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

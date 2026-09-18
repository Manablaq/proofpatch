"use client";

import { TransactionHashVariant } from "genlayer-js/types";
import { publicClient } from "@/lib/genlayer";

type HexAddress = `0x${string}`;

export type ProofPatchV3Config = {
  facade: string;
  target: string;
  network: string;
  chainId: string;
};

export type ProofPatchV3State = {
  config: ProofPatchV3Config;
  proposalCount: string;
  activeProposal: string;
  latestProposal: Record<string, unknown> | null;
  currentReleaseId: string;
  currentVersion: string;
  currentCodeHash: string;
  policyFingerprint: string;
  policyKernelHash: string;
  policy: Record<string, unknown> | null;
  release: Record<string, unknown> | null;
};

const config: ProofPatchV3Config = {
  facade: process.env.NEXT_PUBLIC_PROOFPATCH_V3_FACADE ?? "",
  target: process.env.NEXT_PUBLIC_PROOFPATCH_V3_TARGET ?? "",
  network: process.env.NEXT_PUBLIC_PROOFPATCH_V3_NETWORK ?? "Bradbury Testnet",
  chainId: process.env.NEXT_PUBLIC_PROOFPATCH_V3_CHAIN_ID ?? "4221",
};

function requireConfig(): ProofPatchV3Config {
  if (!config.facade || !config.target) {
    throw new Error("LIVE STATE UNAVAILABLE: V3 facade and target are not configured.");
  }
  return config;
}

function text(value: unknown): string {
  if (typeof value === "bigint") return value.toString();
  if (typeof value === "string") return value;
  if (value === null || value === undefined) return "";
  return String(value);
}

async function readFinal(address: string, functionName: string, args: unknown[] = []) {
  return publicClient.readContract({
    address: address as HexAddress,
    functionName,
    args: args as never[],
    transactionHashVariant: TransactionHashVariant.LATEST_FINAL,
  } as never);
}

function parseRecord(value: unknown, label: string): Record<string, unknown> | null {
  const raw = text(value);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      throw new Error(`${label} is not an object`);
    }
    return parsed as Record<string, unknown>;
  } catch {
    throw new Error(`LIVE STATE UNAVAILABLE: finalized ${label} is malformed.`);
  }
}

export async function getProofPatchV3State(): Promise<ProofPatchV3State> {
  const live = requireConfig();
  const [proposalCountRaw, activeRaw, currentReleaseRaw, currentVersionRaw, currentCodeHashRaw, policyFingerprintRaw, policyKernelHashRaw, policyRaw] = await Promise.all([
    readFinal(live.facade, "get_proposal_count"),
    readFinal(live.facade, "get_active_proposal", [live.target]),
    readFinal(live.facade, "get_current_release_id", [live.target]),
    readFinal(live.facade, "get_current_version", [live.target]),
    readFinal(live.facade, "get_current_code_hash", [live.target]),
    readFinal(live.facade, "get_policy_fingerprint", [live.target]),
    readFinal(live.facade, "get_policy_kernel_hash", [live.target]),
    readFinal(live.facade, "get_state_record", ["policy", live.target]),
  ]);

  const proposalCount = text(proposalCountRaw);
  const activeProposal = text(activeRaw);
  const currentReleaseId = text(currentReleaseRaw);
  const latestId = Number(proposalCount || "0");
  const latestProposal = latestId > 0
    ? parseRecord(await readFinal(live.facade, "get_proposal_summary", [latestId]), "proposal summary")
    : null;
  const release = currentReleaseId
    ? parseRecord(await readFinal(live.facade, "get_release_summary", [currentReleaseId]), "release summary")
    : null;

  return {
    config: live,
    proposalCount,
    activeProposal,
    latestProposal,
    currentReleaseId,
    currentVersion: text(currentVersionRaw),
    currentCodeHash: text(currentCodeHashRaw),
    policyFingerprint: text(policyFingerprintRaw),
    policyKernelHash: text(policyKernelHashRaw),
    policy: parseRecord(policyRaw, "policy record"),
    release,
  };
}

"use client";

import { TransactionHashVariant } from "genlayer-js/types";
import { publicClient } from "@/lib/genlayer";

type HexAddress = `0x${string}`;

export type ProofPatchV2Config = {
  governor: string;
  target: string;
  network: string;
  chainId: string;
};

export type ProofPatchV2State = {
  config: ProofPatchV2Config;
  currentReleaseId: string;
  release: Record<string, unknown> | null;
  activeProposal: string;
  proposalCount: string;
  installedReleaseId: string;
  installedCodeHash: string;
  releaseMode: string;
  kernelHash: string;
  targetGovernor: string;
  owner: string;
};

const config: ProofPatchV2Config = {
  governor: process.env.NEXT_PUBLIC_PROOFPATCH_V2_GOVERNOR ?? "",
  target: process.env.NEXT_PUBLIC_PROOFPATCH_V2_TARGET ?? "",
  network: process.env.NEXT_PUBLIC_PROOFPATCH_V2_NETWORK ?? "Bradbury Testnet",
  chainId: process.env.NEXT_PUBLIC_PROOFPATCH_V2_CHAIN_ID ?? "4221",
};

function requireConfig(): ProofPatchV2Config {
  if (!config.governor || !config.target) {
    throw new Error("LIVE STATE UNAVAILABLE: V2 contract addresses are not configured.");
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

export async function getProofPatchV2State(): Promise<ProofPatchV2State> {
  const live = requireConfig();
  const [proposalCount, activeProposal, currentReleaseId, installedReleaseId, installedCodeHash, releaseMode, kernelHash, targetGovernor, owner] = await Promise.all([
    readFinal(live.governor, "get_proposal_count"),
    readFinal(live.governor, "get_active_proposal", [live.target]),
    readFinal(live.governor, "get_current_release_id", [live.target]),
    readFinal(live.target, "proofpatch_installed_release_id"),
    readFinal(live.target, "proofpatch_installed_candidate_hash"),
    readFinal(live.target, "proofpatch_release_mode"),
    readFinal(live.target, "get_proofpatch_kernel_hash"),
    readFinal(live.target, "get_proofpatch_governor"),
    readFinal(live.target, "get_owner"),
  ]);

  const releaseId = text(currentReleaseId);
  let release: Record<string, unknown> | null = null;
  if (releaseId) {
    const raw = text(await readFinal(live.governor, "get_release_summary", [releaseId]));
    try {
      release = JSON.parse(raw) as Record<string, unknown>;
    } catch {
      throw new Error("LIVE STATE UNAVAILABLE: finalized release summary is malformed.");
    }
  }

  return {
    config: live,
    currentReleaseId: releaseId,
    release,
    activeProposal: text(activeProposal),
    proposalCount: text(proposalCount),
    installedReleaseId: text(installedReleaseId),
    installedCodeHash: text(installedCodeHash),
    releaseMode: text(releaseMode),
    kernelHash: text(kernelHash),
    targetGovernor: text(targetGovernor),
    owner: text(owner),
  };
}

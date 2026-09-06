"use client";

import { useQuery } from "@tanstack/react-query";
import {
  getCanonicalFinalityChain,
  getProofPatchLiveState,
  getProposalActionGateState,
  getProposalWorkspaceState,
} from "@/lib/genlayer";

export function useProofPatchLiveState() {
  return useQuery({
    queryKey: ["proofpatch", "live-state"],
    queryFn: getProofPatchLiveState,
    staleTime: 30_000,
    refetchInterval: 60_000,
    refetchOnWindowFocus: true,
    retry: 1,
  });
}

export function useCanonicalFinalityChain() {
  return useQuery({
    queryKey: ["proofpatch", "finality-chain"],
    queryFn: getCanonicalFinalityChain,
    staleTime: 45_000,
    refetchInterval: 90_000,
    refetchOnWindowFocus: true,
    retry: 1,
  });
}

export function useProposalWorkspaceState() {
  return useQuery({
    queryKey: ["proofpatch", "proposal-workspace"],
    queryFn: getProposalWorkspaceState,
    staleTime: 20_000,
    refetchInterval: 45_000,
    refetchOnWindowFocus: true,
    retry: 1,
  });
}

export function useProposalActionGateState() {
  return useQuery({
    queryKey: ["proofpatch", "proposal-action-gate"],
    queryFn: getProposalActionGateState,
    staleTime: 10_000,
    refetchInterval: 30_000,
    refetchOnWindowFocus: true,
    retry: 1,
  });
}

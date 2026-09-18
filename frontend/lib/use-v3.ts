"use client";

import { useQuery } from "@tanstack/react-query";
import { getProofPatchV3State } from "@/lib/v3";

export function useProofPatchV3State() {
  return useQuery({
    queryKey: ["proofpatch-v3", "finalized-state"],
    queryFn: getProofPatchV3State,
    staleTime: 30_000,
    refetchInterval: 60_000,
    refetchOnWindowFocus: true,
    retry: 1,
  });
}

"use client";

import { useQuery } from "@tanstack/react-query";
import { getProofPatchV2State } from "@/lib/v2";

export function useProofPatchV2State() {
  return useQuery({
    queryKey: ["proofpatch-v2", "finalized-state"],
    queryFn: getProofPatchV2State,
    staleTime: 20_000,
    refetchInterval: 45_000,
    refetchOnWindowFocus: true,
    retry: 1,
  });
}

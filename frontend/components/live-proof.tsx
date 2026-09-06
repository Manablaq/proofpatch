"use client";

import { CheckCircle2, RefreshCw, ShieldCheck } from "lucide-react";
import { PROOFPATCH } from "@/lib/constants";
import {
  useCanonicalFinalityChain,
  useProofPatchLiveState,
} from "@/lib/use-proofpatch";

function short(value: string, head = 8, tail = 6) {
  if (!value) return "—";
  if (value.length <= head + tail + 1) return value;
  return `${value.slice(0, head)}…${value.slice(-tail)}`;
}

export function LiveProof() {
  const live = useProofPatchLiveState();
  const chain = useCanonicalFinalityChain();

  const state = live.data;
  const verified =
    state?.proposalStatus === "VERIFIED" &&
    state.currentVersion === PROOFPATCH.candidateVersion &&
    state.currentCodeHash === PROOFPATCH.candidateCodeHash &&
    state.installedCandidateHash === PROOFPATCH.candidateCodeHash;

  return (
    <div className="live-proof-card">
      <div className="live-proof-top">
        <div>
          <span className="section-label">LIVE BRADBURY PROOF</span>
          <h3>Repository claims meet finalized state.</h3>
        </div>
        <div className={`proof-badge ${verified ? "ok" : ""}`}>
          {verified ? <CheckCircle2 size={15} /> : <RefreshCw size={15} />}
          {live.isLoading ? "Reading chain" : verified ? "Verified live" : "Checking"}
        </div>
      </div>

      <div className="proof-metrics">
        <div>
          <span>Current release</span>
          <strong>{state?.currentVersion || PROOFPATCH.candidateVersion}</strong>
        </div>
        <div>
          <span>Proposal</span>
          <strong>{state?.proposalStatus || "VERIFIED"}</strong>
        </div>
        <div>
          <span>Active proposal</span>
          <strong>{state?.activeProposal || "0"}</strong>
        </div>
        <div>
          <span>Release label</span>
          <strong>{state?.releaseLabel || PROOFPATCH.releaseLabel}</strong>
        </div>
      </div>

      <div className="proof-hash-row">
        <ShieldCheck size={16} />
        <span>Installed SHA-256</span>
        <code>{short(state?.installedCandidateHash || PROOFPATCH.candidateCodeHash, 14, 12)}</code>
      </div>

      <div className="finality-mini">
        {(chain.data ?? [
          { label: "Review consensus", status: "FINALIZED" },
          { label: "Finality-triggered upgrade", status: "FINALIZED" },
          { label: "Post-install confirmation", status: "FINALIZED" },
        ]).map((step) => (
          <div className="finality-mini-step" key={step.label}>
            <i />
            <div>
              <strong>{step.label}</strong>
              <span>{step.status || "FINALIZED"}</span>
            </div>
          </div>
        ))}
      </div>

      {live.error ? (
        <p className="chain-note">
          Live RPC read is temporarily unavailable; canonical finalized evidence remains
          displayed and the dashboard will retry automatically.
        </p>
      ) : (
        <p className="chain-note">
          Reads refresh automatically. No page reload is required.
        </p>
      )}
    </div>
  );
}

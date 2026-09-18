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
    Boolean(state) &&
    !live.isError &&
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
          {live.isLoading ? "Reading chain" : live.isError ? "Unavailable" : verified ? "Verified live" : "Checking"}
        </div>
      </div>

      <div className="proof-metrics">
        <div>
          <span>Current release</span>
          <strong>{state?.currentVersion || "—"}</strong>
        </div>
        <div>
          <span>Proposal</span>
          <strong>{state?.proposalStatus || "—"}</strong>
        </div>
        <div>
          <span>Active proposal</span>
          <strong>{state?.activeProposal || "—"}</strong>
        </div>
        <div>
          <span>Release label</span>
          <strong>{state?.releaseLabel || "—"}</strong>
        </div>
      </div>

      <div className="proof-hash-row">
        <ShieldCheck size={16} />
        <span>Installed SHA-256</span>
        <code>{short(state?.installedCandidateHash || "", 14, 12)}</code>
      </div>

      <div className="finality-mini">
        {(chain.data ?? []).map((step) => (
          <div className="finality-mini-step" key={step.label}>
            <i />
            <div>
              <strong>{step.label}</strong>
            <span>{step.status || "Unavailable"}</span>
            </div>
          </div>
        ))}
        {!chain.data?.length ? <p className="chain-note">Finality reads are unavailable.</p> : null}
      </div>

      {live.error ? (
        <p className="chain-note">
          Live RPC read is temporarily unavailable; contract state remains hidden and the
          dashboard will retry automatically.
        </p>
      ) : (
        <p className="chain-note">
          Reads refresh automatically. No page reload is required.
        </p>
      )}
    </div>
  );
}

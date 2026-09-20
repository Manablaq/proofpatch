"use client";

import { CheckCircle2, RefreshCw, ShieldCheck } from "lucide-react";
import { PROOFPATCH_V3 } from "@/lib/constants";
import { useProofPatchV3State } from "@/lib/use-v3";

function short(value: string, head = 8, tail = 6) {
  if (!value) return "—";
  if (value.length <= head + tail + 1) return value;
  return `${value.slice(0, head)}…${value.slice(-tail)}`;
}

function text(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (value === null || value === undefined) return "";
  return String(value);
}

export function LiveProof() {
  const live = useProofPatchV3State();
  const state = live.data;

  const releaseStatus = text(state?.release?.status);
  const policyTarget = text(state?.policy?.target);

  const verified =
    Boolean(state) &&
    !live.isError &&
    state?.currentReleaseId === PROOFPATCH_V3.rootReleaseId &&
    state?.currentVersion === PROOFPATCH_V3.version &&
    state?.currentCodeHash === PROOFPATCH_V3.codeHash &&
    state?.policyFingerprint === PROOFPATCH_V3.policyFingerprint &&
    policyTarget.toLowerCase() === PROOFPATCH_V3.target.toLowerCase() &&
    releaseStatus === PROOFPATCH_V3.releaseStatus &&
    state?.proposalCount === String(PROOFPATCH_V3.proposalCount) &&
    state?.activeProposal === String(PROOFPATCH_V3.activeProposal);

  return (
    <div className="live-proof-card">
      <div className="live-proof-top">
        <div>
          <span className="section-label">LIVE BRADBURY PROOF</span>
          <h3>Repository claims meet finalized V3 state.</h3>
        </div>

        <div className={`proof-badge ${verified ? "ok" : ""}`}>
          {verified ? <CheckCircle2 size={15} /> : <RefreshCw size={15} />}
          {live.isLoading
            ? "Reading chain"
            : live.isError
              ? "Unavailable"
              : verified
                ? "Verified live"
                : "Checking"}
        </div>
      </div>

      <div className="proof-metrics">
        <div>
          <span>Current release</span>
          <strong>{state?.currentVersion || "—"}</strong>
        </div>
        <div>
          <span>Registration</span>
          <strong>{releaseStatus || "—"}</strong>
        </div>
        <div>
          <span>Active proposal</span>
          <strong>{state?.activeProposal || "—"}</strong>
        </div>
        <div>
          <span>Release ID</span>
          <strong>{state?.currentReleaseId || "—"}</strong>
        </div>
      </div>

      <div className="proof-hash-row">
        <ShieldCheck size={16} />
        <span>Registered SHA-256</span>
        <code>{short(state?.currentCodeHash || "", 14, 12)}</code>
      </div>

      <div className="finality-mini">
        <div className="finality-mini-step">
          <i />
          <div>
            <strong>Registration record</strong>
            <span>{releaseStatus || "Unavailable"}</span>
          </div>
        </div>

        <div className="finality-mini-step">
          <i />
          <div>
            <strong>Policy fingerprint</strong>
            <span>{short(state?.policyFingerprint || "", 12, 10)}</span>
          </div>
        </div>

        <div className="finality-mini-step">
          <i />
          <div>
            <strong>Active slot</strong>
            <span>{state?.activeProposal === "0" ? "CLEAR" : state?.activeProposal || "Unavailable"}</span>
          </div>
        </div>
      </div>

      {live.error ? (
        <p className="chain-note">
          Live RPC read is temporarily unavailable; finalized contract state remains
          hidden and the dashboard will retry automatically.
        </p>
      ) : (
        <p className="chain-note">
          Reads use finalized Bradbury state. No historical V1 value is substituted.
        </p>
      )}
    </div>
  );
}

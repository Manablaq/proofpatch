"use client";

import Link from "next/link";
import { useState } from "react";
import { RefreshCw, ShieldCheck, TriangleAlert } from "lucide-react";
import { getNativeAppealState, type NativeAppealState } from "@/lib/genlayer";
import { useProofPatchV2State } from "@/lib/use-v2";

function short(value: string) {
  return value ? `${value.slice(0, 12)}…${value.slice(-10)}` : "—";
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div className="data-value">
      <span>{label}</span>
      <strong className="mono">{value || "—"}</strong>
    </div>
  );
}

export function V2Console() {
  const state = useProofPatchV2State();
  const data = state.data;
  const releaseStatus = String(data?.release?.status ?? "UNKNOWN");
  const error = state.error instanceof Error ? state.error.message : "";
  const [appealHash, setAppealHash] = useState("");
  const [appealState, setAppealState] = useState<NativeAppealState | null>(null);
  const [appealError, setAppealError] = useState("");
  const [appealBusy, setAppealBusy] = useState(false);

  async function inspectAppeal() {
    setAppealError("");
    setAppealState(null);
    setAppealBusy(true);
    try {
      setAppealState(await getNativeAppealState(appealHash));
    } catch (value) {
      setAppealError(value instanceof Error ? value.message : "Native appeal state is unavailable.");
    } finally {
      setAppealBusy(false);
    }
  }

  return (
    <main className="app-frame">
      <aside className="app-sidebar">
        <Link href="/" className="brand compact"><span className="brand-glyph" aria-hidden><i /><i /><i /></span><span>ProofPatch</span></Link>
        <div className="sidebar-label">V2 HISTORY</div>
        <nav><a className="active" href="#overview"><ShieldCheck size={17} /><span>Release assurance</span></a><a href="#lineage"><RefreshCw size={17} /><span>Lineage</span></a></nav>
        <div className="sidebar-spacer" />
        <Link className="sidebar-docs" href="/app">Current V3</Link>
      </aside>
      <section className="app-main" id="overview">
        <header className="app-topbar"><div><span className="breadcrumb">ProofPatch V2 / historical finalized read console</span><strong>Superseded release evidence</strong></div></header>
        <div className="dashboard-content">
          <section className="hero-panel">
            <div><span className="eyebrow">LIVE CHAIN STATE</span><h1>{data?.releaseMode ?? "LIVE STATE UNAVAILABLE"}</h1><p>Installation, certification, incident and recovery state come from finalized contract reads.</p></div>
            <span className={`status-chip ${data ? "verified" : "pending"}`}>{data ? releaseStatus : "UNAVAILABLE"}</span>
          </section>
          <section className="notice-panel historical-notice">
            <ShieldCheck size={18} />
            <div>
              <strong>Historical V2 surface</strong>
              <p>
                V3 is the canonical deployment. This route is retained for
                provenance and finalized reads only; transaction writes are disabled.
              </p>
            </div>
          </section>
          {error ? <section className="notice-panel"><TriangleAlert size={18} /><div><strong>Live state unavailable</strong><p>{error}</p></div></section> : null}
          <section className="metric-grid">
            <Field label="Network" value={data?.config.network ?? "—"} />
            <Field label="Chain ID" value={data?.config.chainId ?? "—"} />
            <Field label="Current release" value={data?.currentReleaseId ?? "—"} />
            <Field label="Active proposal" value={data?.activeProposal ?? "0"} />
          </section>
          <section className="panel-grid" id="lineage">
            <article className="panel"><div className="panel-heading"><span>Release record</span><ShieldCheck size={17} /></div><Field label="Version" value={String(data?.release?.version ?? "—")} /><Field label="Status" value={releaseStatus} /><Field label="Code hash" value={short(String(data?.release?.code_hash ?? ""))} /><Field label="Lineage hash" value={short(String(data?.release?.lineage_hash ?? ""))} /></article>
            <article className="panel"><div className="panel-heading"><span>ProofPatch kernel</span><ShieldCheck size={17} /></div><Field label="Kernel hash" value={short(data?.kernelHash ?? "")} /><Field label="Installed release" value={data?.installedReleaseId ?? "—"} /><Field label="Installed hash" value={short(data?.installedCodeHash ?? "")} /><Field label="Governor binding" value={data?.targetGovernor ?? "—"} /></article>
          </section>
          <section className="panel appeal-panel" id="appeal">
            <div className="panel-heading"><span>Native appeal inspector</span><RefreshCw size={17} /></div>
            <p>Read-only inspection of historical consensus transactions. Eligibility, bond and lifecycle are read from GenLayer; this historical surface does not submit an appeal.</p>
            <label className="field-label" htmlFor="appeal-hash">Consensus transaction hash</label>
            <input id="appeal-hash" className="text-input mono" value={appealHash} onChange={(event) => setAppealHash(event.target.value)} placeholder="0x…" />
            <div className="lifecycle-actions">
              <button className="button secondary" type="button" onClick={inspectAppeal} disabled={appealBusy || !appealHash.trim()}>{appealBusy ? "Inspecting…" : "Inspect lifecycle"}</button>

            </div>
            {appealState ? <div className="metric-grid appeal-metrics"><Field label="Decision status" value={appealState.status} /><Field label="Execution" value={appealState.execution} /><Field label="Lifecycle" value={appealState.lifecycle || "—"} /><Field label="Appeal bond" value={appealState.appealBond} /><Field label="Eligibility" value={appealState.appealable ? "APPEALABLE" : "NOT APPEALABLE"} /></div> : null}
            {appealError ? <p className="error-copy">{appealError}</p> : null}
          </section>
        </div>
      </section>
    </main>
  );
}

"use client";

import Link from "next/link";
import { RefreshCw, ShieldCheck, TriangleAlert } from "lucide-react";
import { useState } from "react";
import {
  appealNativeTransaction,
  connectBradburyWallet,
  getNativeAppealState,
  type NativeAppealState,
} from "@/lib/genlayer";
import { useProofPatchV3State } from "@/lib/use-v3";

function short(value: string) {
  return value ? `${value.slice(0, 12)}…${value.slice(-10)}` : "—";
}

function valueOf(value: unknown) {
  if (typeof value === "string" && value) return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return "—";
}

function Field({ label, value }: { label: string; value: string }) {
  return <div className="data-value"><span>{label}</span><strong className="mono">{value || "—"}</strong></div>;
}

export function V3Console() {
  const state = useProofPatchV3State();
  const data = state.data;
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

  async function submitAppeal() {
    setAppealError("");
    setAppealBusy(true);
    try {
      const address = await connectBradburyWallet();
      await appealNativeTransaction(appealHash, address);
      setAppealState(await getNativeAppealState(appealHash));
    } catch (value) {
      setAppealError(value instanceof Error ? value.message : "Native appeal submission failed.");
    } finally {
      setAppealBusy(false);
    }
  }

  const unavailable = state.isError || (!state.isLoading && !data);
  const latest = data?.latestProposal;
  const release = data?.release;
  const policy = data?.policy;

  return (
    <main className="app-frame">
      <aside className="app-sidebar">
        <Link href="/" className="brand compact"><span className="brand-glyph" aria-hidden><i /><i /><i /></span><span>ProofPatch</span></Link>
        <div className="sidebar-label">V3 CONSOLE</div>
        <nav><a className="active" href="#overview"><ShieldCheck size={17} /><span>Release assurance</span></a><a href="#appeal"><RefreshCw size={17} /><span>Native appeal</span></a></nav>
        <div className="sidebar-spacer" />
        <Link className="sidebar-docs" href="/legacy">Legacy workspace</Link>
      </aside>
      <section className="app-main" id="overview">
        <header className="app-topbar"><div><span className="breadcrumb">ProofPatch V3 / finalized read console</span><strong>Modular release assurance</strong></div></header>
        <div className="dashboard-content">
          <section className="hero-panel">
            <div><span className="eyebrow">LIVE CHAIN STATE</span><h1>{data?.release?.status ? valueOf(data.release.status) : unavailable ? "LIVE STATE UNAVAILABLE" : "NO RELEASE REGISTERED"}</h1><p>All values below come from finalized reads through the deployed V3 facade. No historical value is substituted after a read failure.</p></div>
            <span className={`status-chip ${data ? "verified" : "pending"}`}>{data ? "FINALIZED READ" : "UNAVAILABLE"}</span>
          </section>
          {error ? <section className="notice-panel"><TriangleAlert size={18} /><div><strong>Live state unavailable</strong><p>{error}</p></div></section> : null}
          <section className="metric-grid">
            <Field label="Network" value={data?.config.network ?? "—"} />
            <Field label="Chain ID" value={data?.config.chainId ?? "—"} />
            <Field label="Proposal count" value={data?.proposalCount ?? "—"} />
            <Field label="Active proposal" value={data?.activeProposal ?? "—"} />
          </section>
          <section className="panel-grid">
            <article className="panel"><div className="panel-heading"><span>Current release</span><ShieldCheck size={17} /></div><Field label="Release ID" value={data?.currentReleaseId ?? "—"} /><Field label="Version" value={data?.currentVersion ?? "—"} /><Field label="Code hash" value={short(data?.currentCodeHash ?? "")} /><Field label="Lineage hash" value={short(valueOf(release?.lineage_hash))} /></article>
            <article className="panel"><div className="panel-heading"><span>Policy binding</span><ShieldCheck size={17} /></div><Field label="Policy fingerprint" value={short(data?.policyFingerprint ?? "")} /><Field label="Kernel hash" value={short(data?.policyKernelHash ?? "")} /><Field label="Owner" value={short(valueOf(policy?.owner))} /><Field label="Target" value={short(valueOf(policy?.target))} /></article>
          </section>
          <section className="panel-grid">
            <article className="panel"><div className="panel-heading"><span>Latest proposal</span><ShieldCheck size={17} /></div><Field label="Status" value={valueOf(latest?.status)} /><Field label="Candidate hash" value={short(valueOf(latest?.candidate_code_hash))} /><Field label="Evidence hash" value={short(valueOf(latest?.evidence_set_hash))} /></article>
            <article className="panel"><div className="panel-heading"><span>Release record</span><ShieldCheck size={17} /></div><Field label="Status" value={valueOf(release?.status)} /><Field label="Proposal ID" value={valueOf(release?.proposal_id)} /><Field label="Recovery incident" value={valueOf(release?.recovery_incident_id)} /></article>
          </section>
          <section className="panel appeal-panel" id="appeal">
            <div className="panel-heading"><span>Native GenLayer appeal</span><RefreshCw size={17} /></div>
            <p>Inspect the actual consensus transaction before signing. Eligibility and bond are read from GenLayer’s finalized appeal system.</p>
            <label className="field-label" htmlFor="appeal-hash">Consensus transaction hash</label>
            <input id="appeal-hash" className="text-input mono" value={appealHash} onChange={(event) => setAppealHash(event.target.value)} placeholder="0x…" />
            <div className="lifecycle-actions"><button className="button secondary" type="button" onClick={inspectAppeal} disabled={appealBusy || !appealHash.trim()}>{appealBusy ? "Inspecting…" : "Inspect lifecycle"}</button>{appealState?.appealable ? <button className="button primary" type="button" onClick={submitAppeal} disabled={appealBusy}>Appeal with native bond</button> : null}</div>
            {appealState ? <div className="metric-grid appeal-metrics"><Field label="Decision status" value={appealState.status} /><Field label="Execution" value={appealState.execution} /><Field label="Lifecycle" value={appealState.lifecycle || "—"} /><Field label="Appeal bond" value={appealState.appealBond} /><Field label="Eligibility" value={appealState.appealable ? "APPEALABLE" : "NOT APPEALABLE"} /></div> : null}
            {appealError ? <p className="error-copy">{appealError}</p> : null}
          </section>
        </div>
      </section>
    </main>
  );
}

"use client";

import {
  Activity,
  ArrowUpRight,
  BookOpen,
  CheckCircle2,
  CircleDot,
  Copy,
  FileCheck2,
  Fingerprint,
  Gauge,
  Hash,
  LayoutDashboard,
  RefreshCw,
  ShieldCheck,
  TerminalSquare,
  Workflow,
} from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";
import { APP_NAV, PROOFPATCH, SECURITY_GATES } from "@/lib/constants";
import {
  useCanonicalFinalityChain,
  useProofPatchLiveState,
} from "@/lib/use-proofpatch";
import { ThemeToggle } from "@/components/theme-toggle";
import { WalletButton } from "@/components/wallet-button";
import { CommandPalette } from "@/components/command-palette";
import { ProposalWorkspace } from "@/components/proposal-workspace";
import { TransactionCenter } from "@/components/transaction-center";

function short(value: string, head = 10, tail = 8) {
  if (!value) return "—";
  return `${value.slice(0, head)}…${value.slice(-tail)}`;
}

async function copy(value: string, label: string) {
  try {
    await navigator.clipboard.writeText(value);
    toast.success(`${label} copied`);
  } catch {
    toast.error("Clipboard permission was denied");
  }
}

function DataValue({
  label,
  value,
  mono = false,
  copyable = false,
}: {
  label: string;
  value: string;
  mono?: boolean;
  copyable?: boolean;
}) {
  return (
    <div className="data-value">
      <span>{label}</span>
      <div>
        <strong className={mono ? "mono" : ""}>{value || "—"}</strong>
        {copyable && value ? (
          <button onClick={() => copy(value, label)} aria-label={`Copy ${label}`}>
            <Copy size={14} />
          </button>
        ) : null}
      </div>
    </div>
  );
}

export function Dashboard({ readOnly = false }: { readOnly?: boolean }) {
  const live = useProofPatchLiveState();
  const finality = useCanonicalFinalityChain();

  const state = live.data;
  const stateAvailable = Boolean(state) && !live.isError;

  const invariantCount = [
    state?.proposalStatus === "VERIFIED",
    state?.currentVersion === PROOFPATCH.candidateVersion,
    state?.currentCodeHash === PROOFPATCH.candidateCodeHash,
    state?.installedProposalId === String(PROOFPATCH.proposalId),
    state?.installedCandidateHash === PROOFPATCH.candidateCodeHash,
    state?.releaseLabel === PROOFPATCH.releaseLabel,
    state?.owner?.toLowerCase() === PROOFPATCH.owner.toLowerCase(),
    state?.governor?.toLowerCase() === PROOFPATCH.governor.toLowerCase(),
    state?.productName === PROOFPATCH.productName,
    state?.protectedValue === PROOFPATCH.protectedValue,
  ].filter(Boolean).length;

  return (
    <div className="app-frame">
      <aside className="app-sidebar">
        <Link href="/" className="brand compact">
          <span className="brand-glyph" aria-hidden>
            <i />
            <i />
            <i />
          </span>
          <span>ProofPatch</span>
        </Link>

        <div className="sidebar-label">WORKSPACE</div>
        <nav>
          {APP_NAV.map((item, index) => {
            const icons = [
              LayoutDashboard,
              Workflow,
              FileCheck2,
              Fingerprint,
              TerminalSquare,
            ];
            const Icon = icons[index] ?? CircleDot;
            return (
              <a href={`#${item.id}`} key={item.id} className={index === 0 ? "active" : ""}>
                <Icon size={17} />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>

        <div className="sidebar-spacer" />

        <div className="sidebar-network">
          <div>
            <i />
            <span>Bradbury</span>
          </div>
          <small>Chain 4221 · GEN</small>
        </div>

        <Link className="sidebar-docs" href="/#documentation">
          <BookOpen size={16} />
          Documentation
        </Link>
      </aside>

      <main className="app-main">
        <header className="app-topbar">
          <div>
            <span className="breadcrumb">Protected targets / Live deployment</span>
            <strong>ProofPatch Protected Target</strong>
          </div>
          <div className="topbar-actions">
            <button
              className="command-trigger"
              onClick={() =>
                window.dispatchEvent(
                  new KeyboardEvent("keydown", { key: "k", metaKey: true }),
                )
              }
            >
              <span>Search</span>
              <kbd>⌘ K</kbd>
            </button>
            <ThemeToggle />
            {readOnly ? (
              <span className="status-chip historical-chip">Historical read-only</span>
            ) : (
              <WalletButton />
            )}
          </div>
        </header>

        <div className="app-content">
          <section id="overview" className="dashboard-hero">
            <div>
              <div className="eyebrow-row">
                <span className="live-dot" />
                {readOnly
                  ? "HISTORICAL FINALIZED EVIDENCE"
                  : stateAvailable
                    ? "FINALIZED BRADBURY STATE"
                    : "BRADBURY STATE UNAVAILABLE"}
              </div>
              <h1>
                {readOnly ? (
                  <>Historical <em>proof.</em></>
                ) : (
                  <>Upgrade <em>verified.</em></>
                )}
              </h1>
              <p>
                {readOnly
                  ? "This superseded deployment is preserved as finalized historical evidence. Its proposal and lifecycle write controls are intentionally disabled."
                  : "Every value in this workspace is read from finalized Bradbury state. Values remain unavailable until the read succeeds."}
              </p>
              <div className="hero-actions">
                <a
                  href={PROOFPATCH.network.explorer}
                  target="_blank"
                  rel="noreferrer"
                  className="button primary"
                >
                  Open Bradbury explorer <ArrowUpRight size={16} />
                </a>
                <button
                  className="button secondary"
                  onClick={() => {
                    void live.refetch();
                    void finality.refetch();
                  }}
                >
                  <RefreshCw size={16} />
                  Refresh reads
                </button>
              </div>
            </div>

            <div className="verification-orb">
              <div className="orb-ring ring-one" />
              <div className="orb-ring ring-two" />
              <div className="orb-core">
                <ShieldCheck size={34} />
                <strong>{stateAvailable ? state?.proposalStatus : "UNAVAILABLE"}</strong>
                <span>install state</span>
              </div>
            </div>
          </section>

          {live.isError ? (
            <div className="rpc-warning">
              <Activity size={17} />
              Bradbury read is temporarily unavailable. Contract state is hidden until
              a finalized read succeeds; no write is retried.
            </div>
          ) : null}

          <section className="metric-grid">
            <article>
              <span>Current version</span>
              <strong>{stateAvailable ? state?.currentVersion : "—"}</strong>
              <small>{stateAvailable ? `advanced from ${PROOFPATCH.parentVersion}` : "read unavailable"}</small>
            </article>
            <article>
              <span>Final invariants</span>
              <strong>{stateAvailable ? `${invariantCount}/10` : "—"}</strong>
              <small>{stateAvailable ? "storage + authority preserved" : "read unavailable"}</small>
            </article>
            <article>
              <span>Active proposal</span>
              <strong>{stateAvailable ? state?.activeProposal : "—"}</strong>
              <small>{stateAvailable ? "release lock state" : "read unavailable"}</small>
            </article>
            <article>
              <span>Network</span>
              <strong>Bradbury</strong>
              <small>GenLayer testnet · 4221</small>
            </article>
          </section>

          {readOnly ? (
            <section className="historical-banner" aria-label="Historical workspace notice">
              <ShieldCheck size={18} />
              <div>
                <strong>Historical deployment — read only</strong>
                <p>
                  The canonical product is ProofPatch V3. This workspace remains
                  available only to inspect the superseded finalized deployment;
                  proposal creation, repair and lifecycle writes are not exposed here.
                </p>
              </div>
              <Link className="button secondary" href="/app">
                Open current V3
              </Link>
            </section>
          ) : (
            <ProposalWorkspace />
          )}

          <section className="dashboard-grid two">
            <article className="dash-card" id="finality">
              <div className="dash-card-head">
                <div>
                  <span className="card-label">FINALITY PROOF</span>
                  <h2>Consequence only after finality.</h2>
                </div>
                <span className="status-chip verified">
                  <CheckCircle2 size={14} /> Complete
                </span>
              </div>
              <div className="finality-list">
                {(finality.data ?? []).map((item, index) => (
                  <div className="finality-row" key={item.hash}>
                    <div className="step-index">{String(index + 1).padStart(2, "0")}</div>
                    <div className="step-copy">
                      <strong>{item.label}</strong>
                      <code>{short(item.hash, 12, 10)}</code>
                    </div>
                    <div className="step-result">
                      <span>{item.status || "Unavailable"}</span>
                      <small>{item.execution || "—"}</small>
                    </div>
                  </div>
                ))}
                {!finality.data?.length ? (
                  <div className="finality-row">
                    <div className="step-index">—</div>
                    <div className="step-copy"><strong>Finality chain unavailable</strong><code>Awaiting finalized reads</code></div>
                    <div className="step-result"><span>Unavailable</span><small>—</small></div>
                  </div>
                ) : null}
              </div>
            </article>

            <article className="dash-card code-card">
              <div className="dash-card-head">
                <div>
                  <span className="card-label">EXACT BYTE IDENTITY</span>
                  <h2>One hash. Three independent checks.</h2>
                </div>
                <Hash size={20} />
              </div>
              <div className="hash-display">
                <span>approved_candidate_sha256</span>
                <code>{stateAvailable ? state?.currentCodeHash : "UNAVAILABLE"}</code>
                <button
                  onClick={() =>
                    copy(
                      stateAvailable ? state?.currentCodeHash ?? "" : "",
                      "Candidate SHA-256",
                    )
                  }
                >
                  <Copy size={15} /> Copy full hash
                </button>
              </div>
              <div className="hash-checks">
                <div><CheckCircle2 size={16} /><span>Governor current hash</span></div>
                <div><CheckCircle2 size={16} /><span>Target installed hash</span></div>
                <div><CheckCircle2 size={16} /><span>Local approved source hash</span></div>
              </div>
            </article>
          </section>

          <section className="dashboard-grid two">
            <article className="dash-card" id="evidence">
              <div className="dash-card-head">
                <div>
                  <span className="card-label">EVIDENCE BINDING</span>
                  <h2>Trust is part of the policy.</h2>
                </div>
                <FileCheck2 size={20} />
              </div>

              <div className="data-stack">
                <DataValue label="Evidence set hash" value={stateAvailable ? state?.evidenceSetHash ?? "" : ""} mono copyable />
                <DataValue label="Policy fingerprint" value={stateAvailable ? state?.policyFingerprint ?? "" : ""} mono copyable />
                <DataValue
                  label="Final audit SHA-256"
                  value={stateAvailable ? PROOFPATCH.evidence.finalAuditSha256 : ""}
                  mono
                  copyable
                />
              </div>
            </article>

            <article className="dash-card" id="policy">
              <div className="dash-card-head">
                <div>
                  <span className="card-label">TARGET INVARIANTS</span>
                  <h2>Upgrade did not rewrite identity.</h2>
                </div>
                <Fingerprint size={20} />
              </div>
              <div className="data-stack compact-stack">
                <DataValue label="Release" value={stateAvailable ? state?.releaseLabel ?? "" : ""} />
                <DataValue label="Owner" value={stateAvailable ? short(state?.owner ?? "") : ""} mono />
                <DataValue label="Governor" value={stateAvailable ? short(state?.governor ?? "") : ""} mono />
                <DataValue
                  label="Protected value"
                  value={stateAvailable ? state?.protectedValue ?? "" : ""}
                  mono
                />
              </div>
            </article>
          </section>

          <section className="dash-card" id="transactions">
            <div className="dash-card-head">
              <div>
                <span className="card-label">TRANSACTION CENTER</span>
                <h2>No blind re-submission.</h2>
              </div>
              <Gauge size={20} />
            </div>
            <TransactionCenter />
          </section>

          <section className="security-grid">
            {SECURITY_GATES.map((gate) => (
              <article key={gate.title}>
                <CheckCircle2 size={17} />
                <strong>{gate.title}</strong>
                <p>{gate.detail}</p>
              </article>
            ))}
          </section>
        </div>
      </main>

      <CommandPalette />
    </div>
  );
}

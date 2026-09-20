"use client";

import Link from "next/link";
import {
  CheckCircle2,
  Copy,
  ExternalLink,
  RefreshCw,
  ShieldCheck,
  TriangleAlert,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  appealNativeTransaction,
  connectBradburyWallet,
  getNativeAppealState,
  type NativeAppealState,
} from "@/lib/genlayer";
import { PROOFPATCH_V3 } from "@/lib/constants";
import { useProofPatchV3State } from "@/lib/use-v3";
import { ThemeToggle } from "@/components/theme-toggle";

function short(value: string, head = 12, tail = 10) {
  if (!value) return "—";
  if (value.length <= head + tail + 1) return value;
  return `${value.slice(0, head)}…${value.slice(-tail)}`;
}

function valueOf(value: unknown) {
  if (typeof value === "string" && value) return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return "—";
}

async function copyText(value: string, label: string) {
  try {
    await navigator.clipboard.writeText(value);
    toast.success(`${label} copied`);
  } catch {
    toast.error("Clipboard permission denied");
  }
}

function Field({
  label,
  value,
  copyable = false,
}: {
  label: string;
  value: string;
  copyable?: boolean;
}) {
  const rendered = value || "—";
  const canCopy = copyable && rendered !== "—";

  return (
    <div className="data-value">
      <span>{label}</span>
      <div className="data-value-row">
        <strong className="mono" title={rendered}>
          {rendered}
        </strong>
        {canCopy ? (
          <button
            type="button"
            className="data-copy"
            aria-label={`Copy ${label}`}
            onClick={() => void copyText(rendered, label)}
          >
            <Copy size={13} />
          </button>
        ) : null}
      </div>
    </div>
  );
}

export function V3Console() {
  const state = useProofPatchV3State();
  const data = state.data;
  const error = state.error instanceof Error ? state.error.message : "";

  const [appealHash, setAppealHash] = useState("");
  const [appealState, setAppealState] = useState<NativeAppealState | null>(null);
  const [appealError, setAppealError] = useState("");
  const [appealBusy, setAppealBusy] = useState(false);
  const [appealConfirmed, setAppealConfirmed] = useState(false);

  useEffect(() => {
    const id = window.location.hash.slice(1);
    if (!id) return;

    const scrollToHash = () => {
      document.getElementById(id)?.scrollIntoView({
        block: "start",
        behavior: "auto",
      });
    };

    const frame = window.requestAnimationFrame(scrollToHash);
    const timer = window.setTimeout(scrollToHash, 120);

    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(timer);
    };
  }, []);

  async function inspectAppeal() {
    setAppealError("");
    setAppealState(null);
    setAppealConfirmed(false);
    setAppealBusy(true);

    try {
      setAppealState(await getNativeAppealState(appealHash));
    } catch (value) {
      setAppealError(
        value instanceof Error
          ? value.message
          : "Native appeal state is unavailable.",
      );
    } finally {
      setAppealBusy(false);
    }
  }

  async function submitAppeal() {
    if (!appealState?.appealable || !appealConfirmed) return;

    setAppealError("");
    setAppealBusy(true);

    try {
      const address = await connectBradburyWallet();
      await appealNativeTransaction(appealHash, address);
      toast.success("Appeal submitted. Re-reading consensus lifecycle.");
      setAppealState(await getNativeAppealState(appealHash));
      setAppealConfirmed(false);
    } catch (value) {
      setAppealError(
        value instanceof Error
          ? value.message
          : "Native appeal submission failed.",
      );
    } finally {
      setAppealBusy(false);
    }
  }

  const loading = state.isLoading && !data;
  const unavailable = state.isError || (!loading && !data);

  const latest = data?.latestProposal;
  const release = data?.release;
  const policy = data?.policy;

  const releaseStatus = valueOf(release?.status);
  const releaseMode = data?.releaseMode ?? "";
  const policyTarget = valueOf(policy?.target);

  const canonicalChecks = data
    ? [
        data.currentReleaseId === PROOFPATCH_V3.rootReleaseId,
        data.currentVersion === PROOFPATCH_V3.version,
        data.currentCodeHash === PROOFPATCH_V3.codeHash,
        data.policyFingerprint === PROOFPATCH_V3.policyFingerprint,
        data.policyKernelHash === PROOFPATCH_V3.kernelHash,
        policyTarget.toLowerCase() === PROOFPATCH_V3.target.toLowerCase(),
        releaseStatus === PROOFPATCH_V3.releaseStatus,
        releaseMode === PROOFPATCH_V3.releaseMode,
        data.proposalCount === String(PROOFPATCH_V3.proposalCount),
        data.activeProposal === String(PROOFPATCH_V3.activeProposal),
      ]
    : [];

  const canonicalPassCount = canonicalChecks.filter(Boolean).length;
  const canonicalMatch =
    canonicalChecks.length > 0 &&
    canonicalPassCount === canonicalChecks.length;

  const headline = loading
    ? "READING FINALITY"
    : unavailable
      ? "STATE UNAVAILABLE"
      : releaseMode || "NO ACTIVE RELEASE";

  const updatedAt =
    data && state.dataUpdatedAt
      ? new Date(state.dataUpdatedAt).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      : "—";

  const registrationSteps = [
    ["Register with ProofPatch", PROOFPATCH_V3.registrationChain.parent],
    ["Register target", PROOFPATCH_V3.registrationChain.registerTarget],
    ["Policy execution", PROOFPATCH_V3.registrationChain.registrationEngine],
    ["Apply policy result", PROOFPATCH_V3.registrationChain.applyPolicyResult],
    ["Confirm registration", PROOFPATCH_V3.registrationChain.confirmation],
  ] as const;

  return (
    <main className="app-frame">
      <aside className="app-sidebar">
        <Link href="/" className="brand compact">
          <span className="brand-glyph" aria-hidden>
            <i />
            <i />
            <i />
          </span>
          <span>ProofPatch</span>
        </Link>

        <div className="sidebar-label">V3 CONSOLE</div>

        <nav aria-label="V3 console">
          <a className="active" href="#overview" aria-current="page">
            <ShieldCheck size={17} />
            <span>Release assurance</span>
          </a>
          <a href="#identity">
            <CheckCircle2 size={17} />
            <span>Deployment proof</span>
          </a>
          <a href="#appeal">
            <RefreshCw size={17} />
            <span>Native appeal</span>
          </a>
        </nav>

        <div className="sidebar-spacer" />

        <div className="sidebar-network">
          <div>
            <i />
            <span>Bradbury</span>
          </div>
          <small>Chain 4221 · finalized reads</small>
        </div>

        <a
          className="sidebar-docs"
          href={PROOFPATCH_V3.network.explorer}
          target="_blank"
          rel="noreferrer"
        >
          <ExternalLink size={15} />
          Explorer
        </a>

        <Link className="sidebar-docs" href="/legacy">
          Historical deployment
        </Link>
      </aside>

      <section className="app-main" id="overview">
        <header className="app-topbar">
          <div>
            <span className="breadcrumb">
              ProofPatch V3 / canonical Bradbury deployment
            </span>
            <strong>Modular release assurance</strong>
          </div>

          <div className="topbar-actions">
            <span className="console-read-time">
              Finalized read · {updatedAt}
            </span>
            <button
              type="button"
              className="console-refresh"
              onClick={() => void state.refetch()}
              disabled={state.isFetching}
              aria-label="Refresh finalized V3 state"
            >
              <RefreshCw
                size={15}
                className={state.isFetching ? "spin" : undefined}
              />
              <span>{state.isFetching ? "Reading…" : "Refresh"}</span>
            </button>
            <ThemeToggle />
          </div>
        </header>

        <div className="dashboard-content">
          <section className="hero-panel" aria-live="polite">
            <div className="hero-panel-copy">
              <span className="eyebrow">LIVE FINALIZED CHAIN STATE</span>
              <h1>{headline}</h1>
              <p>
                Canonical V3 state is read from Bradbury using finalized reads.
                Root registration status and target execution mode are shown
                separately; no historical value is substituted after a read
                failure.
              </p>
            </div>

            <div className="hero-state">
              <span
                className={`status-chip ${
                  canonicalMatch
                    ? "verified"
                    : data
                      ? "warning"
                      : "pending"
                }`}
              >
                {canonicalMatch ? <CheckCircle2 size={14} /> : null}
                {loading
                  ? "READING FINALITY"
                  : unavailable
                    ? "UNAVAILABLE"
                    : canonicalMatch
                      ? "CANONICAL MATCH"
                      : "DRIFT DETECTED"}
              </span>

              <small>
                Root status · {data ? releaseStatus : "—"}
              </small>
            </div>
          </section>

          {error ? (
            <section className="notice-panel" role="alert">
              <TriangleAlert size={18} />
              <div>
                <strong>Finalized state unavailable</strong>
                <p>{error}</p>
              </div>
            </section>
          ) : null}

          {data && !canonicalMatch ? (
            <section className="notice-panel warning-notice" role="status">
              <TriangleAlert size={18} />
              <div>
                <strong>Canonical release drift detected</strong>
                <p>
                  Only {canonicalPassCount}/{canonicalChecks.length} canonical
                  invariants currently match. No stale fallback values are being
                  displayed.
                </p>
              </div>
            </section>
          ) : null}

          <section className="metric-grid" aria-label="Network state">
            <Field label="Network" value={data?.config.network ?? "—"} />
            <Field label="Chain ID" value={data?.config.chainId ?? "—"} />
            <Field label="Proposal count" value={data?.proposalCount ?? "—"} />
            <Field label="Active proposal" value={data?.activeProposal ?? "—"} />
          </section>

          <section className="panel-grid">
            <article className="panel">
              <div className="panel-heading">
                <div>
                  <span className="card-label">CURRENT RELEASE</span>
                  <strong>Installed V3 identity</strong>
                </div>
                <ShieldCheck size={18} />
              </div>

              <Field
                label="Release ID"
                value={data?.currentReleaseId ?? "—"}
                copyable
              />
              <Field label="Version" value={data?.currentVersion ?? "—"} />
              <Field label="Target mode" value={releaseMode || "—"} />
              <Field
                label="Code hash"
                value={data?.currentCodeHash ?? "—"}
                copyable
              />
            </article>

            <article className="panel">
              <div className="panel-heading">
                <div>
                  <span className="card-label">POLICY BINDING</span>
                  <strong>Consequence authority</strong>
                </div>
                <ShieldCheck size={18} />
              </div>

              <Field
                label="Policy fingerprint"
                value={data?.policyFingerprint ?? "—"}
                copyable
              />
              <Field
                label="Kernel hash"
                value={data?.policyKernelHash ?? "—"}
                copyable
              />
              <Field
                label="Owner"
                value={valueOf(policy?.owner)}
                copyable
              />
              <Field
                label="Target"
                value={policyTarget}
                copyable
              />
            </article>
          </section>

          <section className="panel-grid" id="identity">
            <article className="panel">
              <div className="panel-heading">
                <div>
                  <span className="card-label">DEPLOYMENT IDENTITY</span>
                  <strong>Canonical addresses</strong>
                </div>
                <CheckCircle2 size={18} />
              </div>

              <Field
                label="V3 facade"
                value={PROOFPATCH_V3.facade}
                copyable
              />
              <Field
                label="Protected target"
                value={PROOFPATCH_V3.target}
                copyable
              />
              <Field
                label="Root status"
                value={releaseStatus}
              />
              <Field
                label="Canonical checks"
                value={
                  data
                    ? `${canonicalPassCount}/${canonicalChecks.length}`
                    : "—"
                }
              />
            </article>

            <article className="panel">
              <div className="panel-heading">
                <div>
                  <span className="card-label">LATEST PROPOSAL</span>
                  <strong>Current proposal surface</strong>
                </div>
                <ShieldCheck size={18} />
              </div>

              {latest ? (
                <>
                  <Field label="Status" value={valueOf(latest.status)} />
                  <Field
                    label="Candidate hash"
                    value={valueOf(latest.candidate_code_hash)}
                    copyable
                  />
                  <Field
                    label="Evidence hash"
                    value={valueOf(latest.evidence_set_hash)}
                    copyable
                  />
                </>
              ) : (
                <div className="empty-state">
                  <CheckCircle2 size={20} />
                  <div>
                    <strong>No active V3 proposal</strong>
                    <p>
                      Proposal count is {data?.proposalCount ?? "—"} and the
                      active slot is {data?.activeProposal ?? "—"}. The root
                      registration remains the current release.
                    </p>
                  </div>
                </div>
              )}
            </article>
          </section>

          <section className="panel registration-panel">
            <div className="panel-heading">
              <div>
                <span className="card-label">PINNED RELEASE EVIDENCE</span>
                <strong>Finalized registration path</strong>
              </div>
              <span className="status-chip verified">
                <CheckCircle2 size={14} />
                5 / 5 finalized
              </span>
            </div>

            <div className="registration-list">
              {registrationSteps.map(([label, hash], index) => (
                <div className="registration-row" key={hash}>
                  <div className="registration-index">
                    {String(index + 1).padStart(2, "0")}
                  </div>
                  <div>
                    <strong>{label}</strong>
                    <code title={hash}>{short(hash)}</code>
                  </div>
                  <span>FINALIZED</span>
                  <button
                    type="button"
                    className="data-copy"
                    aria-label={`Copy ${label} transaction`}
                    onClick={() => void copyText(hash, `${label} transaction`)}
                  >
                    <Copy size={13} />
                  </button>
                </div>
              ))}
            </div>

            <p className="registration-meta">
              These transaction IDs are the pinned canonical release evidence.
              The live state above is still read independently from finalized
              Bradbury state.
            </p>
          </section>

          <section className="panel appeal-panel" id="appeal">
            <div className="panel-heading">
              <div>
                <span className="card-label">NATIVE CONSENSUS APPEAL</span>
                <strong>Inspect before signing</strong>
              </div>
              <RefreshCw size={18} />
            </div>

            <p>
              Enter an exact GenLayer consensus transaction hash. Eligibility,
              lifecycle and minimum bond are read before any wallet action is
              exposed.
            </p>

            <label className="field-label" htmlFor="appeal-hash">
              Consensus transaction hash
            </label>

            <input
              id="appeal-hash"
              className="text-input mono"
              value={appealHash}
              onChange={(event) => {
                setAppealHash(event.target.value);
                setAppealState(null);
                setAppealError("");
                setAppealConfirmed(false);
              }}
              placeholder="0x…"
              spellCheck={false}
              autoComplete="off"
            />

            <div className="lifecycle-actions">
              <button
                className="button secondary"
                type="button"
                onClick={() => void inspectAppeal()}
                disabled={appealBusy || !appealHash.trim()}
              >
                <RefreshCw size={15} />
                {appealBusy ? "Inspecting…" : "Inspect lifecycle"}
              </button>
            </div>

            {appealState ? (
              <>
                <div className="metric-grid appeal-metrics">
                  <Field label="Decision status" value={appealState.status} />
                  <Field label="Execution" value={appealState.execution} />
                  <Field
                    label="Lifecycle"
                    value={appealState.lifecycle || "—"}
                  />
                  <Field
                    label="Appeal bond"
                    value={appealState.appealBond}
                  />
                  <Field
                    label="Eligibility"
                    value={
                      appealState.appealable
                        ? "APPEALABLE"
                        : "NOT APPEALABLE"
                    }
                  />
                </div>

                {appealState.appealable ? (
                  <div className="appeal-submit-zone">
                    <label className="appeal-confirm">
                      <input
                        type="checkbox"
                        checked={appealConfirmed}
                        onChange={(event) =>
                          setAppealConfirmed(event.target.checked)
                        }
                      />
                      <span>
                        I reviewed this exact transaction and understand that
                        submitting the appeal will request a real Bradbury
                        wallet transaction using the displayed native bond.
                      </span>
                    </label>

                    <button
                      className="button primary"
                      type="button"
                      onClick={() => void submitAppeal()}
                      disabled={
                        appealBusy ||
                        !appealConfirmed
                      }
                    >
                      Appeal with native bond
                    </button>
                  </div>
                ) : null}
              </>
            ) : null}

            {appealError ? (
              <p className="error-copy" role="alert">
                {appealError}
              </p>
            ) : null}
          </section>
        </div>
      </section>
    </main>
  );
}

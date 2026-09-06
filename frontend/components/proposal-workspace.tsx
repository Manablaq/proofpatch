"use client";

import {
  AlertTriangle,
  Ban,
  CheckCircle2,
  Clock3,
  FileCode2,
  LoaderCircle,
  LockKeyhole,
  Play,
  Plus,
  RefreshCw,
  ShieldCheck,
  TimerOff,
  Upload,
  Wrench,
  X,
} from "lucide-react";
import { type ChangeEvent, useEffect, useState } from "react";
import { toast } from "sonner";
import {
  cancelProofPatchProposal,
  createProofPatchProposal,
  expireProofPatchProposal,
  repairProofPatchEvidence,
  reviewProofPatchProposal,
  type ProposalSummary,
} from "@/lib/genlayer";
import {
  EMPTY_PROPOSAL_DRAFT,
  EMPTY_REPAIR_EVIDENCE_DRAFT,
  type ProposalDraft,
  type ProposalPreflight,
  type RepairEvidenceDraft,
  runProposalPreflight,
  runRepairEvidencePreflight,
} from "@/lib/proposal-workflow";
import {
  useProofPatchLiveState,
  useProposalActionGateState,
  useProposalWorkspaceState,
} from "@/lib/use-proofpatch";
import { useTransactionTracker } from "@/lib/transaction-tracker";
import { useWallet } from "@/lib/wallet-context";
import { PROOFPATCH } from "@/lib/constants";

type LifecycleKind = "review" | "cancel" | "expire";

type LifecycleSelection = {
  kind: LifecycleKind;
  proposal: ProposalSummary;
};

function short(value: string) {
  return value ? `${value.slice(0, 12)}…${value.slice(-10)}` : "—";
}

function idOf(summary: ProposalSummary) {
  return Number(summary.proposal_id ?? 0);
}

function statusOf(summary: ProposalSummary) {
  return String(summary.status ?? "UNKNOWN");
}

function terminalTransaction(status: string) {
  const value = status.replaceAll("_", "").replaceAll(" ", "").toUpperCase();
  return value === "FINALIZED" || value === "CANCELED" || value === "CANCELLED";
}

function statusTone(status: string) {
  if (status === "VERIFIED") return "verified";
  if (status === "UPGRADE_QUEUED") return "queued";
  if (
    status === "EVIDENCE_REPAIR_REQUIRED" ||
    status === "REVIEW_RETRY_REQUIRED"
  ) {
    return "warning";
  }
  if (
    status === "REJECTED" ||
    status === "EXECUTION_FAILED" ||
    status === "EXPIRED" ||
    status === "CANCELLED"
  ) {
    return "danger";
  }
  return "neutral";
}

function formatUtc(seconds: number) {
  if (!Number.isFinite(seconds) || seconds <= 0) return "";
  return new Date(seconds * 1000)
    .toISOString()
    .replace("T", " ")
    .replace(".000Z", " UTC");
}

function Preflight({ result }: { result: ProposalPreflight }) {
  return (
    <div className={`preflight-list ${result.passed ? "passed" : ""}`}>
      <div className="preflight-summary">
        {result.passed ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
        <strong>
          {result.passed ? "All frontend gates passed" : "Blocking checks remain"}
        </strong>
        <code>{result.candidateHash}</code>
      </div>
      <div className="preflight-checks">
        {result.checks.map((check, index) => (
          <div
            className={check.ok ? "ok" : "bad"}
            key={`${check.label}-${index}`}
          >
            {check.ok ? (
              <CheckCircle2 size={13} />
            ) : (
              <AlertTriangle size={13} />
            )}
            <span>{check.label}</span>
            <small>{check.detail}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export function ProposalWorkspace() {
  const live = useProofPatchLiveState();
  const actionGate = useProposalActionGateState();
  const workspace = useProposalWorkspaceState();
  const wallet = useWallet();
  const tracker = useTransactionTracker();

  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState<ProposalDraft>(EMPTY_PROPOSAL_DRAFT);
  const [preflight, setPreflight] = useState<ProposalPreflight | null>(null);
  const [busy, setBusy] = useState<"preflight" | "submit" | "">("");

  const [repairProposal, setRepairProposal] =
    useState<ProposalSummary | null>(null);
  const [repairDraft, setRepairDraft] = useState<RepairEvidenceDraft>(
    EMPTY_REPAIR_EVIDENCE_DRAFT,
  );
  const [repairPreflight, setRepairPreflight] =
    useState<ProposalPreflight | null>(null);
  const [repairBusy, setRepairBusy] = useState<"preflight" | "submit" | "">("");

  const [lifecycle, setLifecycle] = useState<LifecycleSelection | null>(null);
  const [lifecycleBusy, setLifecycleBusy] = useState(false);
  const [reviewAcknowledged, setReviewAcknowledged] = useState(false);
  const [now, setNow] = useState(0);

  useEffect(() => {
    const updateNow = () => setNow(Math.floor(Date.now() / 1000));
    updateNow();
    const id = window.setInterval(updateNow, 15_000);
    return () => window.clearInterval(id);
  }, []);

  const pendingCreate = tracker.transactions.some((tx) => {
    return (
      tx.label.startsWith("Create candidate v") &&
      !terminalTransaction(tx.status)
    );
  });

  const canCreate =
    wallet.isOwner &&
    actionGate.data === "0" &&
    !pendingCreate;

  function proposalHasPendingAction(proposalId: number) {
    return tracker.transactions.some(
      (tx) =>
        tx.label.endsWith(`proposal #${proposalId}`) &&
        !terminalTransaction(tx.status),
    );
  }

  function update<K extends keyof ProposalDraft>(
    key: K,
    value: ProposalDraft[K],
  ) {
    setDraft((current) => ({ ...current, [key]: value }));
    setPreflight(null);
  }

  async function loadFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    if (file.size > 512_000) {
      toast.error("Candidate file exceeds the contract's 512,000-byte limit.");
      return;
    }
    update("candidateCode", await file.text());
    toast.success(`${file.name} loaded`);
  }

  async function validate() {
    if (!live.data) {
      toast.error("Finalized target state has not loaded yet.");
      return null;
    }
    setBusy("preflight");
    try {
      const result = await runProposalPreflight(draft, live.data);
      setPreflight(result);
      result.passed
        ? toast.success("Proposal preflight passed")
        : toast.error("Preflight found blocking issues");
      return result;
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Preflight failed");
      return null;
    } finally {
      setBusy("");
    }
  }

  async function submit() {
    if (!wallet.isOwner || !wallet.address) {
      toast.error("Only the registered target owner can create a proposal.");
      return;
    }
    if (pendingCreate) {
      toast.error("A proposal creation transaction is already being tracked.");
      return;
    }

    const freshGate = await actionGate.refetch();
    if (freshGate.data !== "0") {
      toast.error("This target does not have a free finalized proposal slot.");
      return;
    }

    const checked = await validate();
    if (!checked?.passed) return;

    setBusy("submit");
    try {
      const hash = await createProofPatchProposal(draft, wallet.address);
      tracker.trackTransaction(hash, `Create candidate v${draft.candidateVersion}`);
      toast.success("Proposal transaction submitted and persisted for tracking.");
      setOpen(false);
      setDraft(EMPTY_PROPOSAL_DRAFT);
      setPreflight(null);
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "Proposal submission failed",
      );
    } finally {
      setBusy("");
    }
  }

  function openRepair(proposal: ProposalSummary) {
    if (idOf(proposal) === PROOFPATCH.proposalId) {
      toast.error("Proposal #1 is permanently write-locked.");
      return;
    }
    setRepairProposal(proposal);
    setRepairDraft(EMPTY_REPAIR_EVIDENCE_DRAFT);
    setRepairPreflight(null);
  }

  function updateRepair<K extends keyof RepairEvidenceDraft>(
    key: K,
    value: RepairEvidenceDraft[K],
  ) {
    setRepairDraft((current) => ({ ...current, [key]: value }));
    setRepairPreflight(null);
  }

  async function validateRepair() {
    if (!repairProposal) return null;
    setRepairBusy("preflight");
    try {
      const result = await runRepairEvidencePreflight(
        repairDraft,
        repairProposal,
      );
      setRepairPreflight(result);
      result.passed
        ? toast.success("Replacement evidence preflight passed")
        : toast.error("Replacement evidence has blocking issues");
      return result;
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "Repair preflight failed",
      );
      return null;
    } finally {
      setRepairBusy("");
    }
  }

  async function submitRepair() {
    if (!repairProposal) return;
    const proposalId = idOf(repairProposal);

    if (!wallet.isOwner || !wallet.address) {
      toast.error("Only the registered owner can repair proposal evidence.");
      return;
    }
    if (proposalHasPendingAction(proposalId)) {
      toast.error("This proposal already has a transaction being tracked.");
      return;
    }

    const checked = await validateRepair();
    if (!checked?.passed) return;

    setRepairBusy("submit");
    try {
      const hash = await repairProofPatchEvidence(
        proposalId,
        repairDraft,
        wallet.address,
      );
      tracker.trackTransaction(hash, `Repair evidence proposal #${proposalId}`);
      toast.success("Evidence repair transaction submitted.");
      setRepairProposal(null);
      setRepairDraft(EMPTY_REPAIR_EVIDENCE_DRAFT);
      setRepairPreflight(null);
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "Evidence repair failed",
      );
    } finally {
      setRepairBusy("");
    }
  }

  function openLifecycle(kind: LifecycleKind, proposal: ProposalSummary) {
    if (idOf(proposal) === PROOFPATCH.proposalId) {
      toast.error("Proposal #1 is permanently write-locked.");
      return;
    }
    setReviewAcknowledged(false);
    setLifecycle({ kind, proposal });
  }

  async function executeLifecycle() {
    if (!lifecycle || !wallet.address) {
      toast.error("Connect a wallet before submitting this action.");
      return;
    }

    const proposalId = idOf(lifecycle.proposal);
    if (proposalId === PROOFPATCH.proposalId) {
      toast.error("Proposal #1 is permanently write-locked.");
      return;
    }
    if (proposalHasPendingAction(proposalId)) {
      toast.error("This proposal already has a transaction being tracked.");
      return;
    }
    if (lifecycle.kind === "cancel" && !wallet.isOwner) {
      toast.error("Only the registered owner can cancel this proposal.");
      return;
    }
    if (lifecycle.kind === "review" && !reviewAcknowledged) {
      toast.error("Confirm the finality consequence before starting review.");
      return;
    }

    setLifecycleBusy(true);
    try {
      let hash = "";
      let label = "";

      if (lifecycle.kind === "review") {
        hash = await reviewProofPatchProposal(proposalId, wallet.address);
        label = `Review proposal #${proposalId}`;
      } else if (lifecycle.kind === "cancel") {
        hash = await cancelProofPatchProposal(proposalId, wallet.address);
        label = `Cancel proposal #${proposalId}`;
      } else {
        hash = await expireProofPatchProposal(proposalId, wallet.address);
        label = `Expire proposal #${proposalId}`;
      }

      tracker.trackTransaction(hash, label);
      toast.success(`${label} submitted and persisted for tracking.`);
      setLifecycle(null);
      setReviewAcknowledged(false);
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "Lifecycle transaction failed",
      );
    } finally {
      setLifecycleBusy(false);
    }
  }

  const lifecycleConfig = lifecycle
    ? {
        review: {
          eyebrow: "VALIDATOR CONSENSUS",
          title: "Start proposal review?",
          body:
            "This is a real Bradbury transaction. Validators independently evaluate the frozen candidate and evidence. Exact approval moves the proposal to UPGRADE_QUEUED, and the protected target upgrade is emitted only when the review transaction reaches finality.",
          button: "Sign review transaction",
          icon: <Play size={17} />,
        },
        cancel: {
          eyebrow: "OWNER TERMINAL ACTION",
          title: "Cancel this proposal?",
          body:
            "Cancellation is terminal for this proposal and releases the target's active proposal slot. It does not alter installed code.",
          button: "Sign cancellation",
          icon: <Ban size={17} />,
        },
        expire: {
          eyebrow: "LIVENESS RECOVERY",
          title: "Expire this proposal?",
          body:
            "Expiry is permissionless only after the proposal deadline. The contract rejects an early attempt. Successful expiry is terminal and releases the active proposal slot.",
          button: "Sign expiry transaction",
          icon: <TimerOff size={17} />,
        },
      }[lifecycle.kind]
    : null;

  return (
    <section className="proposal-workspace" id="proposals">
      <div className="proposal-workspace-head">
        <div>
          <span className="card-label">UPGRADE WORKSPACE</span>
          <h2>Prepare the next release.</h2>
          <p>
            {wallet.isOwner
              ? pendingCreate
                ? "A proposal creation transaction is already being tracked."
                : actionGate.isLoading
                  ? "Owner verified. Checking the finalized proposal slot…"
                  : actionGate.data === "0"
                    ? "Registered owner verified. The target is free for a new proposal."
                    : `Proposal #${actionGate.data || "?"} already holds the active slot.`
              : wallet.isConnected
                ? `Read-only wallet. Registered owner: ${short(PROOFPATCH.owner)}.`
                : "Connect the registered owner wallet to create an upgrade."}
          </p>
        </div>
        <button
          className="button primary"
          onClick={() => setOpen(true)}
          disabled={!canCreate}
        >
          <Plus size={16} />
          New proposal
        </button>
      </div>

      <div className="proposal-history-head">
        <span>FINALIZED PROPOSAL HISTORY</span>
        <span>{workspace.data?.proposalCount ?? "—"} total</span>
      </div>

      {workspace.isLoading ? (
        <div className="proposal-loading">
          <LoaderCircle className="spin" size={16} />
          Loading proposal history…
        </div>
      ) : null}

      <div className="proposal-history">
        {(workspace.data?.proposals ?? []).map((proposal) => {
          const proposalId = idOf(proposal);
          const status = statusOf(proposal);
          const locked = proposalId === PROOFPATCH.proposalId;
          const pending = proposalHasPendingAction(proposalId);
          const expiresAt = Number(proposal.expires_at ?? 0);
          const executionDeadline = Number(proposal.execution_deadline ?? 0);
          const timeReady = now > 0;
          const expired = timeReady && expiresAt > 0 && now > expiresAt;

          const activeStatuses = [
            "PROPOSED",
            "EVIDENCE_REPAIR_REQUIRED",
            "REVIEW_RETRY_REQUIRED",
          ];

          const reviewable =
            timeReady &&
            !expired &&
            ["PROPOSED", "REVIEW_RETRY_REQUIRED"].includes(status);
          const repairable =
            timeReady &&
            !expired &&
            status === "EVIDENCE_REPAIR_REQUIRED";
          const cancellable = activeStatuses.includes(status);
          const expirable =
            timeReady &&
            expired &&
            activeStatuses.includes(status);

          const deadline =
            status === "UPGRADE_QUEUED"
              ? executionDeadline
              : activeStatuses.includes(status)
                ? expiresAt
                : 0;

          return (
            <div className="proposal-row lifecycle-row" key={proposalId}>
              <div className="proposal-id">
                <strong>#{proposalId}</strong>
                {locked ? <small>historical lock</small> : null}
              </div>

              <div className="proposal-main">
                <strong>
                  {String(proposal.parent_version ?? "—")} →{" "}
                  {String(proposal.candidate_version ?? "—")}
                </strong>
                <code>{short(String(proposal.candidate_code_hash ?? ""))}</code>
                {deadline > 0 ? (
                  <small className="proposal-deadline">
                    <Clock3 size={11} />
                    {status === "UPGRADE_QUEUED"
                      ? "execution deadline"
                      : expired
                        ? "expired"
                        : "proposal deadline"}{" "}
                    · {formatUtc(deadline)}
                  </small>
                ) : null}
              </div>

              <div className={`proposal-state ${statusTone(status)}`}>
                <span>{status}</span>
                <small>
                  {String(proposal.last_review_code ?? "") || "no review code"}
                </small>
              </div>

              <div className="proposal-lifecycle-cell">
                {locked ? (
                  <div className="proposal-action-lock">
                    <LockKeyhole size={13} />
                    Read only
                  </div>
                ) : pending ? (
                  <div className="proposal-action-lock pending">
                    <LoaderCircle className="spin" size={13} />
                    Transaction tracking
                  </div>
                ) : (
                  <div className="lifecycle-actions">
                    {reviewable ? (
                      <button
                        className="lifecycle-button primary-action"
                        onClick={() => openLifecycle("review", proposal)}
                        disabled={!wallet.isConnected}
                      >
                        <Play size={13} />
                        Review
                      </button>
                    ) : null}

                    {repairable ? (
                      <button
                        className="lifecycle-button"
                        onClick={() => openRepair(proposal)}
                        disabled={!wallet.isOwner}
                      >
                        <Wrench size={13} />
                        Repair evidence
                      </button>
                    ) : null}

                    {cancellable ? (
                      <button
                        className="lifecycle-button subtle-danger"
                        onClick={() => openLifecycle("cancel", proposal)}
                        disabled={!wallet.isOwner}
                      >
                        <Ban size={13} />
                        Cancel
                      </button>
                    ) : null}

                    {expirable ? (
                      <button
                        className="lifecycle-button warning-action"
                        onClick={() => openLifecycle("expire", proposal)}
                        disabled={!wallet.isConnected}
                      >
                        <TimerOff size={13} />
                        Expire
                      </button>
                    ) : null}

                    {status === "UPGRADE_QUEUED" ? (
                      <div className="proposal-action-lock queued">
                        <RefreshCw size={13} />
                        Finality / install pending
                      </div>
                    ) : null}

                    {!reviewable &&
                    !repairable &&
                    !cancellable &&
                    !expirable &&
                    status !== "UPGRADE_QUEUED" ? (
                      <div className="proposal-action-lock">
                        <LockKeyhole size={13} />
                        Terminal
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {open ? (
        <div className="proposal-modal-backdrop" onMouseDown={() => setOpen(false)}>
          <div
            className="proposal-modal"
            role="dialog"
            aria-modal="true"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <div className="proposal-modal-head">
              <div>
                <span className="card-label">NEW UPGRADE PROPOSAL</span>
                <h2>Freeze exact bytes before consensus.</h2>
              </div>
              <button className="modal-x" onClick={() => setOpen(false)} aria-label="Close new proposal">
                <X size={18} />
              </button>
            </div>

            <div className="proposal-form">
              <div className="form-grid">
                <label>
                  <span>Candidate version</span>
                  <input
                    value={draft.candidateVersion}
                    onChange={(e) => update("candidateVersion", e.target.value)}
                    placeholder="2.1.0"
                  />
                </label>
                <label className="wide">
                  <span>Immutable candidate source URL</span>
                  <input
                    value={draft.candidateSourceUrl}
                    onChange={(e) => update("candidateSourceUrl", e.target.value)}
                    placeholder="https://raw.githubusercontent.com/owner/repo/<40-char-commit>/contract.py"
                  />
                </label>
                <label className="wide">
                  <span>Candidate source bytes</span>
                  <div className="candidate-upload-row">
                    <label className="file-picker">
                      <Upload size={14} />
                      Load .py file
                      <input type="file" accept=".py,text/plain" onChange={loadFile} />
                    </label>
                    <small>
                      {new TextEncoder().encode(draft.candidateCode).length.toLocaleString()} / 512,000 bytes
                    </small>
                  </div>
                  <textarea
                    rows={10}
                    spellCheck={false}
                    value={draft.candidateCode}
                    onChange={(e) => update("candidateCode", e.target.value)}
                    placeholder="# exact candidate source"
                  />
                </label>
                <label>
                  <span>CI evidence URL</span>
                  <input
                    value={draft.ciEvidenceUrl}
                    onChange={(e) => update("ciEvidenceUrl", e.target.value)}
                  />
                </label>
                <label>
                  <span>CI evidence ID</span>
                  <input
                    value={draft.ciEvidenceId}
                    onChange={(e) => update("ciEvidenceId", e.target.value)}
                  />
                </label>
                <label>
                  <span>Independent audit URL</span>
                  <input
                    value={draft.auditEvidenceUrl}
                    onChange={(e) => update("auditEvidenceUrl", e.target.value)}
                  />
                </label>
                <label>
                  <span>Audit evidence ID</span>
                  <input
                    value={draft.auditEvidenceId}
                    onChange={(e) => update("auditEvidenceId", e.target.value)}
                  />
                </label>
              </div>

              {preflight ? <Preflight result={preflight} /> : null}

              <div className="proposal-submit-row">
                <div className="owner-proof">
                  {wallet.isOwner ? <CheckCircle2 size={15} /> : <LockKeyhole size={15} />}
                  <span>
                    {wallet.isOwner ? `Owner ${short(wallet.address)}` : "Registered owner required"}
                  </span>
                </div>
                <button
                  className="button secondary"
                  onClick={() => void validate()}
                  disabled={Boolean(busy)}
                >
                  {busy === "preflight" ? <LoaderCircle className="spin" size={15} /> : <ShieldCheck size={15} />}
                  Run preflight
                </button>
                <button
                  className="button primary"
                  onClick={() => void submit()}
                  disabled={!wallet.isOwner || !preflight?.passed || Boolean(busy)}
                >
                  {busy === "submit" ? <LoaderCircle className="spin" size={15} /> : <FileCode2 size={15} />}
                  Sign & submit
                </button>
              </div>

              <div className="write-safety-note">
                <AlertTriangle size={15} />
                This button submits a real Bradbury transaction only after you click it and approve the wallet request.
                Bradbury network / GenLayer Snap setup is completed at that write step. A returned transaction hash is
                stored immediately and will not be blindly resubmitted.
              </div>
            </div>
          </div>
        </div>
      ) : null}

      {repairProposal ? (
        <div className="proposal-modal-backdrop" onMouseDown={() => setRepairProposal(null)}>
          <div
            className="proposal-modal repair-evidence-modal"
            role="dialog"
            aria-modal="true"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <div className="proposal-modal-head">
              <div>
                <span className="card-label">CORRECTABLE EVIDENCE FAILURE</span>
                <h2>Repair proposal #{idOf(repairProposal)} evidence.</h2>
                <p className="modal-intro">
                  Candidate bytes, candidate hash, target, parent and policy fingerprint remain frozen.
                  Only approved source/evidence references are replaced.
                </p>
              </div>
              <button className="modal-x" onClick={() => setRepairProposal(null)} aria-label="Close evidence repair">
                <X size={18} />
              </button>
            </div>

            <div className="proposal-form">
              <div className="repair-frozen-binding">
                <LockKeyhole size={15} />
                <div>
                  <strong>Frozen candidate</strong>
                  <code>{String(repairProposal.candidate_code_hash ?? "missing")}</code>
                </div>
              </div>

              <div className="form-grid">
                <label className="wide">
                  <span>Replacement immutable candidate source URL</span>
                  <input
                    value={repairDraft.candidateSourceUrl}
                    onChange={(e) => updateRepair("candidateSourceUrl", e.target.value)}
                    placeholder="Same frozen candidate bytes at an approved immutable URL"
                  />
                </label>
                <label>
                  <span>Replacement CI evidence URL</span>
                  <input
                    value={repairDraft.ciEvidenceUrl}
                    onChange={(e) => updateRepair("ciEvidenceUrl", e.target.value)}
                  />
                </label>
                <label>
                  <span>New CI evidence ID</span>
                  <input
                    value={repairDraft.ciEvidenceId}
                    onChange={(e) => updateRepair("ciEvidenceId", e.target.value)}
                  />
                </label>
                <label>
                  <span>Replacement independent audit URL</span>
                  <input
                    value={repairDraft.auditEvidenceUrl}
                    onChange={(e) => updateRepair("auditEvidenceUrl", e.target.value)}
                  />
                </label>
                <label>
                  <span>New audit evidence ID</span>
                  <input
                    value={repairDraft.auditEvidenceId}
                    onChange={(e) => updateRepair("auditEvidenceId", e.target.value)}
                  />
                </label>
              </div>

              {repairPreflight ? <Preflight result={repairPreflight} /> : null}

              <div className="proposal-submit-row">
                <div className="owner-proof">
                  <LockKeyhole size={15} />
                  <span>Registered owner action</span>
                </div>
                <button
                  className="button secondary"
                  onClick={() => void validateRepair()}
                  disabled={Boolean(repairBusy)}
                >
                  {repairBusy === "preflight" ? <LoaderCircle className="spin" size={15} /> : <ShieldCheck size={15} />}
                  Validate repair
                </button>
                <button
                  className="button primary"
                  onClick={() => void submitRepair()}
                  disabled={!wallet.isOwner || !repairPreflight?.passed || Boolean(repairBusy)}
                >
                  {repairBusy === "submit" ? <LoaderCircle className="spin" size={15} /> : <Wrench size={15} />}
                  Sign repair
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : null}

      {lifecycle && lifecycleConfig ? (
        <div className="proposal-modal-backdrop lifecycle-backdrop" onMouseDown={() => setLifecycle(null)}>
          <div
            className="proposal-modal lifecycle-confirm-modal"
            role="dialog"
            aria-modal="true"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <div className="proposal-modal-head">
              <div>
                <span className="card-label">{lifecycleConfig.eyebrow}</span>
                <h2>{lifecycleConfig.title}</h2>
              </div>
              <button className="modal-x" onClick={() => setLifecycle(null)} aria-label="Close lifecycle confirmation">
                <X size={18} />
              </button>
            </div>

            <div className="lifecycle-confirm-body">
              <div className="lifecycle-proposal-chip">
                <strong>Proposal #{idOf(lifecycle.proposal)}</strong>
                <span>{statusOf(lifecycle.proposal)}</span>
              </div>

              <p>{lifecycleConfig.body}</p>

              {lifecycle.kind === "review" ? (
                <label className="lifecycle-ack">
                  <input
                    type="checkbox"
                    checked={reviewAcknowledged}
                    onChange={(event) => setReviewAcknowledged(event.target.checked)}
                  />
                  <span>
                    I understand that exact validator approval followed by finality can authorize the protected target upgrade.
                  </span>
                </label>
              ) : null}

              <div className="lifecycle-confirm-actions">
                <button className="button secondary" onClick={() => setLifecycle(null)} disabled={lifecycleBusy}>
                  Keep proposal unchanged
                </button>
                <button
                  className={`button ${lifecycle.kind === "cancel" ? "danger-button" : "primary"}`}
                  onClick={() => void executeLifecycle()}
                  disabled={
                    lifecycleBusy ||
                    !wallet.isConnected ||
                    (lifecycle.kind === "review" && !reviewAcknowledged)
                  }
                >
                  {lifecycleBusy ? <LoaderCircle className="spin" size={15} /> : lifecycleConfig.icon}
                  {lifecycleConfig.button}
                </button>
              </div>

              <div className="write-safety-note">
                <AlertTriangle size={15} />
                A transaction hash is persisted immediately after submission. Do not repeat an action merely because
                consensus or finality takes time.
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

"use client";

import {
  AlertTriangle,
  CheckCircle2,
  FileCode2,
  LoaderCircle,
  LockKeyhole,
  Plus,
  ShieldCheck,
  Upload,
  X,
} from "lucide-react";
import { type ChangeEvent, useState } from "react";
import { toast } from "sonner";
import {
  createProofPatchProposal,
  type ProposalSummary,
} from "@/lib/genlayer";
import {
  EMPTY_PROPOSAL_DRAFT,
  type ProposalDraft,
  type ProposalPreflight,
  runProposalPreflight,
} from "@/lib/proposal-workflow";
import {
  useProofPatchLiveState,
  useProposalWorkspaceState,
} from "@/lib/use-proofpatch";
import { useTransactionTracker } from "@/lib/transaction-tracker";
import { useWallet } from "@/lib/wallet-context";
import { PROOFPATCH } from "@/lib/constants";

function short(value: string) {
  return value ? `${value.slice(0, 12)}…${value.slice(-10)}` : "—";
}

function idOf(summary: ProposalSummary) {
  return Number(summary.proposal_id ?? 0);
}

export function ProposalWorkspace() {
  const live = useProofPatchLiveState();
  const workspace = useProposalWorkspaceState();
  const wallet = useWallet();
  const tracker = useTransactionTracker();

  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState<ProposalDraft>(EMPTY_PROPOSAL_DRAFT);
  const [preflight, setPreflight] = useState<ProposalPreflight | null>(null);
  const [busy, setBusy] = useState<"preflight" | "submit" | "">("");

  const canCreate =
    wallet.isOwner &&
    live.data?.activeProposal === "0" &&
    Boolean(live.data);

  function update<K extends keyof ProposalDraft>(key: K, value: ProposalDraft[K]) {
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
    if (live.data?.activeProposal !== "0") {
      toast.error("This target already has an active proposal.");
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
      toast.error(error instanceof Error ? error.message : "Proposal submission failed");
    } finally {
      setBusy("");
    }
  }

  return (
    <section className="proposal-workspace" id="proposals">
      <div className="proposal-workspace-head">
        <div>
          <span className="card-label">UPGRADE WORKSPACE</span>
          <h2>Prepare the next release.</h2>
          <p>
            {wallet.isOwner
              ? live.data?.activeProposal === "0"
                ? "Registered owner verified. The target is free for a new proposal."
                : `Proposal #${live.data?.activeProposal} already holds the active slot.`
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
          const id = idOf(proposal);
          const locked = id === PROOFPATCH.proposalId;
          return (
            <div className="proposal-row" key={id}>
              <div className="proposal-id">
                <strong>#{id}</strong>
                {locked ? <small>historical lock</small> : null}
              </div>
              <div className="proposal-main">
                <strong>
                  {String(proposal.parent_version ?? "—")} →{" "}
                  {String(proposal.candidate_version ?? "—")}
                </strong>
                <code>{short(String(proposal.candidate_code_hash ?? ""))}</code>
              </div>
              <div className="proposal-state">
                <span>{String(proposal.status ?? "UNKNOWN")}</span>
                <small>{String(proposal.last_review_code ?? "") || "no review code"}</small>
              </div>
              <div className="proposal-action-lock">
                {locked ? (
                  <>
                    <LockKeyhole size={13} />
                    Read only
                  </>
                ) : (
                  "Lifecycle actions arrive in the next gated increment"
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
              <button className="modal-x" onClick={() => setOpen(false)}>
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
                      {new TextEncoder()
                        .encode(draft.candidateCode)
                        .length.toLocaleString()}{" "}
                      / 512,000 bytes
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
                    {wallet.isOwner
                      ? `Owner ${short(wallet.address)}`
                      : "Registered owner required"}
                  </span>
                </div>
                <button
                  className="button secondary"
                  onClick={() => void validate()}
                  disabled={Boolean(busy)}
                >
                  {busy === "preflight" ? (
                    <LoaderCircle className="spin" size={15} />
                  ) : (
                    <ShieldCheck size={15} />
                  )}
                  Run preflight
                </button>
                <button
                  className="button primary"
                  onClick={() => void submit()}
                  disabled={!wallet.isOwner || !preflight?.passed || Boolean(busy)}
                >
                  {busy === "submit" ? (
                    <LoaderCircle className="spin" size={15} />
                  ) : (
                    <FileCode2 size={15} />
                  )}
                  Sign & submit
                </button>
              </div>

              <div className="write-safety-note">
                <AlertTriangle size={15} />
                This button submits a real Bradbury transaction only after you click it
                and approve the wallet signature. A returned transaction hash is stored
                immediately and will not be blindly resubmitted.
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

function Preflight({ result }: { result: ProposalPreflight }) {
  return (
    <div className={`preflight-list ${result.passed ? "passed" : ""}`}>
      <div className="preflight-summary">
        {result.passed ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
        <strong>{result.passed ? "All frontend gates passed" : "Blocking checks remain"}</strong>
        <code>{result.candidateHash}</code>
      </div>
      <div className="preflight-checks">
        {result.checks.map((check, index) => (
          <div className={check.ok ? "ok" : "bad"} key={`${check.label}-${index}`}>
            {check.ok ? <CheckCircle2 size={13} /> : <AlertTriangle size={13} />}
            <span>{check.label}</span>
            <small>{check.detail}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

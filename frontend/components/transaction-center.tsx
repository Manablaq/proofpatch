"use client";

import {
  CheckCircle2,
  Clock3,
  Copy,
  LoaderCircle,
  ShieldCheck,
  Trash2,
} from "lucide-react";
import { toast } from "sonner";
import {
  type TrackedTransaction,
  useTransactionTracker,
} from "@/lib/transaction-tracker";

function short(value: string) {
  return value ? `${value.slice(0, 12)}…${value.slice(-10)}` : "—";
}

function normalize(value: string) {
  return value.replaceAll("_", "").replaceAll(" ", "").toUpperCase();
}

function terminal(status: string) {
  const value = normalize(status);
  return (
    value === "FINALIZED" ||
    value === "CANCELED" ||
    value === "CANCELLED"
  );
}

function transactionPhase(tx: TrackedTransaction) {
  const status = normalize(tx.status);

  if (status === "FINALIZED") return "Finalized";
  if (status.includes("ACCEPTED")) return "Accepted · finality pending";
  if (status.includes("APPEAL")) return "Appeal / finality window";
  if (status.includes("REJECT")) return "Rejected";
  if (status === "PENDING" || status === "SUBMITTED") return "Submitted";
  return "Consensus running";
}

function formatCreatedAt(value: number) {
  if (!Number.isFinite(value) || value <= 0) return "";
  return new Date(value).toLocaleString();
}

export function TransactionCenter() {
  const { transactions, removeTransaction } = useTransactionTracker();

  if (transactions.length === 0) {
    return (
      <div className="transaction-empty">
        <Clock3 size={28} />
        <div>
          <strong>No tracked wallet transactions.</strong>
          <p>
            Once a transaction hash exists, ProofPatch stores it immediately and
            follows that exact transaction instead of blindly sending another one.
          </p>
        </div>
        <span className="status-chip">Persistent tracking ready</span>
      </div>
    );
  }

  return (
    <>
      <div className="transaction-truth-note">
        <ShieldCheck size={15} />
        <p>
          <strong>Consensus and execution are separate.</strong> An Accepted
          transaction is not displayed as an executed upgrade. ProofPatch keeps
          consensus status, finality/lifecycle and execution result visible
          independently.
        </p>
      </div>

      <div className="tracked-transactions">
        {transactions.map((tx) => {
          const isDone = terminal(tx.status);
          return (
            <div className="tracked-transaction" key={tx.hash}>
              <div className={`tracked-icon ${isDone ? "done" : ""}`}>
                {isDone ? (
                  <CheckCircle2 size={16} />
                ) : (
                  <LoaderCircle className="spin" size={16} />
                )}
              </div>

              <div className="tracked-main">
                <strong>{tx.label}</strong>
                <code>{short(tx.hash)}</code>
                <small>{formatCreatedAt(tx.createdAt)}</small>
              </div>

              <div className="tracked-state">
                <span className={`tracked-phase ${isDone ? "done" : ""}`}>
                  {transactionPhase(tx)}
                </span>
                <small>
                  <strong>Consensus</strong>
                  {tx.status || "Pending"}
                </small>
                <small>
                  <strong>Execution</strong>
                  {tx.execution || "awaiting execution result"}
                </small>
                {tx.lifecycle ? (
                  <small>
                    <strong>Lifecycle</strong>
                    {tx.lifecycle}
                  </small>
                ) : null}
              </div>

              <div className="tracked-actions">
                <button
                  aria-label="Copy transaction hash"
                  onClick={() =>
                    void navigator.clipboard
                      .writeText(tx.hash)
                      .then(() => toast.success("Transaction hash copied"))
                      .catch(() => toast.error("Clipboard permission denied"))
                  }
                >
                  <Copy size={14} />
                </button>

                {isDone ? (
                  <button
                    aria-label="Remove completed transaction"
                    onClick={() => removeTransaction(tx.hash)}
                  >
                    <Trash2 size={14} />
                  </button>
                ) : null}
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
}

"use client";

import { CheckCircle2, Clock3, Copy, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { useTransactionTracker } from "@/lib/transaction-tracker";

function short(value: string) {
  return value ? `${value.slice(0, 12)}…${value.slice(-10)}` : "—";
}

function terminal(status: string) {
  const value = status.replaceAll("_", "").replaceAll(" ", "").toUpperCase();
  return value === "FINALIZED" || value === "CANCELED" || value === "CANCELLED";
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
            Once a transaction hash exists, ProofPatch stores it immediately and keeps
            following that transaction instead of blindly sending another one.
          </p>
        </div>
        <span className="status-chip">Persistent tracking ready</span>
      </div>
    );
  }

  return (
    <div className="tracked-transactions">
      {transactions.map((tx) => (
        <div className="tracked-transaction" key={tx.hash}>
          <div className={`tracked-icon ${terminal(tx.status) ? "done" : ""}`}>
            {terminal(tx.status) ? <CheckCircle2 size={16} /> : <Clock3 size={16} />}
          </div>
          <div className="tracked-main">
            <strong>{tx.label}</strong>
            <code>{short(tx.hash)}</code>
          </div>
          <div className="tracked-state">
            <span>{tx.status || "Pending"}</span>
            <small>{tx.execution || "awaiting execution result"}</small>
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
            {terminal(tx.status) ? (
              <button
                aria-label="Remove completed transaction"
                onClick={() => removeTransaction(tx.hash)}
              >
                <Trash2 size={14} />
              </button>
            ) : null}
          </div>
        </div>
      ))}
    </div>
  );
}

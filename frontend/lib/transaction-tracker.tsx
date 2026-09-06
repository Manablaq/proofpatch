"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { useQueryClient } from "@tanstack/react-query";
import { getTransactionSnapshot } from "@/lib/genlayer";

const STORAGE_KEY = "proofpatch:tracked-transactions:v1";

export type TrackedTransaction = {
  hash: string;
  label: string;
  createdAt: number;
  status: string;
  execution: string;
};

type TrackerContextValue = {
  transactions: TrackedTransaction[];
  trackTransaction: (hash: string, label: string) => void;
  removeTransaction: (hash: string) => void;
};

const TrackerContext = createContext<TrackerContextValue | null>(null);

function normalize(value: string) {
  return value.replaceAll("_", "").replaceAll(" ", "").toUpperCase();
}

function isTerminal(status: string) {
  const normalized = normalize(status);
  return normalized === "FINALIZED" || normalized === "CANCELED" || normalized === "CANCELLED";
}

export function TransactionTrackerProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const queryClient = useQueryClient();
  const [transactions, setTransactions] = useState<TrackedTransaction[]>([]);
  const hydrated = useRef(false);

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as TrackedTransaction[];
        if (Array.isArray(parsed)) setTransactions(parsed);
      }
    } catch {
      // A storage failure must never block app rendering.
    } finally {
      hydrated.current = true;
    }
  }, []);

  useEffect(() => {
    if (!hydrated.current) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(transactions));
    } catch {
      // Ignore storage quota/privacy failures; in-memory tracking continues.
    }
  }, [transactions]);

  useEffect(() => {
    let cancelled = false;

    async function poll() {
      const active = transactions.filter((tx) => !isTerminal(tx.status));
      if (active.length === 0) return;

      const snapshots = await Promise.all(
        active.map(async (tx) => {
          try {
            return await getTransactionSnapshot(tx.hash);
          } catch {
            return null;
          }
        }),
      );

      if (cancelled) return;

      let shouldRefreshLiveState = false;

      setTransactions((current) =>
        current.map((tx) => {
          const snapshot = snapshots.find((item) => item?.hash === tx.hash);
          if (!snapshot) return tx;

          if (
            snapshot.status !== tx.status ||
            snapshot.execution !== tx.execution
          ) {
            shouldRefreshLiveState = true;
          }

          return {
            ...tx,
            status: snapshot.status || tx.status,
            execution: snapshot.execution || tx.execution,
          };
        }),
      );

      if (shouldRefreshLiveState) {
        await queryClient.invalidateQueries({
          queryKey: ["proofpatch", "live-state"],
        });
        await queryClient.invalidateQueries({
          queryKey: ["proofpatch", "finality-chain"],
        });
        await queryClient.invalidateQueries({
          queryKey: ["proofpatch", "proposal-workspace"],
        });
        await queryClient.invalidateQueries({
          queryKey: ["proofpatch", "proposal-action-gate"],
        });
      }
    }

    void poll();
    const id = window.setInterval(() => void poll(), 5_000);

    return () => {
      cancelled = true;
      window.clearInterval(id);
    };
  }, [queryClient, transactions]);

  const trackTransaction = useCallback((hash: string, label: string) => {
    setTransactions((current) => {
      if (current.some((tx) => tx.hash.toLowerCase() === hash.toLowerCase())) {
        return current;
      }
      return [
        {
          hash,
          label,
          createdAt: Date.now(),
          status: "Pending",
          execution: "",
        },
        ...current,
      ];
    });
  }, []);

  const removeTransaction = useCallback((hash: string) => {
    setTransactions((current) =>
      current.filter((tx) => tx.hash.toLowerCase() !== hash.toLowerCase()),
    );
  }, []);

  const value = useMemo(
    () => ({ transactions, trackTransaction, removeTransaction }),
    [transactions, trackTransaction, removeTransaction],
  );

  return (
    <TrackerContext.Provider value={value}>
      {children}
    </TrackerContext.Provider>
  );
}

export function useTransactionTracker() {
  const value = useContext(TrackerContext);
  if (!value) {
    throw new Error(
      "useTransactionTracker must be used inside TransactionTrackerProvider",
    );
  }
  return value;
}

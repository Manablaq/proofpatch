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
import { getTransactionSnapshot, type ChainTransactionSnapshot } from "@/lib/genlayer";

const STORAGE_KEY = "proofpatch:tracked-transactions:v1";

export type TrackedTransaction = {
  hash: string;
  label: string;
  createdAt: number;
  status: string;
  execution: string;
  lifecycle?: string;
  children: ChainTransactionSnapshot[];
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

function sanitizeTrackedTransactions(value: unknown): TrackedTransaction[] {
  if (!Array.isArray(value)) return [];

  const safe: TrackedTransaction[] = [];
  const seen = new Set<string>();

  for (const item of value) {
    if (!item || typeof item !== "object" || Array.isArray(item)) continue;
    const record = item as Record<string, unknown>;

    const hash = typeof record.hash === "string" ? record.hash.trim() : "";
    const label = typeof record.label === "string" ? record.label.trim() : "";
    const createdAt =
      typeof record.createdAt === "number" && Number.isFinite(record.createdAt)
        ? record.createdAt
        : 0;
    const status =
      typeof record.status === "string" && record.status.trim()
        ? record.status
        : "Pending";
    const execution =
      typeof record.execution === "string" ? record.execution : "";
    const lifecycle =
      typeof record.lifecycle === "string" ? record.lifecycle : "";
    const children = Array.isArray(record.children)
      ? record.children.filter((child): child is ChainTransactionSnapshot => {
          if (!child || typeof child !== "object" || Array.isArray(child)) return false;
          const value = child as Record<string, unknown>;
          return typeof value.hash === "string" && typeof value.status === "string" && typeof value.execution === "string";
        }).map((child) => ({
          hash: child.hash,
          status: child.status,
          execution: child.execution,
          lifecycle: typeof child.lifecycle === "string" ? child.lifecycle : "",
          children: [],
        }))
      : [];

    if (!/^0x[0-9a-f]+$/i.test(hash) || !label || createdAt <= 0) continue;

    const normalizedHash = hash.toLowerCase();
    if (seen.has(normalizedHash)) continue;
    seen.add(normalizedHash);

    safe.push({
      hash,
      label,
      createdAt,
      status,
      execution,
      lifecycle,
      children,
    });
  }

  return safe;
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
        const parsed = JSON.parse(raw) as unknown;
        setTransactions(sanitizeTrackedTransactions(parsed));
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
            const snapshot = await getTransactionSnapshot(tx.hash);
            const children = await Promise.all(
              snapshot.children.map(async (child) => {
                try {
                  return await getTransactionSnapshot(child);
                } catch {
                  return null;
                }
              }),
            );
            return {
              ...snapshot,
              childSnapshots: children.filter((child): child is ChainTransactionSnapshot => Boolean(child)),
            };
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
            snapshot.execution !== tx.execution ||
            snapshot.lifecycle !== (tx.lifecycle ?? "") ||
            JSON.stringify(snapshot.childSnapshots) !== JSON.stringify(tx.children)
          ) {
            shouldRefreshLiveState = true;
          }

          return {
            ...tx,
            status: snapshot.status || tx.status,
            execution: snapshot.execution || tx.execution,
            lifecycle: snapshot.lifecycle || tx.lifecycle || "",
            children: snapshot.childSnapshots,
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
        await queryClient.invalidateQueries({
          queryKey: ["proofpatch-v2", "finalized-state"],
        });
        await queryClient.invalidateQueries({
          queryKey: ["proofpatch-v3", "finalized-state"],
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
          lifecycle: "",
          children: [],
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

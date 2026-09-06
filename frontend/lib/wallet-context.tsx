"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { connectBradburyWallet } from "@/lib/genlayer";
import { PROOFPATCH } from "@/lib/constants";

type WalletContextValue = {
  address: string;
  connecting: boolean;
  isConnected: boolean;
  isOwner: boolean;
  connect: () => Promise<string>;
};

const WalletContext = createContext<WalletContextValue | null>(null);

function firstAccount(value: unknown): string {
  if (!Array.isArray(value)) return "";
  return typeof value[0] === "string" ? value[0] : "";
}

export function WalletProvider({ children }: { children: React.ReactNode }) {
  const [address, setAddress] = useState("");
  const [connecting, setConnecting] = useState(false);

  useEffect(() => {
    const provider = window.ethereum;
    if (!provider) return;

    void provider
      .request({ method: "eth_accounts" })
      .then((accounts) => setAddress(firstAccount(accounts)))
      .catch(() => undefined);

    const onAccountsChanged = (...args: unknown[]) => {
      setAddress(firstAccount(args[0]));
    };

    provider.on?.("accountsChanged", onAccountsChanged);
    return () => provider.removeListener?.("accountsChanged", onAccountsChanged);
  }, []);

  const connect = useCallback(async () => {
    setConnecting(true);
    try {
      const connected = await connectBradburyWallet();
      setAddress(connected);
      return connected;
    } finally {
      setConnecting(false);
    }
  }, []);

  const value = useMemo(
    () => ({
      address,
      connecting,
      isConnected: Boolean(address),
      isOwner:
        Boolean(address) &&
        address.toLowerCase() === PROOFPATCH.owner.toLowerCase(),
      connect,
    }),
    [address, connecting, connect],
  );

  return <WalletContext.Provider value={value}>{children}</WalletContext.Provider>;
}

export function useWallet() {
  const value = useContext(WalletContext);
  if (!value) throw new Error("useWallet must be used inside WalletProvider");
  return value;
}

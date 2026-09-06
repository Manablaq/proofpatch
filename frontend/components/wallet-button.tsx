"use client";

import { Wallet } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { connectBradburyWallet } from "@/lib/genlayer";

function short(value: string) {
  return value ? `${value.slice(0, 6)}…${value.slice(-4)}` : "";
}

export function WalletButton() {
  const [address, setAddress] = useState("");
  const [busy, setBusy] = useState(false);

  async function connect() {
    setBusy(true);
    try {
      const connected = await connectBradburyWallet();
      setAddress(connected);
      toast.success("Wallet connected to Bradbury");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Wallet connection failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <button className="wallet-button" onClick={connect} disabled={busy}>
      <Wallet size={16} />
      <span>{address ? short(address) : busy ? "Connecting…" : "Connect wallet"}</span>
    </button>
  );
}

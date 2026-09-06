"use client";

import { CheckCircle2, Wallet } from "lucide-react";
import { toast } from "sonner";
import { useWallet } from "@/lib/wallet-context";
import { PROOFPATCH } from "@/lib/constants";

function short(value: string) {
  return value ? `${value.slice(0, 6)}…${value.slice(-4)}` : "";
}

export function WalletButton() {
  const wallet = useWallet();

  async function connect() {
    try {
      const connected = await wallet.connect();
      const ownerConnected =
        connected.toLowerCase() === PROOFPATCH.owner.toLowerCase();

      toast.success(
        ownerConnected
          ? "Registered owner wallet connected"
          : "Wallet connected in read-only mode",
      );
    } catch (error) {
      const message =
        error instanceof Error && error.message
          ? error.message
          : "Wallet account connection failed";
      toast.error(message);
    }
  }

  return (
    <button
      className={`wallet-button ${wallet.isOwner ? "owner-wallet" : ""}`}
      onClick={() => void connect()}
      disabled={wallet.connecting}
    >
      {wallet.isOwner ? <CheckCircle2 size={16} /> : <Wallet size={16} />}
      <span>
        {wallet.address
          ? short(wallet.address)
          : wallet.connecting
            ? "Connecting…"
            : "Connect wallet"}
      </span>
    </button>
  );
}

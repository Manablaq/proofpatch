"use client";

import { CheckCircle2, Wallet } from "lucide-react";
import { toast } from "sonner";
import { useWallet } from "@/lib/wallet-context";
import { PROOFPATCH } from "@/lib/constants";

function short(value: string) {
  return value ? `${value.slice(0, 6)}…${value.slice(-4)}` : "";
}

export function WalletButton({
  expectedOwner = PROOFPATCH.owner,
  networkLabel,
}: {
  expectedOwner?: string;
  networkLabel?: string;
}) {
  const wallet = useWallet();

  const ownerConnected =
    Boolean(wallet.address) &&
    wallet.address.toLowerCase() === expectedOwner.toLowerCase();

  async function connect() {
    try {
      const connected = await wallet.connect();

      const isExpectedOwner =
        connected.toLowerCase() === expectedOwner.toLowerCase();

      toast.success(
        isExpectedOwner
          ? "Registered owner wallet connected"
          : "Wallet connected",
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
      type="button"
      className={`wallet-button ${ownerConnected ? "owner-wallet" : ""}`}
      onClick={() => void connect()}
      disabled={wallet.connecting}
      title={
        wallet.address
          ? `${wallet.address}${networkLabel ? ` · ${networkLabel}` : ""}`
          : networkLabel
            ? `Connect wallet for ${networkLabel}`
            : "Connect wallet"
      }
    >
      {ownerConnected ? (
        <CheckCircle2 size={16} />
      ) : (
        <Wallet size={16} />
      )}

      <span>
        {wallet.address
          ? short(wallet.address)
          : wallet.connecting
            ? "Connecting…"
            : "Connect wallet"}
      </span>

      {networkLabel ? (
        <small className="wallet-network-label">
          {networkLabel}
        </small>
      ) : null}
    </button>
  );
}

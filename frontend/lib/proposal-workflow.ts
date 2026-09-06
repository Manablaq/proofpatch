"use client";

import { PROOFPATCH } from "@/lib/constants";

export type ProposalDraft = {
  candidateVersion: string;
  candidateSourceUrl: string;
  candidateCode: string;
  ciEvidenceUrl: string;
  ciEvidenceId: string;
  auditEvidenceUrl: string;
  auditEvidenceId: string;
};

export type PreflightCheck = {
  label: string;
  ok: boolean;
  detail: string;
};

export type ProposalPreflight = {
  candidateHash: string;
  checks: PreflightCheck[];
  passed: boolean;
};

export const EMPTY_PROPOSAL_DRAFT: ProposalDraft = {
  candidateVersion: "",
  candidateSourceUrl: "",
  candidateCode: "",
  ciEvidenceUrl: "",
  ciEvidenceId: "",
  auditEvidenceUrl: "",
  auditEvidenceId: "",
};

type RawGitHubRef = {
  owner: string;
  repo: string;
  commit: string;
};

function bytes(value: string) {
  return new TextEncoder().encode(value);
}

export async function sha256Hex(value: Uint8Array): Promise<string> {
  const input = new ArrayBuffer(value.byteLength);
  new Uint8Array(input).set(value);
  const digest = await crypto.subtle.digest("SHA-256", input);
  return [...new Uint8Array(digest)]
    .map((item) => item.toString(16).padStart(2, "0"))
    .join("");
}

function immutableRawGitHub(value: string): RawGitHubRef | null {
  try {
    const url = new URL(value);
    if (
      url.protocol !== "https:" ||
      url.hostname !== "raw.githubusercontent.com" ||
      url.search ||
      url.hash
    ) {
      return null;
    }
    const parts = url.pathname.split("/").filter(Boolean);
    if (parts.length < 4) return null;
    const [owner, repo, commit] = parts;
    if (!owner || !repo || !/^[0-9a-f]{40}$/i.test(commit)) return null;
    return { owner, repo, commit: commit.toLowerCase() };
  } catch {
    return null;
  }
}

async function fetchBytes(url: string) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return new Uint8Array(await response.arrayBuffer());
}

function checkEvidenceEnvelope(
  raw: unknown,
  expected: {
    kind: "ci" | "audit";
    id: string;
    candidateHash: string;
    parentHash: string;
    policyFingerprint: string;
  },
): PreflightCheck[] {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    return [
      {
        label: `${expected.kind.toUpperCase()} evidence object`,
        ok: false,
        detail: "JSON root must be an object",
      },
    ];
  }

  const value = raw as Record<string, unknown>;
  const published =
    typeof value.published_at === "number" ? value.published_at : NaN;
  const expires = typeof value.expires_at === "number" ? value.expires_at : NaN;
  const now = Math.floor(Date.now() / 1000);

  return [
    {
      label: `${expected.kind.toUpperCase()} schema`,
      ok: value.schema === "proofpatch-evidence-v1",
      detail: String(value.schema ?? "missing"),
    },
    {
      label: `${expected.kind.toUpperCase()} identity`,
      ok:
        value.kind === expected.kind &&
        value.evidence_id === expected.id &&
        typeof value.issuer === "string" &&
        value.issuer.length >= 3,
      detail: `${String(value.kind ?? "missing")} / ${String(value.evidence_id ?? "missing")}`,
    },
    {
      label: `${expected.kind.toUpperCase()} target`,
      ok:
        typeof value.target === "string" &&
        value.target.toLowerCase() === PROOFPATCH.target.toLowerCase(),
      detail: String(value.target ?? "missing"),
    },
    {
      label: `${expected.kind.toUpperCase()} parent + candidate`,
      ok:
        value.parent_sha256 === expected.parentHash &&
        value.candidate_sha256 === expected.candidateHash,
      detail: `${String(value.parent_sha256 ?? "missing")} / ${String(value.candidate_sha256 ?? "missing")}`,
    },
    {
      label: `${expected.kind.toUpperCase()} policy fingerprint`,
      ok: value.policy_fingerprint === expected.policyFingerprint,
      detail: String(value.policy_fingerprint ?? "missing"),
    },
    {
      label: `${expected.kind.toUpperCase()} timestamps`,
      ok:
        Number.isInteger(published) &&
        Number.isInteger(expires) &&
        published <= now &&
        expires >= now &&
        expires >= published,
      detail:
        Number.isFinite(published) && Number.isFinite(expires)
          ? `${published} → ${expires}`
          : "invalid timestamp fields",
    },
  ];
}

export async function runProposalPreflight(
  draft: ProposalDraft,
  live: {
    currentVersion: string;
    currentCodeHash: string;
    policyFingerprint: string;
    activeProposal: string;
  },
): Promise<ProposalPreflight> {
  const candidateBytes = bytes(draft.candidateCode);
  const candidateHash = await sha256Hex(candidateBytes);

  const source = immutableRawGitHub(draft.candidateSourceUrl);
  const ci = immutableRawGitHub(draft.ciEvidenceUrl);
  const audit = immutableRawGitHub(draft.auditEvidenceUrl);
  const repos = [source, ci, audit].map((item) =>
    item ? `${item.owner.toLowerCase()}/${item.repo.toLowerCase()}` : "",
  );

  const checks: PreflightCheck[] = [
    {
      label: "No active proposal",
      ok: live.activeProposal === "0",
      detail: live.activeProposal || "unknown",
    },
    {
      label: "Candidate version",
      ok:
        draft.candidateVersion.length > 0 &&
        bytes(draft.candidateVersion).length <= 96 &&
        draft.candidateVersion !== live.currentVersion,
      detail: draft.candidateVersion || "missing",
    },
    {
      label: "Candidate size",
      ok: candidateBytes.length > 0 && candidateBytes.length <= 512_000,
      detail: `${candidateBytes.length.toLocaleString()} bytes`,
    },
    {
      label: "Candidate differs from installed code",
      ok: candidateHash !== live.currentCodeHash,
      detail: candidateHash,
    },
    {
      label: "Immutable candidate source URL",
      ok: Boolean(source),
      detail: source ? `${source.owner}/${source.repo}@${source.commit}` : "invalid",
    },
    {
      label: "Immutable CI evidence URL",
      ok: Boolean(ci),
      detail: ci ? `${ci.owner}/${ci.repo}@${ci.commit}` : "invalid",
    },
    {
      label: "Immutable audit evidence URL",
      ok: Boolean(audit),
      detail: audit ? `${audit.owner}/${audit.repo}@${audit.commit}` : "invalid",
    },
    {
      label: "Distinct publisher repositories",
      ok: repos.every(Boolean) && new Set(repos).size === 3,
      detail: repos.filter(Boolean).join(" · ") || "missing",
    },
    {
      label: "Independent audit owner",
      ok:
        Boolean(source && audit) &&
        source!.owner.toLowerCase() !== audit!.owner.toLowerCase(),
      detail: source && audit ? `${source.owner} ≠ ${audit.owner}` : "missing",
    },
    {
      label: "Evidence IDs",
      ok:
        bytes(draft.ciEvidenceId).length >= 8 &&
        bytes(draft.ciEvidenceId).length <= 160 &&
        bytes(draft.auditEvidenceId).length >= 8 &&
        bytes(draft.auditEvidenceId).length <= 160 &&
        draft.ciEvidenceId !== draft.auditEvidenceId,
      detail: `${draft.ciEvidenceId || "missing"} / ${draft.auditEvidenceId || "missing"}`,
    },
  ];

  if (source) {
    try {
      const remoteHash = await sha256Hex(await fetchBytes(draft.candidateSourceUrl));
      checks.push({
        label: "Immutable source bytes match local candidate",
        ok: remoteHash === candidateHash,
        detail: remoteHash,
      });
    } catch (error) {
      checks.push({
        label: "Immutable candidate source fetch",
        ok: false,
        detail: error instanceof Error ? error.message : "fetch failed",
      });
    }
  }

  for (const [kind, url, id] of [
    ["ci", draft.ciEvidenceUrl, draft.ciEvidenceId],
    ["audit", draft.auditEvidenceUrl, draft.auditEvidenceId],
  ] as const) {
    if (!immutableRawGitHub(url)) continue;
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const evidence = (await response.json()) as unknown;
      checks.push(
        ...checkEvidenceEnvelope(evidence, {
          kind,
          id,
          candidateHash,
          parentHash: live.currentCodeHash,
          policyFingerprint: live.policyFingerprint,
        }),
      );
    } catch (error) {
      checks.push({
        label: `${kind.toUpperCase()} evidence fetch`,
        ok: false,
        detail: error instanceof Error ? error.message : "fetch failed",
      });
    }
  }

  return {
    candidateHash,
    checks,
    passed: checks.every((check) => check.ok),
  };
}
export type RepairEvidenceDraft = {
  candidateSourceUrl: string;
  ciEvidenceUrl: string;
  ciEvidenceId: string;
  auditEvidenceUrl: string;
  auditEvidenceId: string;
};

export const EMPTY_REPAIR_EVIDENCE_DRAFT: RepairEvidenceDraft = {
  candidateSourceUrl: "",
  ciEvidenceUrl: "",
  ciEvidenceId: "",
  auditEvidenceUrl: "",
  auditEvidenceId: "",
};

export async function runRepairEvidencePreflight(
  draft: RepairEvidenceDraft,
  proposal: {
    target?: string;
    parent_code_hash?: string;
    candidate_code_hash?: string;
    policy_fingerprint?: string;
    status?: string;
    expires_at?: number | string;
  },
): Promise<ProposalPreflight> {
  const candidateHash = String(proposal.candidate_code_hash ?? "").toLowerCase();
  const parentHash = String(proposal.parent_code_hash ?? "").toLowerCase();
  const policyFingerprint = String(proposal.policy_fingerprint ?? "");
  const expiresAt = Number(proposal.expires_at ?? 0);
  const now = Math.floor(Date.now() / 1000);

  const source = immutableRawGitHub(draft.candidateSourceUrl);
  const ci = immutableRawGitHub(draft.ciEvidenceUrl);
  const audit = immutableRawGitHub(draft.auditEvidenceUrl);
  const repos = [source, ci, audit].map((item) =>
    item ? `${item.owner.toLowerCase()}/${item.repo.toLowerCase()}` : "",
  );

  const checks: PreflightCheck[] = [
    {
      label: "Proposal requires repair",
      ok: proposal.status === "EVIDENCE_REPAIR_REQUIRED",
      detail: String(proposal.status ?? "unknown"),
    },
    {
      label: "Proposal repair window",
      ok: expiresAt > 0 && now <= expiresAt,
      detail: expiresAt > 0 ? `${now} <= ${expiresAt}` : "missing expiry",
    },
    {
      label: "Frozen candidate hash present",
      ok: /^[0-9a-f]{64}$/.test(candidateHash),
      detail: candidateHash || "missing",
    },
    {
      label: "Immutable replacement candidate URL",
      ok: Boolean(source),
      detail: source ? `${source.owner}/${source.repo}@${source.commit}` : "invalid",
    },
    {
      label: "Immutable replacement CI URL",
      ok: Boolean(ci),
      detail: ci ? `${ci.owner}/${ci.repo}@${ci.commit}` : "invalid",
    },
    {
      label: "Immutable replacement audit URL",
      ok: Boolean(audit),
      detail: audit ? `${audit.owner}/${audit.repo}@${audit.commit}` : "invalid",
    },
    {
      label: "Distinct publisher repositories",
      ok: repos.every(Boolean) && new Set(repos).size === 3,
      detail: repos.filter(Boolean).join(" · ") || "missing",
    },
    {
      label: "Independent audit owner",
      ok:
        Boolean(source && audit) &&
        source!.owner.toLowerCase() !== audit!.owner.toLowerCase(),
      detail: source && audit ? `${source.owner} != ${audit.owner}` : "missing",
    },
    {
      label: "Replacement evidence IDs",
      ok:
        bytes(draft.ciEvidenceId).length >= 8 &&
        bytes(draft.ciEvidenceId).length <= 160 &&
        bytes(draft.auditEvidenceId).length >= 8 &&
        bytes(draft.auditEvidenceId).length <= 160 &&
        draft.ciEvidenceId !== draft.auditEvidenceId,
      detail: `${draft.ciEvidenceId || "missing"} / ${draft.auditEvidenceId || "missing"}`,
    },
  ];

  if (source && candidateHash) {
    try {
      const remoteHash = await sha256Hex(await fetchBytes(draft.candidateSourceUrl));
      checks.push({
        label: "Replacement source preserves frozen candidate",
        ok: remoteHash === candidateHash,
        detail: remoteHash,
      });
    } catch (error) {
      checks.push({
        label: "Replacement candidate source fetch",
        ok: false,
        detail: error instanceof Error ? error.message : "fetch failed",
      });
    }
  }

  for (const [kind, url, id] of [
    ["ci", draft.ciEvidenceUrl, draft.ciEvidenceId],
    ["audit", draft.auditEvidenceUrl, draft.auditEvidenceId],
  ] as const) {
    if (!immutableRawGitHub(url)) continue;
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const evidence = (await response.json()) as unknown;
      checks.push(
        ...checkEvidenceEnvelope(evidence, {
          kind,
          id,
          candidateHash,
          parentHash,
          policyFingerprint,
        }),
      );
    } catch (error) {
      checks.push({
        label: `${kind.toUpperCase()} replacement evidence fetch`,
        ok: false,
        detail: error instanceof Error ? error.message : "fetch failed",
      });
    }
  }

  return {
    candidateHash,
    checks,
    passed: checks.every((check) => check.ok),
  };
}

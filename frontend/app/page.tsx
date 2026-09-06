import {
  ArrowRight,
  CheckCircle2,
  Code2,
  FileCheck2,
  Fingerprint,
  GitCommitHorizontal,
  LockKeyhole,
  Network,
  ScanSearch,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";
import Link from "next/link";
import { LiveProof } from "@/components/live-proof";
import { Reveal } from "@/components/reveal";
import { ThemeToggle } from "@/components/theme-toggle";
import { PROOFPATCH, SECURITY_GATES } from "@/lib/constants";

const flow = [
  {
    n: "01",
    title: "Register the protected target",
    text: "The target binds ProofPatch as its sole upgrade authority and registers an immutable security policy from the target itself.",
    icon: LockKeyhole,
  },
  {
    n: "02",
    title: "Freeze candidate + evidence",
    text: "Candidate bytes, immutable source URL, CI evidence and independent audit evidence become one proposal envelope.",
    icon: GitCommitHorizontal,
  },
  {
    n: "03",
    title: "Verify provenance first",
    text: "Approved publisher namespaces, immutable references, evidence IDs, freshness windows and corroboration are checked before semantics can matter.",
    icon: FileCheck2,
  },
  {
    n: "04",
    title: "Reach exact semantic consensus",
    text: "Leader and validators independently evaluate the consequential safety vector. Authorization-driving values must agree exactly.",
    icon: ScanSearch,
  },
  {
    n: "05",
    title: "Wait for finality",
    text: "Acceptance is provisional. The upgrade call is emitted only through the finality path—never merely because a committee accepted a receipt.",
    icon: Network,
  },
  {
    n: "06",
    title: "Re-hash, install, confirm",
    text: "The target re-fetches approved bytes, hashes them again, installs the exact candidate, then sends a finality-bound confirmation back to ProofPatch.",
    icon: ShieldCheck,
  },
];

const docs = [
  {
    id: "model",
    label: "01 / Security model",
    title: "A semantic firewall, not an admin multisig.",
    body:
      "ProofPatch separates integrity from authorization. SHA-256 tells the target which bytes it received; policy-bound evidence and validator consensus decide whether those exact bytes are permitted to become live code.",
  },
  {
    id: "evidence",
    label: "02 / Evidence",
    title: "Authority is explicit.",
    body:
      "The policy binds distinct source, CI and independent-audit authorities plus immutable repository prefixes. Evidence has stable IDs, freshness limits and replay resistance. A URL or hash by itself is never treated as proof of authority.",
  },
  {
    id: "repair",
    label: "03 / Repair + recovery",
    title: "Correctable failures stay correctable.",
    body:
      "Fetch, parse and hash problems can move a proposal into a repair/retry state without changing the frozen candidate bytes. TTL and execution deadlines prevent stale proposals from holding an upgrade path indefinitely.",
  },
  {
    id: "consensus",
    label: "04 / Consensus",
    title: "Exact consequences require exact agreement.",
    body:
      "The semantic review evaluates storage compatibility, user rights, privilege paths, upgrader authority, evidence trust, finality safety, liveness and hidden value movement. Consequential values are not accepted through fuzzy tolerance.",
  },
  {
    id: "finality",
    label: "05 / Finality",
    title: "Accepted is not installed.",
    body:
      "A review decision can be accepted while still appealable. ProofPatch does not emit the upgrade consequence on acceptance. Installation is reached through finality, and a separate post-install confirmation proves the target persisted the approved proposal/hash.",
  },
  {
    id: "reads",
    label: "06 / Product UX",
    title: "The UI follows the protocol lifecycle.",
    body:
      "The application keeps a submitted transaction ID, never blindly retries after submission, refreshes responsive non-final state after decisions and refreshes durable finalized state after finalization—without requiring a browser reload.",
  },
];

function short(value: string) {
  return `${value.slice(0, 10)}…${value.slice(-8)}`;
}

export default function HomePage() {
  return (
    <main className="site">
      <header className="site-header">
        <Link className="brand" href="/">
          <span className="brand-glyph" aria-hidden>
            <i />
            <i />
            <i />
          </span>
          <span>ProofPatch</span>
        </Link>

        <nav className="site-nav" aria-label="Primary navigation">
          <a href="#how-it-works">How it works</a>
          <a href="#security">Security</a>
          <a href="#documentation">Docs</a>
          <a href="#live-proof">Live proof</a>
        </nav>

        <div className="header-actions">
          <ThemeToggle />
          <Link className="button header-launch" href="/app">
            Launch app <ArrowRight size={15} />
          </Link>
        </div>
      </header>

      <section className="landing-hero">
        <div className="hero-noise" aria-hidden />
        <div className="lattice-lines" aria-hidden>
          <i className="l1" />
          <i className="l2" />
          <i className="l3" />
          <i className="l4" />
          <b className="node n1" />
          <b className="node n2" />
          <b className="node n3" />
          <b className="node n4" />
        </div>

        <Reveal className="hero-copy">
          <div className="hero-chip">
            <span />
            LIVE ON GENLAYER BRADBURY
          </div>
          <h1>
            Code can change.
            <br />
            <em>Trust shouldn&apos;t.</em>
          </h1>
          <p className="hero-lead">
            ProofPatch is a semantic upgrade firewall for GenLayer Intelligent
            Contracts. An exact candidate becomes live code only after trusted
            evidence, validator consensus, finality and post-install proof.
          </p>
          <div className="hero-cta">
            <Link href="/app" className="button primary large">
              Launch ProofPatch <ArrowRight size={17} />
            </Link>
            <a href="#documentation" className="button secondary large">
              Read the architecture
            </a>
          </div>
          <div className="hero-trust">
            <div>
              <CheckCircle2 size={15} />
              No admin-key bypass
            </div>
            <div>
              <CheckCircle2 size={15} />
              Exact-byte install
            </div>
            <div>
              <CheckCircle2 size={15} />
              Finality-gated consequence
            </div>
          </div>
        </Reveal>

        <Reveal className="hero-product" delay={120}>
          <div className="product-window">
            <div className="window-bar">
              <div className="window-dots"><i /><i /><i /></div>
              <span>proofpatch / live release</span>
              <span className="window-live"><i /> BRADBURY</span>
            </div>
            <div className="window-body">
              <div className="window-title">
                <div>
                  <span>PROTECTED TARGET</span>
                  <strong>ProofPatch Protected Target</strong>
                </div>
                <span className="status-chip verified">
                  <CheckCircle2 size={13} /> VERIFIED
                </span>
              </div>

              <div className="version-route">
                <div>
                  <span>parent</span>
                  <strong>v{PROOFPATCH.parentVersion}</strong>
                  <code>{short(PROOFPATCH.parentCodeHash)}</code>
                </div>
                <div className="route-rail">
                  <i />
                  <ArrowRight size={16} />
                </div>
                <div className="active">
                  <span>installed</span>
                  <strong>v{PROOFPATCH.candidateVersion}</strong>
                  <code>{short(PROOFPATCH.candidateCodeHash)}</code>
                </div>
              </div>

              <div className="consensus-vector">
                {["SOURCE", "CI", "AUDIT", "SEMANTICS", "FINALITY"].map((label) => (
                  <div key={label}>
                    <i />
                    <span>{label}</span>
                    <b>PASS</b>
                  </div>
                ))}
              </div>

              <div className="window-finality">
                <div><span>01</span><p>Review finalized</p><CheckCircle2 size={16} /></div>
                <div><span>02</span><p>Upgrade finalized</p><CheckCircle2 size={16} /></div>
                <div><span>03</span><p>Install confirmed</p><CheckCircle2 size={16} /></div>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      <section className="proof-strip">
        <div><span>GOVERNOR</span><code>{short(PROOFPATCH.governor)}</code></div>
        <div><span>TARGET</span><code>{short(PROOFPATCH.target)}</code></div>
        <div><span>PROPOSAL</span><strong>#1 · VERIFIED</strong></div>
        <div><span>RELEASE</span><strong>2.0.0</strong></div>
      </section>

      <section className="section intro-section">
        <Reveal>
          <div className="section-heading split">
            <div>
              <span className="section-label">THE ADMIN-KEY BLIND SPOT</span>
              <h2>
                A code hash proves bytes.
                <br />
                <em>It does not prove permission.</em>
              </h2>
            </div>
            <p>
              Upgradeable contracts usually answer “who can change code?” ProofPatch
              answers the harder question: “what must be proven before these exact
              replacement bytes are allowed to become the contract?”
            </p>
          </div>
        </Reveal>

        <div className="problem-grid">
          {[
            {
              icon: Code2,
              n: "01",
              title: "Integrity ≠ authority",
              text: "Matching a hash can prove the bytes are unchanged. It says nothing about whether the publisher is trusted or the change is semantically safe.",
            },
            {
              icon: Fingerprint,
              n: "02",
              title: "Schema ≠ semantics",
              text: "A candidate can preserve interfaces while adding a privilege path, weakening evidence rules or changing user rights.",
            },
            {
              icon: Workflow,
              n: "03",
              title: "Accepted ≠ final",
              text: "Consensus decisions remain appealable. Irreversible installation must be bound to protocol finality, not an early status badge.",
            },
          ].map((item, index) => {
            const Icon = item.icon;
            return (
              <Reveal className="problem-card" delay={index * 70} key={item.title}>
                <div><Icon size={21} /><span>{item.n}</span></div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </Reveal>
            );
          })}
        </div>
      </section>

      <section className="section flow-section" id="how-it-works">
        <Reveal>
          <div className="section-heading">
            <span className="section-label">HOW PROOFPATCH WORKS</span>
            <h2>A six-stage path from candidate to consequence.</h2>
            <p>
              Each stage removes a different class of upgrade risk. None is allowed
              to impersonate another.
            </p>
          </div>
        </Reveal>

        <div className="flow-list">
          {flow.map((step, index) => {
            const Icon = step.icon;
            return (
              <Reveal className="flow-row" key={step.n} delay={index * 45}>
                <div className="flow-number">{step.n}</div>
                <div className="flow-icon"><Icon size={20} /></div>
                <div className="flow-copy">
                  <h3>{step.title}</h3>
                  <p>{step.text}</p>
                </div>
                <div className="flow-state">
                  <span>gate</span>
                  <strong>REQUIRED</strong>
                </div>
              </Reveal>
            );
          })}
        </div>
      </section>

      <section className="section security-section" id="security">
        <Reveal>
          <div className="section-heading split">
            <div>
              <span className="section-label">SECURITY MODEL</span>
              <h2>Designed to fail closed.</h2>
            </div>
            <p>
              ProofPatch binds evidence trust, exact consequences and recovery rules
              into the same upgrade policy instead of relying on reviewer convention.
            </p>
          </div>
        </Reveal>

        <div className="security-grid landing-security">
          {SECURITY_GATES.map((gate, index) => (
            <Reveal key={gate.title} delay={index * 55}>
              <article>
                <div className="security-check"><CheckCircle2 size={17} /></div>
                <strong>{gate.title}</strong>
                <p>{gate.detail}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="section docs-section" id="documentation">
        <Reveal>
          <div className="section-heading docs-heading">
            <div>
              <span className="section-label">DOCUMENTATION</span>
              <h2>Understand the system before you launch it.</h2>
            </div>
            <p>
              This landing page is intentionally part product page, part operator
              manual. The app should never ask a user to sign something they do not
              understand.
            </p>
          </div>
        </Reveal>

        <div className="docs-layout">
          <aside className="docs-nav">
            <span>ON THIS PAGE</span>
            {docs.map((doc) => <a href={`#doc-${doc.id}`} key={doc.id}>{doc.label}</a>)}
          </aside>

          <div className="docs-content">
            {docs.map((doc, index) => (
              <Reveal key={doc.id} delay={index * 35}>
                <article id={`doc-${doc.id}`} className="doc-chapter">
                  <span>{doc.label}</span>
                  <h3>{doc.title}</h3>
                  <p>{doc.body}</p>
                </article>
              </Reveal>
            ))}

            <Reveal>
              <article className="architecture-card">
                <div className="architecture-head">
                  <div>
                    <span>REFERENCE FLOW</span>
                    <h3>Consensus → finality → install → confirmation</h3>
                  </div>
                  <Sparkles size={20} />
                </div>
                <pre>{`review_proposal(#1)
    ↓ validators agree on exact consequential result
Accepted (appealable)
    ↓ protocol finalization
proofpatch_upgrade(#1, approved_sha256)
    ↓ target re-hashes approved bytes + replaces code
confirm_install(#1, installed_sha256)
    ↓ confirmation finalizes
VERIFIED / INSTALL_VERIFIED`}</pre>
              </article>
            </Reveal>
          </div>
        </div>
      </section>

      <section className="section live-proof-section" id="live-proof">
        <Reveal>
          <div className="section-heading split">
            <div>
              <span className="section-label">DEPLOYED REALITY</span>
              <h2>Don&apos;t trust the landing page. Read Bradbury.</h2>
            </div>
            <p>
              The product UI reads finalized governor and target state and checks the
              same values preserved in the independent final audit.
            </p>
          </div>
        </Reveal>
        <Reveal delay={80}>
          <LiveProof />
        </Reveal>
      </section>

      <section className="section launch-section">
        <Reveal>
          <div className="launch-panel">
            <div>
              <span className="section-label">READY TO INSPECT THE LIVE SYSTEM?</span>
              <h2>Open the actual ProofPatch workspace.</h2>
              <p>
                Read finalized state without a wallet. Connect only when an authorized
                action genuinely requires a signature.
              </p>
            </div>
            <Link className="button primary large" href="/app">
              Launch ProofPatch <ArrowRight size={18} />
            </Link>
          </div>
        </Reveal>
      </section>

      <footer className="site-footer">
        <Link className="brand compact" href="/">
          <span className="brand-glyph" aria-hidden><i /><i /><i /></span>
          <span>ProofPatch</span>
        </Link>
        <p>Consensus-gated upgrades for GenLayer Intelligent Contracts.</p>
        <div>
          <a href={PROOFPATCH.network.explorer} target="_blank" rel="noreferrer">Bradbury explorer</a>
          <Link href="/app">Launch app</Link>
        </div>
      </footer>
    </main>
  );
}

"use client";

import { BookOpen, FileCheck2, Search, ShieldCheck, Workflow } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

const commands = [
  { label: "Overview", href: "#overview", icon: ShieldCheck },
  { label: "Finality proof", href: "#finality", icon: Workflow },
  { label: "Evidence", href: "#evidence", icon: FileCheck2 },
  { label: "Documentation", href: "/#documentation", icon: BookOpen },
];

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen((value) => !value);
      }
      if (event.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const filtered = useMemo(
    () =>
      commands.filter((item) =>
        item.label.toLowerCase().includes(query.toLowerCase()),
      ),
    [query],
  );

  if (!open) return null;

  return (
    <div className="command-backdrop" onMouseDown={() => setOpen(false)}>
      <div
        className="command-panel"
        role="dialog"
        aria-modal="true"
        aria-label="Command palette"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="command-search">
          <Search size={18} />
          <input
            autoFocus
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Jump to a ProofPatch surface…"
          />
          <kbd>ESC</kbd>
        </div>
        <div className="command-results">
          {filtered.map(({ label, href, icon: Icon }) => (
            <a key={label} href={href} onClick={() => setOpen(false)}>
              <Icon size={17} />
              <span>{label}</span>
              <small>Open</small>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

"use client";

import { Laptop, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

const modes = ["system", "light", "dark"] as const;

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  if (!mounted) {
    return (
      <button className="icon-button" aria-label="Theme">
        <Laptop size={17} />
      </button>
    );
  }

  const current = modes.includes(theme as (typeof modes)[number])
    ? (theme as (typeof modes)[number])
    : "system";
  const next = modes[(modes.indexOf(current) + 1) % modes.length];

  const Icon = current === "light" ? Sun : current === "dark" ? Moon : Laptop;

  return (
    <button
      className="icon-button"
      aria-label={`Theme: ${current}. Switch to ${next}.`}
      title={`Theme: ${current}`}
      onClick={() => setTheme(next)}
    >
      <Icon size={17} />
    </button>
  );
}

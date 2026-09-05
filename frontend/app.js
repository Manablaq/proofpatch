const semanticChecks = [
  "Storage layout compatible",
  "User rights preserved",
  "No privilege escalation",
  "Upgrade authority preserved",
  "Consensus binding preserved",
  "Evidence trust preserved",
  "Finality safety preserved",
  "Liveness preserved",
  "No hidden value transfer",
  "Constitution satisfied",
];

const matrix = document.querySelector("#semanticMatrix");
semanticChecks.forEach((label) => {
  const row = document.createElement("div");
  row.className = "matrix-row";
  row.innerHTML = `<span>${label}</span><b>EXACT PASS</b>`;
  matrix.appendChild(row);
});

const toast = document.querySelector("#toast");
let toastTimer;
function notify(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.add("show");
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
}

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const view = button.dataset.view;
    if (view === "overview") window.scrollTo({ top: 0, behavior: "smooth" });
    if (view === "release") document.querySelector("#releaseDialog").showModal();
    if (view === "evidence") document.querySelector(".trust-card").scrollIntoView({ behavior: "smooth", block: "center" });
    if (view === "policy") document.querySelector(".semantic-panel").scrollIntoView({ behavior: "smooth", block: "center" });
  });
});

const candidateHash = document.querySelector("#candidateHashFull").textContent;
document.querySelector("#copyHash").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(candidateHash);
    notify("Candidate SHA-256 copied");
  } catch {
    notify(candidateHash);
  }
});

document.querySelector("#openProposal").addEventListener("click", () => {
  document.querySelector("#releaseDialog").showModal();
});

document.querySelector("#appealBtn").addEventListener("click", () => {
  notify("Prototype only — live appeal action activates after Bradbury binding.");
});

let seconds = 18 * 60 + 42;
const countdown = document.querySelector("#countdown");
setInterval(() => {
  if (seconds <= 0) return;
  seconds -= 1;
  const h = Math.floor(seconds / 3600).toString().padStart(2, "0");
  const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  countdown.textContent = `${h} : ${m} : ${s}`;
}, 1000);

import { useState, useEffect } from "react";
import { login } from "../api/client";

const NODES = [
  { id: "core", x: 240, y: 220, r: 6, core: true },
  { id: "a", x: 90, y: 100, r: 3.5 },
  { id: "b", x: 55, y: 240, r: 3 },
  { id: "c", x: 110, y: 360, r: 3.2 },
  { id: "d", x: 250, y: 400, r: 3.5 },
  { id: "e", x: 390, y: 350, r: 3.2 },
  { id: "f", x: 420, y: 200, r: 3 },
  { id: "g", x: 360, y: 80, r: 3.2 },
  { id: "h", x: 200, y: 60, r: 3 },
];
const EDGES = ["a", "b", "c", "d", "e", "f", "g", "h"].map((id) => ["core", id]);

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

  const [pulseKey, setPulseKey] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setPulseKey((k) => k + 1), 2400);
    return () => clearInterval(t);
  }, []);

  async function handleLogin(e) {
    e?.preventDefault();
    try {
      setLoading(true);
      setError("");

      await login(email, password);

      window.location.reload();
    } catch {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  const nodeById = Object.fromEntries(NODES.map((n) => [n.id, n]));
  const activeEdge = EDGES[pulseKey % EDGES.length];

  return (
    <div style={S.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; }

        @keyframes hf-gridDrift {
          from { background-position: 0 0; }
          to { background-position: 60px 60px; }
        }
        @keyframes hf-scan {
          0% { transform: translateY(-100%); opacity: 0; }
          10% { opacity: .5; }
          90% { opacity: .5; }
          100% { transform: translateY(100%); opacity: 0; }
        }
        @keyframes hf-fadeUp {
          from { opacity: 0; transform: translateY(14px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes hf-spin {
          to { transform: rotate(360deg); }
        }
        @keyframes hf-drift {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-6px); }
        }
        @keyframes hf-travel {
          from { offset-distance: 0%; opacity: 0; }
          8% { opacity: 1; }
          92% { opacity: 1; }
          to { offset-distance: 100%; opacity: 0; }
        }
        @keyframes hf-glowPulse {
          0%, 100% { opacity: .55; }
          50% { opacity: 1; }
        }

        .hf-grid {
          position: absolute;
          inset: 0;
          background-image:
            linear-gradient(rgba(0,198,255,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,198,255,0.06) 1px, transparent 1px);
          background-size: 46px 46px;
          animation: hf-gridDrift 14s linear infinite;
        }
        .hf-scanline {
          position: absolute;
          left: 0; right: 0;
          height: 140px;
          background: linear-gradient(180deg, transparent, rgba(0,198,255,0.08), transparent);
          animation: hf-scan 6s linear infinite;
          pointer-events: none;
        }

        .hf-edge { stroke: #1E3A66; stroke-width: 1; fill: none; }
        .hf-edge.on { stroke: #00C6FF; stroke-width: 1.4; }
        .hf-pulse { fill: #00C6FF; filter: drop-shadow(0 0 5px rgba(0,198,255,.9)); }

        .hf-field {
          width: 100%;
          padding: 14px 16px;
          border-radius: 10px;
          outline: none;
          background: rgba(255,255,255,0.03);
          color: #EAF4FF;
          font-size: 15px;
          border: 1px solid #1B2C4D;
          transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
          font-family: 'Inter', sans-serif;
        }
        .hf-field::placeholder { color: #4C6690; }
        .hf-field:focus {
          border-color: #00C6FF;
          background: rgba(0,180,255,0.06);
          box-shadow: 0 0 0 4px rgba(0,140,255,0.14);
        }

        .hf-submit {
          width: 100%;
          padding: 15px;
          border-radius: 10px;
          border: none;
          cursor: pointer;
          background: linear-gradient(90deg,#0057D8,#00C6FF);
          background-size: 200% 100%;
          color: #04050A;
          font-weight: 700;
          font-size: 15.5px;
          box-shadow: 0 0 22px rgba(0,180,255,.4);
          transition: transform .15s ease, box-shadow .25s ease, background-position .6s ease;
        }
        .hf-submit:hover:not(:disabled) { box-shadow: 0 0 32px rgba(0,198,255,.65); background-position: 100% 0; }
        .hf-submit:active:not(:disabled) { transform: scale(0.98); }
        .hf-submit:disabled { opacity: 0.75; cursor: default; }
        .hf-submit:focus-visible { outline: 2px solid #00C6FF; outline-offset: 3px; }

        .hf-eye {
          background: none; border: none; cursor: pointer;
          color: #5E7CAE; font-size: 11.5px; letter-spacing: .06em; padding: 4px 6px;
          font-family: 'JetBrains Mono', monospace;
        }
        .hf-eye:hover { color: #8FB7FF; }

        .hf-spinner {
          display: inline-block; width: 14px; height: 14px; border-radius: 50%;
          border: 2px solid rgba(4,5,10,0.3); border-top-color: #04050A;
          animation: hf-spin .7s linear infinite; vertical-align: middle; margin-right: 8px;
        }

        .hf-appear { animation: hf-fadeUp .5s ease both; }

        @media (max-width: 900px) {
          .hf-side { display: none; }
        }
        @media (prefers-reduced-motion: reduce) {
          .hf-grid, .hf-scanline, .hf-appear, .hf-net-wrap { animation: none !important; }
        }
      `}</style>

      {/* LEFT — futuristic signal panel */}
      <div className="hf-side" style={S.side}>
        <div className="hf-grid" />
        <div className="hf-scanline" />

        <div style={{ position: "relative", zIndex: 2 }}>
          <div style={S.brandRow}>
            <span style={S.brandMark}>◆</span>
            <span style={S.brandWord}>HOBBYFI</span>
          </div>

          <h1 style={S.headline}>
            One core.
            <br />
            Every signal.
          </h1>

          <p style={S.subcopy}>
            HobbyFi Copilot keeps every vendor feed synced to a single
            source of truth, in real time, at scale.
          </p>
        </div>

        <div className="hf-net-wrap" style={{ ...S.networkWrap, animation: "hf-drift 7s ease-in-out infinite", position: "relative", zIndex: 2 }}>
          <svg viewBox="0 0 480 440" style={S.networkSvg} aria-hidden="true">
            {EDGES.map(([from, to], i) => {
              const a = nodeById[from];
              const b = nodeById[to];
              const isOn = activeEdge && activeEdge[1] === to;
              return (
                <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} className={`hf-edge${isOn ? " on" : ""}`} />
              );
            })}
            <circle cx={nodeById.core.x} cy={nodeById.core.y} r="20" fill="none" stroke="rgba(0,198,255,0.25)" strokeWidth="1">
              <animate attributeName="r" values="16;26;16" dur="3.2s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.5;0;0.5" dur="3.2s" repeatCount="indefinite" />
            </circle>
            {NODES.map((n) => (
              <circle key={n.id} cx={n.x} cy={n.y} r={n.r} fill={n.core ? "#00C6FF" : "#5E7CAE"} opacity={n.core ? 1 : 0.8} />
            ))}
            {activeEdge && (
              <circle
                key={pulseKey}
                r="3"
                className="hf-pulse"
                style={{
                  offsetPath: `path('M ${nodeById[activeEdge[1]].x} ${nodeById[activeEdge[1]].y} L ${nodeById[activeEdge[0]].x} ${nodeById[activeEdge[0]].y}')`,
                  animation: "hf-travel 2.4s linear forwards",
                }}
              />
            )}
          </svg>
        </div>

        <div style={{ ...S.ticker, position: "relative", zIndex: 2 }}>
          <span style={S.tickerDot} />
          247 vendor feeds synced in the last hour
        </div>
      </div>

      {/* RIGHT — login form */}
      <div style={S.form}>
        <div className="hf-appear" style={S.formInner}>
          <div style={S.mobileBrandRow}>
            <span style={S.brandMark}>◆</span>
            <span style={S.brandWord}>HOBBYFI</span>
          </div>

          <div style={S.iconBadge}>🤖</div>

          <h2 style={S.formTitle}>Sign in to continue</h2>
          <p style={S.formSub}>AI CRM Vendor Portal</p>

          <form onSubmit={handleLogin} noValidate>
            <div style={{ marginBottom: 20 }}>
              <label
                style={{ ...S.label, color: emailFocused ? "#00C6FF" : "#8FB7FF" }}
                htmlFor="hf-email"
              >
                Email Address
              </label>
              <input
                id="hf-email"
                className="hf-field"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onFocus={() => setEmailFocused(true)}
                onBlur={() => setEmailFocused(false)}
                autoComplete="email"
              />
            </div>

            <div style={{ marginBottom: 12 }}>
              <div style={S.pwRow}>
                <label
                  style={{ ...S.label, marginBottom: 0, color: passwordFocused ? "#00C6FF" : "#8FB7FF" }}
                  htmlFor="hf-password"
                >
                  Password
                </label>
                <button
                  type="button"
                  className="hf-eye"
                  onClick={() => setShowPassword((s) => !s)}
                  tabIndex={-1}
                >
                  {showPassword ? "HIDE" : "SHOW"}
                </button>
              </div>
              <input
                id="hf-password"
                className="hf-field"
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onFocus={() => setPasswordFocused(true)}
                onBlur={() => setPasswordFocused(false)}
                autoComplete="current-password"
              />
            </div>

            <div style={{ textAlign: "right", marginBottom: 25 }}>
              <a href="#" style={S.forgotLink}>Forgot password?</a>
            </div>

            <button type="submit" className="hf-submit" disabled={loading}>
              {loading && <span className="hf-spinner" />}
              {loading ? "Authenticating..." : "Login"}
            </button>
          </form>

          {error && (
            <div className="hf-appear" style={S.errorBox}>
              {error}
            </div>
          )}

          <div style={S.footerNote}>
            <span style={S.tickerDot} />
            Secure Vendor Authentication
          </div>
        </div>
      </div>
    </div>
  );
}

const S = {
  page: {
    height: "100vh",
    display: "flex",
    fontFamily: "'Inter', sans-serif",
    background: "#04050A",
    overflow: "hidden",
  },
  side: {
    width: "46%",
    minWidth: 380,
    maxWidth: 560,
    height: "100%",
    background: "linear-gradient(160deg,#04050A 0%,#070C18 45%,#0A1428 100%)",
    color: "#EAF4FF",
    padding: "5vh 44px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    position: "relative",
    overflow: "hidden",
    borderRight: "1px solid rgba(0,198,255,0.12)",
    boxSizing: "border-box",
  },
  brandRow: { display: "flex", alignItems: "center", gap: 10, marginBottom: "3vh" },
  mobileBrandRow: { display: "none" },
  brandMark: { color: "#00C6FF", fontSize: 15 },
  brandWord: {
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 12.5,
    letterSpacing: "0.24em",
    color: "#EAF4FF",
  },
  headline: {
    fontWeight: 700,
    fontSize: "clamp(26px, 3.2vw, 38px)",
    lineHeight: 1.14,
    letterSpacing: "-0.01em",
    margin: "0 0 16px",
    color: "#EAF4FF",
  },
  subcopy: {
    fontSize: 14,
    lineHeight: 1.6,
    color: "#7E97C4",
    maxWidth: 340,
    margin: 0,
  },
  networkWrap: { margin: "10px 0", maxHeight: "34vh", display: "flex", alignItems: "center", justifyContent: "center" },
  networkSvg: { width: "100%", maxHeight: "34vh", height: "auto", display: "block" },
  ticker: {
    display: "flex",
    alignItems: "center",
    gap: 9,
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 11.5,
    color: "#5E7CAE",
    letterSpacing: "0.02em",
  },
  tickerDot: {
    width: 6,
    height: 6,
    borderRadius: "50%",
    background: "#3ED598",
    boxShadow: "0 0 6px rgba(62,213,152,.8)",
    flexShrink: 0,
    display: "inline-block",
  },
  form: {
    flex: 1,
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "24px 32px",
    position: "relative",
    overflowY: "auto",
    boxSizing: "border-box",
  },
  formInner: { width: "100%", maxWidth: 380, margin: "auto" },
  iconBadge: {
    width: 52,
    height: 52,
    margin: "0 auto 14px",
    borderRadius: 14,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 24,
    background: "linear-gradient(145deg, rgba(0,123,255,0.22), rgba(0,198,255,0.08))",
    border: "1px solid rgba(0,180,255,0.3)",
    boxShadow: "0 0 22px rgba(0,140,255,.3)",
  },
  formTitle: {
    fontWeight: 700,
    fontSize: 23,
    color: "#EAF4FF",
    margin: "0 0 6px",
    textAlign: "center",
  },
  formSub: {
    fontSize: 13.5,
    color: "#7E97C4",
    textAlign: "center",
    margin: "0 0 26px",
  },
  label: {
    display: "block",
    fontSize: 14,
    marginBottom: 8,
    transition: "color .2s ease",
  },
  pwRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  forgotLink: { color: "#5E7CAE", fontSize: 13, textDecoration: "none" },
  errorBox: {
    marginTop: 18,
    background: "rgba(255,60,60,.12)",
    border: "1px solid rgba(255,90,90,.3)",
    padding: 12,
    borderRadius: 10,
    color: "#FF9090",
    textAlign: "center",
    fontSize: 13.5,
  },
  footerNote: {
    marginTop: 34,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    fontSize: 12.5,
    color: "#5E7CAE",
  },
};
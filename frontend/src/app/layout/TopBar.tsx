import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../../shared/ui/Button";
import { useAuth } from "../../features/auth/auth";
import "./topbar.css";

type Lang = { code: string; name: string; short: string };

const LANGS: Lang[] = [
  { code: "en", name: "English", short: "EN" },
  { code: "id", name: "Bahasa Indonesia", short: "ID" },
  { code: "ja", name: "日本語", short: "JP" },
  { code: "ko", name: "한국어", short: "KR" },
  { code: "ru", name: "Русский", short: "RU" },
  { code: "vi", name: "Tiếng Việt", short: "VI" },
  { code: "zh-CN", name: "简体中文", short: "CN" },
  { code: "zh-TW", name: "繁體中文", short: "TW" },
  { code: "uk", name: "Українська", short: "UA" }
];

export function TopBar() {
  const nav = useNavigate();
  const { user, isAuthenticated, isLoading, loginWithDiscord, logout } = useAuth();

  const [langOpen, setLangOpen] = useState(false);
  const [lang, setLang] = useState<Lang>(LANGS[0]);
  const langRef = useRef<HTMLDivElement | null>(null);
  const [authBusy, setAuthBusy] = useState(false);

  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (!langRef.current) return;
      if (!langRef.current.contains(e.target as Node)) setLangOpen(false);
    }
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, []);

  const [search, setSearch] = useState("");

  async function handleLogout() {
    try {
      setAuthBusy(true);
      await logout();
      nav("/");
    } finally {
      setAuthBusy(false);
    }
  }

  const displayName = user?.global_name || user?.username || "User";
  const canSeeAdmin = user?.role === "admin" || user?.role === "moderator";

  return (
    <div className="topbar">
      <div className="topbarLeft">
        <button className="brand" onClick={() => nav("/")}>
          <span className="brandMark">Acetaria🥬Alpha</span>
        </button>

        <Button
          variant="outline"
          className="hsrBtn"
          onClick={() => nav("/hsr")}
          title="Go to Honkai: Star Rail"
        >
          Honkai: Star Rail
        </Button>
        <div className="topbarRight">
          <p className="betaTag">Brought to you by: nkenze, qkenze, kenz, кензая, кинза</p>
        </div>
      </div>

      <div className="topbarRight">
        <div className="pillRow">
          <Button hidden={true} variant="ghost">Challenges</Button>
          <Button hidden={true} variant="ghost">Forums</Button>
          <Button hidden={true} variant="ghost">Help</Button>
          <Button variant="ghost">SUPPORT TBD</Button>

          <div className="searchWrap" role="search" aria-label="Search">
            <input
              hidden={true}
              className="searchInput"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search"
            />
          </div>
        </div>

        <div hidden={true} className="divider" />

        <div className="pillRow">
          <div hidden={true} className="langDropdown" ref={langRef}>
            <button
              className="langTrigger"
              onClick={() => setLangOpen((s) => !s)}
              aria-haspopup="listbox"
              aria-expanded={langOpen}
              title="Language (placeholder)"
            >
              <span className="globe" aria-hidden="true">🌐</span>
              <span className="langShort">{lang.short}</span>
              <span className="caret" aria-hidden="true">▾</span>
            </button>

            {langOpen ? (
              <div className="langMenu" role="listbox">
                {LANGS.map((l) => (
                  <button
                    key={l.code}
                    className="langItem"
                    onClick={() => {
                      setLang(l);
                      setLangOpen(false);
                    }}
                  >
                    {l.name}
                  </button>
                ))}
              </div>
            ) : null}
          </div>

          {isLoading ? (
            <span className="authMeta">Checking session...</span>
          ) : isAuthenticated ? (
            <>
              <div className="authUserChip" title={`Role: ${user?.role ?? "user"}`}>
                {user?.avatar ? <img src={user.avatar} alt={displayName} className="authAvatar" /> : null}
                <div className="authUserText">
                  <span className="authUserName">{displayName}</span>
                  <span className="authUserRole">{user?.role}</span>
                </div>
              </div>
              {canSeeAdmin ? (
                <Link className="adminLink" to="/admin">
                  Admin
                </Link>
              ) : null}
              <Button variant="ghost" onClick={() => void handleLogout()} disabled={authBusy}>
                {authBusy ? "Logging out..." : "Log out"}
              </Button>
            </>
          ) : (
            <>
              <Button variant="ghost" onClick={loginWithDiscord}>Log in</Button>
              <Button variant="primary" onClick={loginWithDiscord}>Sign up</Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

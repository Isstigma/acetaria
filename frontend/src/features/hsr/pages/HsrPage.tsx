import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useModesQuery } from "../../games/queries";
import { ModeSelector } from "../components/ModeSelector";
import { LeaderboardTable } from "../components/LeaderboardTable";
import { Button } from "../../../shared/ui/Button";
import { apiGet } from "../../../shared/api/client";
import type { Page } from "../../../shared/api/types";
import "./hsr.css";

const TABS = ["Leaderboards", "News", "Guides", "Resources", "Forums", "Streams", "Stats"] as const;
type Tab = (typeof TABS)[number];

const TAB_ENDPOINTS: Record<Exclude<Tab, "Leaderboards">, string> = {
  News: "/games/hsr/news?page=1&pageSize=20",
  Guides: "/games/hsr/guides?page=1&pageSize=20",
  Resources: "/games/hsr/resources?page=1&pageSize=20",
  Forums: "/forums?page=1&pageSize=20",
  Streams: "/games/hsr/streams?page=1&pageSize=20",
  Stats: "/games/hsr/stats",
};

type NavItem = { id: string; title: string; summary: string; createdAt: string };
type StatsOut = {
  gameSlug: string;
  modeSlug?: string | null;
  totalRuns: number;
  totalLeaderboardEntries: number;
  totalTeamEntries: number;
};

function TabList({ endpoint }: { endpoint: string }) {
  const q = useQuery({
    queryKey: ["hsr-tab", endpoint],
    queryFn: () => apiGet<Page<NavItem>>(endpoint),
  });

  if (q.isLoading) return <div className="subtle">Loading...</div>;
  if (q.isError) return <div className="subtle">Failed to load.</div>;
  if (!q.data?.items?.length) return <div className="subtle">No items.</div>;

  return (
    <div className="tabFeed">
      {q.data.items.map((it) => (
        <div key={it.id} className="feedRow">
          <div className="feedTitle">{it.title}</div>
          <div className="feedSummary">{it.summary}</div>
        </div>
      ))}
    </div>
  );
}

function TabStats({ modeSlug }: { modeSlug: string }) {
  const endpoint = `${TAB_ENDPOINTS.Stats}?mode=${encodeURIComponent(modeSlug)}`;
  const q = useQuery({
    queryKey: ["hsr-stats", modeSlug],
    queryFn: () => apiGet<StatsOut>(endpoint),
  });

  if (q.isLoading) return <div className="subtle">Loading...</div>;
  if (q.isError) return <div className="subtle">Failed to load.</div>;
  if (!q.data) return <div className="subtle">No data.</div>;

  return (
    <div className="tabFeed">
      <div className="feedRow">
        <div className="feedTitle">Stats (placeholder)</div>
        <div className="feedSummary">
          Total Runs: {q.data.totalRuns} • Leaderboard Entries: {q.data.totalLeaderboardEntries} • Team Entries:{" "}
          {q.data.totalTeamEntries}
        </div>
      </div>
    </div>
  );
}

export function HsrPage() {
  const modesQ = useModesQuery("hsr");

  const rawModes = modesQ.data?.items ?? [];
  // Remove legacy/broken modes that still contain "(Cycles)" / "(Time)".
  const modes = useMemo(() => {
    const filtered = rawModes.filter((m) => {
      const badName = /\((cycles|time)\)\s*$/i.test(m.modeName);
      const badSlug = /-(cycles|time)$/.test(m.modeSlug);
      return !badName && !badSlug;
    });

    // De-dup by modeSlug (defensive)
    const seen = new Set<string>();
    return filtered.filter((m) => (seen.has(m.modeSlug) ? false : (seen.add(m.modeSlug), true)));
  }, [rawModes]);

  const latestMode = useMemo(() => {
    return modes.find((m) => m.isLatest)?.modeSlug ?? modes[0]?.modeSlug ?? "";
  }, [modes]);

  const [modeSlug, setModeSlug] = useState<string>("");
  const [tab, setTab] = useState<Tab>("Leaderboards");

  useEffect(() => {
    if (!modeSlug && latestMode) setModeSlug(latestMode);
    if (modeSlug && modes.length && !modes.some((m) => m.modeSlug === modeSlug)) setModeSlug(latestMode);
  }, [latestMode, modeSlug, modes]);

  return (
    <div className="page">
      <div className="pageHeader">
        <h1 className="h1">Honkai: Star Rail</h1>
        <div className="subtle">MVP implementation. Tabs other than Leaderboards show dummy API-backed content.</div>
      </div>

      <div className="tabs">
        {TABS.map((t) => (
          <button
            key={t}
            className={["tab", t === tab ? "tabActive" : ""].join(" ")}
            onClick={() => setTab(t)}
            type="button"
          >
            {t}
          </button>
        ))}
      </div>

      {tab !== "Leaderboards" ? (
        tab === "Stats" ? (
          <TabStats modeSlug={modeSlug} />
        ) : (
          <TabList endpoint={TAB_ENDPOINTS[tab]} />
        )
      ) : (
        <>
          <div className="panel">
            <div className="panelHeader">
              <div className="sectionTitle">Mode</div>
            </div>

            <ModeSelector
              modes={modes}
              value={modeSlug}
              onChange={setModeSlug}
              isLoading={modesQ.isLoading}
              isError={modesQ.isError}
            />
          </div>

          <div className="toolbarRow toolbarRowSplit">
            <div className="toolbarLeft">
              <Button variant="ghost">Filter</Button>
              <Button variant="ghost">0-Cycle</Button>
              <Button variant="ghost">full stars</Button>
            </div>
            <div className="toolbarRight">
              <Button variant="primary">Submit</Button>
            </div>
          </div>

          <LeaderboardTable modeSlug={modeSlug} />
        </>
      )}
    </div>
  );
}

import { useEffect, useMemo, useRef, useState } from "react";
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
  modeId?: string | null;
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

function TabStats({ modeId: modeId }: { modeId: string }) {
  const endpoint = `${TAB_ENDPOINTS.Stats}?mode=${encodeURIComponent(modeId)}`;
  const q = useQuery({
    queryKey: ["hsr-stats", modeId],
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

  const rawModes = modesQ.data ?? [];
  const modes = useMemo(() => {
    const filtered = rawModes.filter((m) => {
      const badName = /\((cycles|time)\)\s*$/i.test(m.name);
      const badSlug = /-(cycles|time)$/.test(m.id);
      return !badName && !badSlug;
    });

    // De-dup by modeSlug (defensive)
    const seen = new Set<string>();
    return filtered.filter((m) => (seen.has(m.id) ? false : (seen.add(m.id), true)));
  }, [rawModes]);

  const [modeId, setModeId] = useState<string>("");
  const [modeEntryId, setModeEntryId] = useState<number>(0);
  const [tab, setTab] = useState<Tab>("Leaderboards");

  // useEffect(() => {
  //   if (!modeId && latestMode) setModeEntryId(latestMode?.game_mode_entries?.[0]?.stage_id ?? 0);
  //   if (modeId && modes.length && !modes.some((m) => m.id === modeId)) setModeId(latestMode?.id ?? "");
  // }, [latestMode, modeId, modes]);

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
          <TabStats modeId={modeId} />
        ) : (
          <TabList endpoint={TAB_ENDPOINTS[tab]} />
        )
      ) : (
        <>
          <ModeSelector
            modes={modes}
            modeId={modeId}
            stageId={modeEntryId}
            onModeStageChange={setModeEntryId}
            onModeChange={setModeId}
            isLoading={modesQ.isLoading}
            isError={modesQ.isError}
          />

          <LeaderboardTable stageId={modeEntryId} mode={rawModes.find(m => m.id === modeId)} />
        </>
      )}
    </div>
  );
}

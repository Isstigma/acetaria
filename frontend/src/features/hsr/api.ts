import { apiGet } from "../../shared/api/client";
import type { Page, LeaderboardEntry, TeamEntry } from "../../shared/api/types";

export function getHsrLeaderboards(modeSlug: string, page: number, pageSize: number) {
  const qs = new URLSearchParams({
    mode: modeSlug,
    page: String(page),
    pageSize: String(pageSize)
  });
  return apiGet<Page<LeaderboardEntry>>(`/games/hsr/leaderboards?${qs.toString()}`);
}

export function getTeams(entryId: string, page: number, pageSize: number) {
  const qs = new URLSearchParams({
    page: String(page),
    pageSize: String(pageSize)
  });
  return apiGet<Page<TeamEntry>>(`/leaderboard-entries/${encodeURIComponent(entryId)}/teams?${qs.toString()}`);
}

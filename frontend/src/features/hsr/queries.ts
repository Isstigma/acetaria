import { useQuery } from "@tanstack/react-query";
import { getHsrLeaderboards, getTeams } from "./api";

export function useHsrLeaderboardQuery(modeSlug: string, page: number, pageSize: number) {
  return useQuery({
    queryKey: ["hsr", "leaderboards", modeSlug, page, pageSize],
    queryFn: () => getHsrLeaderboards(modeSlug, page, pageSize),
    enabled: !!modeSlug
  });
}

export function useTeamsQuery(entryId: string, enabled: boolean) {
  return useQuery({
    queryKey: ["hsr", "teams", entryId],
    queryFn: () => getTeams(entryId, 1, 20),
    enabled: enabled && !!entryId
  });
}

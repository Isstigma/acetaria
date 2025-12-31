import { useQuery } from "@tanstack/react-query";
import { getGames, getModes } from "./api";

export function useGamesQuery() {
  return useQuery({
    queryKey: ["games"],
    queryFn: getGames
  });
}

export function useModesQuery(gameSlug: string) {
  return useQuery({
    queryKey: ["modes", gameSlug],
    queryFn: () => getModes(gameSlug),
    enabled: !!gameSlug
  });
}

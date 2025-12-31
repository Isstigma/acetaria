import { useQuery } from "@tanstack/react-query";
import { getLatestRuns } from "./api";

export function useLatestRunsQuery(limit: number) {
  return useQuery({
    queryKey: ["runs", "latest", limit],
    queryFn: () => getLatestRuns(limit)
  });
}

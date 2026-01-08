import { useQuery } from "@tanstack/react-query";
import { getAllChars, getAllCosts, getLatestRuns, getRunsByStageId } from "./api";

export function useLatestRunsQuery(limit: number) {
  return useQuery({
    queryKey: ["runs", "latest", limit],
    queryFn: () => getLatestRuns(limit)
  });
}
export function useRunsByStageIdQuery(stageId: number) {
  return useQuery({
    queryKey: ["runs", stageId],
    queryFn: () => getRunsByStageId(stageId)
  });
}

export function useGetAllCharsQuery() {
  return useQuery({
    queryKey: ["hsr", "chars"],
    queryFn: () => getAllChars()
  });
}

export function useGetAllCostsQuery() {
  return useQuery({
    queryKey: ["hsr", "costs"],
    queryFn: () => getAllCosts()
  });
}
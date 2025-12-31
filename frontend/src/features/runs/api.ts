import { apiGet } from "../../shared/api/client";
import type { Page, LatestRunCard } from "../../shared/api/types";

export function getLatestRuns(limit: number) {
  return apiGet<Page<LatestRunCard>>(`/runs/latest?limit=${encodeURIComponent(String(limit))}`);
}

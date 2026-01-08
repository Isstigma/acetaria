import { apiGet } from "../../shared/api/client";
import type { Page, LatestRunCard, Run, Character, Cost } from "../../shared/api/types";

export function getLatestRuns(limit: number) {
  return apiGet<Page<LatestRunCard>>(`/runs/latest?limit=${encodeURIComponent(String(limit))}`);
}

export function getRunsByStageId(stageId: number) {
  return apiGet<Run[]>(`/runs/${(String(stageId))}`);
}


export function getAllChars() {
  return apiGet<Character[]>(`/games/hsr/chars`);
}

export function getAllCosts() {
  return apiGet<Cost[]>(`/costs`);
}
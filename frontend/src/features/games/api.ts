import { apiGet } from "../../shared/api/client";
import type { Page, Game, Mode } from "../../shared/api/types";

export function getGames() {
  return apiGet<Page<Game>>("/games?page=1&pageSize=50");
}

export function getModes(gameSlug: string) { 
  // const dummmy: Page<Mode> = {page: 0, total: 10, pageSize: 10, items: [{modeSlug: 'as', isLatest: true, playMetricType: "cycles", modeName: 'AS'}]}
  const a = apiGet<Mode[]>(`/games/${encodeURIComponent(gameSlug)}/modes?page=1&pageSize=50`);
  return a;
}

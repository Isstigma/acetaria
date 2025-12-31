import { apiGet } from "../../shared/api/client";
import type { Page, Game, Mode } from "../../shared/api/types";

export function getGames() {
  return apiGet<Page<Game>>("/games?page=1&pageSize=50");
}

export function getModes(gameSlug: string) {
  return apiGet<Page<Mode>>(`/games/${encodeURIComponent(gameSlug)}/modes?page=1&pageSize=50`);
}

export type Page<T> = {
  items: T[];
  page: number;
  pageSize: number;
  total: number;
};

export type Game = { slug: string; name: string };

export type Mode = {
  modeSlug: string;
  modeName: string;
  playMetricType: "cycles" | "time";
  isLatest: boolean;
};

export type Metric =
  | { type: "cycles"; cycles: number }
  | { type: "time"; timeMs: number };

export type Video = {
  platform: "youtube" | "bilibili" | "twitch";
  url: string;
  title: string;
  durationMs: number;
  thumbnailUrl: string;
};

export type LatestRunCard = {
  runId: string;
  gameSlug: string;
  gameName: string;
  modeSlug: string;
  modeName: string;
  title: string;
  place: number;
  metric: Metric;
  playerName: string;
  publishedAt: string;
  video: Video;
};

export type Character = { id: string; name: string; portraitUrl: string };

export type LeaderboardEntry = {
  entryId: string;
  character: Character;
  limStd: number;
  metric: Metric;
  player: { displayName: string };
  rank?: number | null;
};

export type TeamMemberPortrait = { id: string; portraitUrl: string };

export type TeamEntry = {
  teamEntryId: string;
  team: TeamMemberPortrait[];
  limStd: number;
  metric: Metric;
  player: { displayName: string };
  video: Video;
};

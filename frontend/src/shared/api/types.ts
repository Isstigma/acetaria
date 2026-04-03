export type Page<T> = {
  items: T[];
  page: number;
  pageSize: number;
  total: number;
};

export type Game = { slug: string; name: string };

export type Mode = {
  id: string;
  name: string;
  kind: "Unknown" |"Moc12" |"Pf" |"As" |"Aak1" |"Aak2" |"Aak3" |"Aacm" |"Aazz" 
  primary_score_kind: "cycles" | "time" | "points" | "av";
  primary_score_reverse_sorting: boolean;
  secondary_score_kind: "cycles" | "time" | "points" | "av" | null;
  secondary_score_reverse_sorting: boolean | null;
  game_mode_entries: GameModeEntry[];
  // name: string;
  // playMetricType: "cycles" | "time";
  // isLatest: boolean;
};

export type GameModeEntry = {
  name: string; 
  stage_id: number; 
  active_from: string; 
  active_to: string;
};


export type Metric =
  | { type: "cycles"; cycles: number }
  | { type: "time"; timeMs: number }
  | { type: "points"; points: number }
  | { type: "av", avValue: number };

export type Video = {
  platform: "youtube" | "bilibili" | "twitch";
  url: string;
  title: string;
  durationMs: number;
  thumbnailUrl: string;
};

export type Run = {
  id: string;
  game_mode_entry_id: number;
  primary_score: number;
  secondary_score: number | null;
  flags: "revive" | "nohit" | null;
  author: string;
  link: string;
  name: string;
  submitted_at: string;
  team: Team;
  run_costs: RunCost[];
}

export type RunCost = {
  cost_id: number;
  value: number;
}

export type Cost = {
  id: number;
  name: string;
}

export type Team = {
  id: number;
  name: string;
  units: Unit[];
}

export type Unit = {
  id: number;
  char_id: number;
  char_eidolon: number;
  lc_id: number;
  lc_superimposition: number;
}

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

export type Character = { 
  id: number; 
  name: string; 
  icon_url: string;
  rarity: number;
};

export type Lightcone = { 
  id: number; 
  name: string; 
  icon_url: string;
  rarity: number;
  sig_of_char_id: number | null;
};

export type LeaderboardEntry = {
  entryId: string;
  character: Character;
  limStd: number;
  metric: Metric;
  player: { displayName: string };
  rank?: number | null;
};

export type TeamMemberPortrait = { id: string; icon_url: string };

export type TeamEntry = {
  teamEntryId: string;
  team: TeamMemberPortrait[];
  limStd: number;
  metric: Metric;
  player: { displayName: string };
  video: Video;
};

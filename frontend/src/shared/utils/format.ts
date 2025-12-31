import type { Metric } from "../api/types";

export function formatMetric(metric: Metric): string {
  if (metric.type === "cycles") {
    if (metric.cycles === 0) return "0-Cycle";
    return `${metric.cycles} cycles`;
  }
  return formatDuration(metric.timeMs);
}

export function formatDuration(ms: number): string {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const millis = ms % 1000;

  if (minutes > 0) {
    return `${minutes}m ${seconds.toString().padStart(2, "0")}s`;
  }
  return `${seconds}s ${millis.toString().padStart(3, "0")}ms`;
}

export function platformLabel(p: "youtube" | "bilibili" | "twitch"): string {
  if (p === "youtube") return "YouTube";
  if (p === "bilibili") return "Bilibili";
  return "Twitch";
}

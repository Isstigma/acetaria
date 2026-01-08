import { useLatestRunsQuery } from "../features/runs/queries";
import { LoadingState } from "../shared/ui/LoadingState";
import { ErrorState } from "../shared/ui/ErrorState";
import { EmptyState } from "../shared/ui/EmptyState";
import { formatMetric } from "../shared/utils/format";
import { timeAgo } from "../shared/utils/time";

export function HomePage() {
  const q = useLatestRunsQuery(10);

  return (
    <div className="page">
      <div className="pageHeader">
        <h1 className="h1">Home</h1>
        <div className="subtle">Acetaria MVP: Honkai: Star Rail</div>
      </div>

      <div className="sectionTitle">Latest Runs</div>

      {q.isLoading && <LoadingState label="Loading latest runs..." />}
      {q.isError && <ErrorState error={(q.error as any)?.message ?? "Failed to fetch"} />}
      {!q.isLoading && !q.isError && (!q.data?.items || q.data.items.length === 0) && (
        <EmptyState label="No runs yet. Seed the database." />
      )}

      <div className="gridCards">
        {q.data?.items?.map((r) => (
          <a
            key={r.runId}
            className="card cardLink"
            href={r.video.url}
            target="_blank"
            rel="noreferrer"
          >
            <div className="cardTitleRow">
              <div className="cardGame">{r.gameName}</div>
              <div className="badge">{r.modeName}</div>
            </div>

            <div className="cardMain">
              <div className="runTitle">{r.title}</div>
              <div className="runPlace">
                Place: <span className="accentText">#{r.place}</span>
              </div>
            </div>

            <div className="cardMetaRow">
              <div className="metric">{formatMetric(r.metric)}</div>
              <div className="muted">{r.playerName}</div>
            </div>

            <div className="muted small">{timeAgo(r.publishedAt)}</div>
          </a>
        ))}
      </div>
    </div>
  );
}

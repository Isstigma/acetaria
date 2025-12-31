import { useTeamsQuery } from "../queries";
import { LoadingState } from "../../../shared/ui/LoadingState";
import { ErrorState } from "../../../shared/ui/ErrorState";
import { EmptyState } from "../../../shared/ui/EmptyState";
import { formatMetric, platformLabel, formatDuration } from "../../../shared/utils/format";

export function TeamsSubtable({ entryId }: { entryId: string }) {
  const q = useTeamsQuery(entryId, true);

  if (q.isLoading) return <LoadingState label="Loading teams..." />;
  if (q.isError) return <ErrorState error={q.error} />;
  if ((q.data?.items?.length ?? 0) === 0) return <EmptyState label="No teams for this entry." />;

  return (
    <div className="subtableWrap">
      <div className="subtableHeader">
        <div className="subtle">Teams (loaded on-demand)</div>
      </div>

      <table className="subtable">
        <thead>
          <tr>
            <th className="th">Team</th>
            <th className="th">Lim/Std</th>
            <th className="th">Play</th>
            <th className="th">Player (opens video)</th>
            <th className="th">Video</th>
          </tr>
        </thead>
        <tbody>
          {q.data?.items.map((t) => (
            <tr key={t.teamEntryId} className="tr">
              <td className="td">
                <div className="teamRow">
                  {t.team.map((m) => (
                    <img key={m.id} className="portraitSm" src={m.portraitUrl} alt={m.id} />
                  ))}
                </div>
              </td>
              <td className="td">{t.limStd}</td>
              <td className="td metric">{formatMetric(t.metric)}</td>
              <td className="td">
                <a className="link" href={t.video.url} target="_blank" rel="noreferrer">
                  {t.player.displayName}
                </a>
              </td>
              <td className="td">
                <div className="videoCell">
                  <img className="thumb" src={t.video.thumbnailUrl} alt={t.video.title} />
                  <div>
                    <div className="videoTitle">{t.video.title}</div>
                    <div className="muted small">
                      {platformLabel(t.video.platform)} • {formatDuration(t.video.durationMs)}
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

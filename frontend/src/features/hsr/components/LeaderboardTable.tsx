import { useMemo, useState } from "react";
import { useModesQuery } from "../../games/queries";
import { useHsrLeaderboardQuery } from "../queries";
import { Table } from "../../../shared/ui/Table";
import { LoadingState } from "../../../shared/ui/LoadingState";
import { ErrorState } from "../../../shared/ui/ErrorState";
import { EmptyState } from "../../../shared/ui/EmptyState";
import { formatMetric } from "../../../shared/utils/format";
import { TeamsSubtable } from "./TeamsSubtable";

export function LeaderboardTable({ modeSlug }: { modeSlug: string }) {
  const modesQ = useModesQuery("hsr");
  const modes = modesQ.data?.items ?? [];
  const selectedMode = useMemo(() => modes.find((m) => m.modeSlug === modeSlug), [modes, modeSlug]);

  const page = 1;
  const pageSize = 50;
  const q = useHsrLeaderboardQuery(modeSlug, page, pageSize);

  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const playLabel = selectedMode?.playMetricType === "time" ? "Play (time)" : "Play (cycles)";

  return (
    <div className="panel">
      <div className="panelHeader">
        <div className="sectionTitle">Leaderboards</div>
        <div className="muted small">
          Ranking: primary lowest {selectedMode?.playMetricType ?? "metric"}, tie-breaker lowest Lim/Std. (Place is shown only on Home.)
        </div>
      </div>

      {q.isLoading && <LoadingState label="Loading leaderboard..." />}
      {q.isError && <ErrorState error={q.error} />}
      {!q.isLoading && !q.isError && (q.data?.items?.length ?? 0) === 0 && (
        <EmptyState label="No leaderboard entries. Seed the database." />
      )}

      {!q.isLoading && !q.isError && (q.data?.items?.length ?? 0) > 0 && (
        <Table>
          <table className="table">
            <thead>
              <tr>
                <th className="th narrow" />
                <th className="th">Character</th>
                <th className="th">Lim/Std</th>
                <th className="th">{playLabel}</th>
                <th className="th">Player</th>
              </tr>
            </thead>
            <tbody>
              {q.data?.items.map((row) => {
                const isOpen = !!expanded[row.entryId];
                return (
                  <>
                    <tr key={row.entryId} className="tr">
                      <td className="td narrow">
                        <button
                          className="expander"
                          onClick={() =>
                            setExpanded((s) => ({ ...s, [row.entryId]: !s[row.entryId] }))
                          }
                          aria-label={isOpen ? "Collapse" : "Expand"}
                        >
                          {isOpen ? "▾" : "▸"}
                        </button>
                      </td>

                      <td className="td">
                        <div className="charCell">
                          <img className="portrait" src={row.character.portraitUrl} alt={row.character.name} />
                          <div className="charName">{row.character.name}</div>
                        </div>
                      </td>

                      <td className="td">{row.limStd}</td>
                      <td className="td metric">{formatMetric(row.metric)}</td>
                      <td className="td">{row.player.displayName}</td>
                    </tr>

                    {isOpen ? (
                      <tr className="trSub" key={`${row.entryId}_sub`}>
                        <td className="tdSub" colSpan={5}>
                          <TeamsSubtable entryId={row.entryId} />
                        </td>
                      </tr>
                    ) : null}
                  </>
                );
              })}
            </tbody>
          </table>
        </Table>
      )}
    </div>
  );
}

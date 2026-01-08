import { useTeamsQuery } from "../queries";
import { LoadingState } from "../../../shared/ui/LoadingState";
import { ErrorState } from "../../../shared/ui/ErrorState";
import { EmptyState } from "../../../shared/ui/EmptyState";
import { formatMetric, platformLabel, formatDuration } from "../../../shared/utils/format";
import { Character, Run } from "../../../shared/api/types";
import { getCostValueFromRunById } from "../../../shared/utils/utils";

export function TeamsSubtable({ entryId, runs, chars, ltdCostId, stdCostId }: 
  { 
    entryId: string, 
    runs: Run[] | undefined, 
    chars: Character[] | undefined,
    ltdCostId: number | undefined,
    stdCostId: number | undefined,
  }) {
  // const q = useTeamsQuery(entryId, true);

  // if (q.isLoading) return <LoadingState label="Loading teams..." />;
  // if (q.isError) return <ErrorState error={q.error} />;
  if ((runs?.length ?? 0) === 0) return <EmptyState label="No teams for this entry." />;

  return (
    <div className="subtableWrap">
      <table className="subtable">
        <thead>
          <tr>
            <th className="th">Team</th>
            <th className="th">Lim/Std</th>
            <th className="th">Cycles</th>
            <th className="th">Player (opens video)</th>
            <th className="th">Author</th>
          </tr>
        </thead>
        <tbody>
          {runs?.map((r) => {
            return (
              <tr key={r.id} className="tr">
                <td className="td">
                  <div className="teamRow">
                    {r.team.units.map((m) => {
                      const char = chars?.find(c => c.id === m.char_id);
                      return (
                        <div >
                          <img key={m.id}
                            className="portraitSm"
                            src={char?.icon_url}
                            alt={char?.name ?? m.char_id.toString()} />
                          <p id={m.id.toString() + "_eidolon"} 
                            className="muted small" 
                            style={
                              {
                                textAlign: "center", 
                                marginTop: "-22px",
                                marginLeft: "24px",
                                paddingLeft: "4px",
                                fontSize: "16px",
                                position: "absolute",
                                display: "flex",
                                borderRadius: "50%",
                                justifyContent: "center",
                                alignItems: "center",
                                fontWeight: "600",
                                backgroundColor: "black",
                                zIndex: 19,
                                color: "rgba(255,255,255,1)",}}>
                                  {m.char_eidolon}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </td>
                <td className="td">{getCostValueFromRunById(r, ltdCostId)} + {getCostValueFromRunById(r, stdCostId)}</td>
                <td className="td metric">{r.primary_score}</td>
                <td className="td">
                  <a className="link" href={r.link} target="_blank" rel="noreferrer">
                    {r.team.name}
                  </a>
                </td>
                <td className="td">
                  <div className="videoCell">
                    {/* <img className="thumb" src={t.video.thumbnailUrl} alt={t.video.title} /> */}
                    <div>
                      <div className="videoTitle">{r.author}</div>
                      <div className="muted small">
                        {/* {platformLabel(t.video.platform)} • {formatDuration(t.video.durationMs)} */}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

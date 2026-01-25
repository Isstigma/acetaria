import { EmptyState } from "../../../shared/ui/EmptyState";
import { Character, Lightcone, Run } from "../../../shared/api/types";
import { getCostValueFromRunById } from "../../../shared/utils/utils";

export function TeamsSubtable({ entryId, runs, chars, lcs, ltdCostId, stdCostId }: 
  { 
    entryId: string, 
    runs: Run[] | undefined, 
    chars: Character[] | undefined,
    lcs: Lightcone[] | undefined,
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
                    {r.team.units.map((unit) => {
                      // console.log(r.team.units);
                      const char = chars?.find(c => c.id === unit.char_id);
                      const lc = lcs?.find(l => l.id === unit.lc_id);
                      return (
                        <div >
                          <img key={unit.id}
                            className="portraitSm"
                            src={char?.icon_url}
                            alt={char?.name ?? unit.char_id.toString()} />
                          <p id={unit.id.toString() + "_eidolon"} 
                            className="eidolonSm small" >
                                  {unit.char_eidolon}
                          </p>
                          <img key={unit.lc_id}
                            className="lcIconSm"
                            src={lc?.icon_url}
                            alt={lc?.name ?? unit.lc_id.toString()} />
                          <p id={unit.id.toString() + "_superimposition"} 
                            className="superimpositionSm" >
                                  {unit.lc_superimposition}
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

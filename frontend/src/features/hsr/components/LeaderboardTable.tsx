import { useMemo, useState } from "react";
import { useModesQuery } from "../../games/queries";
import { useHsrLeaderboardQuery } from "../queries";
import { Table } from "../../../shared/ui/Table";
import { LoadingState } from "../../../shared/ui/LoadingState";
import { ErrorState } from "../../../shared/ui/ErrorState";
import { EmptyState } from "../../../shared/ui/EmptyState";
import { formatMetric } from "../../../shared/utils/format";
import { TeamsSubtable } from "./TeamsSubtable";
import { useGetAllCharsQuery, useGetAllCostsQuery, useRunsByStageIdQuery } from "../../runs/queries";
import { Mode, Run, RunCost } from "../../../shared/api/types";
import { getCostValueFromRunById } from "../../../shared/utils/utils";

const STD_COST_NAME = "Standard 5 stars";
const LTD_COST_NAME = "Limited 5 stars";

export function LeaderboardTable({ stageId, mode }: { stageId: number, mode: Mode | undefined }) {
  const selectedMode = mode;
  
  const chars = useGetAllCharsQuery()

  const costs = useGetAllCostsQuery();

  const stdCostId = costs?.data?.find(c => c.name === STD_COST_NAME)?.id;
  const ltdCostId = costs?.data?.find(c => c.name === LTD_COST_NAME)?.id;
  

  const stageRuns = useRunsByStageIdQuery(stageId);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const playLabel = "Play " + selectedMode?.primary_score_kind;

  // console.log(stageRuns?.data);
  // console.log(stageRuns.data?.length, stageRuns.data?.length ?? 0 < 1);
  if((stageRuns.data?.length ?? 0) <= 0) {
    // console.log("No runs found for stageId:", stageId);
    return;
  } 
  const stageCharRuns = chars.data?.map((char) => {
    const stageRunsForChar = stageRuns.data
    ?.filter((run) => run.team.units.some(u => u.char_id === char.id))
    ?.sort((a, b) => {
      if(a.primary_score - b.primary_score !== 0) {
        if(selectedMode?.primary_score_reverse_sorting) {
          return b.primary_score - a.primary_score;
        }
        return a.primary_score - b.primary_score;
      }
      
      if(a.secondary_score !== null && b.secondary_score !== null 
        && a.secondary_score !== b.secondary_score) {
        if(selectedMode?.secondary_score_reverse_sorting) {
          return b.secondary_score - a.secondary_score;
        }
        return a.secondary_score - b.secondary_score;
      }

      const aLtdScore = getCostValueFromRunById(a, ltdCostId) ?? Number.POSITIVE_INFINITY;
      const bLtdScore = getCostValueFromRunById(b, ltdCostId) ?? Number.POSITIVE_INFINITY;
      if(aLtdScore !== bLtdScore) {
        return aLtdScore - bLtdScore;
      }
      const aStdScore = getCostValueFromRunById(a, stdCostId) ?? Number.POSITIVE_INFINITY;
      const bStdScore = getCostValueFromRunById(b, stdCostId) ?? Number.POSITIVE_INFINITY;
      return aStdScore - bStdScore;
    });

    const bestRun = stageRunsForChar?.reduce((best, run) => {
      const runLtdScore = getCostValueFromRunById(run, ltdCostId);
      const bestLtdScore = getCostValueFromRunById(best, ltdCostId);
      const runStdScore = getCostValueFromRunById(run, stdCostId);
      const bestStdScore = getCostValueFromRunById(best, stdCostId);
      if (best === null || best.primary_score === null
        || (selectedMode?.primary_score_reverse_sorting ? run.primary_score > best.primary_score : run.primary_score < best.primary_score)) {
        return run;
      } else if (run.primary_score === best.primary_score 
        && run.secondary_score && best.secondary_score && (
          selectedMode?.secondary_score_reverse_sorting 
            ? run.secondary_score > best.secondary_score 
            : run.secondary_score < best.secondary_score)) {
        return run;
      } else if (
        run.primary_score === best.primary_score 
        && ((runLtdScore && bestLtdScore && runLtdScore! < bestLtdScore!))
      ) {
        return run;
      } else if (run.primary_score === best.primary_score 
        && runLtdScore === bestLtdScore
        && (runStdScore && bestStdScore && runStdScore! < bestStdScore!)) {
        return run;
      }
      return best;
    }, {primary_score: null, run_costs: [] as RunCost[]} as unknown as Run | null);

    const res = {
      char: char,
      runs: stageRunsForChar,
      bestPrimaryScore: bestRun?.primary_score,
      bestSecondaryScore: bestRun?.secondary_score,
      bestLtdScore: getCostValueFromRunById(bestRun, ltdCostId),
      bestStdScore: getCostValueFromRunById(bestRun, stdCostId),
      bestRun: bestRun,
    };
    return res;
  })
  .filter(r => r.runs && (r.runs?.length ?? 0) > 0)
  .sort((a, b) => {
    const aScore = a.bestPrimaryScore ?? Number.POSITIVE_INFINITY;
    const bScore = b.bestPrimaryScore ?? Number.POSITIVE_INFINITY;
    if(aScore === bScore) {
      const aLtd = a.bestLtdScore ?? Number.POSITIVE_INFINITY;
      const bLtd = b.bestLtdScore ?? Number.POSITIVE_INFINITY;
      if(aLtd === bLtd) {
        const aStd = a.bestStdScore ?? Number.POSITIVE_INFINITY;
        const bStd = b.bestStdScore ?? Number.POSITIVE_INFINITY;
        return aStd - bStd;
      }
      if(selectedMode?.secondary_score_reverse_sorting) {
        return bLtd - aLtd;
      }
      return aLtd - bLtd;
    }
    if(selectedMode?.primary_score_reverse_sorting) {
      return bScore - aScore;
    }
    return aScore - bScore;
  });
  
  // console.log(stageCharRuns);
  return (
    <div className="panel">
      <div className="panelHeader">
        <div className="sectionTitle" style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>Leaderboards</div>
        <div className="muted small" style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>
          Ranking: primary {
          selectedMode?.primary_score_reverse_sorting ? "highest " : "lowest "
          }{
            selectedMode?.primary_score_kind ?? "metric"
          }{
            selectedMode?.secondary_score_kind === null 
              ? "" 
              : `, secondary ${selectedMode?.secondary_score_reverse_sorting 
                ? "highest" 
                : "lowest"} ${
                  selectedMode?.secondary_score_kind ?? "metric"
                }`
          }, tie-breaker lowest Lim/Std
        </div>
      </div>

      {stageRuns.isLoading && <LoadingState label="Loading leaderboard..." />}
      {stageRuns.isError && <ErrorState error={stageRuns.error} />}
      {!stageRuns.isLoading && !stageRuns.isError && (stageRuns.data?.length ?? 0) === 0 && (
        <EmptyState label="No leaderboard entries. Seed the database." />
      )}

      {!stageRuns.isLoading && !stageRuns.isError && (stageRuns.data?.length ?? 0) > 0 && (
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
              {stageCharRuns?.map((row) => {
                console.log(row);
                const isOpen = !!expanded[row.char.id];
                return (
                  <>
                    <tr key={row.char.id} className="tr">
                      <td className="td narrow">
                        <button
                          className="expander"
                          onClick={() =>
                            setExpanded((s) => ({ ...s, [row.char.id]: !s[row.char.id] }))
                          }
                          aria-label={isOpen ? "Collapse" : "Expand"}
                        >
                          {isOpen ? "▾" : "▸"}
                        </button>
                      </td>

                      <td className="td">
                        <div className="charCell">
                          <img className="portrait" src={row.char.icon_url} alt={row.char.name} />
                          <div className="charName">{row.char.name}</div>
                        </div>
                      </td>

                      <td className="td">
                        {`${row.bestLtdScore} + ${row.bestStdScore}`}</td>
                      <td className="td metric">{row.bestRun?.primary_score} {mode?.primary_score_kind}</td>
                      <td className="td">{row.bestRun?.author}</td>
                    </tr>

                    {isOpen ? (
                      <tr className="trSub" key={`${row.char.id}_sub`}>
                        <td className="tdSub" colSpan={5}>
                          <TeamsSubtable 
                            entryId={row.char.id.toString()} 
                            runs={row.runs} 
                            chars={chars.data}  
                            ltdCostId={ltdCostId}
                            stdCostId={stdCostId}
                          />
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

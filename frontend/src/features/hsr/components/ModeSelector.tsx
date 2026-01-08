import { useState } from "react";
import type { GameModeEntry, Mode } from "../../../shared/api/types";
import { Button } from "../../../shared/ui/Button";

export function ModeSelector(props: {
  modes: Mode[];
  modeId: string;
  stageId?: number;
  onModeStageChange: (v: number) => void;
  onModeChange: (v: string) => void;
  isLoading: boolean;
  isError: boolean;
}) {
  const { modes, modeId, stageId, onModeStageChange, onModeChange, isLoading, isError } = props;
  const [stageOpen, setStageOpen] = useState(false);
  const [stage, setStage] = useState<GameModeEntry>(null!);
  const [gameMode, setGameMode] = useState<Mode>(null!);
  const [stages, setStages] = useState<GameModeEntry[]>(null!);

  return (
    <div className="modeSelector">
      {isLoading && <div className="muted">Loading modes...</div>}
      {isError && <div className="muted">Failed to load modes.</div>}

      <div className="pillRow" style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>
        {modes.map((m) => {
          return (
            <button
              key={m.id}
              className={["pill", modeId === m.id ? "pillActive" : ""].join(" ")}
              onClick={() => {
                setGameMode(m);
                setStages(m.game_mode_entries);
                onModeChange(m.id)
                onModeStageChange(stage?.stage_id)
                return ;
              } }
              type="button"
              title={m.primary_score_kind === "cycles" ? "Rank by lowest cycles" : "Rank by lowest time"}
            >
              {m.name}
            </button>
          );
        })}
      </div>
        <div className="stageDropdown" style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>
          <button
            className="stageTrigger"
            onClick={() => {
              // console.log(stages);
              // console.log(gameMode);
              return setStageOpen((s) => !s);
            }}
            aria-haspopup="listbox"
            aria-expanded={stageOpen}
            title="Stage (placeholder)"
          >
            <span className="stageShort">{stage?.name ?? 'Select stage'}</span>
            <span className="caret" aria-hidden="true">▾</span>
          </button>

          {stageOpen ? (
            <div className="stageMenu" role="listbox">
              {stages?.map((l) => (
                <button
                  key={l.name}
                  className="langItem"
                  onClick={() => {
                    setStage(l);
                    onModeStageChange(l.stage_id)
                    onModeChange(gameMode.id)
                    setStageOpen(false);
                  }}
                >
                  {l.name}
                </button>
              ))}
            </div>
          ) : null}
          
        </div>      
          <div className="" style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>
            <div className="toolbarLeft"  style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>
              <Button style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>Filter</Button>
              <Button hidden={true}  variant="ghost">0-Cycle</Button>
              <Button hidden={true} variant="ghost">full stars</Button>
            </div>
            <div className="toolbarRight"  style={{display: 'inline-block', flexDirection: 'column', gap: '8px', marginRight: 15}}>
              <Button variant="primary">Submit</Button>
            </div>
          </div>
    </div>
  );
}

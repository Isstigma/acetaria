import type { Mode } from "../../../shared/api/types";

export function ModeSelector(props: {
  modes: Mode[];
  value: string;
  onChange: (v: string) => void;
  isLoading: boolean;
  isError: boolean;
}) {
  const { modes, value, onChange, isLoading, isError } = props;

  return (
    <div className="modeSelector">
      {isLoading && <div className="muted">Loading modes...</div>}
      {isError && <div className="muted">Failed to load modes.</div>}

      <div className="pillRow">
        {modes.map((m) => (
          <button
            key={m.modeSlug}
            className={["pill", value === m.modeSlug ? "pillActive" : ""].join(" ")}
            onClick={() => onChange(m.modeSlug)}
            type="button"
            title={m.playMetricType === "cycles" ? "Rank by lowest cycles" : "Rank by lowest time"}
          >
            {m.modeName}
            {m.isLatest ? <span className="pillTag">latest</span> : null}
          </button>
        ))}
      </div>
    </div>
  );
}

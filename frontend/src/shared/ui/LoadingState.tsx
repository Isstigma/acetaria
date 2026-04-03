export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return <div className="state stateLoading">{label}</div>;
}

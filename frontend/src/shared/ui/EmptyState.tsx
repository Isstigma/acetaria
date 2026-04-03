export function EmptyState({ label = "Nothing here yet." }: { label?: string }) {
  return <div className="state stateEmpty">{label}</div>;
}

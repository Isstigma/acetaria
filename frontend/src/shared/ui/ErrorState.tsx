export function ErrorState({ error }: { error: unknown }) {
  const msg = error instanceof Error ? error.message : "Unknown error";
  return (
    <div className="state stateError">
      <div className="stateTitle">Something went wrong</div>
      <div className="stateBody">{msg}</div>
    </div>
  );
}

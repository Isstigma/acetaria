import React from "react";

export function Table({ children }: { children: React.ReactNode }) {
  return <div className="tableWrap">{children}</div>;
}

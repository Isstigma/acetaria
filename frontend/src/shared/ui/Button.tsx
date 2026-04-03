import React from "react";

type Variant = "primary" | "outline" | "ghost";

export function Button(
  props: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }
) {
  const { variant = "outline", className = "", ...rest } = props;

  return (
    <button
      {...rest}
      className={[
        "btn",
        variant === "primary" ? "btnPrimary" : "",
        variant === "ghost" ? "btnGhost" : "",
        variant === "outline" ? "btnOutline" : "",
        className
      ].join(" ")}
    />
  );
}

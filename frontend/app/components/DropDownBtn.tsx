"use client";
import { useState, useRef, useEffect } from "react";

interface DropdownProps {
  label: string;
  items: string[];
  width: number;
  onSelect?: (value: string) => void;
}

export default function Dropdown({ label, items,  width }: DropdownProps) {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState(items[0]);

  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (item: string) => {
    setSelected(item);
    setOpen(false);
  };

  return (
    <div ref={ref} className="relative" style={{ width: `${width}px` }}>
      
      {/* floating label */}
      <span className="absolute -top-2 left-3 px-1 text-xs bg-bg-dark ">
        {label}
      </span>

      {/* button */}
      <button
        onClick={() => setOpen(!open)}
        className="
          w-full text-left px-4 py-2 pt-3
          rounded-xl bg-bg-light
          flex justify-between items-center
        "
      >
     <span>{selected}</span>

        <span className={`transition-transform ${open ? "rotate-180" : ""}`}>
          ▾
        </span>
      </button>

      {/* dropdown menu */}
      {open && (
        <div className="absolute mt-2 w-full rounded-2xl bg-bg-dark shadow-lg overflow-hidden dropdown-animate">
          {items.map((item) => (
            <button
              key={item}
              onClick={() => handleSelect(item)}
              className="block w-full text-left px-4 py-2 hover:bg-bg-light transition-colors"
            >
              {item}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

const API_BASE = import.meta.env.VITE_API_BASE_URL as string | undefined;

function assertBaseUrl(): string {
  if (!API_BASE) throw new Error("VITE_API_BASE_URL is not set");
  return API_BASE.replace(/\/+$/, "");
}

export async function apiGet<T>(path: string): Promise<T> {
  const url = `${assertBaseUrl()}${path.startsWith("/") ? "" : "/"}${path}`;
  const res = await fetch(url, { headers: { "Accept": "application/json" } });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${text || res.statusText}`);
  }
  return res.json() as Promise<T>;
}

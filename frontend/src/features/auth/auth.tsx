import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { getApiBaseUrl } from "../../shared/api/client";

export type AuthUser = {
  id: string;
  discord_id: string | null;
  username: string;
  global_name: string | null;
  avatar: string | null;
  role: "user" | "moderator" | "admin";
  is_active: boolean;
};

type AuthContextValue = {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  loginWithDiscord: () => void;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

async function fetchCurrentUser(): Promise<AuthUser | null> {
  const res = await fetch(`${getApiBaseUrl()}/auth/me`, {
    method: "GET",
    credentials: "include",
    headers: { Accept: "application/json" },
  });

  if (res.status === 401) return null;
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Auth ${res.status}: ${text || res.statusText}`);
  }

  return (await res.json()) as AuthUser;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    setIsLoading(true);
    try {
      const nextUser = await fetchCurrentUser();
      setUser(nextUser);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refreshUser();
  }, [refreshUser]);

  const loginWithDiscord = useCallback(() => {
    window.location.assign(`${getApiBaseUrl()}/auth/discord/login`);
  }, []);

  const logout = useCallback(async () => {
    const res = await fetch(`${getApiBaseUrl()}/auth/logout`, {
      method: "POST",
      credentials: "include",
      headers: { Accept: "application/json" },
    });

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`Logout ${res.status}: ${text || res.statusText}`);
    }

    setUser(null);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isLoading,
      isAuthenticated: !!user,
      loginWithDiscord,
      logout,
      refreshUser,
    }),
    [user, isLoading, loginWithDiscord, logout, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used within AuthProvider");
  return value;
}

import { useCallback, useState } from "react";

import type { FactRecord } from "../lib/facts";

export type Actions = {
  type: string;
  factText?: string;
  factId?: string;
};

export function useActions() {
  const [facts, setFacts] = useState<FactRecord[]>([]);
  const [error] = useState<string | null>(null);
  const loading = false;

  const performAction = useCallback(async (action: Actions) => {
    if (action.type === "chart_generator") {
      console.log(`performAction chart_generator`);
    }  
    if (action.type === "save") {
      setFacts((current) => {
        const text = (action.factText ?? "").trim();
        if (!text) {
          return current;
        }
        if (current.some((fact) => fact.id === action.factId)) {
          return current;
        }
        const saved: FactRecord = {
          id: action.factId,
          text,
          status: "saved",
          createdAt: new Date().toISOString(),
        };
        return [...current, saved];
      });
    }
  }, []);

  const refresh = useCallback(() => {
    /* no-op: facts are stored in-memory */
  }, []);

  return { facts, loading, error, refresh, performAction };
}

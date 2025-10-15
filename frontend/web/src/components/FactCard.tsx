import { ChevronRight } from "lucide-react";

import type { FactRecord } from "../lib/facts";

export function FactCard({ fact }: { fact: FactRecord }) {
  return (
    <li className="group flex items-start gap-1 text-sm font-medium text-slate-600 dark:text-slate-300">
      <ChevronRight className="h-5 w-5 text-slate-800 dark:text-slate-200" />
      {fact.text}
    </li>
  );
}

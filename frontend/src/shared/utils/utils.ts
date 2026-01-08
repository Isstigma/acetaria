import { Run } from "../api/types";

export function getCostValueFromRunById(run: Run | null | undefined, 
  costId: number| undefined): number | undefined { 
    return run?.run_costs.find(c => c.cost_id === costId)?.value;
  }
import { Sheet } from "~~/types/Model"

var costState: Sheet;

export const useCostState = () => useState<Sheet>('costState', () => costState);
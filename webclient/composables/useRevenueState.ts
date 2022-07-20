import { Sheet } from "~~/types/Model"

var revenueState: Sheet;

export const useRevenueState = () => useState<Sheet>('revenueState', () => revenueState);
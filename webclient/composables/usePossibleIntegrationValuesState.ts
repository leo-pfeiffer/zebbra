import { IntegrationValueInfo } from "~~/types/IntegrationValueInfo";

var possibleIntegrationValuesState: IntegrationValueInfo[];

export const usePossibleIntegrationValuesState = () => useState<IntegrationValueInfo[]>('possibleIntegrationValuesState', () => possibleIntegrationValuesState);
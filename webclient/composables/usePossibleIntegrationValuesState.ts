import { IntegrationValue } from "~~/types/IntegrationValue";

var possibleIntegrationValuesState: IntegrationValue[];

export const usePossibleIntegrationValuesState = () => useState<IntegrationValue[]>('possibleIntegrationValuesState', () => possibleIntegrationValuesState);
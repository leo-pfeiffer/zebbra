import { Variable } from "~~/types/Model"

export const useVariableTimeSeriesMap = (variables: Variable[]) => {

    var variableTimeSeriesMap: Map<string, boolean> = new Map<string,boolean>();

    for(let i=0; i < variables.length; i++) {
        variableTimeSeriesMap.set(variables[i]._id, variables[i].time_series);
    }
    
    return variableTimeSeriesMap;
}
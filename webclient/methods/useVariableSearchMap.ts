import { Variable } from "~~/types/Model"

export const useVariableSearchMap = (variables: Variable[]) => {

    var variableMap: Map<string, string> = new Map<string,string>();

    for(let i=0; i < variables.length; i++) {
        variableMap.set(variables[i]._id, variables[i].name);
    }
    
    return variableMap;
}
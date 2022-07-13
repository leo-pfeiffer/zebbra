import { ValueObject } from "~~/types/ValueObject";
import { useFormulaParser } from "./useFormulaParser";


//method that returns the a human readable formula based on the value stored in the db
export const useGetHumanReadableFormula = (inputString:string, currentAssumptionId:string, variableSearchMap:Map<string, string>) => {

    const valueObject:ValueObject = useFormulaParser().createValueObject(inputString);

    for(let i=0; i < valueObject.indexes.length; i++) {
        var ref = valueObject.value_array[valueObject.indexes[i]];

        var refHumanReadableName:string = "";

        if(ref[0] === "$") { //is internal ref

            refHumanReadableName = variableSearchMap.get(currentAssumptionId) + "[" + ref.substring(1) + "]"

        } else if(ref[0] === "#") { //is external ref

            if(ref.includes("$")) {
                var refSplitted = ref.substring(1).split("$");
                var externalId = refSplitted[0];
                refHumanReadableName = variableSearchMap.get(externalId) + "[" + refSplitted[1] + "]"
            } else {
                var externalId = ref.substring(1);
                refHumanReadableName = variableSearchMap.get(externalId) + "[0]"
                
            }

        } else {
            throw Error;
        }
        valueObject.value_array[valueObject.indexes[i]] = refHumanReadableName;
    }

    var outputString:string = "";

    for(let i=0; i < valueObject.value_array.length; i++) {
        outputString = outputString + valueObject.value_array[i];
    }

    return outputString;

}
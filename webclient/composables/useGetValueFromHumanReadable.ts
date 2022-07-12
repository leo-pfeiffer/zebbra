import { useFormulaParser } from "./useFormulaParser";

//method that returns the variable value with refs to be stored in db form human readable input
export const useGetValueFromHumanReadable = (humanReadableInput:string, currentAssumptionId:string, variableSearchMap:Map<string, string>) => {

    var example = "Customers[1]*(1+Customer Growth[0])";
    
    var output:string = "";

    for(let i=0; i < humanReadableInput.length; i++) {

        const char = humanReadableInput[i];
        if(useFormulaParser().charIsNumerical(char) || useFormulaParser().charIsOperator(char)) {

            output = output + char;
        } else {
            var counter:number = 0;
            var refNameWithTimeDiff:string = "";
            //get the name of the ref[timeDiff]
            while(!useFormulaParser().charIsNumerical(humanReadableInput[i + counter]) && !useFormulaParser().charIsOperator(humanReadableInput[i + counter]) && humanReadableInput[i + counter] != undefined) {

                if(humanReadableInput[i + counter] === "[") {
                    var counter2 = 0;
                    while(humanReadableInput[i + counter + counter2] != "]") {
                        refNameWithTimeDiff = refNameWithTimeDiff + humanReadableInput[i + counter + counter2];
                        counter2++;
                    }
                    counter = counter + counter2;
                } else {
                    refNameWithTimeDiff = refNameWithTimeDiff + humanReadableInput[i + counter];
                    counter++;
                }
            }

            var refId:string;
            var refTimeDiff:string;

            if(refNameWithTimeDiff.includes("[")) {
                var splitted = refNameWithTimeDiff.split("[");
                refId = getRefIdByName(splitted[0], variableSearchMap);
                refTimeDiff = splitted[1].split("]")[0];
            } else {
                refId = getRefIdByName(refNameWithTimeDiff, variableSearchMap);
                refTimeDiff = ""
            }

            if(refId === currentAssumptionId) {
                output = output + "$" + refTimeDiff;
            } else {
                if(refTimeDiff === "0") {
                    output = output + "#" + refId;
                } else {
                    output = output + "#" + refId + "$" + refTimeDiff;
                }
            }
            i = i + counter - 1; //reduce by 1 as for loop adds one
        }
    }

    return output;

}

const getRefIdByName = (name:string, variableSearchMap:Map<string, string>) => {

    for (let [key, value] of variableSearchMap.entries()) {
        if (value === name)
          return key;
      }

}
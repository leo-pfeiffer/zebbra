import { useFormulaParser } from "./useFormulaParser";

//method that returns the variable value with refs to be stored in db form human readable input
export const useGetValueFromHumanReadable = (humanReadableInput:string, currentAssumptionId:string, variableSearchMap:Map<string, string>) => {

    let inputWithoutWhitespace = humanReadableInput.replace(/\s/g,'');
    
    var output:string = "";

    for(let i=0; i < inputWithoutWhitespace.length; i++) {

        const char = inputWithoutWhitespace[i];
        if(useFormulaParser().charIsNumerical(char) || useFormulaParser().charIsOperator(char) || char === ".") {
            output = output + char;
        } else {
            var counter:number = 0;
            var refNameWithTimeDiff:string = "";
            //get the name of the ref[timeDiff]
            while(!useFormulaParser().charIsOperator(inputWithoutWhitespace[i + counter]) && inputWithoutWhitespace[i + counter] != undefined) {

                if(inputWithoutWhitespace[i + counter] === "[") {
                    var counter2 = 0;
                    while(inputWithoutWhitespace[i + counter + counter2] != "]") {
                        refNameWithTimeDiff = refNameWithTimeDiff + inputWithoutWhitespace[i + counter + counter2];
                        counter2++;
                    }
                    counter = counter + counter2;
                } else {
                    refNameWithTimeDiff = refNameWithTimeDiff + inputWithoutWhitespace[i + counter];
                    counter++;
                }
            }

            //handle cases where refNameWithTimeDiff is only spaces
            if(!(refNameWithTimeDiff.trim().length === 0)) {

                //remove leading SPACE if there
                if(refNameWithTimeDiff[0] === " ") {
                    refNameWithTimeDiff = refNameWithTimeDiff.substring(1);
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
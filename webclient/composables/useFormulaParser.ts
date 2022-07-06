import { Variable } from "~~/types/Model";

import * as MathParser from 'math-expression-evaluator';

export const useFormulaParser = () => {

    type ValueObject = {
        indexes: number[];
        valueArray: string[];
    }


        //todo: add model context??
    //method that takes an array of variables and returns the values to be displayed for every variable
    const getSheetRowValues = (variables:Variable[]) => {

        //todo decide the order in which the row values must be created

        var rowValuesArray: string[][] = [];

        for (let i = 0; i < variables.length; i++) {

            var rowValuesToDisplay: string[] = [];

            var variable: Variable = variables[i];

            if (!variable.timeSeries || typeof variable.value != "string") {
                for (let i = 0; i < 24; i++) {
                    rowValuesToDisplay.push("–");
                }
                rowValuesArray.push(rowValuesToDisplay);
            } else {
                try {
                    rowValuesToDisplay = getRowValues(variable);
                } catch (e) {
                    console.log(e);
                    for (let i = 0; i < 24; i++) {
                        rowValuesToDisplay.push("#REF!");
                    }
                }
                rowValuesArray.push(rowValuesToDisplay);
            }

        }
        return rowValuesArray;
    }
    
    //composable that takes a variable and return the values to be displayed based on the value string
    const getRowValues = (variableInput:Variable) => {

        var valueString:string = variableInput.value;
    
        //object that stores splits out the refs from the value string and stores their location
        const valueObject:ValueObject = createValueObject(valueString);

    
        //stores all the values that need to be displayed e.g. are returned at the end
        var valuesToDisplay:string[] = [];
    
        //push empty values for startingAt
        for(let i=0; i < variableInput.startingAt; i++) {
            valuesToDisplay.push("–");
        }
    
        if(variableInput.firstValueDiff) {
             //TODO: push the starting value if available
            //var firstValue:string = variableInput.value_1;
            var firstValue:string = "1000";
            valuesToDisplay.push(firstValue);
        }
        
        //change starting point of 'i' in for loop depending on startingAt and whether first value is different
        let startingPointForI = 0 + variableInput.startingAt;
        if(variableInput.firstValueDiff) {
            startingPointForI++;
        }
    
        for(let i=startingPointForI; i < 24; i++) {
            
            //store valueArray with refs in new array so refs can be overwritten
            var valueArrayToBeOverwritten:string[] = [...valueObject.valueArray];
    
            //get the refs in the valueArray and replace them with the actual value
            for(let j=0; j < valueObject.indexes.length; j++) {
                var ref:string = valueArrayToBeOverwritten[valueObject.indexes[j]];
                var refValue = getRefValue(ref, i, valuesToDisplay);
                valueArrayToBeOverwritten[valueObject.indexes[j]] = refValue;
            }
    
            //concatinate the updated valueArray to single string
            var stringForParser:string = "";
            for(let x=0; x < valueArrayToBeOverwritten.length; x++) {
                stringForParser = stringForParser + valueArrayToBeOverwritten[x];
            }
            
            //run the string through the maths parser
            const valueToDisplay:string = Math.floor(MathParser.eval(stringForParser)).toString();
            
            //add the solution of maths parser to the valuesToDisplay string
            valuesToDisplay.push(valueToDisplay);
        }
        return valuesToDisplay;
    
    }
    
    //gets gets the valueString and returns an object with an array of the components and an array of the indexes of the refs
    const createValueObject = (valueString:string) => {
        
        //instantiate valueObject for output
        let valueObjectOut:ValueObject = {
            indexes: [],
            valueArray: []
        };
    
        let valueArray:string[] = [];
        let indexes:number[] = [];
        
        //instantiate index to store where in the array the refs are stored
        let index = 0;
        
        /* loop over the valueString and separate refs from rest and store the different parts 
        in the valueArray while storing the indexes of the refs in the indexes array */
        for(let i=0; i < valueString.length; i++) {
            let char = valueString[i];
            if(char === "$") {
                var internalRef:string = char;
                var counter = 1;
                while(charIsNumerical(valueString[i+counter]) && (valueString[i+counter] != undefined)) {
                    internalRef = internalRef + valueString[i+counter];
                    counter++;
                    if((i+counter >= valueString.length)) {
                        break;
                    }
                }
                valueArray.push(internalRef);
                indexes.push(index);
                index++;
                i = i + counter -1;
            } else if (char === "#") {
                var externalRef:string = char;
                var counter = 1;
                while(charIsNumerical(valueString[i+counter]) && (valueString[i+counter] != undefined)) {
                    externalRef = externalRef + valueString[i+counter];
                    counter++;
                    if((i+counter >= valueString.length)) {
                        break;
                    }
                }
                valueArray.push(externalRef);
                indexes.push(index);
                index++;
                i = i + counter -1;
            } else {
                var nonRefPart = char;
                var counter = 1;
                while(!charIsRefToken(valueString[i+counter]) && (valueString[i+counter] != undefined)) {
                    nonRefPart = nonRefPart + valueString[i+counter];
                    counter++
                    if((i+counter >= valueString.length)) {
                        break;
                    }
                }
                valueArray.push(nonRefPart);
                index++;
                i = i + counter -1;
            }
        }
    
        valueObjectOut.valueArray = valueArray;
        valueObjectOut.indexes = indexes;
        return valueObjectOut;
    }
    
    /* takes any ref and returns its value */
    const getRefValue = (ref:string, index:number, valuesToDisplay:string[]) => {
    
        let returnValue:string;
    
        if(ref[0] == "$") {
            returnValue = getInternalRefValue(ref, index, valuesToDisplay);
        } else if(ref[0] == "#") {
            returnValue = getExternalRefValue(ref, index);
        }
    
        return returnValue;
    
    }
    
    /* takes an internal ref, the current position, and the current state of the valuesToDisplay array and returns the value */
    const getInternalRefValue = (internalRef:string, index:number, valuesToDisplay:string[]) => {
    
        const indexDiff:number = +internalRef.substring(1);
    
        return valuesToDisplay[index - indexDiff];
    
    }
    
    /* takes external ref and returns the value */
    const getExternalRefValue = (externalRef:string, index:number) => {
    
        //todo
        return "0.05";
    
    }
    
    const charIsNumerical = (char:string) => {
    
        if(char === "0" || char === "1" || char === "2" || char === "3" || char === "4" || char === "5" || char === "6" || char === "7" || char === "8" || char === "9") {
            return true;
        } else {
            return false;
        }
    
    }
    
    const charIsRefToken = (char:string) => {
    
        if(char === "$" || char === "#") {
            return true;
        } else {
            return false;
        }
    
    }

    return { getSheetRowValues }

}





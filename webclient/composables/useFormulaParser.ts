import { Variable } from "~~/types/Model";

export const useFormulaParser = () => {

    type ValueObject = {
        indexes: number[];
        valueArray: string[];
    }
    
    //composable that takes a variable and return the values to be displayed based on the value string
    const getValuesToDisplay = (variableInput:Variable) => {
    
        const valueString:string = variableInput.value;
    
        //object that stores splits out the refs from the value string and stores their location
        const valueObject:ValueObject = getValueObject(valueString);
    
        //stores all the values that need to be displayed e.g. are returned at the end
        var valuesToDisplay:string[];
    
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
    
            //get the refs in the valueArray and replace them with the actual value
            for(let j=0; j < valueObject.indexes.length; j++) {
                let ref:string = valueObject.valueArray[valueObject.indexes[j]];
                let refValue = getRefValue(ref, i, valuesToDisplay);
                valueObject.valueArray[valueObject.indexes[j]] = refValue;
            }
    
            //concatinate the updated valueArray to single string
            var stringForParser;
            for(let x=0; x < valueObject.valueArray.length; x++) {
                stringForParser = stringForParser + valueObject.valueArray[x];
            }
    
            //run the string through the maths parser
            //const valueToDisplay = mathParser(stringForParser);
            
            //add the solution of maths parser to the valuesToDisplay string
            //valuesToDisplay.push(valueToDisplay);
        }
    
        return valuesToDisplay;
    
    }
    
    //gets gets the valueString and returns an object with an array of the components and an array of the indexes of the refs
    const getValueObject = (valueString:string) => {
        
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
            console.log("i is: " + i);
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
                console.log("externalRef: " + externalRef);
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
                console.log("nonRefPart: " + nonRefPart);
                valueArray.push(nonRefPart);
                index++;
                i = i + counter -1;
            }
        }
    
        valueObjectOut.valueArray = valueArray;
        valueObjectOut.indexes = indexes;
        console.log("valueObjectOut: " + valueObjectOut);
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
        return "";
    
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

    return { getValuesToDisplay, getValueObject, getRefValue }

}





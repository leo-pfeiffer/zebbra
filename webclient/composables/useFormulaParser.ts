import { Variable } from "~~/types/Model";

import { useMathParser } from "./useMathParser";

import { ValueObject } from "~~/types/ValueObject";

export const useFormulaParser = () => {

    type Reference = {
        id: string;
        refs: string[];
    }

    type VariableInfo = {
        row_values:string[];
        time_series:boolean;
        value:string;
    }

    //todo: add model context??
    //method that takes an array of variables and returns the values to be displayed for every variable
    const getSheetRowValues = (variables: Variable[]) => {

        //get the order in which the variables get created
        var order: string[] = getCreationOrder(variables);

        var variablesMap = new Map<string, VariableInfo>();
        //var rowTimeSeriesMap = new Map<string, boolean>();

        for (let i = 0; i < order.length; i++) {

            var rowValuesToDisplay: string[] = [];

            var index = 0;
            while (variables[index]._id != order[i]) {
                index++
            }
            var variable: Variable = variables[index];

            if (!variable.time_series || typeof variable.value != "string") {
                for (let i = 0; i < 24; i++) {
                    rowValuesToDisplay.push("–");
                }

                var varInfo:VariableInfo = {
                    row_values: rowValuesToDisplay,
                    time_series: variable.time_series,
                    value: variable.value
                }
                variablesMap.set(variable._id, varInfo);
                
            } else {
                try {
                    rowValuesToDisplay = getRowValues(variable, variablesMap);
                } catch (e) {
                    console.log(e);
                    for (let i = 0; i < 24; i++) {
                        rowValuesToDisplay.push("#REF!");
                    }
                }
                var varInfo:VariableInfo = {
                    row_values: rowValuesToDisplay,
                    time_series: variable.time_series,
                    value: variable.value
                }
                variablesMap.set(variable._id, varInfo);
            }

        }
        //reset original order
        var rowValuesArray: string[][] = [];
        
        for(let i=0; i < variables.length; i++) {
            rowValuesArray.push(variablesMap.get(variables[i]._id).row_values);
        }

        return rowValuesArray;
    }

    //method that takes a variable and returns the values to be displayed based on the value string
    const getRowValues = (variableInput: Variable, variablesAlreadyCovered: Map<string, VariableInfo>) => {

        var valueString: string = variableInput.value;

        //object that stores splits out the refs from the value string and stores their location
        const valueObject: ValueObject = createValueObject(valueString);

        //stores all the values that need to be displayed e.g. are returned at the end
        var valuesToDisplay: string[] = [];

        //push empty values for startingAt
        for (let i = 0; i < variableInput.starting_at; i++) {
            valuesToDisplay.push("–");
        }

        if (variableInput.first_value_diff) {
            var firstValue:string;
            if(variableInput.value_1.includes("#")) {
                firstValue = getExternalRefValue(variableInput.value_1, variableInput.starting_at, variablesAlreadyCovered);
            } else {
                firstValue = useMathParser(variableInput.value_1).toString();
            }
            valuesToDisplay.push(firstValue);
        }

        //change starting point of 'i' in for loop depending on startingAt and whether first value is different
        let startingPointForI = 0 + variableInput.starting_at;
        if (variableInput.first_value_diff) {
            startingPointForI++;
        }

        for (let i = startingPointForI; i < 24; i++) {

            //store valueArray with refs in new array so refs can be overwritten
            var valueArrayToBeOverwritten: string[] = [...valueObject.value_array];

            //get the refs in the valueArray and replace them with the actual value
            for (let j = 0; j < valueObject.indexes.length; j++) {
                var ref: string = valueArrayToBeOverwritten[valueObject.indexes[j]];
                var refValue = getRefValue(ref, i, valuesToDisplay, variablesAlreadyCovered);
                valueArrayToBeOverwritten[valueObject.indexes[j]] = refValue;
            }

            //concatinate the updated valueArray to single string
            var stringForParser: string = "";
            for (let x = 0; x < valueArrayToBeOverwritten.length; x++) {
                stringForParser = stringForParser + valueArrayToBeOverwritten[x];
            }

            //run the string through the maths parser
            const valueToDisplay: string = Math.floor(useMathParser(stringForParser)).toString();

            //add the solution of maths parser to the valuesToDisplay string
            valuesToDisplay.push(valueToDisplay);
        }
        return valuesToDisplay;

    }

    //gets gets the valueString and returns an object with an array of the components and an array of the indexes of the refs
    const createValueObject = (valueString: string) => {

        //instantiate valueObject for output
        let valueObjectOut: ValueObject = {
            indexes: [],
            value_array: []
        };

        let valueArray: string[] = [];
        let indexes: number[] = [];

        //instantiate index to store where in the array the refs are stored
        let index = 0;

        /* loop over the valueString and separate refs from rest and store the different parts 
        in the valueArray while storing the indexes of the refs in the indexes array */
        for (let i = 0; i < valueString.length; i++) {
            let char = valueString[i];
            if (char === "$") {
                var internalRef: string = char;
                var counter = 1;
                while (charIsNumerical(valueString[i + counter]) && (valueString[i + counter] != undefined)) {
                    internalRef = internalRef + valueString[i + counter];
                    counter++;
                    if ((i + counter >= valueString.length)) {
                        break;
                    }
                }
                valueArray.push(internalRef);
                indexes.push(index);
                index++;
                i = i + counter - 1;
            } else if (char === "#") {
                var externalRef: string = char;
                var counter = 1;
                while ((charIsNumerical(valueString[i + counter]) || valueString[i + counter] === "$") && (valueString[i + counter] != undefined)) {
                    externalRef = externalRef + valueString[i + counter];
                    counter++;
                    if ((i + counter >= valueString.length)) {
                        break;
                    }
                }
                valueArray.push(externalRef);
                indexes.push(index);
                index++;
                i = i + counter - 1;
            } else {
                var nonRefPart = char;
                var counter = 1;
                while (!charIsRefToken(valueString[i + counter]) && (valueString[i + counter] != undefined)) {
                    nonRefPart = nonRefPart + valueString[i + counter];
                    counter++
                    if ((i + counter >= valueString.length)) {
                        break;
                    }
                }
                valueArray.push(nonRefPart);
                index++;
                i = i + counter - 1;
            }
        }

        valueObjectOut.value_array = valueArray;
        valueObjectOut.indexes = indexes;
        return valueObjectOut;
    }

    /* takes any ref and returns its value */
    const getRefValue = (ref: string, index: number, valuesToDisplay: string[], variablesAlreadyCovered: Map<string, VariableInfo>) => {

        let returnValue: string;

        if (ref[0] == "$") {
            returnValue = getInternalRefValue(ref, index, valuesToDisplay);
        } else if (ref[0] == "#") {
            returnValue = getExternalRefValue(ref, index, variablesAlreadyCovered);
        }
        return returnValue;

    }

    /* takes an internal ref, the current position, and the current state of the valuesToDisplay array and returns the value */
    const getInternalRefValue = (internalRef: string, index: number, valuesToDisplay: string[]) => {

        const indexDiff: number = +internalRef.substring(1);

        return valuesToDisplay[index - indexDiff];

    }

    /* takes external ref and returns the value */
    const getExternalRefValue = (externalRef: string, index: number, variablesAlreadyCovered: Map<string, VariableInfo>) => {

        var ref:string;
        var indexDiff:number = 0;
        var outputValue:string;

        if(externalRef.includes("$")) {
            ref = externalRef.slice(0, externalRef.indexOf("$")).substring(1);
            indexDiff = +externalRef.slice(externalRef.indexOf("$")).substring(1);
        } else {
            ref = externalRef.substring(1);
        }

        if(variablesAlreadyCovered.get(ref).time_series) {
            outputValue = variablesAlreadyCovered.get(ref).row_values[index - indexDiff];
        } else {
            outputValue = useMathParser(variablesAlreadyCovered.get(ref).value).toString();
        }

        return outputValue;

    }

    const charIsNumerical = (char: string) => {

        if (char === "0" || char === "1" || char === "2" || char === "3" || char === "4" || char === "5" || char === "6" || char === "7" || char === "8" || char === "9") {
            return true;
        } else {
            return false;
        }

    }

    const charIsRefToken = (char: string) => {

        if (char === "$" || char === "#") {
            return true;
        } else {
            return false;
        }

    }

    const charIsOperator = (char: string) => {

        if (char === "+" || char === "-" || char === "*" || char === "/" || char === "(" || char === ")") {
            return true;
        } else {
            return false;
        }

    }

    //method that defines the order in which the variables must be calculated based on their hierarchy
    //return an ordered array of ids
    const getCreationOrder = (variables: Variable[]) => {

        var referenceArray: Reference[] = getReferenceArray(variables);

        //use Kahns algo to get the order in which the variables need to be handled based on references
        var order: string[] = kahnTopologicalSort(referenceArray);
        return order;
    }

    //method that creates an array of references (e.g. objects containing variable ids and an array of ids they are referenced in)
    const getReferenceArray = (variables: Variable[]) => {

        //first create an (inverted) referenceArray where for every id the references occurring in their value are stored
        var referenceArrayInverted: Reference[] = [];

        for (let i = 0; i < variables.length; i++) {

            //get the values_1 and value_2 from all variables in the sheet
            const valueString = variables[i].value + variables[i].value_1;

            //for every variable get the external refs (#) and store them in the reference
            var refsArray: string[] = [];

            for (let i = 0; i < valueString.length; i++) {
                let char = valueString[i];
                if (char === "#") {
                    var ref: string = ""; //empty string to store id (ie number after the #)
                    var counter = 1;
                    //only getting the numerical because only the ids are needed not the point in time (e.g. t-1)
                    while (charIsNumerical(valueString[i + counter]) && (valueString[i + counter] != undefined)) {
                        ref = ref + valueString[i + counter];
                        counter++;
                        if ((i + counter >= valueString.length)) {
                            break;
                        }
                    }
                    refsArray.push(ref);
                    i = i + counter - 1;
                }
            }

            var reference: Reference = {
                id: variables[i]._id,
                refs: []
            };

            if (refsArray.length > 0) {
                reference.refs = refsArray;
            }
            referenceArrayInverted.push(reference);
        }

        //the inverted referenceArray must be turned, so for every ID the ids are stored in which the ID is reverenced in
        var referenceArrayOut: Reference[] = []

        //populate a referenceArray only with the ids of the variables
        for (let i = 0; i < referenceArrayInverted.length; i++) {
            var reference: Reference = {
                id: referenceArrayInverted[i].id,
                refs: []
            }
            referenceArrayOut.push(reference);
        }

        //for every variable check if id is included in references of other ids and add other ids if yes
        for (let i = 0; i < referenceArrayOut.length; i++) {
            let id = referenceArrayOut[i].id;
            for (let j = 0; j < referenceArrayInverted.length; j++) {
                if (referenceArrayInverted[j].refs.includes(id)) {
                    referenceArrayOut[i].refs.push(referenceArrayInverted[j].id);
                }
            }
        }
        return referenceArrayOut;
    }

    //adopted from https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/
    const kahnTopologicalSort = (referenceArray: Reference[]) => {

        const numRows = referenceArray.length;

        // This is a hashmap that holds that allows you to look up the index
        // of every Reference object in the referenceArray based on its ID
        // Result: { A: 0, B: 1, C: 2, D: 3, E: 4, F: 5 }
        // and you can access the index by doing indexMap["C"] (== 2)
        const indexMap = {}
        for (let i = 0; i < numRows; i++) {
            indexMap[referenceArray[i].id] = i;
        }

        // This is a hashmap containing the indegrees for every ID.
        // calculate the indegrees of each row
        const indegrees = {}

        // initialize all IDs with 0
        for (let i = 0; i < numRows; i++) {
            let row = referenceArray[i];
            indegrees[row.id] = 0;
        }

        // and every time an ID is contained in a "refs" array, add 1 to the
        // count in the indegrees object
        // Result: { A: 2, B: 2, C: 1, D: 1, E: 0, F: 0 }
        for (let i = 0; i < numRows; i++) {
            let row = referenceArray[i];
            for (let j = 0; j < row.refs.length; j++) {
                let ref = row.refs[j];
                indegrees[ref] += 1;
            }
        }
            
        // Queue all IDs with indegree of 0
        //  Initally, that is only [ 'E', 'F' ]
        const queue = [];

        for (let i = 0; i < numRows; i++) {
            let row = referenceArray[i]
            if (indegrees[row.id] === 0) {
                queue.push(row.id);
            }
        }
        
        // store the IDs in the final order
        const finalOrder = [];

        // continue until no more elements in queue
        while (queue.length > 0) {

            // remove and return the first ID from queue
            const next = queue.shift();
            finalOrder.push(next);

            // use the index map to get the index of the Reference of the ID
            // in the referenceArray
            const nextIndex = indexMap[next];

            // Get the Reference from the referenceArray based on this index
            const nextReference = referenceArray[nextIndex];

            // Iterate over References of the current row and reduce indegree by 1
            for (let i = 0; i < nextReference.refs.length; i++) {

                // ID of the reference
                let ref = nextReference.refs[i];
                indegrees[ref] -= 1;

                // Queue the ID of the reference if it now has indegree 0
                if (indegrees[ref] === 0) {
                    queue.push(ref);
                }
            }
        }

        if (finalOrder.length != numRows) {
            console.log("error");
            return []
        } else {
            return finalOrder;
        }

    }

    return { getSheetRowValues, createValueObject, charIsNumerical, charIsRefToken, charIsOperator, getCreationOrder, getReferenceArray, kahnTopologicalSort }

}

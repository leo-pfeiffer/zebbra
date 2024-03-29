import { expect, it, describe } from 'vitest';

import { useFormulaParser } from '../methods/useFormulaParser';

import { Variable } from "~~/types/Model";

type ValueObject = {
    indexes: number[];
    value_array: string[];
}

type Reference = {
    id: string;
    refs: string[];
}

describe('Tests for getSheetRowValues', () => {

    it('should generate the correct values for variable without refs and timeSeries === false', () => {

        const inputVariable:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: false,
            starting_at: 0,
            first_value_diff: undefined,
            value: "100",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [ inputVariable ];

        var expectedOutput:string[] = [];
        
        for(let i=0; i < 24; i++) {
            expectedOutput.push("–");
        }

        expect(useFormulaParser().getSheetRowValues(input)[0]).toStrictEqual(expectedOutput);

    })

    it('should generate the correct values for variable with internal refs', () => {

        const inputVariable:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: true,
            starting_at: 0,
            first_value_diff: true,
            value: "$1+1",
            value_1: "100",
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [ inputVariable ];

        var expectedOutput:string[] = [];
        
        let startingValue:number = 100;

        for(let i=0; i < 24; i++) {
            var value:number = startingValue + i;
            var valueToDisplay = value.toString();
            expectedOutput.push(valueToDisplay);
        }

        expect(useFormulaParser().getSheetRowValues(input)[0]).toStrictEqual(expectedOutput);
        
    })

    it('should generate the correct values for variable with starting_at >0', () => {

        const inputVariable:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: true,
            starting_at: 10,
            first_value_diff: true,
            value: "$1+1",
            value_1: "1000",
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [ inputVariable ];

        var expectedOutput:string[] = [];

        for(let i=0; i < inputVariable.starting_at; i++) {
            expectedOutput.push("–");
        }
        
        let startingValue:number = 1000;

        for(let i=0; i < (24 - inputVariable.starting_at); i++) {
            var value:number = startingValue + i;
            var valueToDisplay = value.toString();
            expectedOutput.push(valueToDisplay);
        }

        expect(useFormulaParser().getSheetRowValues(input)[0]).toStrictEqual(expectedOutput);
        
    })

    it('should generate the correct values for variables with internal and external refs', () => {

        const inputVariable1:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: true,
            starting_at: 0,
            first_value_diff: true,
            value: "$1+#3",
            value_1: "#2",
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: false,
            starting_at: 0,
            first_value_diff: false,
            value: "1000",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable3:Variable = {
            _id: "3",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: false,
            starting_at: 0,
            first_value_diff: false,
            value: "1",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [ inputVariable1, inputVariable2, inputVariable3 ];

        var expectedOutput:string[] = [];

        let startingValue:number = 1000;

        for(let i=0; i < (24); i++) {
            var value:number = startingValue + i;
            var valueToDisplay = value.toString();
            expectedOutput.push(valueToDisplay);
        }

        expect(useFormulaParser().getSheetRowValues(input)[0]).toStrictEqual(expectedOutput);
        
    })

    it('should generate correct output if it variable only refs external variable', () => {

        const inputVariable1:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: true,
            starting_at: 0,
            first_value_diff: true,
            value: "$1+1",
            value_1: "100",
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: true,
            starting_at: 0,
            first_value_diff: false,
            value: "#1",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [ inputVariable1, inputVariable2 ];

        expect(useFormulaParser().getSheetRowValues(input)[0]).toStrictEqual(useFormulaParser().getSheetRowValues(input)[1]);

    });

    it('should output #REF! on an incorrect input', () => {

        const inputVariable1:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: true,
            starting_at: 0,
            first_value_diff: true,
            value: "$1+#3", //  <------  #3 is not provided
            value_1: "#2",
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: false,
            starting_at: 0,
            first_value_diff: false,
            value: "1000",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [ inputVariable1, inputVariable2 ];

        var expectedOutput:string[] = [];

        for(let i=0; i < (24); i++) {
            expectedOutput.push("#REF!");
        }

        expect(useFormulaParser().getSheetRowValues(input)[0]).toStrictEqual(expectedOutput);
        
    })
})

describe('Tests for createValueObject method', () => {

    it('should create the correct ValueObject on input with multiple refs', () => {

        const input:string = "$123+#345*(1+#567)";

        const expectedOutput:ValueObject = {
            indexes: [0, 2, 4],
            value_array: ["$123", "+", "#345", "*(1+", "#567", ")"]
        }

        const output:ValueObject = useFormulaParser().createValueObject(input);

        expect(output.indexes).toStrictEqual(expectedOutput.indexes);
        expect(output.value_array).toStrictEqual(expectedOutput.value_array);

    });

    it('should create the correct ValueObject on input with no refs', () => {

        const input:string = "100*100";

        const expectedOutput:ValueObject = {
            indexes: [],
            value_array: ["100*100"]
        }

        const output:ValueObject = useFormulaParser().createValueObject(input);

        expect(output.indexes).toStrictEqual(expectedOutput.indexes);
        expect(output.value_array).toStrictEqual(expectedOutput.value_array);

    });

    it('should create the correct ValueObject on empty input', () => {

        const input:string = "";

        const expectedOutput:ValueObject = {
            indexes: [],
            value_array: []
        }

        const output:ValueObject = useFormulaParser().createValueObject(input);

        expect(output.indexes).toStrictEqual(expectedOutput.indexes);
        expect(output.value_array).toStrictEqual(expectedOutput.value_array);

    });

});

describe('Tests for charIsRefToken method', () => {

    it('should return true when RefTokens are entered', () => {
        expect(useFormulaParser().charIsRefToken("$")).toBe(true);
        expect(useFormulaParser().charIsRefToken("#")).toBe(true);
    })

    it('should return false when numericals or letters are entered', () => {
        expect(useFormulaParser().charIsRefToken("1")).toBe(false);
        expect(useFormulaParser().charIsRefToken("3")).toBe(false);
        expect(useFormulaParser().charIsRefToken("34")).toBe(false);
        expect(useFormulaParser().charIsRefToken("56778")).toBe(false);
        expect(useFormulaParser().charIsRefToken("x")).toBe(false);
        expect(useFormulaParser().charIsRefToken("Hello")).toBe(false);
    })

})

describe('Tests for charIsNumerical method', () => {
    it('should return true when numerical is entered', () => {
        expect(useFormulaParser().charIsNumerical("1")).toBe(true);
        expect(useFormulaParser().charIsNumerical("2")).toBe(true);
        expect(useFormulaParser().charIsNumerical("3")).toBe(true);
        expect(useFormulaParser().charIsNumerical("4")).toBe(true);
        expect(useFormulaParser().charIsNumerical("5")).toBe(true);
        expect(useFormulaParser().charIsNumerical("6")).toBe(true);
        expect(useFormulaParser().charIsNumerical("7")).toBe(true);
        expect(useFormulaParser().charIsNumerical("8")).toBe(true);
        expect(useFormulaParser().charIsNumerical("9")).toBe(true);
        expect(useFormulaParser().charIsNumerical("0")).toBe(true);
    })

    it('should return false when non-numericals are entered', () => {
        expect(useFormulaParser().charIsNumerical("x")).toBe(false);
        expect(useFormulaParser().charIsNumerical("X")).toBe(false);
        expect(useFormulaParser().charIsNumerical("asdfcaövsklj")).toBe(false);
        expect(useFormulaParser().charIsNumerical("XAÖSLDFKJ")).toBe(false);
    })
})

describe('Tests for charIsOperator method', () => {
    it('should return true when operators are entered', () => {
        expect(useFormulaParser().charIsOperator("+")).toBe(true);
        expect(useFormulaParser().charIsOperator("-")).toBe(true);
        expect(useFormulaParser().charIsOperator("*")).toBe(true);
        expect(useFormulaParser().charIsOperator("/")).toBe(true);
        expect(useFormulaParser().charIsOperator("(")).toBe(true);
        expect(useFormulaParser().charIsOperator(")")).toBe(true);
    })

    it('should return false when non-operators are entered', () => {
        expect(useFormulaParser().charIsOperator("0")).toBe(false);
        expect(useFormulaParser().charIsOperator("1")).toBe(false);
        expect(useFormulaParser().charIsOperator("x")).toBe(false);
        expect(useFormulaParser().charIsOperator("asöldfkjas")).toBe(false);
    })
})

describe('Tests for getCreationOrder method', () => {

    it('should return the correct order', () => {

        const inputVariable1:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "1*1",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "#3*2",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable3:Variable = {
            _id: "3",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "$1*(1+0.01)",
            value_1: "#1",
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [inputVariable1, inputVariable2, inputVariable3];

        const expectedOutput:string[] = ["1", "3", "2"];

        expect(useFormulaParser().getCreationOrder(input)).toStrictEqual(expectedOutput);

    });

});

describe('Tests for getReferenceArray Method', () => {

    it('should generate the correct references', () => {

        const inputVariable1:Variable = {
            _id: "123456",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "1*1",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "234567",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "#123456*2",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [inputVariable1, inputVariable2];

        const expectedOutput1:Reference = {
            id: "123456",
            refs: ["234567"]
        }

        const expectedOutput2:Reference = {
            id: "234567",
            refs: []
        }

        const output:Reference[] = useFormulaParser().getReferenceArray(input);

        expect(output[0].id).toBe(expectedOutput1.id);
        expect(output[0].refs).toStrictEqual(expectedOutput1.refs);
        expect(output[1].id).toBe(expectedOutput2.id);
        expect(output[1].refs).toStrictEqual(expectedOutput2.refs);

    });

    it('should generate the correct Reference with value_1 input', () => {

        const inputVariable1:Variable = {
            _id: "1",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "1*1",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "#3*2",
            value_1: undefined,
            integration_name: undefined,
            integration_values: undefined
        }

        const inputVariable3:Variable = {
            _id: "3",
            name: undefined,
            val_type: undefined,
            decimal_places: 0,
            editable: undefined,
            var_type: undefined,
            time_series: undefined,
            starting_at: undefined,
            first_value_diff: undefined,
            value: "$1*(1+0.01)",
            value_1: "#1",
            integration_name: undefined,
            integration_values: undefined
        }

        const input:Variable[] = [inputVariable1, inputVariable2, inputVariable3];

        const expectedOutput1:Reference = {
            id: "1",
            refs: ["3"]
        }

        const expectedOutput2:Reference = {
            id: "2",
            refs: []
        }

        const expectedOutput3:Reference = {
            id: "3",
            refs: ["2"]
        }

        const output:Reference[] = useFormulaParser().getReferenceArray(input);

        expect(output[0].id).toBe(expectedOutput1.id);
        expect(output[0].refs).toStrictEqual(expectedOutput1.refs);
        expect(output[1].id).toBe(expectedOutput2.id);
        expect(output[1].refs).toStrictEqual(expectedOutput2.refs);
        expect(output[2].id).toBe(expectedOutput3.id);
        expect(output[2].refs).toStrictEqual(expectedOutput3.refs);

    })
})

describe('Topologial Sort Tests', () => {

    it('should generate the correct order (simple input)', () => {

        const input:Reference[] = [
            {id: "A", refs: []},
            {id: "B", refs: ["A"]},
        ];
        const expectedOutput:string[] = ["B", "A"];
        expect(useFormulaParser().kahnTopologicalSort(input)).toStrictEqual(expectedOutput);

    })

    it('should generate the correct order (medium input)', () => {

        const input:Reference[] = [
            {id: "A", refs: ["C"]},
            {id: "B", refs: ["A"]},
            {id: "C", refs: []},
        ];
        const expectedOutput:string[] = ["B", "A", "C"];
        expect(useFormulaParser().kahnTopologicalSort(input)).toStrictEqual(expectedOutput);

    })

    it('should generate the correct order (complex input)', () => {

        const input:Reference[] = [
            {id: "A", refs: []},
            {id: "B", refs: []},
            {id: "C", refs: ["D"]},
            {id: "D", refs: ["B"]},
            {id: "E", refs: ["A", "B"]},
            {id: "F", refs: ["A", "C"]}
        ];
        const expectedOutput:string[] = ["E", "F", "A", "C", "D", "B"];
        expect(useFormulaParser().kahnTopologicalSort(input)).toStrictEqual(expectedOutput);

    })

})

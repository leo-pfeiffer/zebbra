import { expect, it, describe, test } from 'vitest';

import { useFormulaParser } from '../composables/useFormulaParser';

import { Variable } from "~~/types/Model";

type ValueObject = {
    indexes: number[];
    valueArray: string[];
}

type Reference = {
    id: string;
    refs: string[];
}

describe('Tests for createValueObject method', () => {

    it('should create the correct ValueObject on input with multiple refs', () => {

        const input:string = "$123+#345*(1+#567)";

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

describe('Tests for getCreationOrder method', () => {

    it('should return the correct order', () => {

        const inputVariable1:Variable = {
            _id: "1",
            name: undefined,
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "1*1",
            value_1: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "#3*2",
            value_1: undefined,
            integration_values: undefined
        }

        const inputVariable3:Variable = {
            _id: "3",
            name: undefined,
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "$1*(1+0.01)",
            value_1: "#1",
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
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "1*1",
            value_1: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "234567",
            name: undefined,
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "#123456*2",
            value_1: undefined,
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
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "1*1",
            value_1: undefined,
            integration_values: undefined
        }

        const inputVariable2:Variable = {
            _id: "2",
            name: undefined,
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "#3*2",
            value_1: undefined,
            integration_values: undefined
        }

        const inputVariable3:Variable = {
            _id: "3",
            name: undefined,
            valType: undefined,
            editable: undefined,
            varType: undefined,
            timeSeries: undefined,
            startingAt: undefined,
            firstValueDiff: undefined,
            value: "$1*(1+0.01)",
            value_1: "#1",
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

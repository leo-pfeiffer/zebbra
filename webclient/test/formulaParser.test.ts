import { expect, it, describe, test } from 'vitest';

import { useFormulaParser } from '../composables/useFormulaParser';


describe('Test: charIsRefToken', () => {

    it('should return TRUE when RefTokens are entered', () => {
        expect(useFormulaParser().charIsRefToken("$")).toBe(true);
        expect(useFormulaParser().charIsRefToken("#")).toBe(true);
    })

    it('should return FALSE when numericals or letters are entered', () => {
        expect(useFormulaParser().charIsRefToken("1")).toBe(false);
        expect(useFormulaParser().charIsRefToken("3")).toBe(false);
        expect(useFormulaParser().charIsRefToken("34")).toBe(false);
        expect(useFormulaParser().charIsRefToken("56778")).toBe(false);
        expect(useFormulaParser().charIsRefToken("x")).toBe(false);
        expect(useFormulaParser().charIsRefToken("Hello")).toBe(false);
    })

})

describe('Test: charIsNumerical', () => {
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

describe('Topologial Sort Tests', () => {

    type Reference = {
        id: string;
        refs: string[];
    }

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

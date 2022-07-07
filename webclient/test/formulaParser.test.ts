import { expect, it, describe, test } from 'vitest'

import { useFormulaParser } from '../composables/useFormulaParser'

it("Test: charIsRefToken", () => {

    expect(useFormulaParser().charIsRefToken("$")).toBe(true);
    expect(useFormulaParser().charIsRefToken("#")).toBe(true);
    expect(useFormulaParser().charIsRefToken("1")).toBe(false);
    expect(useFormulaParser().charIsRefToken("x")).toBe(false);
})

it("Test: charIsNumerical'", () => {

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

    expect(useFormulaParser().charIsNumerical("x")).toBe(false);
    expect(useFormulaParser().charIsNumerical("X")).toBe(false);
})

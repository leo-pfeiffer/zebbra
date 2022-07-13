import { expect, it, describe, beforeAll } from 'vitest';
import { useGetValueFromHumanReadable } from '../methods/useGetValueFromHumanReadable';
import { Variable } from '../types/Model';

describe('useGetValueFromHumanReadable Tests', () => {

    const initialCustomers:Variable = {
        _id: "1",
        name: "Initial Customers",
        val_type: "number",
        editable: true,
        var_type: "value",
        time_series: false,
        starting_at: 0,
        first_value_diff: false,
        value: "1000",
        value_1: undefined,
        integration_values: undefined
    };

    const customerGrowth:Variable = {
        _id: "2",
        name: "Customer Growth",
        val_type: "percentage",
        editable: true,
        var_type: "value",
        time_series: false,
        starting_at: 0,
        first_value_diff: false,
        value: "0.3",
        value_1: undefined,
        integration_values: undefined
    }

    const customers:Variable = {
        _id: "3",
        name: "Customers",
        val_type: "number",
        editable: true,
        var_type: "formula",
        time_series: true,
        starting_at: 0,
        first_value_diff: true,
        value: "$1*(1+#2)",
        value_1: "#1",
        integration_values: undefined
    }

    const variableSearchMap:Map<string, string> = new Map<string, string>();

    beforeAll(() => {
        variableSearchMap.set(initialCustomers._id, initialCustomers.name);
        variableSearchMap.set(customerGrowth._id, customerGrowth.name);
        variableSearchMap.set(customers._id, customers.name);
    })

    it('should return the correct value from a human readable input', () => {

        const humanReadableInput:string = "Customers[1]*(1+Customer Growth[0])";
        const expectedOutput:string = "$1*(1+#2)"

        expect(useGetValueFromHumanReadable(humanReadableInput, customers._id, variableSearchMap)).toStrictEqual(expectedOutput);

    });

    it('should return the correct value from a human readable input with previous value on external ref', () => {

        const humanReadableInput:string = "Customers[1]*(1+Customer Growth[1])";
        const expectedOutput:string = "$1*(1+#2$1)"

        expect(useGetValueFromHumanReadable(humanReadableInput, customers._id, variableSearchMap)).toStrictEqual(expectedOutput);

    });

    it('should return the correct value from a human readable input without any refs', () => {

        const humanReadableInput1:string = "1+1+1+1";
        const expectedOutput1:string = "1+1+1+1";
        expect(useGetValueFromHumanReadable(humanReadableInput1, customers._id, variableSearchMap)).toStrictEqual(expectedOutput1);

        const humanReadableInput2:string = "123456789";
        const expectedOutput2:string = "123456789";
        expect(useGetValueFromHumanReadable(humanReadableInput2, customers._id, variableSearchMap)).toStrictEqual(expectedOutput2);

        const humanReadableInput3:string = "1+2*4/5(7*89)";
        const expectedOutput3:string = "1+2*4/5(7*89)";
        expect(useGetValueFromHumanReadable(humanReadableInput3, customers._id, variableSearchMap)).toStrictEqual(expectedOutput3);

        const humanReadableInput4:string = "0.3";
        const expectedOutput4:string = "0.3";
        expect(useGetValueFromHumanReadable(humanReadableInput4, customers._id, variableSearchMap)).toStrictEqual(expectedOutput4);

    });

    it('should work with leading SPACES before the refs', () => {

        const humanReadableInput:string = "Customers[1] * (1 + Customer Growth[1])";
        const expectedOutput:string = "$1*(1+#2$1)"

        expect(useGetValueFromHumanReadable(humanReadableInput, customers._id, variableSearchMap)).toStrictEqual(expectedOutput);

    })

})
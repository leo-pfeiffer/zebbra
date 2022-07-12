import { expect, it, describe, beforeAll } from 'vitest';
import { useGetValueFromHumanReadable } from '~~/composables/useGetValueFromHumanReadable';
import { Variable } from '~~/types/Model';

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
        variableSearchMap.set(initialCustomers._id, initialCustomers.value);
        variableSearchMap.set(customerGrowth._id, customerGrowth.value);
        variableSearchMap.set(customers._id, customers.value);
    })

    it('should return the correct value from a human readable input', () => {

        const humanReadableInput:string = "Customers[1]*(1+Customer Growth[0])";
        const expectedOutput:string = "$1*(1+#2)"

        expect(useGetValueFromHumanReadable(humanReadableInput, customers._id, variableSearchMap)).toStrictEqual(expectedOutput);

    });

})
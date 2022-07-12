import { expect, it, describe, beforeAll } from 'vitest';
import { useGetHumanReadableFormula } from '../composables/useGetHumanReadableFormula';
import { Variable } from '../types/Model';

describe('useGetHumanReadableFormula Tests', () => {

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

    const customersWithPrevious:Variable = {
        _id: "4",
        name: "Customers",
        val_type: "number",
        editable: true,
        var_type: "formula",
        time_series: true,
        starting_at: 0,
        first_value_diff: true,
        value: "$1*(1+#2$1)",
        value_1: "#1",
        integration_values: undefined
    }

    const variableSearchMap:Map<string, string> = new Map<string, string>();

    beforeAll(() => {
        variableSearchMap.set(initialCustomers._id, initialCustomers.name);
        variableSearchMap.set(customerGrowth._id, customerGrowth.name);
        variableSearchMap.set(customers._id, customers.name);
        variableSearchMap.set(customersWithPrevious._id, customersWithPrevious.name);
    })

    it('should return the correct human readable fromat with external and internal ref', () => {

        const expectedOuputValue:string = "Customers[1]*(1+Customer Growth[0])"
        expect(useGetHumanReadableFormula(customers.value, customers._id, variableSearchMap)).toStrictEqual(expectedOuputValue);

        const expectedOuputValue1:string = "Initial Customers[0]"
        expect(useGetHumanReadableFormula(customers.value_1, customers._id, variableSearchMap)).toStrictEqual(expectedOuputValue1);
    });

    it('should return the correct human readable fromat with previous external ref', () => {

        const expectedOuputValue:string = "Customers[1]*(1+Customer Growth[1])"
        expect(useGetHumanReadableFormula(customersWithPrevious.value, customersWithPrevious._id, variableSearchMap)).toStrictEqual(expectedOuputValue);

    });

})
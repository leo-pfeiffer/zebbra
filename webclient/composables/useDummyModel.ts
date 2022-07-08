import { Model, Sheet, Variable } from "~~/types/Model"

const assumption1:Variable = {
    _id: "123456",
    name: "Customer Growth Rate",
    val_type: "percentage",
    editable: true,
    var_type: "value",
    time_series: false,
    starting_at: 0,
    first_value_diff: false,
    value: "0.01",
    value_1: undefined,
    integration_values: undefined
}

const assumption2:Variable = {
    _id: "1235642",
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
}

const assumption3:Variable = {
    _id: "1",
    name: "Avg. Contract Value",
    val_type: "currency",
    editable: true,
    var_type: "value",
    time_series: false,
    starting_at: 0,
    first_value_diff: false,
    value: "20",
    value_1: undefined,
    integration_values: undefined
}

const assumption4:Variable = {
    _id: "4",
    name: "Static Formula",
    val_type: "number",
    editable: true,
    var_type: "formula",
    time_series: false,
    starting_at: 2,
    first_value_diff: false,
    value: "2*100",
    value_1: undefined,
    integration_values: undefined
}

const assumption5:Variable = {
    _id: "5",
    name: "Reducing Number",
    val_type: "number",
    editable: true,
    var_type: "formula",
    time_series: true,
    starting_at: 0,
    first_value_diff: true,
    value: "$1*(1-0.01)",
    value_1: "1000",
    integration_values: undefined
}

const assumption6:Variable = {
    _id: "6",
    name: "Customers",
    val_type: "number",
    editable: true,
    var_type: "formula",
    time_series: true,
    starting_at: 0,
    first_value_diff: true,
    value: "$1*(1+#123456$1)",
    value_1: "#1235642",
    integration_values: undefined
}

const assumption7:Variable = {
    _id: "7",
    name: "Revenue",
    val_type: "currency",
    editable: true,
    var_type: "formula",
    time_series: true,
    starting_at: 4,
    first_value_diff: false,
    value: "#6$2*#1",
    value_1: undefined,
    integration_values: undefined
}

const variable1:Variable = {
    _id: "7",
    name: "Customers",
    val_type: "number",
    editable: true,
    var_type: "formula",
    time_series: true,
    starting_at: 0,
    first_value_diff: true,
    value: "$1*(1+#123456&1)",
    value_1: "#2",
    integration_values: undefined
}

const variable2:Variable = {
    _id: "8",
    name: "Avg. Price",
    val_type: "number",
    editable: true,
    var_type: "value",
    time_series: false,
    starting_at: 0,
    first_value_diff: false,
    value: "123",
    value_1: undefined,
    integration_values: undefined
}

const dummyRevenueSheet:Sheet = {
    meta: {
        name: "Revenues"
    },
    assumptions: [
        assumption1, assumption2, assumption3, assumption4, assumption5, assumption6, assumption7
    ],
    sections: [{
        name: "Dummy Product",
        rows: [
            variable1, variable2
        ],
        endrow: undefined
    }]
}

const dummyModel:Model = {
    _id: "ölasdkfjaösdflkj",
    meta: {
        name: "Dummy Model",
        starting_month: "2022-07-01",
        admins: [],
        editors: [],
        viewers: [],
        workspace: "Dummy Workspace"
    },
    sheets: [
        dummyRevenueSheet
    ]

}



export const useDummyModelState = () => useState<Model>('dummyModelState', () => dummyModel);
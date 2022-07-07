import { Model, Sheet, Variable } from "~~/types/Model"

const assumption1:Variable = {
    _id: "123456",
    name: "Customer Growth Rate",
    valType: "percentage",
    editable: true,
    varType: "value",
    timeSeries: false,
    startingAt: 0,
    firstValueDiff: false,
    value: "0.01",
    value_1: undefined,
    integration_values: undefined
}

const assumption2:Variable = {
    _id: "1235642",
    name: "Initial Customers",
    valType: "number",
    editable: true,
    varType: "value",
    timeSeries: false,
    startingAt: 0,
    firstValueDiff: false,
    value: "1000",
    value_1: undefined,
    integration_values: undefined
}

const assumption3:Variable = {
    _id: "1",
    name: "Avg. Contract Value",
    valType: "currency",
    editable: true,
    varType: "value",
    timeSeries: false,
    startingAt: 0,
    firstValueDiff: false,
    value: "20",
    value_1: undefined,
    integration_values: undefined
}

const assumption4:Variable = {
    _id: "4",
    name: "Static Formula",
    valType: "number",
    editable: true,
    varType: "formula",
    timeSeries: false,
    startingAt: 2,
    firstValueDiff: false,
    value: "2*100",
    value_1: undefined,
    integration_values: undefined
}

const assumption5:Variable = {
    _id: "5",
    name: "Reducing Number",
    valType: "number",
    editable: true,
    varType: "formula",
    timeSeries: true,
    startingAt: 0,
    firstValueDiff: true,
    value: "$1*(1-0.01)",
    value_1: "1000",
    integration_values: undefined
}

const assumption6:Variable = {
    _id: "6",
    name: "Customers",
    valType: "number",
    editable: true,
    varType: "formula",
    timeSeries: true,
    startingAt: 0,
    firstValueDiff: true,
    value: "$1*(1+#123456$1)",
    value_1: "#1235642",
    integration_values: undefined
}

const assumption7:Variable = {
    _id: "7",
    name: "Revenue",
    valType: "currency",
    editable: true,
    varType: "formula",
    timeSeries: true,
    startingAt: 4,
    firstValueDiff: false,
    value: "#6$2*#1",
    value_1: undefined,
    integration_values: undefined
}

const variable1:Variable = {
    _id: "7",
    name: "Customers",
    valType: "number",
    editable: true,
    varType: "formula",
    timeSeries: true,
    startingAt: 0,
    firstValueDiff: true,
    value: "$1*(1+#123456&1)",
    value_1: "#2",
    integration_values: undefined
}

const variable2:Variable = {
    _id: "8",
    name: "Avg. Price",
    valType: "number",
    editable: true,
    varType: "value",
    timeSeries: false,
    startingAt: 0,
    firstValueDiff: false,
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
        starting_month: new Date(),
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
import { Model, Sheet, Variable } from "~~/types/Model"

const assumption1:Variable = {
    _id: "1",
    name: "Customer Growth Rate",
    valType: "percentage",
    editable: true,
    varType: "value",
    timeSeries: false,
    startingAt: 0,
    firstValueDiff: false,
    value: "0.2",
    value_1: undefined,
    integration_values: undefined
}

const assumption2:Variable = {
    _id: "2",
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
    startingAt: 10,
    firstValueDiff: false,
    value: "200",
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
    value_1: "#2",
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
    value_1: "10000",
    integration_values: undefined
}

const assumption6:Variable = {
    _id: "6",
    name: "Customers",
    valType: "number",
    editable: true,
    varType: "formula",
    timeSeries: true,
    startingAt: 1,
    firstValueDiff: true,
    value: "$1*(1+#1)",
    value_1: "#2",
    integration_values: undefined
}

const dummyRevenueSheet:Sheet = {
    meta: {
        name: "Revenues"
    },
    assumptions: [
        assumption1, assumption2, assumption3, assumption4, assumption5, assumption6
    ],
    sections: [{
        name: "Dummy Product",
        rows: undefined,
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
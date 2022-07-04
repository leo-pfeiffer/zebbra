export interface Model {
    _id: string;
    meta: {
        name: string,
        starting_month:Date,
        admins: string[],
        editors: string[],
        viewers: string[],
        workspace: string
    };
    sheets: Sheet[];
}

export interface Sheet {
    meta: {
        name: string
    },
    assumptions: Variable[],
    sections: {
        name: string,
        rows: Variable[],
        endrow: Variable
    }[]
}

export interface Variable {
    _id: string, //required to be able to reference between different variables
    name: string, //e.g. "Churn Rate" -> how is it called?
    valType: string, // "number", "percentage", "currency" -> how is it displayed?
    editable: boolean, // true, false -> can the user change anything?
    varType: string, // value, formula, integration
    timeSeries: boolean, //true or false -> is the value changing over time or not?
    startingAt: number // -> t+startingAt; default = 0
    firstValueDiff: boolean //is the first value different?
    value: string, //parsed in the frontend -> varType is relevant for this
    value_1: string, //only relevant if firstValueDiff == true
    integration_values:IntegrationValue[]
}

export interface IntegrationValue {
    date:string,
    value:string
}
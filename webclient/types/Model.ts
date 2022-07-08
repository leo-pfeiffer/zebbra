export interface Model {
    _id: string;
    meta: ModelMeta;
    sheets: Sheet[];
}

export interface ModelMeta {
    name: string,
    starting_month:string,
    admins: string[],
    editors: string[],
    viewers: string[],
    workspace: string
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
    val_type: string, // "number", "percentage", "currency" -> how is it displayed?
    editable: boolean, // true, false -> can the user change anything?
    var_type: string, // value, formula, integration
    time_series: boolean, //true or false -> is the value changing over time or not?
    starting_at: number // -> t+startingAt; default = 0
    first_value_diff: boolean //is the first value different?
    value: string, //parsed in the frontend -> varType is relevant for this
    value_1: string, //only relevant if firstValueDiff == true
    integration_values:IntegrationValue[]
}

export interface IntegrationValue {
    date:string,
    value:string
}
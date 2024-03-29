export interface Model {
    _id: string;
    meta: ModelMeta;
    sheets: Sheet[];
    payroll: Payroll;
    starting_balance: number,
    starting_month: string
}

export interface Payroll {
    payroll_values:IntegrationValue[],
    employees:Employee[]
}

export interface Employee {
    _id:string,
    name:string,
    start_date:string,
    end_date:string,
    title:string,
    department:string,
    monthly_salary:number,
    from_integration:boolean,
}

export interface ModelMeta {
    name: string,
    starting_month:string,
    starting_balance:number,
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
    sections: Section[]
}

export interface Section {
    name: string,
    rows: Variable[],
    end_row: Variable
}

export interface Variable {
    _id: string, //required to be able to reference between different variables
    name: string, //e.g. "Churn Rate" -> how is it called?
    val_type: string, // "number", "percentage", "currency" -> how is it displayed?
    editable: boolean, // true, false -> can the user change anything?
    decimal_places: number,
    var_type: string, // value, formula, integration
    time_series: boolean, //true or false -> is the value changing over time or not?
    starting_at: number // -> t+startingAt; default = 0
    first_value_diff: boolean //is the first value different?
    value: string, //parsed in the frontend -> varType is relevant for this
    value_1: string, //only relevant if firstValueDiff == true
    integration_name: string,
    integration_values:IntegrationValue[]
}

export interface IntegrationValue {
    date:string,
    value:string
}
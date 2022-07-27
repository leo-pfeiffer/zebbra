export interface ProfitLoss {
    gross_income: {
        revenue_streams: Row[],
        total: Row
    },
    cost_of_goods_sold: Row,
    gross_margin: Row,
    payroll_cost: Row,
    operating_cost: Row,
    operating_income: Row,
    other_cost: Row,
    net_income: Row
}

export interface Row {
    name:string,
    values:string[]
}
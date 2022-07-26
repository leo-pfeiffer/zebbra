export interface DashboardSeriesElement {
    name: string,
    data: [Number, Number][]
}

export interface DashboardData {
    profit: DashboardSeriesElement[],
    cashBalance: DashboardSeriesElement[],
    revenues: DashboardSeriesElement[],
    costs: DashboardSeriesElement[],
    payrollCosts: DashboardSeriesElement[],
    headcount: DashboardSeriesElement[],
}
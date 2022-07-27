export interface DashboardSeriesElement {
    name: string,
    data: [number, number][]
}

export interface DashboardData {
    profit: DashboardSeriesElement[],
    cashBalance: DashboardSeriesElement[],
    cashBalanceCalc: (startingBalance: number, cashBalance: DashboardSeriesElement[]) => DashboardSeriesElement[],
    revenues: DashboardSeriesElement[],
    costs: DashboardSeriesElement[],
    payrollCosts: DashboardSeriesElement[],
    headcount: DashboardSeriesElement[],
}
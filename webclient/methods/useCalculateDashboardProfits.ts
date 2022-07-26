import {DashboardData} from "~/types/DashboardSeries";
import { Payroll, Sheet } from "~~/types/Model";
import {useCalculateProfitLoss} from "~/methods/useCalculateProfitLoss";


/**
 * Check if a date is between two dates.
 * */
const isDateBetweenDates = function(d1:Date, d2:Date|null, toCheck:Date) {
    if (d2 === null) {
        return d1 <= toCheck
    }
    return (d1 <= toCheck && toCheck <= d2)
}

/**
 * Helper method to convert a string date of format YYYY-MM-DD to a date object
 * */
const stringToDate = function(dateString:string) {
    const dateParts = dateString.split('-');
    return new Date(Number(dateParts[0]), Number(dateParts[1]) - 1, Number(dateParts[2]));
}


export const useCalculateDashboardProfits = (
    revenueState:Sheet, costState:Sheet, payrollState:Payroll, startingMonth:Date, startingBalance:number
) => {

    startingMonth.setDate(1)
    const dates = [startingMonth]
    let currDate = startingMonth
    for (let i = 0; i < 23; i++) {
        const newDate = new Date(currDate);
        newDate.setMonth(currDate.getMonth()+1)
        dates.push(newDate)
        currDate = newDate
    }

    // get data from profit and loss statement
    const profitLoss = useCalculateProfitLoss(revenueState, costState, payrollState)

    // initialize output object
    let dashboardData: DashboardData = {
        profit: [],
        cashBalance: [],
        revenues: [],
        costs: [],
        payrollCosts: [],
        headcount: [],
    }

    // Calculate profit
    dashboardData.profit = [{
        name: "Profits",
        data: dates.map((date, index) => [+date, Number(profitLoss.net_income.values[index])])
    }]
    dates.map((date, index) => [+date, Number(profitLoss.net_income.values[index])])

    // Calculate cash balance
    dashboardData.cashBalance = [{
        name: "Cash Balance",
        data: []
    }]

    let currBalance = startingBalance;
    for (let i = 0; i < dates.length; i++) {
        currBalance += Number(profitLoss.net_income.values[i])
        dashboardData.cashBalance[0].data.push([+dates[i], currBalance])
    }

    // Calculate revenues
    dashboardData.revenues = []
    for (let row of profitLoss.gross_income.revenue_streams) {
        dashboardData.revenues.push(
            {
                name: row.name,
                data: dates.map((date, index) => [+date, Number(row.values[index])])
            }
        )
    }

    // Calculate costs
    dashboardData.costs = [
        {
            name: "Payroll Costs",
            data: dates.map((date, index) => [+date, Number(profitLoss.payroll_cost.values[index])])
        },
        {
            name: "Cost of Goods Sold",
            data: dates.map((date, index) => [+date, Number(profitLoss.cost_of_goods_sold.values[index])])
        },
        {
            name: "Operating Cost",
            data: dates.map((date, index) => [+date, Number(profitLoss.operating_cost.values[index])])
        },
        {
            name: "Other Cost",
            data: dates.map((date, index) => [+date, Number(profitLoss.other_cost.values[index])])
        },
    ]

    // prepare payroll data for further processing
    const actualDepartments = payrollState.employees.map(e => e.department)
    const departments = [...new Set([...actualDepartments, "Other"])]
    const payrollSeries = {}
    const headcountSeries = {}

    // initialize objects
    for (let dep of [...departments]) {
        payrollSeries[dep] = {}
        headcountSeries[dep] = {}
        for (let date of dates) {
            payrollSeries[dep][date] = 0
            headcountSeries[dep][date] = 0
        }
    }

    // aggregate monthly department salary and monthly headcount
    for (let employee of payrollState.employees) {
        for (let date of dates) {
            const end_date = employee.end_date !== null ? stringToDate(employee.end_date) : null
            if (isDateBetweenDates(startingMonth, end_date, date)) {
                const department = employee.department !== null ? employee.department : "Other"
                payrollSeries[department][date] += employee.monthly_salary
                headcountSeries[department][date] += 1
            }
        }
    }

    // Calculate payroll costs
    dashboardData.payrollCosts = []
    for (let dep of departments) {
        dashboardData.payrollCosts.push({
            name: dep,
            data: dates.map((date) => [+date, payrollSeries[dep][date]])
        })
    }

    // Calculate headcount
    dashboardData.headcount = []
    for (let dep of departments) {
        dashboardData.headcount.push({
            name: dep,
            data: dates.map((date) => [+date, headcountSeries[dep][date]])
        })
    }

    return dashboardData
}
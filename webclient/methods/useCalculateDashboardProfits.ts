import {DashboardData, DashboardSeriesElement} from "~/types/DashboardSeries";
import { Payroll, Sheet } from "~~/types/Model";

export const useCalculateDashboardProfits = (revenueState:Sheet, costState:Sheet, payrollState:Payroll) => {

    let dashboardData: DashboardData = {
        profit: [],
        cashBalance: [],
        revenues: [],
        costs: [],
        payrollCosts: [],
        headcount: [],
    }

    dashboardData.profit = [{
        name: "Profits",
        data: [
            [+ new Date(2020, 1, 1), 100],
            [+ new Date(2020, 2, 1), 200],
            [+ new Date(2020, 3, 1), 300],
            [+ new Date(2020, 4, 1), 200],
            [+ new Date(2020, 5, 1), 300],
            [+ new Date(2020, 6, 1), 400],
            [+ new Date(2020, 7, 1), 300],
        ]
    }]

    dashboardData.cashBalance = [{
        name: "Cash Balance",
        data: [
            [+ new Date(2020, 1, 1), 100],
            [+ new Date(2020, 2, 1), 200],
            [+ new Date(2020, 3, 1), 100],
            [+ new Date(2020, 4, 1), 5],
            [+ new Date(2020, 5, 1), -25],
            [+ new Date(2020, 6, 1), -50],
            [+ new Date(2020, 7, 1), -100],
        ]
    }]

    dashboardData.revenues = [{
        name: "Product A",
        data: [
            [+ new Date(2020, 1, 1), 100],
            [+ new Date(2020, 2, 1), 200],
            [+ new Date(2020, 3, 1), 100],
            [+ new Date(2020, 4, 1), 120],
            [+ new Date(2020, 5, 1), 150],
            [+ new Date(2020, 6, 1), 225],
            [+ new Date(2020, 7, 1), 300],
        ]
    }, {
        name: "Product B",
        data: [
            [+ new Date(2020, 1, 1), 50],
            [+ new Date(2020, 2, 1), 130],
            [+ new Date(2020, 3, 1), 110],
            [+ new Date(2020, 4, 1), 70],
            [+ new Date(2020, 5, 1), 75],
            [+ new Date(2020, 6, 1), 100],
            [+ new Date(2020, 7, 1), 150],
        ]
    }]

    dashboardData.costs = [{
        name: "Product A",
        data: [
            [+ new Date(2020, 1, 1), 110],
            [+ new Date(2020, 2, 1), 150],
            [+ new Date(2020, 3, 1), 120],
            [+ new Date(2020, 4, 1), 170],
            [+ new Date(2020, 5, 1), 190],
            [+ new Date(2020, 6, 1), 215],
            [+ new Date(2020, 7, 1), 100],
        ]
    }, {
        name: "Product B",
        data: [
            [+ new Date(2020, 1, 1), 75],
            [+ new Date(2020, 2, 1), 150],
            [+ new Date(2020, 3, 1), 130],
            [+ new Date(2020, 4, 1), 90],
            [+ new Date(2020, 5, 1), 95],
            [+ new Date(2020, 6, 1), 300],
            [+ new Date(2020, 7, 1), 210],
        ]
    }]

    dashboardData.payrollCosts = [{
        name: "Sales",
        data: [
            [+ new Date(2020, 1, 1), 110],
            [+ new Date(2020, 2, 1), 150],
            [+ new Date(2020, 3, 1), 120],
            [+ new Date(2020, 4, 1), 170],
            [+ new Date(2020, 5, 1), 190],
            [+ new Date(2020, 6, 1), 215],
            [+ new Date(2020, 7, 1), 100],
        ]
    }, {
        name: "R&D",
        data: [
            [+ new Date(2020, 1, 1), 75],
            [+ new Date(2020, 2, 1), 150],
            [+ new Date(2020, 3, 1), 130],
            [+ new Date(2020, 4, 1), 90],
            [+ new Date(2020, 5, 1), 95],
            [+ new Date(2020, 6, 1), 300],
            [+ new Date(2020, 7, 1), 210],
        ]
    }]

    dashboardData.headcount = [{
        name: "Sales",
        data: [
            [+ new Date(2020, 1, 1), 20],
            [+ new Date(2020, 2, 1), 30],
            [+ new Date(2020, 3, 1), 40],
            [+ new Date(2020, 4, 1), 35],
            [+ new Date(2020, 5, 1), 25],
            [+ new Date(2020, 6, 1), 25],
            [+ new Date(2020, 7, 1), 30],
        ]
    }, {
        name: "R&D",
        data: [
            [+ new Date(2020, 1, 1), 25],
            [+ new Date(2020, 2, 1), 15],
            [+ new Date(2020, 3, 1), 20],
            [+ new Date(2020, 4, 1), 25],
            [+ new Date(2020, 5, 1), 30],
            [+ new Date(2020, 6, 1), 25],
            [+ new Date(2020, 7, 1), 30],
        ]
    }]

    return dashboardData
}
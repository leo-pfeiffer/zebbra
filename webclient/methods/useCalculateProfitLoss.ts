import { Payroll, Sheet, Variable } from "~~/types/Model";
import { ProfitLoss, Row } from "~~/types/ProfitLoss";
import { useMathParser } from "./useMathParser";
import { useFormulaParser } from "./useFormulaParser";

export const useCalculateProfitLoss = (revenueState:Sheet, costState:Sheet, payrollState:Payroll) => {

    const emptyRow:Row = {
        name: "",
        values: []
    }
    
    var profitLoss: ProfitLoss = {
        gross_income: {
            revenue_streams: [],
            total: {...emptyRow}
        },
        cost_of_goods_sold: {...emptyRow},
        gross_margin: {...emptyRow},
        payroll_cost: {...emptyRow},
        operating_cost: {...emptyRow},
        operating_income: {...emptyRow},
        other_cost: {...emptyRow},
        net_income: {...emptyRow}
    }

    //pushing the endRowValues of each section into gross income
    for (let i = 0; i < revenueState.sections.length; i++) {
        var sectionVariables: Variable[] = [...revenueState.sections[i].rows];
        var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(revenueState.assumptions.concat(sectionVariables.concat(revenueState.sections[i].end_row)));
        
        valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + revenueState.assumptions.length);
        
        var rowStorage:Row = {
            name: "",
            values: []
        };
        rowStorage.name = revenueState.sections[i].name;
        rowStorage.values = valuesOfVariablesAndEndRow[0];
        profitLoss.gross_income.revenue_streams.push(rowStorage);
    };

    //calculating the total gross income
    var totalGrossIncome:string[] = [];
    for (let i=0; i < 24; i++) {
        var calcString:string = "";
        for(let j=0; j < profitLoss.gross_income.revenue_streams.length; j++) {
            if(calcString.length === 0) {
                calcString = calcString + profitLoss.gross_income.revenue_streams[j].values[i];
            } else {
                calcString = calcString + "+" + profitLoss.gross_income.revenue_streams[j].values[i];
            }
        }

        var output:string;
        try {
            output = useMathParser(calcString).toString();
        } catch(e) {
            output = "#REF!"
        }
        totalGrossIncome.push(output);
    }
    profitLoss.gross_income.total.name = "Gross Income";
    profitLoss.gross_income.total.values = totalGrossIncome;

    //getting the all the cost sections and storing them
    var costRowStorage: Row[] = [];
    for (let i = 0; i < costState.sections.length; i++) {
        var sectionVariables: Variable[] = [...costState.sections[i].rows];
        var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(costState.assumptions.concat(sectionVariables.concat(costState.sections[i].end_row)));
        
        valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + costState.assumptions.length);
        
        var rowStorage:Row = {
            name: "",
            values: []
        };
        rowStorage.name = costState.sections[i].name;
        rowStorage.values = valuesOfVariablesAndEndRow[0];
        costRowStorage.push(rowStorage);
    };

    if(costRowStorage[0]) {
        profitLoss.cost_of_goods_sold = costRowStorage[0];
    }

    if(costRowStorage[1]) {
        profitLoss.operating_cost = costRowStorage[1];
    }

    if(costRowStorage[2]) {
        profitLoss.other_cost = costRowStorage[2];
    }

    //getting the payroll costs
    var payrollCost:string[] = [];
    for(let i=0; i < payrollState.payroll_values.length; i++) {
        payrollCost.push(payrollState.payroll_values[i].value);
    }
    profitLoss.payroll_cost.name = "Payroll Cost";
    profitLoss.payroll_cost.values = payrollCost;
    
    //calculating the gross margin
    var grossMargin:string[] = [];
    for (let i=0; i < 24; i++) {
        var calcString:string = profitLoss.gross_income.total.values[i] + "-" + profitLoss.cost_of_goods_sold.values[i];
        var output:string;
        try {
            output = useMathParser(calcString).toString();
        } catch(e) {
            output = "#REF!"
        }
        grossMargin.push(output);
    }
    profitLoss.gross_margin.name = "Gross Margin";
    profitLoss.gross_margin.values = grossMargin;

    //calculating the operating income
    var operatingIncome:string[] = [];
    for (let i=0; i < 24; i++) {
        var calcString:string = profitLoss.gross_margin.values[i] + "-" + profitLoss.operating_cost.values[i] + "-" + profitLoss.payroll_cost.values[i];
        var output:string;
        try {
            output = useMathParser(calcString).toString();
        } catch(e) {
            output = "#REF!"
        }
        operatingIncome.push(output);
    }
    profitLoss.operating_income.name = "Operating Income";
    profitLoss.operating_income.values = operatingIncome;

    //calculating the net income
    var netIncome:string[] = [];
    for (let i=0; i < 24; i++) {
        var calcString:string = profitLoss.operating_income.values[i] + "-" + profitLoss.other_cost.values[i];
        var output:string;
        try {
            output = useMathParser(calcString).toString();
        } catch(e) {
            output = "#REF!"
        }
        netIncome.push(output);
    }
    profitLoss.net_income.name = "Net Income";
    profitLoss.net_income.values = netIncome;
    
    return profitLoss;

}
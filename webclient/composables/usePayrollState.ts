import { Payroll } from "~~/types/Model"

var payrollState: Payroll;

export const usePayrollState = () => useState<Payroll>('payrollState', () => payrollState);
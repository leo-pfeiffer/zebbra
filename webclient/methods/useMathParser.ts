import * as MathParser from 'math-expression-evaluator';

//takes a mathematical operation as a string and returns the result
export const useMathParser = (input:string) => {
    return MathParser.eval(input);
}
<template>
    <div class="flex">
        <div class="flex">
            <div @dblclick="addErrormessage()"
                :class="{ 'border-t border-r border-zinc-300': hierarchy === 'low', 'bg-zinc-50 border-t border-zinc-300': hierarchy === 'med', 'bg-zinc-200 font-medium border-t-2 border-t-zinc-400 border-b border-zinc-400 border-b-zinc-300': hierarchy === 'high', 'text-red-600': isNegative(value) }"
                class="tabular-nums text-xs py-2 px-2 min-w-[90px] max-w-[90px] h-full text-right overflow-hidden overflow-x-scroll no-scrollbar"
                v-for="value in computedValues(values)">{{ value }}</div>
        </div>
        <SheetErrorMessages @close="errorMessages.splice(index, 1)" :errorMessages="errorMessages"></SheetErrorMessages>
    </div>
</template>

<script lang="ts">

export default {
    data() {
        return {
            errorMessages: [],
            errorMessage: "Single cells can't be changed. Double click on the values field of the row to define a formula or a constant value."
        }
    },
    props: {
        values: Object as () => string[],
        roundTo: Number,
        hierarchy: String
    },
    methods: {
        closeErrorMessage(index: number) {
            this.errorMessages.splice(index, 1)
        },
        async addErrormessage() {

            this.errorMessages.push(this.errorMessage);

            setTimeout(() => {
                this.closeErrorMessage(this.errorMessages.length - 1);
            }, 3000)

        },
        computedValues(input: string[]) {
            var output: string[] = [];

            for (let i = 0; i < input.length; i++) {
                var value: string = input[i];
                if (value === null) {
                    output.push("–"); //error handling for null values (could be coming from integration)
                } else if (value === "#REF!" || value === "–") {
                    output.push(value);
                } else if (value.includes(".")) {
                    var splittedValue = value.split(".");

                    var valueWithDecimals: string;

                    if (splittedValue[1].length > this.roundTo) {
                        valueWithDecimals = (+value).toFixed(this.roundTo).toString();
                    } else if (splittedValue[1].length < this.roundTo) {
                        valueWithDecimals = value;
                        for (let i = 0; i < (this.roundTo - splittedValue[1].length); i++) {
                            valueWithDecimals = valueWithDecimals + "0"
                        }
                    } else {
                        valueWithDecimals = value;
                    }
                    output.push(valueWithDecimals);
                } else {
                    if (this.roundTo > 0) {
                        let valueToPush: string = value + "."
                        for (let i = 0; i < this.roundTo; i++) {
                            valueToPush = valueToPush + "0";
                        }
                        output.push(valueToPush);
                    } else {
                        output.push(value);
                    }
                }
            }
            return output;
        },
        isNegative(value: string) {
            if (value[0] === "-") {
                return true;
            } else {
                return false;
            }
        }
    }
}
</script>
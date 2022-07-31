<template>
    <div class="flex">
        <div class="flex">
            <div :class="{'border-t border-r border-zinc-300': hierarchy === 'low', 'bg-zinc-50 border-t border-zinc-300': hierarchy === 'med', 'bg-zinc-200 font-medium border-t-2 border-t-zinc-400 border-b border-zinc-400 border-b-zinc-300': hierarchy === 'high', 'text-red-600': isNegative(value)}" class="tabular-nums text-xs py-2 px-2 min-w-[90px] max-w-[90px] h-full text-right overflow-hidden overflow-x-scroll no-scrollbar" v-for="value in computedValues(values)">{{value}}</div>
        </div>
    </div>
</template>

<script lang="ts">

export default {
    data() {
        return {
        }
    },
    props: {
        values: Object as () => string[],
        roundTo: Number,
        hierarchy: String
    },
    methods: {
        computedValues(input:string[]) {
            var output:string[] = [];

            for(let i=0; i < input.length; i++) {
                var value:string = input[i];
                if(value === null) {
                    output.push("–"); //error handling for null values (could be coming from integration)
                } else if(value.includes(".")) {
                    var splittedValue = value.split(".");

                    var valueWithDecimals;
                    
                    if(splittedValue[1].length > this.roundTo) {
                        valueWithDecimals = (+value).toFixed(this.roundTo);
                    } else {
                        valueWithDecimals = value;
                    }
                    output.push(valueWithDecimals);
                } else {
                    output.push(value);
                }
            }
            return output;
        },
        isNegative(value:string) {
            if(value[0] === "-") {
                return true;
            } else {
                return false;
            }
        }
    }
}
</script>
<template>
    <div class="flex">
        <div class="flex">
            <div :class="{'text-zinc-700 font-medium bg-zinc-50 border-b border-zinc-300': isFinalRow}" class="tabular-nums text-xs py-2 px-2 border-t border-r border-zinc-300 min-w-[75px] max-w-[75px] h-full text-right overflow-hidden overflow-x-scroll" v-for="value in computedValues(values)">{{value}}</div>
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
        isFinalRow: Boolean
    },
    methods: {
        computedValues(input:string[]) {
            var output:string[] = [];

            for(let i=0; i < input.length; i++) {
                var value:string = input[i];
                if(value.includes(".")) {
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
        }
    }
}
</script>
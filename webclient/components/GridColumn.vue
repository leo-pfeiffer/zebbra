<template>
    <div class="flex">
        <div class="flex">
            <div class="text-xs py-2 px-2 border-t border-r border-zinc-300 min-w-[75px] max-w-[75px] h-full text-right" v-for="value in values">{{value}}</div>
        </div>
    </div>
</template>

<script lang="ts">

import { Variable } from "~~/types/Model"

export default {
    data() {
        return {
        }
    },
    props: {
        assumption: Object as () => Variable,
    },
    computed: {
        values() {
            var returnArray = [];
            if(!this.assumption.timeSeries) {
                for(let i=0; i < 24; i++) {
                    returnArray.push("–");
                }
                return returnArray;
            } else {
                //returnArray = useFormulaParser(this.assumption);
                return returnArray;
            }
            
        }
    },
}

</script>
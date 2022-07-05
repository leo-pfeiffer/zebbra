<template>
    <div>
        <div class="flex">
            <div class="text-xs py-2 pl-5 pr-2 border-t border-x border-zinc-300 min-w-[250px] max-w-[250px]">
                <span v-show="(valType === 'currency')" class="mr-2 text-green-600"><i class="bi bi-currency-dollar"></i></span>
                <span v-show="(valType === 'percentage')" class="mr-2 text-amber-600"><i class="bi bi-percent"></i></span>
                <span v-show="(valType === 'number')" class="mr-2 text-zinc-500"><i class="bi bi-hash"></i></span>
                {{ assumption.name }}
            </div>
            <form @submit="updateValue" class="h-full w-full">
                <div v-if="selected" 
                    class="absolute text-xs border-zinc-300 min-w-[125px] max-w-[125px] text-right">
                    <input autofocus @focusout="toggleInput" @keydown.esc="toggleInput" v-model="inputValue" class=" border-t w-full py-2 px-2 font-mono font-sm focus:rounded-none focus:outline-green-600 border-r-2 border-zinc-300" type=text>
                </div>
                <div v-else 
                    class="text-xs border-t border-r border-zinc-300 min-w-[125px] max-w-[125px] h-full text-right">
                    <div @dblclick="toggleInput" class="h-full text-right text-xs py-2 px-2 border-r-2 border-zinc-300">{{ outputValue }}</div>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts">

import { Variable } from "~~/types/Model"

export default {
    data() {
        return {
            inputValue: "",
            valType: "",
            selected: false
        }
    },
    props: {
        assumption: Object as () => Variable,
        assumptionIndex: Number
    },
    methods: {
        toggleInput() {
            if(!this.selected) {
                this.selected = true;
            } else {
                this.selected = false;
            }
        },
        async updateValue(){
            console.log("update value");

            const model = useDummyModelState();
            const sheet = model.value.sheets[0].assumptions[this.assumptionIndex].value = this.inputValue.toString();


            /* const sheet = useSheetState();
            sheet.value.sheets[0].assumptions[0].data.column1 = this.inputValue;

            const route = useRoute()

            const requestBody = sheet.value.sheets;
            console.log(requestBody);

            const updateModel = await useFetchAuth(
            'http://localhost:8000/model/sheet/update/data',{ method: 'POST',
            params: {
                model_id: route.params.modelId,
                name: sheet.value.sheets[0].meta.name
            },
            body: { requestBody }
            }).then((data) => {
                console.log(data);
            }).catch((error) => {
            console.log(error);
            });

            sheet.value = await updateSheetState(route.params.modelId); */

        }
    },
    beforeMount() {
        this.inputValue = this.assumption.value;
        this.valType = this.assumption.valType;
    },
    computed: {
        outputValue(){
            return this.inputValue;
        }
    }
}

</script>
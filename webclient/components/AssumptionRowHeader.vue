<script setup lang="ts">

const route = useRoute();

</script>
<template>
    <div>
        <div class="flex">
                <div class="group text-xs py-2 pl-5 pr-2 border-t border-x border-zinc-300 min-w-[250px] max-w-[250px]">
                    <span v-show="(valType === 'currency')" class="mr-2 text-green-600"><i
                            class="bi bi-currency-dollar"></i></span>
                    <span v-show="(valType === 'percentage')" class="mr-2 text-amber-600"><i
                            class="bi bi-percent"></i></span>
                    <span v-show="(valType === 'number')" class="mr-2 text-zinc-500"><i class="bi bi-hash"></i></span>
                    <span v-if="!nameChangeSelected" @dblclick="toggleNameChange">{{ assumption.name }}</span>
                    <span v-else><input autofocus @keydown.enter="updateName" v-model="newName" class="bg-zinc-100/0 focus:border-b border-sky-600 focus:outline-none placeholder:text-zinc-500" type="text"
                            placeholder="Click to set a name"></span>
                    <span class="text-xs float-right hidden group-hover:block"><button type="button" @click="deleteVariable" class="mr-1"><i class="bi bi-trash3 text-zinc-500"></i></button></span>
                </div>
            <div class="h-full w-full">
                <div v-if="!valueInputSelected" class="text-xs border-t border-r border-zinc-300 min-w-[125px] max-w-[125px] h-full w-full text-right">
                    <div @dblclick="toggleInput" class="h-full text-right text-xs py-2 px-2 border-r-2 border-zinc-300">
                        {{ outputValue }}</div>
                </div>
                <div v-else class="text-xs border-zinc-300 min-w-[125px] max-w-[125px] h-full w-full text-right">
                    <input v-show="valueInputSelected" autofocus @keydown.enter="updateValue" @keydown.esc="toggleInput" v-model="inputValue"
                        class="border-t w-full py-2 px-2 font-mono font-sm focus:rounded-none focus:outline-green-600 border-r-2 border-zinc-300"
                        type=text>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">

import { Variable } from "~~/types/Model"

export default {
    data() {
        return {
            inputValue: "",
            newName: "",
            valType: "",
            valueInputSelected: false,
            nameChangeSelected: false
        }
    },
    props: {
        assumption: Object as () => Variable,
        assumptionIndex: Number
    },
    methods: {
        toggleNameChange() {
            if (!this.nameChangeSelected) {
                this.nameChangeSelected = true;
            } else {
                this.nameChangeSelected = false;
            }
        },
        toggleInput() {
            if (!this.valueInputSelected) {
                this.valueInputSelected = true;
            } else {
                this.valueInputSelected = false;
            }
        },
        async updateValue() {
            //todo: proper error handling
            if(this.inputValue.length > 0) {
                const sheet = useRevenueState();
                sheet.value.assumptions[this.assumptionIndex].value = this.inputValue.toString();
                try {
                    await updateRevenueState(this.route.params.modelId, sheet.value);
                    this.toggleInput();
                } catch (e) {
                    console.log(e);
                } finally {
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await getRevenueState(this.route.params.modelId);
                    const sheet = useRevenueState();
                    if(!(actualSheet.assumptions[this.assumptionIndex].value === sheet.value.assumptions[this.assumptionIndex].value)) {
                        sheet.value = actualSheet;
                    }
                }
            } else {
                //todo:throw error
            }
        },
        async updateName() {

            //todo: proper error handling
            if (this.newName.length > 0) {
                const sheet = useRevenueState();
                sheet.value.assumptions[this.assumptionIndex].name = this.newName;
                try {
                    await updateRevenueState(this.route.params.modelId, sheet.value);
                    this.toggleNameChange();
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await getRevenueState(this.route.params.modelId);
                    const sheet = useRevenueState();
                    if(!(actualSheet.assumptions[this.assumptionIndex].name === sheet.value.assumptions[this.assumptionIndex].name)) {
                        sheet.value = actualSheet;
                    }
                }
            }
        },
        async deleteVariable() {
            //first directly change the state
            const sheet = useRevenueState();
            sheet.value.assumptions.splice(this.assumptionIndex, 1);
            const assumptionValuesArrayState = useState<string[][]>('assumptionValues');
            assumptionValuesArrayState.value.splice(this.assumptionIndex, 1);
            
            //then update the backend
            try {
                await updateRevenueState(this.route.params.modelId, sheet.value);
            } catch(e) {
                console.log(e) //todo: throw error message
            } finally {
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await getRevenueState(this.route.params.modelId);
                const sheet = useRevenueState();
                if(!(actualSheet.assumptions.length === sheet.value.assumptions.length)) {
                    sheet.value = actualSheet;
                    const assumptionValuesArrayState = useState<string[][]>('assumptionValues');
                    var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(actualSheet.assumptions);
                    let index = assumptionValuesArray.length - 1;
                    assumptionValuesArrayState.value.push(assumptionValuesArray[index])
                }
            }
        }
    },
    beforeMount() {
        if (this.assumption.value === "" || this.assumption.value === undefined) {
            this.inputValue = "–"
        } else {
            this.inputValue = this.assumption.value;
        }
        this.valType = this.assumption.val_type;

        if (this.assumption.name === "" || this.assumption.value === undefined) {
            this.nameChangeSelected = true;
        }
    },
    computed: {
        outputValue() {
            return this.inputValue;
            //todo: display calculated number or "formula sign"
        }
    }
}

</script>
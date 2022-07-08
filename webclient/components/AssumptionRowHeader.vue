<script setup lang="ts">

const route = useRoute();

</script>
<template>
    <div>
        <div class="flex">
                <div class="group text-xs py-2 pl-5 pr-2 border-t border-x border-zinc-300 min-w-[250px] max-w-[250px] hover:bg-zinc-50">
                    <span v-show="(valType === 'currency')" class="mr-2 text-green-600"><i
                            class="bi bi-currency-dollar"></i></span>
                    <span v-show="(valType === 'percentage')" class="mr-2 text-amber-600"><i
                            class="bi bi-percent"></i></span>
                    <span v-show="(valType === 'number')" class="mr-2 text-zinc-500"><i class="bi bi-hash"></i></span>
                    <span v-if="!nameChangeSelected" @dblclick="toggleNameChange">{{ assumption.name }}</span>
                    <span v-else><input autofocus @keydown.enter="updateName" v-model="newName" class="bg-zinc-100/0 focus:border-b border-sky-600 focus:outline-none placeholder:text-zinc-500" type="text"
                            placeholder="Change variable name"></span>
                    <span class="text-xs float-right hidden group-hover:block"><button type="button" @click="toggleDeleteModal" class="mr-1"><i class="bi bi-x-lg text-zinc-500 shadow hover:text-zinc-700"></i></button></span>
                </div>
            <div class="h-full w-full">
                <div v-if="!valueInputSelected" class="text-xs border-t border-r border-zinc-300 min-w-[125px] max-w-[125px] h-full w-full text-right">
                    <div @dblclick="toggleInput" class="h-full text-right text-xs py-2 px-2 border-r-2 border-zinc-300">
                        {{ outputValue }}</div>
                </div>
                <div v-else class="absolute text-xs border-zinc-300 min-w-[200px] max-w-[200px] h-full w-full text-right">
                    <input v-show="valueInputSelected" autofocus @keydown.enter="updateValue" @keydown.esc="toggleInput" v-model="inputValue"
                        class="border-t w-full py-2 px-2 font-mono font-sm focus:rounded-none focus:outline-green-600 border-r-2 border-zinc-300"
                        type=text>
                </div>
            </div>
        </div>
        <Teleport to="body">

            <div v-show="deleteModalOpen" class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
              <div>
                  <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to delete this variable?</h3>
              </div>
              <p class="text-zinc-500 text-xs mb-3">Deleting <b>{{assumption.name}}</b> cannot be undone.</p>
              <div class="float-right">
                <button
                  class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                  @click="toggleDeleteModal">Cancel</button>
                <button class="ml-2 bg-red-600  drop-shadow-sm
                            shadow-zinc-50 text-xs font-medium px-2 py-1 
                            border border-red-500 rounded text-neutral-100" @click="deleteVariable">Delete</button>
              </div>
            </div>
            <div v-show="deleteModalOpen" @click="toggleDeleteModal"
              class="fixed top-0 left-0 w-[100vw] h-[100vh] z-40 bg-zinc-100/50">
            </div>
          </div>

        </Teleport>
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
            nameChangeSelected: false,
            deleteModalOpen: false
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
            this.toggleDeleteModal();
        },
        toggleDeleteModal() {
            if (this.deleteModalOpen === false) {
                this.deleteModalOpen = true;
            } else {
                this.deleteModalOpen = false;
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
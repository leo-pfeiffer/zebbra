<script setup lang="ts">

const route = useRoute();

</script>
<template>
    <div class="">
        <div class="flex">
            <div
                class="relative group text-xs py-2 pl-5 pr-2 border-t border-x border-zinc-300 min-w-[250px] max-w-[250px] hover:bg-zinc-50">
                <span v-show="(valType === 'currency')" class="mr-2 text-green-600"><i
                        class="bi bi-currency-dollar"></i></span>
                <span v-show="(valType === 'percentage')" class="mr-2 text-amber-600"><i
                        class="bi bi-percent"></i></span>
                <span v-show="(valType === 'number')" class="mr-2 text-zinc-500"><i class="bi bi-hash"></i></span>
                <span v-if="!nameChangeSelected" @dblclick="toggleNameChange">{{ assumption.name }}</span>
                <span v-else><input ref="name" @keydown.enter="updateName" @keydown.esc="toggleNameChange"
                        v-model="newName"
                        class="bg-zinc-100/0 focus:border-b border-sky-600 focus:outline-none placeholder:text-zinc-500"
                        type="text" placeholder="Change variable name"></span>
                <span class="text-[10px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleDeleteModal" class="mr-1"><i title="Delete variable"
                            class="bi bi-x-lg text-zinc-500 hover:text-zinc-700"></i></button></span>
                <span class="text-[9px] float-right hidden group-hover:block"><button type="button" @click=""
                        class="mr-3"><i title="Take value from integration"
                            class="bi bi-server text-zinc-500 hover:text-zinc-700"></i></button></span>
                <span class="text-[9px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleSettings" class="mr-3"><i title="Variable settings"
                            class="bi bi-gear-fill text-zinc-500 hover:text-zinc-700"></i></button></span>
                <div v-show="settingsOpen"
                    class="z-50 absolute p-3 border rounded shadow-md text-xs border-zinc-300 bg-white top-0 right-0 translate-x-36 -translate-y-1.5 text-[11px] w-[200px]">
                    <div class="text-zinc-900 font-medium mb-2">Variable Type</div>
                    <div class="grid grid-rows-2 grid-flow-col gap-x-1 gap-y-3 mb-3">
                        <div>
                            <input v-model="valType" :checked="(valType == 'number')" :id="'number' + assumptionIndex"
                                type="radio" value="number" :name="'variable-type-select' + assumptionIndex"
                                class="hidden peer">
                            <label :for="'number' + assumptionIndex"
                                class="px-1.5 py-0.5 bg-zinc-100 border border-zinc-300 text-zinc-700 rounded peer-checked:text-white peer-checked:bg-sky-600 peer-checked:border-sky-500"><i
                                    class="bi bi-hash mr-1"></i>Number</label>
                        </div>
                        <div>
                            <input v-model="valType" :checked="(valType == 'currency')"
                                :id="'currency' + assumptionIndex" type="radio" value="currency"
                                :name="'variable-type-select' + assumptionIndex" class="hidden peer">
                            <label :for="'currency' + assumptionIndex"
                                class="px-1.5 py-0.5 bg-zinc-100 border border-zinc-300 text-zinc-700 rounded peer-checked:text-white peer-checked:bg-sky-600 peer-checked:border-sky-500"><i
                                    class="bi bi-currency-dollar mr-1"></i>Currency</label>
                        </div>
                        <div>
                            <input v-model="valType" :checked="(valType == 'percentage')"
                                :id="'percentage' + assumptionIndex" type="radio" value="percentage"
                                :name="'variable-type-select' + assumptionIndex" class="hidden peer">
                            <label :for="'percentage' + assumptionIndex"
                                class="px-1.5 py-0.5 bg-zinc-100 border border-zinc-300 text-zinc-700 rounded peer-checked:text-white peer-checked:bg-sky-600 peer-checked:border-sky-500"><i
                                    class="bi bi-percent mr-1"></i>Percentage</label>
                        </div>
                    </div>
                    <div class="text-zinc-900 font-medium mb-2">Custom starting value</div>
                    <div class="mb-3">
                        <input v-model="value1" :id="'value1-input-' + assumptionIndex" type="text"
                            class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                    </div>
                    <div class="text-zinc-900 font-medium mb-2">Starting at</div>
                    <div class="mb-3 flex justify-start align-middle">
                        <div class="w-3/5">First month plus:</div>
                        <div class="w-2/5"><input v-model="startingAt" :id="'starting-at-' + assumptionIndex" min="0"
                                type="number"
                                class="border-zinc-300 border rounded font-mono w-16 float-right px-2 py-1"></div>
                    </div>
                    <div class="flex justify-end w-full">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-[12px] px-1.5 py-0.5 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleSettings">Cancel</button>
                        <button class="ml-2 bg-sky-600  drop-shadow-sm
                                shadow-zinc-50 text-xs px-1.5 py-0.5 font-medium
                                border border-sky-500 rounded text-neutral-100" @click="updateSettings">Update</button>
                    </div>
                </div>
            </div>
            <div class="h-full w-full">
                <div v-if="!valueInputSelected"
                    class="text-xs border-t border-r border-zinc-300 min-w-[125px] max-w-[125px] h-full w-full text-right">
                    <div @dblclick="toggleInput" class="h-full text-right text-xs py-2 px-2 border-r-2 border-zinc-300">
                        <span class="bg-white">{{ outputValue }}</span>
                    </div>
                </div>
                <div v-else
                    class="absolute text-xs border-zinc-300 min-w-[200px] max-w-[200px] h-full w-full text-right">
                    <input v-show="valueInputSelected" autofocus @keydown.enter="updateValue" @keydown.esc="toggleInput"
                        v-model="inputValue"
                        class="border-t w-full py-2 px-2 font-mono font-sm focus:rounded-none focus:outline-green-600 border-r-2 border-zinc-300"
                        type=text>
                </div>
            </div>
        </div>
        <Teleport to="body">
            <div v-show="deleteModalOpen" class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
                <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                    <div>
                        <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to delete this variable?
                        </h3>
                    </div>
                    <p class="text-zinc-500 text-xs mb-3">Deleting <b>{{ assumption.name }}</b> cannot be undone.</p>
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
            valueInputSelected: false,
            nameChangeSelected: false,
            settingsOpen: false,
            valType: "",
            value1: undefined,
            startingAt: 0,
            deleteModalOpen: false
        }
    },
    props: {
        assumption: Object as () => Variable,
        assumptionIndex: Number,
        timeSeriesMap: Map
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
        toggleSettings() {
            if (!this.settingsOpen) {
                this.settingsOpen = true;
            } else {
                this.settingsOpen = false;
                this.valType = this.assumption.val_type;
                this.value1 = this.assumption.value_1;
                this.startingAt = this.assumption.starting_at;
            }
        },
        isTimeSeries(inputValue: string) {
            if (inputValue.includes("$")) {
                return true;
            } else if (inputValue.includes("#") && !inputValue.includes("$")) {

                //create an array with all the refs in a variable string
                var refsArray: string[] = [];

                for (let i = 0; i < inputValue.length; i++) {
                    let char = inputValue[i];
                    if (char === "#") {
                        var ref: string = ""; //empty string to store id (ie number after the #)
                        var counter = 1;
                        //only getting the numerical because only the ids are needed not the point in time (e.g. t-1)
                        while (useFormulaParser().charIsNumerical(inputValue[i + counter]) && (inputValue[i + counter] != undefined)) {
                            ref = ref + inputValue[i + counter];
                            counter++;
                            if ((i + counter >= inputValue.length)) {
                                break;
                            }
                        }
                        refsArray.push(ref);
                        i = i + counter - 1;
                    }
                }

                //for every ref check timeSeriesMap and return true if one is timeseries
                for (let i = 0; i < refsArray.length; i++) {
                    if (this.timeSeriesMap.get(refsArray[i])) {
                        return true;
                    }
                }

                return false;

            } else {
                return false;
            }
        },
        async updateValue() {
            if (this.inputValue.length > 0) {
                const sheet = useRevenueState();
                sheet.value.assumptions[this.assumptionIndex].time_series = this.isTimeSeries(this.inputValue);
                sheet.value.assumptions[this.assumptionIndex].value = this.inputValue.toString();
                if (this.inputValue.includes("+") || this.inputValue.includes("-") || this.inputValue.includes("*") || this.inputValue.includes("/") || this.inputValue.includes("–")) {
                    sheet.value.assumptions[this.assumptionIndex].var_type = "formula";
                } else {
                    sheet.value.assumptions[this.assumptionIndex].var_type = "value";
                }

                try {
                    //update RevenueState
                    await updateRevenueState(this.route.params.modelId, sheet.value);
                    //Update sheet values valuesToDisplay
                    const revenues = useRevenueState();
                    const assumptionValuesArrayState = useState<string[][]>('assumptionValues');
                    var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions);;
                    assumptionValuesArrayState.value[this.assumptionIndex] = assumptionValuesArray[this.assumptionIndex];
                    this.toggleInput();
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await getRevenueState(this.route.params.modelId);
                    const sheet = useRevenueState();
                    if (!(actualSheet.assumptions[this.assumptionIndex].value === sheet.value.assumptions[this.assumptionIndex].value)) {
                        sheet.value = actualSheet;
                    }
                }
            } else {
                //todo:throw error
            }
        },
        async updateSettings() {

            const sheet = useRevenueState();

            sheet.value.assumptions[this.assumptionIndex].val_type = this.valType;
            sheet.value.assumptions[this.assumptionIndex].value_1 = this.value1;
            sheet.value.assumptions[this.assumptionIndex].first_value_diff = (this.value1 != undefined || this.value1 != "");
            sheet.value.assumptions[this.assumptionIndex].starting_at = this.startingAt;

            try {
                //update RevenueState
                await updateRevenueState(this.route.params.modelId, sheet.value);
                //Update sheet values valuesToDisplay
                const revenues = useRevenueState();
                const assumptionValuesArrayState = useState<string[][]>('assumptionValues');
                var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions);;
                assumptionValuesArrayState.value[this.assumptionIndex] = assumptionValuesArray[this.assumptionIndex];
            } catch (e) {
                console.log(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await getRevenueState(this.route.params.modelId);
                const sheet = useRevenueState();
                if (!(actualSheet.assumptions[this.assumptionIndex].value === sheet.value.assumptions[this.assumptionIndex].value)) {
                    sheet.value = actualSheet;
                }
            }
            this.toggleSettings();
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
                    if (!(actualSheet.assumptions[this.assumptionIndex].name === sheet.value.assumptions[this.assumptionIndex].name)) {
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
            } catch (e) {
                console.log(e) //todo: throw error message
                const actualSheet = await getRevenueState(this.route.params.modelId);
                const sheet = useRevenueState();
                if (!(actualSheet.assumptions.length === sheet.value.assumptions.length)) {
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
        this.value1 = this.assumption.value_1;
        this.startingAt = this.assumption.starting_at;

        if (this.assumption.name === "" || this.assumption.value === undefined) {
            this.nameChangeSelected = true;
        }
    },
    computed: {
        outputValue() {
            try {
                if(this.valType === "number") {
                    var output: string = useMathParser(this.assumption.value).toFixed(2).toString();
                    const splitted: string[] = output.split(".");
                    if (splitted[1] === "00") {
                        return splitted[0];
                    } else {
                        return output;
                    }
                } else if(this.valType === "percentage") {
                    var calc1: string = useMathParser(this.assumption.value).toString();
                    var calc2:string = useMathParser(calc1 + "*100").toFixed(2).toString();
                    const splitted: string[] = calc2.split(".");
                    if (splitted[1] === "00") {
                        return splitted[0] + " %";
                    } else {
                        return calc2  + " %";
                    }
                } else if(this.valType === "currency") {
                    var output: string = useMathParser(this.assumption.value).toFixed(2).toString();
                    const splitted: string[] = output.split(".");
                    if (splitted[1] === "00") {
                        return "$ " + splitted[0];
                    } else {
                        return "$ " + output;
                    }
                }
            } catch (e) {
                if (this.assumption.var_type === "formula") {

                    return "Formula"

                } else if (this.assumption.var_type === "integration") {

                    return "Integration"

                } else {
                    return "!!";
                }
            }
        },
        outputValueIsError() {
            return this.outputValue === "!!"
        }
    }
}

</script>
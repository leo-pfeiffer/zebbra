<template>
    <div class="">
        <div class="flex text-zinc-900">
            <div class="relative group text-xs py-2 border-t border-x border-zinc-300 min-w-[320px] max-w-[320px]"
                :class="{ 'hover:bg-zinc-50 pl-10 pr-2': !isEndRow, 'px-3': isEndRow, 'text-zinc-700 border-zinc-300 bg-zinc-50': hierarchy === 'med' }">
                <span v-show="(valType === 'currency') && !isEndRow" class="mr-3 text-green-600"><i
                        class="bi bi-currency-dollar"></i></span>
                <span v-show="(valType === 'percentage') && !isEndRow" class="mr-3 text-amber-600"><i
                        class="bi bi-percent"></i></span>
                <span v-show="(valType === 'number') && !isEndRow" class="mr-3 text-zinc-500"><i
                        class="bi bi-hash"></i></span>
                <span v-show="isEndRow" class="font-medium">
                    <li class="marker:text-white/0">Total – {{ sectionName }}<InfoToggle :position="'inline'" :text="'Define the total for this section. It will be be added to the P&L.'"></InfoToggle></li>
                </span>
                <span v-show="!isEndRow" class="hover:underline hover:decoration-sky-600" v-if="!nameChangeSelected" @dblclick="toggleNameChange">{{ variable.name
                }}</span>
                <span v-show="!isEndRow" v-else><input :ref="`name-change-${variable._id}`"
                        @keydown.enter="$emit('updateName', newName, variableIndex, sectionIndex); closeNameChange()"
                        @focusout="$emit('updateName', newName, variableIndex, sectionIndex); closeNameChange()"
                        v-model="newName"
                        class="bg-zinc-100/0 focus:border-b border-sky-600 focus:outline-none placeholder:text-zinc-500"
                        type="text" placeholder="Change variable name"></span>
                <span v-show="!isEndRow && !userIsViewer"
                    class="text-[10px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleDeleteModal" class="mr-1"><i title="Delete variable"
                            class="bi bi-x-lg text-zinc-500 hover:text-zinc-700"></i></button></span>
                <span v-show="!isEndRow && showIntegration && !userIsViewer"
                    class="text-[9px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleIntegrationMenu()" class="mr-3"><i title="Take value from integration"
                            class="bi bi-server text-zinc-500 hover:text-zinc-700"></i></button></span>
                <span v-show="!isEndRow && !userIsViewer"
                    class="text-[9px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleSettings" class="mr-3"><i title="Variable settings"
                            class="bi bi-gear-fill text-zinc-500 hover:text-zinc-700"></i></button></span>
                <div v-show="settingsOpen && !isEndRow"
                    class="z-50 absolute p-3 border rounded shadow-md text-xs border-zinc-300 bg-white top-0 right-0 translate-x-36 -translate-y-1.5 text-[11px] w-[200px]">
                    <div class="text-zinc-900 font-medium mb-1">Variable Type</div>
                    <div class="grid grid-rows-2 grid-flow-col gap-x-1 gap-y-3 mb-2">
                        <div>
                            <input v-model="valType" :checked="(valType == 'number')" :id="'number' + variable._id"
                                type="radio" value="number" :name="'variable-type-select' + variable._id"
                                class="hidden peer">
                            <label :for="'number' + variable._id"
                                class="px-1.5 py-0.5 bg-zinc-100 border border-zinc-300 text-zinc-700 rounded peer-checked:text-white peer-checked:bg-sky-600 peer-checked:border-sky-500"><i
                                    class="bi bi-hash mr-1"></i>Number</label>
                        </div>
                        <div>
                            <input v-model="valType" :checked="(valType == 'currency')" :id="'currency' + variable._id"
                                type="radio" value="currency" :name="'variable-type-select' + variable._id"
                                class="hidden peer">
                            <label :for="'currency' + variable._id"
                                class="px-1.5 py-0.5 bg-zinc-100 border border-zinc-300 text-zinc-700 rounded peer-checked:text-white peer-checked:bg-sky-600 peer-checked:border-sky-500"><i
                                    class="bi bi-currency-dollar mr-1"></i>Currency</label>
                        </div>
                        <div>
                            <input v-model="valType" :checked="(valType == 'percentage')"
                                :id="'percentage' + variable._id" type="radio" value="percentage"
                                :name="'variable-type-select' + variable._id" class="hidden peer">
                            <label :for="'percentage' + variable._id"
                                class="px-1.5 py-0.5 bg-zinc-100 border border-zinc-300 text-zinc-700 rounded peer-checked:text-white peer-checked:bg-sky-600 peer-checked:border-sky-500"><i
                                    class="bi bi-percent mr-1"></i>Percentage</label>
                        </div>
                    </div>
                    <div class="text-zinc-900 font-medium mb-1">Rounding Values</div>
                    <div class="mb-2 flex justify-start align-middle">
                        <div class="w-3/5">Decimal places:</div>
                        <div class="w-2/5"><input v-model="decimalPlaces" :id="'decimal-places' + variable._id" min="0"
                                type="number"
                                class="border-zinc-300 border rounded font-mono w-16 float-right px-2 py-1"></div>
                    </div>
                    <div class="text-zinc-900 font-medium mb-1">Custom Starting Value</div>
                    <div class="mb-2">
                        <input v-model="value1" :id="'value1-input-' + variable._id" type="text"
                            class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                    </div>
                    <div class="text-zinc-900 font-medium mb-1">Starting At</div>
                    <div class="mb-2 flex justify-start align-middle">
                        <div class="w-3/5">First month plus:</div>
                        <div class="w-2/5"><input v-model="startingAt" :id="'starting-at-' + variable._id" min="0"
                                type="number"
                                class="border-zinc-300 border rounded font-mono w-16 float-right px-2 py-1"></div>
                    </div>
                    <div class="flex justify-end w-full">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-[12px] px-1.5 py-0.5 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleSettings">Cancel</button>
                        <button class="ml-2 bg-sky-600  drop-shadow-sm
                                shadow-zinc-50 text-xs px-1.5 py-0.5 font-medium
                                border border-sky-500 rounded text-neutral-100"
                            @click="$emit('updateSettings', variableIndex, value1, valType, decimalPlaces, startingAt, sectionIndex); toggleSettings()">Update</button>
                    </div>
                </div>
                <div v-if="showIntegration && !isEndRow" v-show="integrationMenuOpen"
                    class="z-50 absolute p-3 border rounded shadow-md text-xs border-zinc-300 bg-white top-0 right-0 translate-x-36 -translate-y-1.5 text-[11px] w-[200px]">
                    <div class="text-zinc-900 font-medium mb-2">Choose Integration Value</div>
                    <div class="w-full mb-3">
                        <select v-model="integrationSelected"
                            class="w-full border border-zinc-300 rounded bg-white py-2 px-1 text-xs">
                            <option>None</option>
                            <option v-for="integrationValueInfo in possibleIntegrationValues">{{ integrationValueInfo.id
                            }}</option>
                        </select>
                    </div>
                    <div class="text-[11px] p-2 mb-3 border rounded border-sky-300 bg-sky-100 text-sky-700">
                        If available, the integration value overrides the manually defined value. Values which lay in
                        the future will still be covered by the manually entered value.
                    </div>
                    <div class="flex justify-end w-full">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-[12px] px-1.5 py-0.5 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleIntegrationMenu">Cancel</button>
                        <button class="ml-2 bg-sky-600  drop-shadow-sm
                                shadow-zinc-50 text-xs px-1.5 py-0.5 font-medium
                                border border-sky-500 rounded text-neutral-100"
                            @click="$emit('updateIntegration', integrationSelected, timeSeriesMap, variableIndex, sectionIndex); toggleIntegrationMenu()">Set
                            Integration</button>
                    </div>
                </div>
            </div>
            <div class="h-full w-full relative" :class="{'bg-zinc-50': hierarchy === 'med' }">
                <div v-show="!valueInputSelected"
                    class="text-xs relative group border-t border-r border-zinc-300 min-w-[150px] max-w-[150px] h-full w-full text-right">
                    <div @dblclick="toggleInput" :class="{'text-sky-700': variable.var_type === 'value'}"
                        class="float-right h-full min-w-[130px] max-w-[130px] text-right text-xs py-2 px-2 border-r-2 border-zinc-300 tabular-nums truncate overflow-hidden">
                        {{ outputValue }}
                    </div>
                    <div class="absolute top-2 left-2 flex justify-center">
                        <i v-if="variable.var_type === 'formula' && variable.time_series === false" title="Formula"
                            class="text-[10px] text-amber-600/50 bi-calculator-fill"></i>
                        <i v-if="variable.var_type === 'formula' && variable.time_series === true"
                            title="Time-Series Formula" class="text-[10px] text-green-500/50 bi-bar-chart-fill"></i>
                        <i v-else-if="variable.var_type === 'integration'" title="Integration"
                            class="text-[8px] text-sky-700/50 bi bi-server"></i>
                    </div>
                </div>
                <div v-show="valueInputSelected"
                    class="absolute top-0 left-0 text-xs min-w-[500px] max-w-[500px] h-full w-full text-right z-40">
                    <input :ref="`input-${variable._id}`" v-show="valueInputSelected"
                        @keydown.enter="$emit('updateValue', humanReadableInputValue, variable._id, variableSearchMap, timeSeriesMap, variableIndex, sectionIndex); toggleInput()"
                        @keydown.esc="closeInput()" v-model="humanReadableInputValue"
                        class="border-2 -translate-y-[1px] -translate-x-[1px] rounded bg-white w-full py-2 px-2 font-mono font-sm focus:rounded-none focus:outline-green-600 border-r-2 border-zinc-300"
                        type=text>
                    <SearchDropDown v-show="variableSearch.size > 0" :variableSearch="variableSearch"
                        @search-click="addSearchItemToInputValue"></SearchDropDown>
                </div>
            </div>
        </div>
        <Teleport to="body">
            <div v-show="deleteModalOpen"
                class="absolute left-0 top-1/3 w-full flex justify-center align-middle z-50">
                <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                    <div>
                        <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to delete this variable?
                        </h3>
                    </div>
                    <p class="text-zinc-500 text-xs mb-3">Deleting <b>{{ variable.name }}</b> cannot be undone.</p>
                    <div class="float-right">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleDeleteModal">Cancel</button>
                        <button class="ml-2 bg-red-600  drop-shadow-sm
                            shadow-zinc-50 text-xs font-medium px-2 py-1 
                            border border-red-500 rounded text-neutral-100"
                            @click="$emit('deleteVariable', variableIndex, sectionIndex); toggleDeleteModal()">Delete</button>
                    </div>
                </div>
                <div v-show="deleteModalOpen" @click="toggleDeleteModal"
                    class="fixed top-0 left-0 w-[100vw] h-[100vh] z-49 bg-zinc-100/50">
                </div>
            </div>
        </Teleport>
    </div>
</template>

<script lang="ts">

import { Variable } from "~~/types/Model"
import { IntegrationValueInfo } from "~~/types/IntegrationValueInfo"
import { useGetHumanReadableFormula } from "~~/methods/useGetHumanReadableFormula";
import { useMathParser } from "~~/methods/useMathParser";
import { useFormulaParser } from "~~/methods/useFormulaParser";

export default {
    data() {
        return {
            humanReadableInputValue: "",
            newName: "",
            valueInputSelected: false,
            nameChangeSelected: false,
            settingsOpen: false,
            integrationMenuOpen: false,
            valType: "",
            value1: undefined,
            decimalPlaces: 0,
            startingAt: 0,
            integrationSelected: "None",
            deleteModalOpen: false
        }
    },
    props: {
        variable: Object as () => Variable,
        variableIndex: Number,
        timeSeriesMap: Map,
        variableSearchMap: Map,
        sectionIndex: Number,
        sectionName: String,
        isEndRow: Boolean,
        hierarchy: String,
        showIntegration: Boolean,
        possibleIntegrationValues: Object as () => IntegrationValueInfo[],
        userIsViewer: Boolean
    },
    mounted() {

        //set correct humanReadableInputValue to be displayed
        if (this.variable.value === "" || this.variable.value === undefined) {
            this.humanReadableInputValue = "–"
        } else {
            this.humanReadableInputValue = useGetHumanReadableFormula(this.variable.value, this.variable._id, this.variableSearchMap);
        }

        //set correct value_1 to be displayed
        if (this.variable.value_1 != "" || this.variable.value_1 != undefined) {
            this.value1 = this.variable.value_1;
        } else {
            this.value1 = this.variable.value_1;
        }

        this.valType = this.variable.val_type;
        this.decimalPlaces = this.variable.decimal_places;
        this.startingAt = this.variable.starting_at;

        // show name input if name is undefined
        if (this.variable.name === "" || this.variable.value === undefined) {
            this.nameChangeSelected = true;
        }

        //set correct integration value if applicable
        if (this.variable.integration_name === null || this.variable.integration_name === undefined || this.variable.integration_name === "" || this.variable.integration_name === "None") {
            this.integrationSelected = "None";
        } else {
            this.integrationSelected = this.variable.integration_name;
        }

    },
    methods: {
        closeNameChange() {
            if(this.nameChangeSelected && !this.userIsViewer) {
                this.nameChangeSelected = false;
            }
        },
        toggleNameChange() {

            const regex = new RegExp("[+\\*\\(\\)\\[\\$\\#\\,]+")
            
            if (this.userIsViewer) {
                this.nameChangeSelected = false;
            } else {
                if (this.nameChangeSelected && this.newName.length > 0 && !useFormulaParser().charIsNumerical(this.newName[0]) && !this.newName.match(regex) && !this.newName.includes("-") && !this.newName.includes("/") && !this.newName.includes("]")) {
                    this.nameChangeSelected = false;
                } else {
                    this.nameChangeSelected = true;
                }

                if(this.nameChangeSelected) {
                    setTimeout(() => {
                        this.$refs[`name-change-${this.variable._id}`].focus();
                    }, 50)
                }
            }
        },
        closeInput() {
            if(this.valueInputSelected && !this.userIsViewer) {
                this.valueInputSelected = false;
            }

            if (this.variable.value === "" || this.variable.value === undefined) {
                this.humanReadableInputValue = "–"
            } else {
                this.humanReadableInputValue = useGetHumanReadableFormula(this.variable.value, this.variable._id, this.variableSearchMap);
            }
        },
        async toggleInput() {
            if (!this.valueInputSelected && !this.userIsViewer) {
                this.valueInputSelected = true;
            } else {
                this.valueInputSelected = false;
            }

            if(this.valueInputSelected) {
                setTimeout(() => {this.$refs["input-" + this.variable._id].focus();}, 50)
            }
        },
        toggleSettings() {
            if (!this.settingsOpen && !this.userIsViewer) {
                this.settingsOpen = true;
            } else {
                this.settingsOpen = false;
                this.valType = this.variable.val_type;
                this.value1 = this.variable.value_1;
                this.startingAt = this.variable.starting_at;
            }
        },
        toggleIntegrationMenu() {
            if (!this.integrationMenuOpen && !this.userIsViewer) {
                this.integrationMenuOpen = true;
            } else {
                this.integrationMenuOpen = false;
            }
        },
        toggleDeleteModal() {
            if (!this.deleteModalOpen && !this.userIsViewer) {
                this.deleteModalOpen = true;
            } else {
                this.deleteModalOpen = false;
            }
        },
        addSearchItemToInputValue(key: string, searchTimeDiff: string) {

            var lastIndex = this.humanReadableInputValue.length - 1;
            const regex = new RegExp(/[()+*/-]+/);
            while (!regex.test(this.humanReadableInputValue[lastIndex]) && lastIndex >= 0) {
                this.humanReadableInputValue = this.humanReadableInputValue.slice(0, -1);
                lastIndex--;
            }

            this.humanReadableInputValue = this.humanReadableInputValue + this.variableSearchMap.get(key);

            if (searchTimeDiff === "current") {
                this.humanReadableInputValue = this.humanReadableInputValue + "[0]";
            } else if (searchTimeDiff === "previous") {
                this.humanReadableInputValue = this.humanReadableInputValue + "[1]";
            } else if (searchTimeDiff === "T-2") {
                this.humanReadableInputValue = this.humanReadableInputValue + "[2]";
            } else if (searchTimeDiff === "T-12") {
                this.humanReadableInputValue = this.humanReadableInputValue + "[12]";
            }

            this.$refs["input-" + this.variable._id].focus();
            
        }
    },
    computed: {
        variableSearch(): Map<string, string> {
            const splittedInput: string[] = this.humanReadableInputValue.split(/[()+*/-]+/);
            var searchTerm: string = splittedInput[splittedInput.length - 1];
            if (searchTerm[0] === " ") {
                searchTerm = searchTerm.substring(1);
            }
            var searchOutput: Map<string, string> = new Map<string, string>()
            if (this.humanReadableInputValue === "") {
                return searchOutput;
            }
            for (let [key, value] of this.variableSearchMap.entries()) {
                if (value.toLowerCase() === searchTerm.toLowerCase() || value.toLowerCase().includes(searchTerm.toLowerCase())) {
                    searchOutput.set(key, value);
                }
            }
            return searchOutput;
        },
        outputValue() {
            try {
                if (this.valType === "number") {
                    //update
                    var output: string = useMathParser(this.variable.value).toFixed(2).toString();
                    const splitted: string[] = output.split(".");
                    if (splitted[1] === "00") {
                        return splitted[0];
                    } else {
                        return output;
                    }
                } else if (this.valType === "percentage") {
                    var calc1: string = useMathParser(this.variable.value).toString();
                    var calc2: string = useMathParser(calc1 + "*100").toFixed(2).toString();
                    const splitted: string[] = calc2.split(".");
                    if (splitted[1] === "00") {
                        return splitted[0] + "%";
                    } else {
                        return calc2 + "%";
                    }
                } else if (this.valType === "currency") {
                    var output: string = useMathParser(this.variable.value).toFixed(2).toString();
                    const splitted: string[] = output.split(".");
                    if (splitted[1] === "00") {
                        return "$ " + splitted[0];
                    } else {
                        return "$ " + output;
                    }
                }
            } catch (e) {
                return this.humanReadableInputValue;
            }
        }
    }
}

</script>
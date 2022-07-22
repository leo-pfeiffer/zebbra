<script setup lang="ts">

const route = useRoute();

</script>
<template>
    <div class="">
        <div class="flex text-zinc-900">
            <div
                class="relative group hover:bg-zinc-50 text-xs py-2 pl-10 pr-2 border-t border-r-2 border-x border-zinc-300 w-full h-full">
                <span v-if="employee.from_integration" class="mr-3 text-zinc-400 text-[10px]"><i class="bi bi-server"></i></span>
                <span v-else class="mr-3 text-zinc-400"><i class="bi bi-person"></i></span>
                <span class="text-zinc-900">{{ employee.name }}</span>
                <span class="ml-2 text-zinc-400">{{ employee.title }} | {{ employee.department }}</span>
                <span class="text-[10px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleDeleteModal" class="mr-1"><i title="Delete variable"
                            class="bi bi-x-lg text-zinc-500 hover:text-zinc-700"></i></button></span>
                <span class="text-[9px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleSettings" class="mr-3"><i title="Variable settings"
                            class="bi bi-gear-fill text-zinc-500 hover:text-zinc-700"></i></button></span>
                <div v-show="settingsOpen"
                    class="z-50 absolute p-3 border rounded shadow-md text-xs border-zinc-300 bg-white top-0 right-0 translate-x-36 -translate-y-1.5 text-[11px] w-[200px]">
                    <div class="text-zinc-900 font-medium mb-2">Name</div>
                    <div class="grid grid-rows-2 grid-flow-col gap-x-1 gap-y-3 mb-3">
                        todo
                    </div>
                    <div class="flex justify-end w-full">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-[12px] px-1.5 py-0.5 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleSettings">Cancel</button>
                        <button class="ml-2 bg-sky-600  drop-shadow-sm
                                shadow-zinc-50 text-xs px-1.5 py-0.5 font-medium
                                border border-sky-500 rounded text-neutral-100" @click="$emit('updateEmployee'); toggleSettings()">Update</button>
                    </div>
                </div>
            </div>
        </div>
        <Teleport to="body">
            <div v-show="deleteModalOpen" class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
                <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                    <div>
                        <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to delete this employee?
                        </h3>
                    </div>
                    <p class="text-zinc-500 text-xs mb-3">Deleting <b>{{ employee.name }}</b> cannot be undone.</p>
                    <div class="float-right">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleDeleteModal">Cancel</button>
                        <button class="ml-2 bg-red-600  drop-shadow-sm
                            shadow-zinc-50 text-xs font-medium px-2 py-1 
                            border border-red-500 rounded text-neutral-100" @click="$emit('deleteEmployee', employeeIndex); toggleDeleteModal()">Delete</button>
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

import { Employee } from "~~/types/Model"

export default {
    data() {
        return {
            settingsOpen: false,
            deleteModalOpen: false
        }
    },
    props: {
        employee: Object as () => Employee,
        employeeIndex: Number,
    },
    mounted() {

        //todo

    },
    methods: {
        toggleSettings() {
            if (!this.settingsOpen) {
                this.settingsOpen = true;
            } else {
                this.settingsOpen = false;
                this.valType = this.variable.val_type;
                this.value1 = this.variable.value_1;
                this.startingAt = this.variable.starting_at;
            }
        },
        toggleDeleteModal() {
            if (this.deleteModalOpen === false) {
                this.deleteModalOpen = true;
            } else {
                this.deleteModalOpen = false;
            }
        },
    }
}

</script>
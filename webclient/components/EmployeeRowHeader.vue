<script setup lang="ts">

const route = useRoute();

</script>
<template>
    <div class="">
        <div class="flex text-zinc-900">
            <div
                class="relative group hover:bg-zinc-50 text-xs py-2 pl-10 pr-2 border-t border-r-2 border-x border-zinc-300 w-full h-full">
                <span v-if="employee.from_integration" class="mr-3 text-zinc-300 text-[10px] pl-[1px] pr-[2px]"><i class="bi bi-server"></i></span>
                <span v-else class="mr-3 text-green-500"><i class="bi bi-person"></i></span>
                <span class="text-zinc-900">{{ employee.name }}</span>
                <span class="ml-2 text-zinc-400">{{ employee.title }} | {{ employee.department }}</span>
                <span v-if="!employee.from_integration" class="text-[10px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleDeleteModal" class="mr-1"><i title="Delete employee"
                            class="bi bi-x-lg text-zinc-500 hover:text-zinc-700"></i></button></span>
                <span v-if="!employee.from_integration" class="text-[9px] float-right hidden group-hover:block"><button type="button"
                        @click="toggleSettings" class="mr-3"><i title="Variable settings"
                            class="bi bi-gear-fill text-zinc-500 hover:text-zinc-700"></i></button></span>
                <div v-show="settingsOpen"
                    class="z-50 absolute p-3 border rounded shadow-md text-xs border-zinc-300 bg-white top-0 right-0 translate-x-36 -translate-y-1.5 text-[11px] w-[350px]">
                    <div class="columns-2">

                        <div>
                            <div class="text-zinc-900 font-medium mb-1">Name</div>
                            <div class="mb-2">
                                <input v-model="newName" :id="'name-input-' + employee._id" type="text"
                                    class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                            </div>
                            <div class="text-zinc-900 font-medium mb-1">Monthly Salary</div>
                            <div class="mb-2">
                                <input v-model="newSalary" :id="'salary-input-' + employee._id" type="number"
                                    class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                            </div>
                            <div class="text-zinc-900 font-medium mb-1">Start Date</div>
                            <div class="mb-2">
                                <input v-model="newStartDate" :id="'start-date-input-' + employee._id" type="text"
                                    placeholder="YYYY-MM-DD"
                                    class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                            </div>

                        </div>
                        <div>
                            <div class="text-zinc-900 font-medium mb-1">Title</div>
                            <div class="mb-2">
                                <input v-model="newTitle" :id="'position-input-' + employee._id" type="text"
                                    class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                            </div>
                            <div class="text-zinc-900 font-medium mb-1">Department</div>
                            <div class="mb-2">
                                <input v-model="newDepartment" :id="'department-input-' + employee._id" type="text"
                                    class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                            </div>
                                <div class="text-zinc-900 font-medium mb-1">End Date</div>
                            <div class="mb-2">
                                <input v-model="newEndDate" :id="'end-date-input-' + employee._id" type="text"
                                    placeholder="YYYY-MM-DD"
                                    class="border-zinc-300 border rounded w-full font-mono px-2 py-1">
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-end w-full">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-[12px] px-1.5 py-0.5 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleSettings">Cancel</button>
                        <button class="ml-2 bg-sky-600  drop-shadow-sm
                                shadow-zinc-50 text-xs px-1.5 py-0.5 font-medium
                                border border-sky-500 rounded text-neutral-100" @click="$emit('updateEmployee', employeeIndex, newName, newSalary, newTitle, newDepartment, newStartDate, newEndDate); toggleSettings()">Update</button>
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
            deleteModalOpen: false,
            newName: "",
            newTitle: "",
            newDepartment: "",
            newSalary: null,
            newStartDate: "",
            newEndDate: ""
        }
    },
    props: {
        employee: Object as () => Employee,
        employeeIndex: Number,
    },
    mounted() {

        this.newName = this.employee.name;
        this.newTitle = this.employee.title;
        this.newDepartment = this.employee.department;
        this.newSalary = this.employee.monthly_salary;
        this.newStartDate = this.employee.start_date;
        this.newEndDate = this.employee.end_date;

    },
    methods: {
        toggleSettings() {
            if (!this.settingsOpen) {
                this.settingsOpen = true;
            } else {
                this.settingsOpen = false;
                this.newName = this.employee.name;
                this.newTitle = this.employee.title;
                this.newDepartment = this.employee.department;
                this.newSalary = this.employee.monthly_salary;
                this.newStartDate = this.employee.start_date;
                this.newEndDate = this.employee.end_date;
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
<template>
<div class="relative">
    <button @click="toggleDots" type="button"><i class="bi bi-three-dots"></i></button>
    <div v-show="clicked"
        class="absolute z-10 bg-white border border-zinc-300 shadow rounded text-xs w-max">
        <div class="text-zinc-700 py-1 border-b border-zinc-300">
            <button type="button" @click="toggleChangeNameModal" class="hover:bg-zinc-100 px-3 py-2 w-full text-left"><i class="bi bi-type mr-1.5 text-zinc-400"></i>Rename model</button>
        </div>
        <div class="text-zinc-700 py-1">
            <button type="button" @click="toggleDeleteModelModal" class="hover:bg-zinc-100 px-3 py-2 w-full text-left"><i class="bi bi-trash mr-1.5 text-zinc-400"></i>Delete model</button>
        </div>
    </div>
    <div v-show="clicked" @click="toggleDots" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0"></div>

    <Teleport to="body">
        <div v-show="deleteModelModalOpen" class="fixed left-0 top-1/3 w-full h-full flex justify-center align-middle text-xs">
            <div class="p-6 border h-max w-fit shadow-lg bg-white border-zinc-300 rounded z-50">
                <div>
                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you want to delete this model?</h3>
                </div>
                <p class="text-zinc-500 mb-4">Removing <span class="font-semibold">{{ modelName }}</span> can't be undone.</p>
                <div class="float-right">
                    <button type="button"
                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                        @click="toggleDeleteModelModal">Cancel</button>
                    <button type="button" class="ml-2 bg-red-600  drop-shadow-sm
                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                        border border-red-500 rounded text-neutral-100" @click="deleteModel">Delete</button>
                </div>
                <div v-show="showDeleteModelError" class="mt-11 flex justify-center">
                    <ErrorMessage :error-message="deleteModelErrorMessage"></ErrorMessage>
                </div>
            </div>
            <div v-show="deleteModelModalOpen" @click="toggleDeleteModelModal" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
        </div>
    </Teleport>

    <Teleport to="body">
        <div v-show="changeNameModalOpen" class="fixed left-0 top-1/3 w-full h-full flex justify-center align-middle text-xs">
            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                <div>
                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Change {{modelName}} to:</h3>
                </div>
                <form @submit.prevent="changeModelName">
                <div class="mb-4">
                    <div class="mt-1">
                        <input required autofocus :name="`new-name-${modelId}`"
                        class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                        :id="`new-name-${modelId}`" type="text" placeholder="New model name" v-model="newName">
                    </div>
                </div>
                <div class="float-right">
                    <button type="button"
                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                        @click="toggleChangeNameModal">Cancel</button>
                    <button type="submit" class="ml-2 bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                        border border-sky-500 rounded text-neutral-100">Change name</button>
                </div>
                </form>
                <div v-show="showChangeChangeNameError" class="mt-11 flex justify-center">
                    <ErrorMessage :error-message="changeNameErrorMessage"></ErrorMessage>
                </div>
            </div>
            <div v-show="changeNameModalOpen" @click="toggleChangeNameModal" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
        </div>
    </Teleport>
</div>
</template>

<script lang="ts">

import { useFetchAuth } from '~~/methods/useFetchAuth';

export default {

    data() {
        return {
            clicked: false,
            deleteModelModalOpen: false,
            showDeleteModelError: false,
            deleteModelErrorMessage: "Something went wrong!",
            newName: "",
            changeNameModalOpen: false,
            showChangeChangeNameError: false,
            changeNameErrorMessage: "Something went wrong!"
        }
    },
    props: {
        modelId: String,
        modelName: String,
    },
    methods: {
        toggleDots() {
            if (this.clicked) {
                this.clicked = false;
            } else {
                this.clicked = true;
            }
        },
        toggleDeleteModelModal() {
            if (this.deleteModelModalOpen) {
                this.deleteModelModalOpen = false;
            } else {
                this.deleteModelModalOpen = true;
                this.toggleDots();
            }
        },
        async deleteModel() {
            
            const deleteModel = await useFetchAuth(
            '/model/delete', {
                method: 'POST',
            params: {
               model_id: this.modelId
            }
            }
            ).then((data) => {
                console.log("Model deleted sucessfully.");
                location.reload();
            }).catch((error) => {
            console.log(error);
                this.deleteModelErrorMessage = error.data.details;
                this.showDeleteModelError = true;
            });
            
        },
        toggleChangeNameModal() {
            if (this.changeNameModalOpen) {
                this.changeNameModalOpen = false;
                this.newName = "";
            } else {
                this.changeNameModalOpen = true;
                this.toggleDots();
            }
        },
        async changeModelName(){

            const changeModelName = await useFetchAuth(
            '/model/rename', {
                method: 'POST',
            params: {
               model_id: this.modelId,
               name: this.newName
            }
            }
            ).then((data) => {
                console.log("Model renamed sucessfully.");
                location.reload();
            }).catch((error) => {
            console.log(error);
                this.changeNameErrorMessage = error.data.details;
                this.showChangeChangeNameError = true;
            });
        }
    }
}

</script>

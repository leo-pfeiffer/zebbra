<script setup lang="ts">

import { useLogout } from '~~/methods/useLogout';

//get the current user state
const user = useUserState();

</script>

<template>
    <div class="w-screen h-screen flex">
        <div class="w-48 min-w-[12rem] bg-zinc-100 px-3 py-4 border-r border-zinc-300 overflow-hidden">
            <div class="text-sm ml-0.5">
                <NuxtLink :to="`/${user.workspaces[0].name}`">
                    <span class="px-2 py-1 rounded-md bg-green-500 text-neutral-50 shadow-sm">
                        {{ user.workspaces[0].name[0] }}
                    </span>
                    <span class="ml-2 text-zinc-900">
                        {{ user.workspaces[0].name }}
                    </span>
                </NuxtLink>
            </div>
            <div class="text-xs my-4">
                <NuxtLink :to="`/${user.workspaces[0].name}/settings/workspace`">
                    <div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                        <i class="bi bi-gear-fill text-zinc-400"></i><span class="pl-2">Settings</span>
                    </div>
                </NuxtLink>
                <NuxtLink :to="`/${user.workspaces[0].name}/settings/integrations`">
                    <div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                        <i class="bi bi-server text-[11px] text-zinc-400"></i><span class="pl-2">Integrations</span>
                    </div>
                </NuxtLink>
                <NuxtLink to="https://leo-pfeiffer.github.io/zebbra/" target="_blank">
                    <div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                        <i class="bi bi-file-earmark-code-fill text-zinc-400"></i><span
                            class="pl-2">Documentation</span>
                    </div>
                </NuxtLink>
            </div>
            <div class="my-4 flex justify-center w-full">

                <button type="button" @click="toggleNewModelModal"
                    class=" bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs pl-2.5 pr-3 py-1 border border-zinc-300 rounded text-zinc-700"><i
                        class="bi bi-plus-lg mr-1"></i>Create New Model</button>

            </div>
            <div class="pb-3">
                <div>
                    <span class="text-xs text-zinc-500">Your Models</span>
                    <div v-if="true" class="overflow-auto min-h-[55vh] max-h-[55vh] px-2">
                        <ModelDropdown v-for="model in user.models" :model=model></ModelDropdown>
                    </div>
                    <div v-else>
                        <p class="text-xs mt-2 text-zinc-500">Start by creating your first model.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="absolute bottom-0 left-0 bg-zinc-100 border-r border-zinc-300 w-48 flex justify-center px-3">
            <div class="flex justify-center w-full border-t border-zinc-300 py-3">
                <button type="button" @click="useLogout()"
                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Logout</button>
            </div>
        </div>
        <div class="flex-grow overflow-y-scroll">
            <slot />
        </div>
        <Teleport to="body">
            <div v-show="newModelModalOpen"
                class="fixed left-0 top-1/3 w-full h-full flex justify-center align-middle text-xs z-50">
                <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                    <div>
                        <h3 class="text-zinc-900 font-medium text-sm mb-2">Create a new model</h3>
                    </div>
                    <form @submit.prevent="createNewModel">
                        <div class="mb-4">
                            <div class="mt-1">
                                <input required autofocus
                                    class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                                    type="text" placeholder="New model name" v-model="newModelName">
                            </div>
                        </div>
                        <div class="float-right">
                            <button type="button"
                                class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                                @click="toggleNewModelModal">Cancel</button>
                            <button type="submit" class="ml-2 bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                        border border-sky-500 rounded text-neutral-100">Create</button>
                        </div>
                    </form>
                    <div v-show="showCreateNewModalError" class="mt-11 flex justify-center">
                        <ErrorMessage :error-message="createNewModalErrorMessage"></ErrorMessage>
                    </div>
                </div>
                <div v-show="newModelModalOpen" @click="toggleNewModelModal"
                    class="fixed top-0 left-0 w-[100vw] h-[100vh] z-49 bg-zinc-100/50"></div>
            </div>
        </Teleport>
    </div>
</template>

<script lang="ts">

import { useFetchAuth } from '~~/methods/useFetchAuth';
import { Model } from '~~/types/Model';

export default {
    data() {
        return {
            newModelName: "",
            newModelModalOpen: false,
            showCreateNewModalError: false,
            createNewModalErrorMessage: "Something went wrong."

        }
    },
    methods: {
        toggleNewModelModal() {
            if (this.newModelModalOpen) {
                this.newModelModalOpen = false;
                this.newModelName = "";
            } else {
                this.newModelModalOpen = true;
            }
        },
        async createNewModel() {

            var newModelId;

            const createModel = await useFetchAuth(
                '/model/add', {
                method: 'POST',
                params: {
                    name: this.newModelName,
                    workspace_id: this.user.workspaces[0]._id
                }
            }
            ).then((data:Model) => {
                console.log("Model created sucessfully.");
                newModelId = data._id;
                navigateTo(`/${this.user.workspaces[0].name}/${newModelId}/dashboard`);
            }).catch((error) => {
                console.log(error);
                this.createNewModalErrorMessage = error.data.details;
                this.showCreateNewModalError = true;
            });

        }
    },
}


</script>

<style>
.right-page {
    width: calc(100% - 12rem);
}
</style>
<script setup lang="ts">

const userState = useUserState();

</script>


<template>
<div class="relative">
    <button @click="toggleDots" type="button"><i class="bi bi-three-dots"></i></button>
    <div v-show="clicked"
        class="absolute z-10 bg-white border border-zinc-300 shadow rounded text-xs w-max">
        <div class="text-zinc-700 py-1 border-b border-zinc-300">
            <button type="button" @click="toggleChangeNameModal" class="hover:bg-zinc-100 px-3 py-2 w-full text-left"><i class="bi bi-type mr-1.5 text-zinc-400"></i>Rename model</button>
        </div>
        <div class="text-zinc-700 py-1 border-b border-zinc-300">
            <button type="button" @click="toggleAccessRightsModal" class="hover:bg-zinc-100 px-3 py-2 w-full text-left"><i class="bi bi-pen mr-1.5 text-zinc-400"></i>Manage access rights</button>
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
    <Teleport to="body">
        <div v-show="accessRightsModalOpen" class="fixed left-0 top-1/4 w-full h-full flex justify-center align-middle text-xs">
            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                <div>
                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Manage access rights for <span class="underline">{{modelName}}</span>:</h3>
                </div>
                <div class="mb-4">
                    <div class="text-xs text-zinc-900 my-2"><i class="bi bi-people mr-1"></i>Manage existing users</div>
                    <div class="">
                        <div>
                            <table class="w-full text-xs text-left table-auto">
                                <tr>
                                    <td class="text-[10px] text-zinc-500 uppercase">
                                       Name
                                    </td>
                                    <td class="text-[10px] px-2 text-zinc-500 uppercase">
                                        Email
                                    </td>
                                    <td class="text-[10px] px-2 text-zinc-500 uppercase">
                                        Role
                                    </td>
                                    <td class="text-[10px] px-2">
                                        
                                    </td>
                                    <td class="text-[10px] px-2">
                                       
                                    </td>
                                </tr>
                                <ModelAccessTableRow @grant-access="grantAccess" @revoke-access="revokeAccess" v-for="user in modelUsers" :user="user"></ModelAccessTableRow>
                            </table>
                        </div>
                        <SuccessMessage v-show="showAccessRightsSuccess" :successMessage="accessRightsSuccessMessage"></SuccessMessage>
                    </div>
                </div>
                <div class="py-3 mb-2 border-t border-zinc-300">
                    <div class="text-xs text-zinc-900 mb-2"><i class="bi bi-person-plus mr-1"></i>Invite user to model</div>
                    <table class="w-full text-xs text-left table-auto">
                        <tr>
                            <td class="text-[10px] text-zinc-500 uppercase">
                                Select user
                            </td>
                            <td class="text-[10px] text-zinc-500 uppercase">
                                Select role
                            </td>
                            <td>
                                
                            </td>
                        </tr>
                        <tr>
                            <td class="text-zinc-500 pr-2">
                                <select v-model="userInviteSelected" class="border border-zinc-300 p-1 rounded w-full">
                                    <option v-for="user in workspaceUsers">{{ user.username }}</option>
                                </select>
                            </td>
                            <td class="pr-2 text-zinc-500">
                                <select v-model="userInviteRoleSelected" class="border border-zinc-300 p-1 rounded w-full">
                                    <option>Editor</option>
                                    <option>Viewer</option>
                                    <option>Admin</option>
                                </select>
                            </td>
                            <td class="pl-2 text-zinc-500">
                                <button @click="inviteUserToModel" type="button" class="font-medium text-xs text-green-600">Invite</button>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class="float-right">
                    <button type="button"
                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                        @click="toggleAccessRightsModal">Close</button>
                </div>
                <div v-show="showAccessRightsError" class="mt-11 flex justify-center">
                    <ErrorMessage :error-message="accessRightsErrormessage"></ErrorMessage>
                </div>
            </div>
            <div v-if="accessRightsModalOpen" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
        </div>
    </Teleport>
</div>
</template>

<script lang="ts">

import { useFetchAuth } from '~~/methods/useFetchAuth';
import { useGetModelPermissions } from '~~/methods/useGetModelPermissions';

export default {

    data() {
        return {
            workspaceUsers: [],
            userInviteSelected: "",
            userInviteRoleSelected: "Editor",
            clicked: false,
            deleteModelModalOpen: false,
            showDeleteModelError: false,
            deleteModelErrorMessage: "Something went wrong!",
            newName: "",
            changeNameModalOpen: false,
            showChangeChangeNameError: false,
            changeNameErrorMessage: "Something went wrong!",
            modelUsers: [],
            accessRightsModalOpen: false,
            showAccessRightsSuccess: false,
            accessRightsSuccessMessage: "Success!",
            showAccessRightsError: false,
            accessRightsErrormessage: "Something went wrong!",
        }
    },
    props: {
        modelId: String,
        modelName: String,
    },
    async mounted() {
        await this.updateModelUsers();
        await this.getWorkspaceUsers();
        this.showAccessRightsSuccess = false;
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
        toggleAccessRightsModal() {
            if (this.accessRightsModalOpen) {
                this.accessRightsModalOpen = false;
                this.showAccessRightsSuccess = false;
            } else {
                this.accessRightsModalOpen = true;
                this.toggleDots();
            }
        },
        async getWorkspaceUsers() {
            try {
                await useFetchAuth(
                        '/workspace/users', {
                        method: 'GET',
                        params: {
                            workspace_id: this.userState.workspaces[0]._id
                        }
                    }
                    ).then((data) => {
                        this.workspaceUsers = data;
                    })
            } catch(e) {
                console.log("Error fetching workspace users");
            }

        },
        async inviteUserToModel() {

            this.showAccessRightsSuccess = false;

            var getUserId:string;

            for(let i=0; i < this.workspaceUsers.length; i++) {
                if(this.userInviteSelected === this.workspaceUsers[i].username) {
                    getUserId = this.workspaceUsers[i]._id;
                    break;
                }
            }

            await this.grantAccess(getUserId, this.userInviteRoleSelected);
            await this.updateModelUsers();

        },
        async updateModelUsers() {

            this.showAccessRightsSuccess = false;

            try {
                this.modelUsers = await useGetModelPermissions(this.modelId);
                this.accessRightsSuccessMessage = "Users successfully updated!"
                this.showAccessRightsSuccess = true;
            } catch(e) {
                this.accessRightsErrormessage = e.data;
                console.log(this.accessRightsErrormessage);
            }
        },
        async grantAccess(userId: string, role:string) {

            try {
            await useFetchAuth(
                    '/model/grant', {
                    method: 'POST',
                    params: {
                        model_id: this.modelId,
                        role: role.toLowerCase(),
                        user_id: userId
                    }
                }
                ).then((data) => {
                    //todo:success
                    this.updateModelUsers();
                })

            } catch(e) {
                this.accessRightsErrormessage = "Chaning the user role failed. Please try again.";
                console.log(this.accessRightsErrormessage);
            }
        },
        async revokeAccess(userId: string, role:string) {

            this.showAccessRightsSuccess = false;


            try {
            await useFetchAuth(
                    '/model/revoke', {
                    method: 'POST',
                    params: {
                        model_id: this.modelId,
                        role: role.toLowerCase(),
                        user_id: userId
                    }
                }
                ).then((data) => {
                    this.updateModelUsers();
                    this.accessRightsSuccessMessage = "Users successfully updated!"
                })

            } catch(e) {
                this.accessRightsErrormessage = "Removing the user failed. Please try again.";
            }

        },
        async deleteModel() {
            
            const deleteModel = await useFetchAuth(
            '/model/delete', {
                method: 'DELETE',
            params: {
               model_id: this.modelId
            }
            }
            ).then((data) => {
                console.log("Model deleted sucessfully.");
                location.reload();
            }).catch((error) => {
                this.deleteModelErrorMessage = error.data.detail;
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

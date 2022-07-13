<script setup lang="ts">

const config = useRuntimeConfig()

</script>

<template>
<div>
    <button @click="toggleDots"><i class="bi bi-three-dots"></i></button>
    <div v-show="clicked"
        class="absolute z-10 -translate-x-full bg-white border border-zinc-300 shadow rounded text-xs w-max">
        <div class="text-zinc-700 py-1 border-b border-zinc-300">
            <button @click="toggleChangeAdminModal" class="hover:bg-zinc-100 px-3 py-2 w-full text-left"><i class="bi bi-star-fill mr-1.5 text-zinc-400"></i>Make admin</button>
        </div>
        <div class="text-zinc-700 py-1">
            <button @click="toggleDeleteUserModal" class="hover:bg-zinc-100 px-3 py-2 w-full text-left"><i class="bi bi-person-dash-fill mr-1.5 text-zinc-400"></i>Remove user</button>
        </div>
    </div>
    <div v-show="clicked" @click="toggleDots" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0"></div>

    <Teleport to="body">
        <div v-show="deleteUserModalOpen" class="fixed left-0 top-1/3 w-full h-full flex justify-center align-middle text-xs">
            <div class="p-6 border h-max w-fit shadow-lg bg-white border-zinc-300 rounded">
                <div>
                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you want to remove this user?</h3>
                </div>
                <p class="text-zinc-500 mb-4">Removing <span class="font-semibold">{{ username }}</span> can't be undone.</p>
                <div class="float-right">
                    <button
                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                        @click="toggleDeleteUserModal">Cancel</button>
                    <button class="ml-2 bg-red-600  drop-shadow-sm
                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                        border border-red-500 rounded text-neutral-100" @click="deleteUser">Remove</button>
                </div>
                <div v-show="showDeleteUserError" class="mt-11 flex justify-center">
                    <ErrorMessage :error-message="deleteUserErrorMessage"></ErrorMessage>
                </div>
            </div>
        </div>
    </Teleport>

    <Teleport to="body">
        <div v-show="changeAdminModalOpen" class="fixed left-0 top-1/3 w-full h-full flex justify-center align-middle text-xs">
            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded">
                <div>
                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you want to change the workspace admin?</h3>
                </div>
                <div class="flex align-middle mb-4">
                    <span class="text-zinc-500 mr-2 mt-1.5">Be aware that making <span class="font-semibold">{{ username }}</span> the admin of the workspace also removes you as an admin.</span>
                </div>
                <div class="float-right">
                    <button
                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                        @click="toggleChangeAdminModal">Cancel</button>
                    <button @click="makeUserAdmin" class="ml-2 bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                        border border-sky-500 rounded text-neutral-100">Change admin</button>
                </div>
                <div v-show="showChangeAdminError" class="mt-11 flex justify-center">
                    <ErrorMessage :error-message="changeAdminErrorMessage"></ErrorMessage>
                </div>
            </div>
        </div>
    </Teleport>
</div>
</template>

<script lang="ts">

export default {

    data() {
        return {
            clicked: false,
            deleteUserModalOpen: false,
            showDeleteUserError: false,
            deleteUserErrorMessage: "Something went wrong!",
            changeAdminModalOpen: false,
            showChangeAdminError: false,
            changeAdminErrorMessage: "Something went wrong!"
        }
    },
    props: {
        userId: String,
        username: String,
    },
    methods: {
        toggleDots() {
            if (this.clicked) {
                this.clicked = false;
            } else {
                this.clicked = true;
            }
        },
        toggleDeleteUserModal() {
            if (this.deleteUserModalOpen) {
                this.deleteUserModalOpen = false;
            } else {
                this.deleteUserModalOpen = true;
                this.toggleDots();
            }
        },
        async deleteUser() {

            const user = useUserState();
            
            const removeUser = await useFetchAuth(
            `${this.config.backendUrlBase}/workspace/remove`, {
                method: 'POST',
            params: {
                user_id: this.userId,
                workspace_id: user.value.workspaces[0]._id
            }
            }
            ).then((data) => {
                console.log("Member removed successfully");
                location.reload();
            }).catch((error) => {
            console.log(error);
                this.deleteUserErrorMessage = error.data.details;
                this.showDeleteUserError = true;
            });
            
            
        },
        toggleChangeAdminModal() {
            if (this.changeAdminModalOpen) {
                this.changeAdminModalOpen = false;
            } else {
                this.changeAdminModalOpen = true;
                this.toggleDots();
            }
        },
        async makeUserAdmin(){

            const user = useUserState();
            
            const makeUserAdmin = await useFetchAuth(
            `${this.config.public.backendUrlBase}/workspace/changeAdmin`, {
                method: 'POST',
            params: {
                user_id: this.userId,
                workspace_id: user.value.workspaces[0]._id
            }
            }
            ).then((data) => {
                console.log("Admin changed successfully");
                location.reload();
            }).catch((error) => {
                this.changeAdminErrorMessage = error.data.details;
                this.showChangeAdminError = true;
            });
        }
    }
}

</script>

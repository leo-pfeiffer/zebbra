<template>
<div>
    <button @click="toggleDots"><i class="bi bi-three-dots"></i></button>
    <div v-show="clicked"
        class="absolute z-10 -translate-x-full bg-white border border-zinc-300 shadow rounded text-xs w-max">
        <div class="text-zinc-500 py-1 border-b border-zinc-300">
            <button @click="toggleChangeUserTypeModal" class="hover:bg-zinc-200 px-3 py-2 w-full text-left"><i class="bi bi-layers-fill mr-1.5 text-zinc-400"></i>Change role</button>
        </div>
        <div class="text-zinc-500 py-1">
            <button @click="toggleDeleteUserModal" class="hover:bg-zinc-200 px-3 py-2 w-full text-left"><i class="bi bi-person-dash-fill mr-1.5 text-zinc-400"></i>Remove user</button>
        </div>
    </div>
    <div v-show="clicked" @click="toggleDots" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0"></div>

    <div v-show="deleteUserModalOpen" class="absolute -translate-x-full w-max h-max flex justify-center align-middle text-xs">
        <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded">
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
        </div>
    </div>

    <div v-show="changeUserTypeModalOpen" class="absolute -translate-x-full w-max h-max flex justify-center align-middle text-xs">
        <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded">
            <div>
                <h3 class="text-zinc-900 font-medium text-sm mb-2">Change User Role</h3>
            </div>
            <form @submit.prevent="updateUserType">
                <div class="flex align-middle mb-4">
                    <span class="text-zinc-500 mr-2 mt-1.5">Change <span class="font-semibold">{{ username }}'s</span> account to:</span>
                    <select
                    class="text-zinc-700 border shadow-sm bg-white border-zinc-300 rounded py-1 px-1" 
                    v-model="this.selectedUserType"
                    required>
                        <option>
                            Admin
                        </option>
                        <option>
                            Member
                        </option>
                    </select>
                </div>
                <div class="float-right">
                    <button
                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                        @click="toggleChangeUserTypeModal">Cancel</button>
                    <button type="submit" class="ml-2 bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                        border border-sky-500 rounded text-neutral-100">Change</button>
                </div>
            </form>
        </div>
    </div>
</div>
</template>

<script>

export default {
    data() {
        return {
            clicked: false,
            deleteUserModalOpen: false,
            changeUserTypeModalOpen: false,
            selectedUserType: ""
        }
    },
    props: {
        username: String
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
        deleteUser() {
            //todo
        },
        toggleChangeUserTypeModal() {
            if (this.changeUserTypeModalOpen) {
                this.changeUserTypeModalOpen = false;
            } else {
                this.changeUserTypeModalOpen = true;
                this.toggleDots();
            }
        },
        updateUserType(){
            //todo
        }
    }
}

</script>

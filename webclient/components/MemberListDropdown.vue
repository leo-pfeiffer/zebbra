<template>
<div>
    <button @click="toggleDots"><i class="bi bi-three-dots"></i></button>
    <div v-show="clicked"
        class="absolute z-10 -translate-x-full bg-white border border-zinc-300 shadow-sm rounded text-sm w-max">
        <div class="text-zinc-500 p-3 border-b border-zinc-300"><button @click="toggleChangeUserTypeModal"><i
                    class="bi bi-layers-fill mr-1.5 text-zinc-400"></i>Change role</button></div>
        <div class="text-zinc-500 p-3"><button @click="toggleDeleteUserModal"><i class="bi bi-person-dash-fill mr-1.5 text-zinc-400"></i>Remove user</button></div>
    </div>
    <div v-show="clicked" @click="toggleDots" class="absolute top-0 left-0 w-[100vw] h-[100vh] z-0"></div>

    <div v-show="deleteUserModalOpen" class="absolute -translate-x-full w-max h-max flex justify-center align-middle">
        <div class="p-3 border h-max shadow-sm bg-white border-zinc-300 rounded">
            <p class="text-zinc-500 text-sm mb-3">Are you sure you want to remove <span class="font-semibold">{{ username }}'s</span> account?</p>
            <div class="float-right">
                <button
                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                    @click="toggleDeleteUserModal">Cancel</button>
                <button class="ml-2 bg-red-600  drop-shadow-sm
                    shadow-zinc-50 text-xs font-medium px-2 py-1 
                    border border-red-600 rounded text-neutral-100" @click="deleteUser">Remove</button>
            </div>
        </div>
    </div>

    <div v-show="changeUserTypeModalOpen" class="absolute -translate-x-full w-max h-max flex justify-center align-middle">
        <div class="p-3 border h-max shadow-sm bg-white border-zinc-300 rounded">
            <form @submit.prevent="updateUserType">
                <div class="flex align-middle mb-3">
                    <span class="text-zinc-500 mr-2 mt-1">Change <span class="font-semibold">{{ username }}'s</span> account to:</span>
                    <select
                    class="text-zinc-700 border shadow-sm bg-white border-zinc-300 rounded text-sm py-1 px-1" 
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
                        border border-sky-600 rounded text-neutral-100">Change</button>
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

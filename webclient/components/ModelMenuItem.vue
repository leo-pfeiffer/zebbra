<script setup>

const user = useUserState();

</script>

<template>
    <div
        class="my-3 group flex align-center align-middle rounded border border-zinc-300 p-3 hover:border-sky-500 hover:shadow-md hover:shadow-sky-50">
        <div>
            <span class="text-sm font-medium text-zinc-700">{{ modelName }}</span>
        </div>
        <div class="-translate-y-0.5">
            <span class="ml-2 text-[10px] uppercase rounded border border-zinc-300 px-1 py-0.5 text-zinc-500 bg-zinc-50"> {{ modelAccess }}</span>
        </div>
        <div class="flex-grow">
            <span v-if="isModelAdmin" class="ml-1.5 hidden group-hover:inline-block text-zinc-500 hover:text-zinc-700 z-50">
                <ModelListDropdown :modelId="modelId" :modelName="modelName"></ModelListDropdown>
            </span>
        </div>
        <div class="group-hover:inline-block hidden">
            <NuxtLink :to="`/${user.workspaces[0].name}/${modelId}/dashboard`"><span
                    class="text-sm font-medium text-sky-600">--></span></NuxtLink>
        </div>
    </div>
</template>

<script>

import { useGetModelPermissions } from '~~/methods/useGetModelPermissions';

export default {
    data() {
        return {
            modelUsers: [],
        }
    },
    props: {
        modelName: String,
        modelId: String
    },
    async mounted() {
        try {
            this.modelUsers = await useGetModelPermissions(this.modelId);
            console.log(this.modelUsers)
        } catch (e) {
            console.log(e);
        }
    },
    computed: {
        isModelAdmin() {
            for(let i=0; i < this.modelUsers.length; i++) {
                if(this.user._id === this.modelUsers[i]._id && this.modelUsers[i].user_role === "Admin") {
                    return true;
                }
            }
            return false;
        },
        modelAccess() {
            for(let i=0; i < this.modelUsers.length; i++) {
                if(this.user._id === this.modelUsers[i]._id) {
                    return this.modelUsers[i].user_role;
                }
            }
            return null;
        }
    },
}
</script>
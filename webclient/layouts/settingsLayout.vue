<template>
    <div class="w-screen h-screen flex" v-if="!userDataLoading">
        <div class="w-48 min-w-[12rem] bg-zinc-100 px-3 py-4 border-r border-zinc-300 overflow-hidden">
            <div class="text-sm flex align-middle">
                <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}`"><div class="text-zinc-400 py-1 pl-1.5 pr-1 hover:bg-zinc-200 hover:text-zinc-500 rounded-md hover:shadow-sm">
                    <i class="bi bi-arrow-up-left"></i>
                </div></NuxtLink>
                <div class="ml-1 text-zinc-900 font-medium text-lg">Settings</div>
            </div>
            <div class="text-xs pl-2 mt-8">
                <div class="text-zinc-500 text-semibold"><i class="bi bi-house-door-fill mr-2 text-zinc-400"></i>Workspace</div>
                <div class="mt-1.5">
                    <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}/settings/workspace`" activeClass="font-semibold"><div class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">General</div></NuxtLink>
                    <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}/settings/members`" activeClass="font-semibold"><div id="workspace-members" class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">Members</div></NuxtLink>
                    <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}/settings/integrations`" activeClass="font-semibold"><div class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">Integrations</div></NuxtLink>
                </div>
            </div>
            <div class="text-xs pl-2 mt-6">
                <div class="text-zinc-500 text-semibold"><i class="bi bi-person-fill mr-2 text-zinc-400"></i>Profile</div>
                <div class="mt-1.5">
                    <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}/settings/profile`" activeClass="font-semibold"><div id="profile-general" class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">General</div></NuxtLink>
                    <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}/settings/models`" activeClass="font-semibold"><div id="profile-general" class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">Models</div></NuxtLink>
                </div>
            </div>
        </div>
        <div class="absolute bottom-0 left-0 bg-zinc-100 border-r border-zinc-300 w-48 flex justify-center px-3">
            <div class="flex justify-center w-full border-t border-zinc-300 py-3">
                <button @click="logout()" class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Logout</button>
            </div>
        </div>
        <div class="flex-grow overflow-y-scroll">
            <slot />
        </div>
    </div>
</template>

<script lang="ts">

import { useLogout } from '~~/methods/useLogout';
import { mapState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';

export default {

    data() {
        return {
            userDataLoading: true,
        }
    },
    async mounted () {
        this.userDataLoading = true;
        try {
            await this.updatePiniaUserStore();
            this.userDataLoading = false;
        } catch (e) {
            console.log(e)
        }
    },
    computed: {
        ...mapState(useUserStore, ['piniaUserStore']),
    },
    methods: {
        ...mapActions(useUserStore, ['updatePiniaUserStore']),
        logout() {
            useLogout();
        }
    },
}

</script>
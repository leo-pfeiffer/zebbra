<template>
    <div class="my-2 text-xs text-zinc-700">
        <div @click="clickDropdown" class="hover:cursor-pointer flex align-middle">
            <i v-if="!opened" class="bi bi-caret-right-fill mr-2 text-xs text-zinc-400"></i>
            <i v-else class="bi bi-caret-down-fill mr-2 text-xs text-zinc-400"></i>
            {{ model.name }}
        </div>
        <div v-show="opened" class="text-xs text-zinc-700 pl-10 mt-1">
            <ul class="list-disc">
                <NuxtLink active-class="font-semibold" :to="`/${piniaUserStore.workspaces[0].name}/${model._id}/dashboard`"><li class="my-1.5">Dashboard</li></NuxtLink>
                <NuxtLink active-class="font-semibold" :to="`/${piniaUserStore.workspaces[0].name}/${model._id}/profit-loss`"><li class="my-1.5">Profit & Loss</li></NuxtLink>
                <NuxtLink active-class="font-semibold" :to="`/${piniaUserStore.workspaces[0].name}/${model._id}/revenues`"><li class="my-1.5">Revenues</li></NuxtLink>
                <NuxtLink active-class="font-semibold" :to="`/${piniaUserStore.workspaces[0].name}/${model._id}/costs`"><li class="my-1.5">Costs</li></NuxtLink>
            </ul>
        </div>
    </div>
</template>

<script>
import { mapState } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
export default {
    data() {
        return {
            opened: false
        }
    },
    props: {
        model: Object
    },
    computed: {
    ...mapState(useUserStore, ['piniaUserStore']),
    },
    methods: {
        clickDropdown() {
            if (this.opened === true) {
                this.opened = false;
            } else {
                this.opened = true;
            }
        }
    },
    beforeMount() {
        //open toggle for current model
        const routeModelId = this.$route.fullPath.split("/")[2];
        if(routeModelId === this.model._id) {
            this.opened = true;
        }
    }
}

</script>
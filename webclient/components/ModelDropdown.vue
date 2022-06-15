<template>
    <div class="my-2 text-zinc-500">
        <div @click="clickDropdown" class="hover:cursor-pointer flex align-middle">
            <i v-if="!opened" class="bi bi-caret-right-fill mr-2 text-sm"></i>
            <i v-else class="bi bi-caret-down-fill mr-2 text-sm"></i>
            {{ model.name }}
        </div>
        <div v-show="opened" class="text-sm ml-10 mt-1">
            <ul class="list-disc">
                <!-- todo: update links, add active state and default open for selected model -->
                <NuxtLink to="/tesla/{{ $model.id }}/dashboard"><li class="my-1">Dashboard</li></NuxtLink>
                <NuxtLink to="/tesla/{{ $model.id }}/profit-loss"><li class="my-1">Profit & Loss</li></NuxtLink>
                <NuxtLink to="/tesla/{{ $model.id }}/Revenues"><li class="my-1">Revenues</li></NuxtLink>
                <NuxtLink to="/tesla/{{ $model.id }}/costs"><li class="my-1 ">Costs</li></NuxtLink>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            opened: false
        }
    },
    props: {
        model: Object
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
}

</script>
<script setup>
definePageMeta({
  middleware: ["auth", "route-check"]
})
</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <h1>Model ID: {{ $route.params.modelId }}</h1>
            <p>Revenues</p>
            <div class="mt-3 ml-1 py-3 pl-2 mr-0 overflow-x-hidden">
                <div class="flex">
                    <div class="">
                        <div class="flex mb-4">
                            <div class="text-xs text-center font-mono italic py-2 px-2 border-b border border-zinc-300 min-w-[50px] max-w-[50px]">fx</div>
                            <div class="text-xs border-y border-r border-zinc-300 min-w-[325px] max-w-[325px] text-right"><input type="text" class="font-mono w-full h-full px-2"></div>
                        </div>
                        <ColumnHeader v-for="variable in assumptions" :name="variable.name" :value="variable.initialValue"></ColumnHeader>
                    </div>
                    <div class="overflow-x-auto">
                        <div class="flex mb-4">
                            <div class="text-xs py-2 px-2 border-y border-r border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700" v-for="index in 24" :key="index">{{index}}</div>
                        </div>
                        <GridColumn v-for="index in assumptions"></GridColumn>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script>
export default {
    data() {
        return {
            assumptions: [
                {
                    name: 'Initial Customers',
                    variableType: "Number",
                    timeSeries: false,
                    formula: null,
                    initialValue: 1000,
                    consequValues: null  },
                {   name: 'Churn Rate',
                    variableType: "Percentage",
                    timeSeries: false,
                    formula: null,
                    initialValue: 0.05,
                    consequValues: null  },
                {   name: 'Churn Rate',
                    variableType: "Percentage",
                    timeSeries: false,
                    formula: null,
                    initialValue: 0.05,
                    consequValues: null  },
                ]
        }
    },
    props: {
    },
    methods: {},
}

</script>
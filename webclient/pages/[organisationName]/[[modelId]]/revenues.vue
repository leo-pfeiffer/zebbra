<template>
    <NuxtLayout name="navbar">
        <div>
            <h1>Model ID: {{ $route.params.modelId }}</h1>
            <p>Revenues</p>
            <div class="mt-3 ml-1 py-3 pl-2 mr-0 overflow-x-hidden">
                <div class="flex">
                    <div class="border-t border-l border-zinc-300">
                        <ColumnHeader v-for="variable in assumptions" :name="variable.name" :value="variable.initialValue"></ColumnHeader>
                    </div>
                    <div class="overflow-x-auto border-t border-zinc-300">
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
                ]
        }
    },
    props: {
    },
    methods: {},
}

</script>
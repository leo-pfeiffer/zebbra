<template>
    <div>
        <form @submit.prevent="getValueObject">
            <input required type="text" placeholder="input" v-model="input" class="border m-5">
            <button type="submit">submit</button>
        </form>
        <div>
            {{output}}
        </div>
    </div>
</template>

<script lang="ts">

export default {
    data() {
        return {
            input: "",
            output: ""
        }
    },
    methods: {
        getValueObject() {

            this.output = useFormulaParser().getValueObject(this.input);

        }
    }
}
</script>
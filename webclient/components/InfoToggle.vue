<template>
    <span class="group right-3 z-50 max-w-fit" :class="{'absolute': position === 'absolute', 'ml-1 relative' : position === 'inline', 'relative' :position === 'list'}">
        <span class="absolute z-50 translate-y-7 -translate-x-1/4 text-center min-w-fit">
            <span
                class="max-w-[350px] min-w-[200px] hidden z-50 font-normal bg-zinc-500 text-[11px] rounded px-2 py-1 text-white normal-case group-hover:inline-block">
                {{text}}</span>
        </span>
        <i class="bi bi-info-circle hover:text-zinc-500 text-zinc-400" :class="{'ml-4': position === 'list', 'ml-3' : position === 'inline'}"></i>
    </span>
</template>

<script>
export default {
    props: {
        text: String,
        position: String,
    },

}
</script>

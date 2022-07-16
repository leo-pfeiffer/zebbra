<template>

<div :class="getRandomColor"
class="sm:inline-block hidden rounded-full font-mono text-neutral-50 shadow-sm p-1.5 w-7 h-7 mr-3 align-middle text-center">{{ this.firstName[0] }}{{ this.lastName[0] }}</div>

</template>
<script>
export default {
  data() {
    return {}
  },
  props: {
    firstName: String,
    lastName: String
  },
  computed: {
    getRandomColor() {
      const colors = [
        "bg-green-400",
        "bg-sky-400",
        "bg-amber-400",
        "bg-neutral-400",
        "bg-orange-400",
        "bg-violet-400",
        "bg-rose-400",
        "bg-lime-400",
        "bg-emerald-400",
        "bg-yellow-400",
        "bg-teal-400",
        "bg-cyan-400",
        "bg-indigo-400",
        "bg-fuchsia-400",
        "bg-red-400"
      ];
      const randomIndex = Math.floor(Math.random() * colors.length);
      return colors[randomIndex];
    }
  }
  }

</script>
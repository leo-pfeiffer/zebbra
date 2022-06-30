<template>

<span :class="getRandomColor"
class="rounded-full tracking-tighter text-neutral-50 shadow-sm p-1.5 mr-2">{{ this.firstName[0] }}{{ this.lastName[0] }}</span>

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
        "bg-green-500",
        "bg-sky-500",
        "bg-amber-400",
        "bg-neutral-400",
        "bg-orange-500",
        "bg-violet-500",
        "bg-rose-500",
        "bg-lime-500",
        "bg-emerald-500",
        "bg-yellow-500",
        "bg-teal-500",
        "bg-cyan-500",
        "bg-indigo-500",
        "bg-fuchsia-500",
        "bg-red-500"
      ];
      const randomIndex = Math.floor(Math.random() * colors.length);
      return colors[randomIndex];
    }
  }
  }

</script>
<template>

<div :class="getRandomColor,{'mr-3': margin, 'hover:drop-shadow-lg': !margin}"
class="sm:inline-block hidden rounded-full font-mono text-neutral-50 shadow-sm p-1.5 w-7 h-7 align-middle text-center">{{ this.firstName[0] }}{{ this.lastName[0] }}</div>

</template>
<script>
export default {
  data() {
    return {}
  },
  props: {
    firstName: String,
    lastName: String,
    margin: Boolean
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

      // convert the name into a byte array
      const utf8Encode = new TextEncoder();
      const byteArr = utf8Encode.encode(this.firstName + this.lastName);

      // sum up the bytes
      const byteSum = byteArr.reduce((a, b) => a + b)

      // trim the bytes to get an index from the colors
      const index = byteSum % colors.length

      return colors[index];
    }
  }
}

</script>
<script setup>
definePageMeta({
  middleware: ["auth"]
})
</script>

<template>
  <NuxtLayout name="settings-layout">
    <div class="container">
      <div class="mt-8 px-2 sm:px-[10%] lg:px-[15%]">
        <h1 class="text-2xl my-1 font-medium text-zinc-900">Members</h1>
        <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage the members within your workspace</p>
        <div class="py-6">

          <div class="border border-zinc-300 rounded">
            <table class="w-full text-sm text-left">
              <tr class="border-b border-zinc-300">
                <td
                  class="py-3 px-3 text-xs uppercase font-medium text-zinc-500 bg-zinc-100 border-zinc-300 rounded-tl">
                  NAME</td>
                <td class="py-3 px-3 text-xs uppercase font-medium text-zinc-500 bg-zinc-100 border-zinc-300">EMAIL</td>
                <td class="py-3 px-3 text-xs uppercase font-medium text-zinc-500 bg-zinc-100">ROLE</td>
                <td class="py-3 px-3 text-xs uppercase font-medium text-zinc-500 bg-zinc-100 rounded-tr"></td>
              </tr>
              <tr v-for="member in members" class="border-b border-zinc-300 last:border-0">
                <td class="py-3 px-3 text-zinc-900"><span
                    class="rounded-full bg-green-500 text-neutral-50 shadow-sm text-xs p-1.5 mr-2">{{ member.first_name[0] }}{{ member.last_name[0] }}</span>{{ member.first_name }}
                  {{ member.last_name }}</td>
                <td class="py-3 px-3 text-zinc-500">{{ member.username }}</td>
                <td class="py-3 px-3 text-zinc-500">{{ member.user_role }}</td>
                <td class="py-3 px-3 text-zinc-500">
                  <MemberListDropdown :username="member.username"></MemberListDropdown>
                </td>
              </tr>
            </table>
          </div>

          <div v-show="showError" class="w-full flex justify-center">
            <ErrorMessage error-message="Failed to load members. Try again!"></ErrorMessage>
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
      members: [
        {
          first_name: "Patrick",
          last_name: "Schnyder",
          username: "patrick@schnyder.com",
          user_role: "Admin"
        },
        {
          first_name: "Leopold",
          last_name: "Pfeiffer",
          username: "leopold@pfeiffer.com",
          user_role: "Member"
        },
        {
          first_name: "John",
          last_name: "Doe",
          username: "john@doe.com",
          user_role: "Member"
        },
      ],
      showError: false,
    };
  },
  async beforeMount() {

    //get user data and pre fill the form
    /* const data = await useFetchAuth(
      'http://localhost:8000/workspace/users', {
        method: 'GET',
      params: {
        name: "",
      }
    },
    ).then((data) => {
      console.log(data);
    }).catch((error) => {
      console.log(error);
      this.showError = true;
    }); */
  },
  methods: {}
}
</script>
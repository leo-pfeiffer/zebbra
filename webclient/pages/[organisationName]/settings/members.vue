<script setup lang="ts">
definePageMeta({
  middleware: ["auth", "route-check"]
})

</script>

<template>
  <NuxtLayout name="settings-layout">
    <div class="container">
      <div class="mt-8 px-2 sm:px-[10%] lg:px-[15%]">
        <h1 class="text-2xl my-1 font-medium text-zinc-900">Members</h1>
        <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage the members within your workspace</p>
        <div class="w-full py-4"><button @click="toggleInviteUserModal"
            class="float-right bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700"><i
              class="bi bi-person-plus-fill mr-1"></i>Invite</button></div>
        <div class="py-6">
          <div class="border border-zinc-300 rounded">
            <table class="w-full text-xs text-left">
              <tr class="border-b border-zinc-300">
                <td class="py-3 px-3 uppercase font-medium text-zinc-500 bg-zinc-100 border-zinc-300 rounded-tl">
                  NAME</td>
                <td class="py-3 px-3 uppercase font-medium text-zinc-500 bg-zinc-100 border-zinc-300">EMAIL</td>
                <td class="py-3 px-3 uppercase font-medium text-zinc-500 bg-zinc-100">ROLE</td>
                <td v-show="userIsWorkspaceAdmin"
                  class="py-3 px-3 uppercase font-medium text-zinc-500 bg-zinc-100 rounded-tr"></td>
              </tr>
              <tr v-for="member in members" class="border-b border-zinc-300 last:border-0">
                <td class="py-3 px-3 text-zinc-900">
                  <Avatar :first-name="member.first_name" :last-name="member.last_name"></Avatar>{{ member.first_name }}
                  {{ member.last_name }}
                </td>
                <td class="py-3 px-3 text-zinc-500">{{ member.username }}</td>
                <td class="py-3 px-3 text-zinc-500">{{ member.user_role }}</td>
                <td v-show="userIsWorkspaceAdmin" class="text-sm py-3 px-3 text-zinc-500">
                  <MemberListDropdown :username="member.username"></MemberListDropdown>
                </td>
              </tr>
            </table>
          </div>

          <div v-show="showError" class="w-full flex justify-center">
            <ErrorMessage error-message="Failed to load members. Try again!"></ErrorMessage>
          </div>

        </div>
        <div v-show="inviteUserModalOpen" class="absolute left-0 top-1/3 w-full flex justify-center align-middle text-xs">
          <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
            <div>
              <h3 class="text-zinc-900 font-medium text-sm mb-2">Invite people to the workspace</h3>
            </div>
            <p class="text-zinc-500 mb-4">Copy the following link to and send it to your team mates.</p>
            <div class="w-full my-4"><input disabled v-model="inviteCode" type="text" class="w-full border border-zinc-300 rounded px-2 py-1 text-xs"></div>
            <div class="float-right">
              <button
                class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                @click="toggleInviteUserModal">Back</button>
            </div>
          </div>
          <div v-show="inviteUserModalOpen" @click="toggleInviteUserModal" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script lang="ts">

import { WorkspaceUser } from "~~/types/WorkspaceUser";
import { GetWorkspaceInviteCodeResponse } from "~~/types/GetWorkspaceInviteCodeResponse";

export default {
  data() {
    return {
      members: [],
      inviteCode: "Retrieving the code failed... Please reload the page!",
      showError: false,
      userIsWorkspaceAdmin: false,
      inviteUserModalOpen: false
    }
  },
  async beforeMount() {
    //check if user is admin
    this.userIsWorkspaceAdmin = await useIsWorkspaceAdmin();
    const user = useUserState();

    const getWorkspaceMembers = await useFetchAuth(
      'http://localhost:8000/workspace/users', {
        method: 'GET',
      params: {
        workspace_id: user.value.workspaces[0]._id
      }
    }
    ).then((data: WorkspaceUser[]) => {
      this.members = data;
    }).catch((error) => {
      console.log(error);
      this.showError = true;
    });

    const getInviteCode = await useFetchAuth(
      'http://localhost:8000/workspace/inviteCode', {
        method: 'GET',
      params: {
        workspace_id: user.value.workspaces[0]._id
      }
    }
    ).then((data: GetWorkspaceInviteCodeResponse) => {
      this.inviteCode = data.invite_code;
    }).catch((error) => {
      console.log(error);
    });


  },
  computed: {
    getRandomColor() {
      const colors = [
        "bg-green-400",
        "bg-sky-400",
        "bg-amber-400"
      ];
      const randomIndex = Math.floor(Math.random() * colors.length);
      return colors[randomIndex];
    }
  },
  methods: {
    toggleInviteUserModal() {
      if (this.inviteUserModalOpen) {
        this.inviteUserModalOpen = false;
      } else {
        this.inviteUserModalOpen = true;
      }
    }
  }
}
</script>
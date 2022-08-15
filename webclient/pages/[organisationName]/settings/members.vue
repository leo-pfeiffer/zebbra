<script setup lang="ts">
definePageMeta({
  middleware: ["auth", "route-check"]
})
</script>

<template>
  <NuxtLayout name="settings-layout">
    <div class="container">
      <div class="mt-8 px-2 sm:px-[10%] lg:px-[15%]">
        <button v-show="userIsWorkspaceAdmin" @click="toggleInviteUserModal"
          class="float-right mt-4 bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"><i
            class="bi bi-person-plus-fill mr-1"></i>Invite members</button>
        <h1 class="text-2xl my-1 font-medium text-zinc-900">Members</h1>
        <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage the members within your workspace</p>
        <div class="py-6">
          <div class="px-1">
            <table class="w-full text-xs text-left table-auto">

              <tr v-for="member in members" class="border-b border-zinc-300 last:border-0">
                <td class="py-4 px-3 text-zinc-900">
                  <Avatar :margin="true" :first-name="member.first_name" :last-name="member.last_name"></Avatar>
                  <div class="inline-block align-middle"><span>{{ member.first_name }} {{ member.last_name }}</span>
                  </div>
                </td>
                <td class="py-4 px-3 text-zinc-500">{{ member.username }}</td>
                <td class="py-4 px-3 text-zinc-500">{{ member.user_role }}</td>
                <td v-show="userIsWorkspaceAdmin" class="text-base py-4 px-3 text-zinc-500">
                  <MemberListDropdown :user-id="member._id" :username="member.username"
                    v-show="(member._id != piniaUserStore._id)"></MemberListDropdown>
                </td>
              </tr>
            </table>
          </div>
          <div v-show="showError" class="w-full flex justify-center">
            <ErrorMessage error-message="Failed to load members. Try again!"></ErrorMessage>
          </div>

        </div>
        <Teleport to="body">
          <div v-show="inviteUserModalOpen"
            class="absolute left-0 top-1/3 w-full flex justify-center align-middle text-xs">
            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
              <div>
                <h3 class="text-zinc-900 font-medium text-sm mb-2">Invite people to the workspace</h3>
              </div>
              <p class="text-zinc-500 mb-4">Copy the following link to and send it to your team mates.</p>
              <div class="w-full my-4"><input disabled v-model="inviteCode" type="text"
                  class="w-full border border-zinc-300 rounded px-2 py-1 text-xs"></div>
              <div class="float-right">
                <button
                  class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                  @click="toggleInviteUserModal">Back</button>
              </div>
            </div>
            <div v-show="inviteUserModalOpen" @click="toggleInviteUserModal"
              class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50">
            </div>
          </div>
        </Teleport>
      </div>
    </div>
  </NuxtLayout>
</template>

<script lang="ts">

import { mapState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
import { useFetchAuth } from "~~/methods/useFetchAuth";
import { WorkspaceUser } from "~~/types/WorkspaceUser";
import { GetWorkspaceInviteCodeResponse } from "~~/types/GetWorkspaceInviteCodeResponse";
import { useIsWorkspaceAdmin } from '~~/methods/useIsWorkspaceAdmin';

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

    try {
      await this.updatePiniaUserStore()
    } catch(e) {
      console.log(e);
    }

    //check if user is admin
    this.userIsWorkspaceAdmin = await useIsWorkspaceAdmin();

    const getWorkspaceMembers = await useFetchAuth(
      '/workspace/users', {
      method: 'GET',
      params: {
        workspace_id: this.piniaUserStore.workspaces[0]._id
      }
    }
    ).then((data: WorkspaceUser[]) => {
      this.members = data;
    }).catch((error) => {
      console.log(error);
      this.showError = true;
    });

    if (this.userIsWorkspaceAdmin) {
      const getInviteCode = await useFetchAuth(
        '/workspace/inviteCode', {
        method: 'POST',
        params: {
          workspace_id: this.piniaUserStore.workspaces[0]._id
        }
      }
      ).then((data: GetWorkspaceInviteCodeResponse) => {
        this.inviteCode = data.invite_code;
      }).catch((error) => {
        console.log(error);
      });

    }
  },
  computed: {
    ...mapState(useUserStore, ['piniaUserStore']),
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
    ...mapActions(useUserStore, ['updatePiniaUserStore']),
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
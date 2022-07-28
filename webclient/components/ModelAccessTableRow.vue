<script setup>

const userState = useUserState();
</script>

<template>
    <tr class="border-b border-zinc-300 last:border-0">
        <td class="py-2 text-zinc-900">{{ user.first_name }} {{ user.last_name }}</td>
        <td class="py-2 px-2 text-zinc-500">{{ user.username }}</td>
        <td class="py-2 px-2 text-zinc-500">
            <span class="pl-1" v-if="user.user_role === 'Admin' && user._id === userState._id">Admin</span>
            <span class="pl-1" v-else-if="user._id === userState._id">{{user.user_role}}</span>
            <div v-else>
                <select v-model="roleSelected">
                    <option>Admin</option>
                    <option>Editor</option>
                    <option>Viewer</option>
                </select>
            </div>
        </td>
        <td class="py-2 px-2">
            <button v-if="!(user._id === userState._id)" @click="$emit('grantAccess', user._id, roleSelected)" class="font-medium text-xs text-green-600">Update</button>
        </td>
        <td class="py-2 px-2">
            <button v-if="!(user._id === userState._id)" @click="$emit('revokeAccess', user._id, roleSelected)" class="font-medium text-xs text-red-600">Remove</button>
        </td>
    </tr>
</template>

<script>
export default {
    data() {
        return {
            roleSelected: ""
        }
    },
    props: {
        user: Object
    },
    mounted () {
        this.roleSelected = this.user.user_role;
    },
    watch: {
        user: function(newVal, oldVal) {
            this.roleSelected = newVal.user_role;
        }
    }
}
</script>
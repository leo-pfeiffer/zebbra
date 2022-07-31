<template>
    <div class="relative align-middle">
        <div class="inline-block align-middle">
            <div class="">
                <h1 class="font-semibold text-xl inline-block align-middle text-zinc-900">{{sheetName}}</h1>
                <p class="text-xs text-zinc-500">{{ workspaceName }} / {{ modelName }}
                </p>
            </div>
        </div>
        <div class="float-right h-full pt-2 pr-2">
            <div class="text-xs">
                <span class="mr-2 text-[10px] uppercase rounded border border-zinc-300 px-1 py-0.5 text-zinc-500 bg-zinc-50">{{userType}}</span><NuxtLink :to="`/${workspaceName}/settings/profile`"><Avatar :firstName="user.first_name" :lastName="user.last_name"></Avatar></NuxtLink>
            </div>
        </div>
    </div>
</template>

<script lang="ts">

import { GetUserResponse } from "~~/types/GetUserResponse"
import { ModelMeta } from "~~/types/Model"
    export default {
        props: {
            sheetName:String,
            workspaceName: String,
            modelName: String,
            user: Object as () => GetUserResponse,
            modelMeta: Object as () => ModelMeta
        },
        computed: {
            userType() {
                if(this.modelMeta.admins.includes(this.user._id)) {
                    return "Admin";
                } else if(this.modelMeta.editors.includes(this.user._id)) {
                    return "Editor";
                } else {
                    return "Viewer";
                }
            }
        },
        
    }
</script>
<script setup lang="ts">
import { useFetchAuth } from '~~/methods/useFetchAuth';
import { useToken } from '~~/methods/useToken';
import { GetIntegrationProvidersResponse } from '~~/types/GetIntegrationProvidersResponse';

definePageMeta({
    middleware: ["auth", "route-check"]
})
</script>

<template>
    <NuxtLayout name="settings-layout">
        <div class="container">
            <div class="mt-8 px-4 sm:px-[20%] lg:px-[30%]">
                <h1 class="text-2xl my-1 font-medium text-zinc-900">Integrations</h1>
                <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Sync your accounting and payroll tools
                    with Zebbra to save time and have more accurate models.</p>
                <div class="py-6">
                    <h2 class="text-xl text-zinc-900 mb-2">Accounting</h2>
                    <p class="text-xs text-zinc-500">Connect your favorite accounting tools and access all accouting
                        data within your models.</p>
                    <div class="w-full border border-zinc-300 rounded py-5 px-4 mt-5">
                        <div class="flex align-middle max-h-fit mb-3">
                            <div><img src="~~/assets/img/xero_logo.png" alt="Xero accounting logo" width="19px"
                                    height="19px"></div>
                            <div class="font-medium text-zinc-900 text-xs ml-1.5 flex align-middle py-0.5">
                                <div><span class="mr-2">Connect Zebbra with Xero Accounting</span><span
                                        v-if="piniaXeroStore.connected && !piniaXeroStore.requires_reconnect"
                                        class="text-[10px] uppercase bg-green-500 text-neutral-50 px-1 py-0.5 rounded">Connected</span>
                                    <span v-else-if="piniaXeroStore.requires_reconnect"
                                        class="text-[10px] uppercase bg-red-500 text-neutral-50 px-1 py-0.5 rounded">Reconnect</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex text-xs text-left">
                            <div class="text-zinc-500 mr-3">
                                Once you connected Xero, you will be able to add your actual accounting data such as
                                revenues, profits or cost centers to both the revenues as well as cost models.
                            </div>
                            <div class="min-w-fit">
                                <button type="button" v-if="!piniaXeroStore.connected || piniaXeroStore.requires_reconnect"
                                    @click="connectXero"
                                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700">Connect
                                    Xero</button>
                                <button v-else @click="toggleXeroDisconnectModal"
                                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-red-600">Disconnect
                                    Xero</button>
                            </div>
                        </div>
                    </div>
                    <Teleport to="body">
                        <div v-show="disconnectXeroModalOpen"
                            class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
                            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                                <div>
                                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to disconnect
                                        Xero?</h3>
                                </div>
                                <p class="text-zinc-500 text-xs mb-3">Disconnecting it might break models that use
                                    integration values from Xero.</p>
                                <div class="float-right">
                                    <button
                                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                                        @click="toggleXeroDisconnectModal">Cancel</button>
                                    <button class="ml-2 bg-red-600  drop-shadow-sm
                                            shadow-zinc-50 text-xs font-medium px-2 py-1 
                                            border border-red-500 rounded text-neutral-100"
                                        @click="disconnectIntegration('Xero'); toggleXeroDisconnectModal()">Disconnect</button>
                                </div>
                            </div>
                        </div>
                        <div v-show="disconnectXeroModalOpen" @click="toggleXeroDisconnectModal"
                            class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
                    </Teleport>
                </div>
                <div class="py-4">
                    <h2 class="text-xl text-zinc-900 mb-2">Payroll</h2>
                    <p class="text-xs text-zinc-500">Connect your favorite payroll and HR tools and access all payroll
                        and employee data within your models.</p>
                    <div class="w-full border border-zinc-300 rounded py-5 px-4 mt-5">
                        <div class="flex align-middle max-h-fit mb-3">
                            <div><img src="~~/assets/img/gusto_logo.png" alt="Gusto payroll logo" width="19px"
                                    height="19px"></div>
                            <div class="font-medium text-zinc-900 text-xs ml-1.5 flex align-middle py-0.5">
                                <div><span class="mr-2">Connect Zebbra with Gusto</span><span
                                        v-if="piniaGustoStore.connected && !piniaGustoStore.requires_reconnect"
                                        class="text-[10px] uppercase bg-green-500 text-neutral-50 px-1 py-0.5 rounded">Connected</span>
                                    <span v-else-if="piniaGustoStore.requires_reconnect"
                                        class="text-[10px] uppercase bg-red-500 text-neutral-50 px-1 py-0.5 rounded">Reconnect</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex text-xs text-left">
                            <div class="text-zinc-500 mr-3">
                                Once you connected Gusto, Zebbra will automatically add all your existing employees to
                                the cost model. You will still be able to add new employees to take future hires into
                                account.
                            </div>
                            <div class="min-w-fit">
                                <button type="button" v-if="!piniaGustoStore.connected || piniaGustoStore.requires_reconnect"
                                    @click="connectGusto"
                                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700">Connect
                                    Gusto</button>
                                <button v-else @click="toggleGustoDisconnectModal"
                                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-red-600">Disconnect
                                    Gusto</button>
                            </div>
                        </div>
                    </div>
                    <Teleport to="body">
                        <div v-show="disconnectGustoModalOpen"
                            class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
                            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                                <div>
                                    <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to disconnect
                                        Gusto?</h3>
                                </div>
                                <p class="text-zinc-500 text-xs mb-3">Disconnecting it might break models that use
                                    integration values from Gusto.</p>
                                <div class="float-right">
                                    <button
                                        class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                                        @click="toggleGustoDisconnectModal">Cancel</button>
                                    <button class="ml-2 bg-red-600  drop-shadow-sm
                                            shadow-zinc-50 text-xs font-medium px-2 py-1 
                                            border border-red-500 rounded text-neutral-100"
                                        @click="disconnectIntegration('Gusto'); toggleGustoDisconnectModal()">Disconnect</button>
                                </div>
                            </div>
                        </div>
                        <div v-show="disconnectGustoModalOpen" @click="toggleGustoDisconnectModal"
                            class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
                    </Teleport>
                </div>
                <div class="pt-4 pb-8">
                    <h2 class="text-xl text-zinc-900 mb-2">Custom</h2>
                    <p class="text-xs text-zinc-500">Create an integration into any other accounting or payroll
                        software.</p>
                    <div class="w-full border border-zinc-300 rounded py-5 px-4 mt-5">
                        <div class="flex align-middle max-h-fit mb-3">
                            <div><i class="bi bi-plug-fill text-sky-600"></i></div>
                            <div class="font-medium text-zinc-900 text-xs ml-1.5 flex align-middle py-0.5">
                                <div>Use the Zebbra API to integrate with any software</div>
                            </div>
                        </div>
                        <div class="flex text-xs text-left">
                            <div class="text-zinc-500 mr-3">
                                Due to its open API Zebbra allows you to build custom integrations to any other
                                accounting or payroll software very easily.
                            </div>
                            <div class="min-w-fit">
                                <NuxtLink to="https://leo-pfeiffer.github.io/zebbra/add_integration/" target="_blank"
                                    class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700">
                                    Learn
                                    more <i class="bi bi-arrow-up-right"></i></NuxtLink> <!-- todo: link -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <SheetErrorMessages v-if="(errorMessages.length > 0)" :errorMessages="errorMessages"
                @close="closeErrorMessage"></SheetErrorMessages>
            <SheetSuccessMessages v-if="(successMessages.length > 0)" :successMessages="successMessages"
                @close="closeSuccessMessage"></SheetSuccessMessages>
        </div>
    </NuxtLayout>
</template>

<script lang="ts">

import { mapWritableState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
import { useIntegrationStore } from '~~/store/useIntegrationStore';

export default {
    data() {
        return {
            disconnectXeroModalOpen: false,
            disconnectGustoModalOpen: false,
            successMessages: [],
            errorMessages: [],
        }
    },
    async beforeMount() {

        try {
            await this.updatePiniaUserStore();
            await this.updatePiniaIntegrationStore(this.piniaUserStore.workspaces[0]._id);
        } catch (e) {
            console.log(e);
        }

    },
    computed: {
        ...mapWritableState(useUserStore, ['piniaUserStore']),
        ...mapWritableState(useIntegrationStore, ['piniaXeroStore']),
        ...mapWritableState(useIntegrationStore, ['piniaGustoStore']),
    },
    methods: {
        ...mapActions(useUserStore, ['updatePiniaUserStore']),
        ...mapActions(useIntegrationStore, ['updatePiniaIntegrationStore']),
        toggleXeroDisconnectModal() {
            if (this.disconnectXeroModalOpen === false) {
                this.disconnectXeroModalOpen = true;
            } else {
                this.disconnectXeroModalOpen = false;
            }
        },
        toggleGustoDisconnectModal() {
            if (this.disconnectGustoModalOpen === false) {
                this.disconnectGustoModalOpen = true;
            } else {
                this.disconnectGustoModalOpen = false;
            }
        },
        closeErrorMessage(index: number) {
            this.errorMessages.splice(index, 1)
        },
        closeSuccessMessage(index: number) {
            this.successMessages.splice(index, 1)
        },
        connectXero() {

            const accessToken = useToken().getToken();

            var w = window.open(`${this.$config.public.backendUrlBase}/integration/xero/login?workspace_id=${this.piniaUserStore.workspaces[0]._id}&access_token=${accessToken}`, "_blank");

            const timer = setInterval(() => {
                if (w.closed) {
                    clearInterval(timer);
                    this.updatePiniaIntegrationStore(this.piniaUserStore.workspaces[0]._id);
                }
            })
        },
        connectGusto() {

            const accessToken = useToken().getToken();

            var w = window.open(`${this.$config.public.backendUrlBase}/integration/gusto/login?workspace_id=${this.piniaUserStore.workspaces[0]._id}&access_token=${accessToken}`, "_blank");

            const timer = setInterval(() => {
                if (w.closed) {
                    clearInterval(timer);
                    this.updatePiniaIntegrationStore(this.piniaUserStore.workspaces[0]._id);
                }
            })
        },
        async disconnectIntegration(integrationName: string) {
            try {
                await useFetchAuth(
                    '/integration/disconnect', {
                    method: 'POST',
                    params: {
                        workspace_id: this.piniaUserStore.workspaces[0]._id,
                        integration: integrationName
                    }
                }
                ).then((data) => {
                    this.successMessages.push(integrationName + " successfully disconnected!")
                    this.updatePiniaIntegrationStore(this.piniaUserStore.workspaces[0]._id);
                })
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try again.")
            }
        }
    }
}

</script>
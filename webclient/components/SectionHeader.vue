<template>

    <div
        class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-l border-t">
        <span class="font-medium" v-if="!changingEnabled">
        <i v-if="sectionName === 'Payroll'" class="text-zinc-500 bi bi-people-fill -ml-1 mr-2"></i>
        <i v-else-if="sectionName === 'Cost of Goods Sold'" class="text-zinc-500 bi bi-wallet-fill -ml-1 mr-2"></i>
        <i v-else-if="sectionName === 'Operational Costs'" class="text-zinc-500 bi bi-hammer -ml-1 mr-2"></i>
        <i v-else-if="sectionName === 'Other Costs'" class="text-zinc-500 bi bi-layers-fill -ml-1 mr-2"></i>
        {{sectionName }}</span>
        <span class="font-medium hover:underline hover:decoration-sky-600" v-if="!sectionNameChangeSelected && changingEnabled"
            @dblclick="toggleSectionNameChange">
            <li class="marker:text-zinc-500">{{ sectionName }}</li>
        </span>
        <span v-else-if="sectionNameChangeSelected && changingEnabled">
            <input :ref="`section-name-${sectionIndex}`"
                @keydown.enter="$emit('changeSectionName', sectionIndex, sectionNameInput); toggleSectionNameChange()"
                @keydown.esc="toggleSectionNameChange()" v-model="sectionNameInput"
                class="bg-zinc-100/0 focus:border-b border-sky-600 focus:outline-none placeholder:text-zinc-500"
                type="text" placeholder="Change Section name"></span>
        <span v-if="changingEnabled && !userIsViewer" class="ml-2 hidden group-hover:block text-[10px]"><button
                @click="toggleSectionDeleteModal"><i title="Delete section"
                    class="bi bi-x-lg text-zinc-500 hover:text-zinc-700"></i></button></span>
        <Teleport to="body">
            <div v-if="changingEnabled && !userIsViewer" v-show="deleteSectionModalOpen"
                class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
                <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
                    <div>
                        <h3 class="text-zinc-900 font-medium text-sm mb-2">Do you really want to delete this section?
                        </h3>
                    </div>
                    <p class="text-zinc-500 text-xs mb-3">Deleting <b>{{ sectionName }}</b> cannot be undone.</p>
                    <div class="float-right">
                        <button
                            class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                            @click="toggleSectionDeleteModal">Cancel</button>
                        <button class="ml-2 bg-red-600  drop-shadow-sm
                                                        shadow-zinc-50 text-xs font-medium px-2 py-1 
                                                        border border-red-500 rounded text-neutral-100"
                            @click="$emit('deleteSection', sectionIndex), toggleSectionDeleteModal()">Delete</button>
                    </div>
                </div>
                <div v-show="deleteSectionModalOpen" @click="toggleSectionDeleteModal"
                    class="fixed top-0 left-0 w-[100vw] h-[100vh] z-40 bg-zinc-100/50">
                </div>
            </div>
        </Teleport>
    </div>

</template>


<script>
export default {
    data() {
        return {
            sectionNameInput: "",
            sectionNameChangeSelected: false,
            deleteSectionModalOpen: false
        }
    },
    props: {
        sectionIndex: Number,
        sectionName: String,
        changingEnabled: Boolean,
        userIsViewer: Boolean
    },
    mounted () {
        if(this.sectionName === "") {
            this.sectionNameChangeSelected = true;
        } else {
            this.sectionNameChangeSelected = false;
        }
    },
    methods: {
        toggleSectionNameChange() {
            if (!this.sectionNameChangeSelected && !this.userIsViewer) {
                this.sectionNameChangeSelected = true;
            } else {
                this.sectionNameChangeSelected = false;
            }

            if(this.sectionNameChangeSelected) {
                setTimeout(() => {
                    this.$refs[`section-name-${this.sectionIndex}`].focus();
                }, 50)
            }
        },
        toggleSectionDeleteModal() {
            if (!this.deleteSectionModalOpen && !this.userIsViewer) {
                this.deleteSectionModalOpen = true;
            } else {
                this.deleteSectionModalOpen = false;
            }
        }
    }
}


</script>
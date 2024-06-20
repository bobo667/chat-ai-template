<template>
  <div>
    <!-- Sidebar -->
    <aside class="flex menu">
      <div
        class="flex h-[100svh] w-60 flex-col overflow-y-auto bg-slate-50 pt-8 dark:border-slate-700 dark:bg-slate-900 sm:h-[100vh] sm:w-64"
      >
        <div class="flex px-4">
          <!-- Logo -->
          <logo-icon />
          <h2 class="px-5 text-lg font-medium text-slate-800 dark:text-slate-200">
            Chats
            <span class="mx-2 rounded-full bg-blue-600 px-2 py-1 text-xs text-slate-200"
              >6</span
            >
          </h2>
        </div>
        <div class="mx-2 mt-8">
          <button
            class="flex w-full gap-x-4 rounded-lg border border-slate-300 p-4 text-left text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <add-icon />
            New Chat
          </button>
        </div>
        <!-- Previous chats container -->
        <div
          class="h-2/3 space-y-4 overflow-y-auto border-b border-slate-300 px-2 py-4 dark:border-slate-700"
        >
          <button
            class="flex w-full flex-col gap-y-2 rounded-lg px-3 py-2 text-left transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:hover:bg-slate-800"
          >
            <h1 class="text-sm font-medium capitalize text-slate-700 dark:text-slate-200">
              Tailwind Classes
            </h1>
            <p class="text-xs text-slate-500 dark:text-slate-400">12 Mar</p>
          </button>
        </div>
        <div class="mt-3 w-full space-y-4 px-2 py-4">
          <button
            class="flex w-full gap-x-2 rounded-lg px-3 py-2 text-left text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:text-slate-200 dark:hover:bg-slate-800"
          >
          <user-logo/>
            User
          </button>
          <button
            @click="openSetting"
            class="flex w-full gap-x-2 rounded-lg px-3 py-2 text-left text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:text-slate-200 dark:hover:bg-slate-800"
          >
          <setting-icon />
            Settings
          </button>
        </div>
      </div>
    </aside>
  </div>
</template>

<script>
import UserLogo from '@/components/icon/user-icon.vue';
import SettingIcon from '@/components/icon/setting-icon.vue';
import AddIcon from '@/components/icon/add-icon.vue';
import LogoIcon from '@/components/icon/logo-icon.vue';
import { EventBus } from '@/util/eventBus';

export default {
	name: 'Menu',
	components: {
		LogoIcon, AddIcon, UserLogo, SettingIcon,
	},
	data() {
		return {
			// Your data properties here
		};
	},
	methods: {
		openSetting() {
			EventBus.$emit( 'openSetting' );
		},
		// Your methods here
	},
	mounted() {
		// Code to run when the component is mounted
	},
};
</script>

<style scoped>
/* Your CSS styles here */
.menu {
  height: 100vh;
}
</style>

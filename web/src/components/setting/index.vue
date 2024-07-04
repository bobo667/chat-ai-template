<template>
  <div class="flex flex-row-reverse">
    <!-- Sidebar -->
    <aside class="flex">
      <div
        class="relative h-screen w-60 overflow-y-auto border-l border-slate-300 bg-slate-50 py-8 dark:border-slate-700 dark:bg-slate-900 sm:w-64"
      >
        <div
          class="mb-4 flex items-center gap-x-2 px-2 text-slate-800 dark:text-slate-200"
        >
          <button @click="close" class="inline-flex rounded-lg p-1 hover:bg-slate-700">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z"
              ></path>
              <path d="M9 4v16"></path>
              <path d="M14 10l2 2l-2 2"></path>
            </svg>
            <span class="sr-only">Close settings sidebar</span>
          </button>
          <h2 class="text-lg font-medium">Settings</h2>
        </div>


        <!-- More Settings -->
        <div
          class="my-4 border-t border-slate-300 px-2 py-4 text-slate-800 dark:border-slate-700 dark:text-slate-200"
        >
          <label class="px-2 text-xs uppercase text-slate-500 dark:text-slate-400"
          >Advanced</label
          >

          <label
            for="select-model"
            class="mb-2 mt-4 block px-2 text-sm font-medium"
          >Model</label
          >
          <select
            name="select-model"
            id="select-model"
            @change="($event) => save('model',$event.target.value)"
            :value="config.model.config_value"
            class="block w-full cursor-pointer rounded-lg border-r-4 border-transparent bg-slate-200 py-3 pl-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-600 dark:bg-slate-800 dark:placeholder-slate-400 dark:focus:ring-blue-600"
          >
            <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
            <option value="gpt-4o">gpt-4o</option>
          </select>

          <label for="max-tokens" class="mb-2 mt-4 block px-2 text-sm font-medium"
          >Temperature</label
          >
          <input
            type="number"
            id="max-tokens"
            :value="config.temperature.config_value"
            @blur="($event) => save('temperature',$event.target.value)"
            class="block w-full rounded-lg bg-slate-200 p-2.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-600 dark:bg-slate-800 dark:placeholder-slate-400 dark:focus:ring-blue-600"
            :placeholder="config.temperature.config_value"
          />
        </div>
      </div>
    </aside>
  </div>
</template>
<script>
import { querySysConfig, saveConfig } from '@/api/sysConfig';

export default {
	name: 'Setting',
	components: {},
	data() {
		return {
			config: {
				model: {
					config_code: 'llm_model',
					config_value: 'gpt-3.5-turbo',
				},
				temperature: {
					config_code: 'llm_temperature',
					config_value: '0.2',
				},
			},
		};
	},
	computed: {},
	mounted() {
		this.querySysConfig( 'model' );
		this.querySysConfig( 'temperature' );
	},
	methods: {
		querySysConfig( key ) {
			querySysConfig( this.config[key].config_code ).then( ( res ) => {
				if ( res.data ) {
					this.config[key].config_value = res.data;
				}
			} );
		},
		save( key, val ) {
			this.config[key].config_value = val;
			saveConfig( this.config[key] ).then( ( res ) => {
				this.$message.success( '修改成功' );
			} );
		},
		close() {
			this.$emit( 'close' );
		},
	},
};
</script>

<template>
  <div class="contents">
    <!-- Prompt Messages Container - Modify the height according to your need -->
    <div class="flex overflow-y-auto w-full flex-col half-screen-height">
      <!-- Prompt Messages -->
      <div
        class="flex-1 space-y-6 overflow-y-auto rounded-xl bg-slate-200 p-4 text-sm leading-6 text-slate-900 shadow-sm dark:bg-slate-900 dark:text-slate-300 sm:text-base sm:leading-7"
      >
        <div
          :class="
            'flex ' + (item.role === 'user' ? 'flex-row-reverse' : '') + ' items-start'
          "
          v-for="item in messageList"
        >
          <img class="mr-2 h-8 w-8 rounded-full" :src="imgInfo[item.role]" />
          <div
            class="flex rounded-b-xl rounded-tr-xl bg-slate-50 p-4 dark:bg-slate-800 sm:max-w-md md:max-w-2xl"
          >
            <p>{{ item.content }}</p>
          </div>
          <div
            v-if="item.role === 'assistant'"
            class="mr-2 mt-1 flex flex-col-reverse gap-2 text-slate-500 sm:flex-row"
          >
            <button class="hover:text-blue-600" type="button">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                <path
                  d="M8 8m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z"
                ></path>
                <path
                  d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Prompt message input -->
    <promptInput @send="send"/>
  </div>
</template>

<script>
import promptInput from '../proment-input/index.vue';

export default {
	components: { promptInput },
	name: 'Index',
	data() {
		return {
			imgInfo: {
				user: 'https://dummyimage.com/128x128/363536/ffffff&text=U',
				assistant: 'https://dummyimage.com/128x128/354ea1/ffffff&text=AI',
			},
			formData: {


			},
			messageList: [
				// {
				//   content: "Explain quantum computing in simple terms",
				//   role: "user",
				// },
				// {
				//   content:
				//     "Certainly! Quantum computing is a new type of computing that relies on the principles of quantum physics. Traditional computers, like the one you might be using right now, use bits to store and process information. These bits can represent either a 0 or a 1. In contrast, quantum computers use quantum bits, or qubits.Unlike bits, qubits can represent not only a 0 or a 1 but also a superposition of both states simultaneously. This means that a qubit can be in multiple states at once, which allows quantum computers to perform certain calculations much faster and more efficiently",
				//   role: "assistant",
				// },
				// {
				//   content: "Explain quantum computing in simple terms",
				//   role: "user",
				// },
			],
		};
	},
	methods: {
		send() {

		},
		// Your component methods go here
	},
	mounted() {
		// Code to run when the component is mounted goes here
	},
};
</script>

<style scoped>
.half-screen-height {
  height: 74vh;
}

</style>

<template>
  <transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-100"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="show" class="fixed bottom-6 right-6 z-50 w-full max-w-lg overflow-hidden rounded-xl bg-white shadow-2xl ring-1 ring-black ring-opacity-5 transition-all transform">
      <div class="p-5">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg v-if="type === 'success'" class="h-8 w-8 text-emobilio-green" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true">
               <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0z" />
               <path stroke-linecap="round" stroke-linejoin="round" d="M12 15.75h.005v.005H12v-.005z" />
            </svg>
          </div>
          <div class="ml-4 w-0 flex-1 pt-0.5">
            <p class="text-lg font-bold text-emobilio-navy">{{ title }}</p>
            <p class="mt-1 text-base text-emobilio-navy/70">{{ message }}</p>
          </div>
          <div class="ml-4 flex flex-shrink-0">
            <button type="button" @click="$emit('close')" class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
              <span class="sr-only">Schließen</span>
              <svg class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: Boolean,
  type: {
    type: String,
    default: 'success' // success, error
  },
  title: String,
  message: String
});
defineEmits(['close']);
</script>

<template>
  <Teleport to="body">
    <!-- Backdrop -->
    <transition
      enter-active-class="ease-out duration-300 transition-opacity"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="ease-in duration-200 transition-opacity"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="isOpen" class="fixed inset-0 bg-emobilio-navy/80 backdrop-blur-sm z-[100]" @click="close" aria-hidden="true"></div>
    </transition>

    <!-- Modal Container -->
    <transition
      enter-active-class="ease-out duration-300 transition-all transform"
      enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
      enter-to-class="opacity-100 translate-y-0 sm:scale-100"
      leave-active-class="ease-in duration-200 transition-all transform"
      leave-from-class="opacity-100 translate-y-0 sm:scale-100"
      leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
    >
      <div v-if="isOpen" class="fixed inset-0 z-[110] overflow-y-auto pointer-events-none" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          
          <!-- Trick to center modal -->
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
  
          <!-- Modal panel -->
          <div class="pointer-events-auto relative inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl sm:my-8 sm:align-middle sm:max-w-lg w-full border border-emobilio-navy/10">
            <div class="px-6 pt-6 pb-4 sm:px-8 sm:pt-8 sm:pb-6">
              <div class="flex items-start justify-between">
                  <div>
                      <h3 class="text-2xl leading-6 font-bold text-emobilio-navy" id="modal-title">
                      Prämie aktualisieren
                      </h3>
                      <p class="mt-2 text-sm text-emobilio-navy/60">
                      Dies setzt die Prämie für <span class="font-bold text-emobilio-navy">{{ selectedCount }}</span> ausgewählte Anträge fest.
                      </p>
                  </div>
                  <!-- Close button -->
                   <button @click="close" class="mt-1 flex-shrink-0 bg-white rounded-full p-2 text-emobilio-navy/40 hover:text-emobilio-navy hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emobilio-green transition-colors">
                      <span class="sr-only">Schließen</span>
                      <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                  </button>
              </div>

              <div class="mt-6">
                <div class="mb-4">
                  <label for="premium_amount" class="block text-sm font-semibold text-emobilio-navy mb-2">Neue Prämie (€)</label>
                  <div class="relative rounded-md shadow-sm">
                      <input 
                          type="text" 
                          id="premium_amount" 
                          v-model="premiumInput" 
                          @keyup.enter="save"
                          @input="formatInput"
                          class="block w-full px-4 py-3 border border-emobilio-navy/20 rounded-xl focus:ring-2 focus:ring-emobilio-green focus:border-emobilio-green sm:text-base text-emobilio-navy font-medium bg-gray-50 placeholder-emobilio-navy/30 transition-all" 
                          placeholder="z.B. 150.00 oder 150,00"
                      />
                       <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                          <span class="text-emobilio-navy/50 font-medium">€</span>
                       </div>
                  </div>
                   <p v-if="errorMsg" class="mt-2 text-sm text-red-600 flex items-center">
                       <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                       </svg>
                      {{ errorMsg }}
                   </p>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-6 py-4 sm:px-8 sm:flex sm:flex-row-reverse border-t border-emobilio-navy/5">
              <button 
                type="button" 
                @click="save"
                class="w-full inline-flex justify-center rounded-full border border-transparent shadow-lg shadow-emobilio-green/20 px-6 py-3 bg-emobilio-green text-base font-bold text-white hover:bg-[#00A8AD] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emobilio-green sm:ml-3 sm:w-auto sm:text-sm transition-all"
              >
                Prämie speichern
              </button>
              <button 
                type="button" 
                @click="close"
                class="mt-3 w-full inline-flex justify-center rounded-full border border-emobilio-navy/20 px-6 py-3 bg-white text-base font-bold text-emobilio-navy hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emobilio-navy sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-all"
              >
                Abbrechen
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>
  
  <script setup>
  import { ref, watch } from 'vue';
  
  const props = defineProps({
      isOpen: {
          type: Boolean,
          default: false
      },
      selectedCount: {
          type: Number,
          default: 0
      }
  });
  
  const emit = defineEmits(['close', 'save']);
  
  const premiumInput = ref('');
  const errorMsg = ref('');
  
  // Watch for modal opening to reset state
  watch(() => props.isOpen, (newVal) => {
      if (newVal) {
          premiumInput.value = '';
          errorMsg.value = '';
      }
  });

  const formatInput = (e) => {
      // Allow only numbers, comma, and period
      let val = e.target.value;
      val = val.replace(/[^0-9.,]/g, '');
      premiumInput.value = val;
  };
  
  const close = () => {
      emit('close');
  };
  
  const save = () => {
      errorMsg.value = '';
      if (!premiumInput.value || premiumInput.value.trim() === '') {
          errorMsg.value = 'Bitte geben Sie einen Wert ein.';
          return;
      }
  
      // Replace comma with period for parsing
      const cleanVal = premiumInput.value.replace(',', '.');
      const floatVal = parseFloat(cleanVal);
      
      if (isNaN(floatVal)) {
          errorMsg.value = 'Ungültiges Preisformat. Bitte eine Zahl eingeben.';
          return;
      }

      if (floatVal < 0) {
          errorMsg.value = 'Die Prämie kann nicht negativ sein.';
          return;
      }
  
      emit('save', floatVal);
  };
  </script>

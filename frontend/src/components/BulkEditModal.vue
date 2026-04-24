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
          
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
  
          <!-- Modal panel -->
          <div class="pointer-events-auto relative inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl sm:my-8 sm:align-middle sm:max-w-xl w-full border border-emobilio-navy/10">
            <div class="px-6 pt-6 pb-4 sm:px-8 sm:pt-8 sm:pb-6">
              <div class="flex items-start justify-between mb-2">
                  <div>
                      <h3 class="text-2xl leading-6 font-bold text-emobilio-navy" id="modal-title">
                        Stapelverarbeitung
                      </h3>
                      <p class="mt-2 text-sm text-emobilio-navy/60">
                        Dies überschreibt die aktivierten Felder für <span class="font-bold text-emobilio-navy">{{ selectedCount }}</span> ausgewählte Anträge. Nur markierte Felder werden geändert.
                      </p>
                  </div>
                   <button @click="close" class="bg-white rounded-full p-2 text-emobilio-navy/40 hover:text-emobilio-navy hover:bg-gray-100 transition-colors">
                      <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                  </button>
              </div>

              <div class="mt-8 space-y-6">
                 
                <!-- Status Toggle -->
                <div class="flex items-start bg-gray-50 p-4 rounded-xl border border-gray-100 hover:border-emobilio-navy/10 transition-colors">
                  <div class="flex items-center h-5 mt-1">
                      <input id="edit-status" type="checkbox" v-model="editFlags.status" class="w-5 h-5 text-emobilio-green border-gray-300 rounded focus:ring-emobilio-green transition-shadow cursor-pointer"/>
                  </div>
                  <div class="ml-4 flex-1 text-sm">
                      <label for="edit-status" class="font-bold text-emobilio-navy cursor-pointer block select-none" :class="{'opacity-50': !editFlags.status}">Status umstellen auf:</label>
                      <select v-model="formData.status" :disabled="!editFlags.status" class="mt-2 block w-full px-4 py-3 rounded-lg border border-emobilio-navy/10 bg-white text-emobilio-navy focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green font-medium transition-all disabled:opacity-50 disabled:bg-gray-100">
                      <option value="Fahrzeug registriert">Fahrzeug registriert</option>
                      <option value="Fahrzeug verifiziert">Fahrzeug verifiziert</option>
                      <option value="Fahrzeug erneut prüfen">Fahrzeug erneut prüfen</option>
                      <option value="Fahrzeug abgelehnt (kein Elektro)">Fahrzeug abgelehnt (kein Elektro)</option>
                      <option value="Fahrzeug braucht User Eingabe">Fahrzeug braucht User Eingabe</option>
                      <option value="Fahrzeug in Prüfung">Fahrzeug in Prüfung</option>
                      <option value="Fahrzeug bestätigt">Fahrzeug bestätigt</option>
                      <option value="Fahrzeug abgelehnt">Fahrzeug abgelehnt</option>
                      <option value="Zur Auszahlung offen">Zur Auszahlung offen</option>
                      <option value="Fahrzeug-Bonus ausgezahlt">Fahrzeug-Bonus ausgezahlt</option>
                      <option value="Auszahlungsanspruch verfallen">Auszahlungsanspruch verfallen</option>
                      <option value="Fahrzeug ignorieren(spam)">Fahrzeug ignorieren(spam)</option>
                      <option value="In Kündigung">In Kündigung</option>
                      <option value="Gekündigt">Gekündigt</option>
                      <option value="Fahrzeug-Entwurf">Fahrzeug-Entwurf</option>
                      </select>
                  </div>
                </div>

                <!-- Premium Toggle -->
                <div class="flex items-start bg-gray-50 p-4 rounded-xl border border-gray-100 hover:border-emobilio-navy/10 transition-colors">
                  <div class="flex items-center h-5 mt-1">
                      <input id="edit-premium" type="checkbox" v-model="editFlags.premium" class="w-5 h-5 text-emobilio-green border-gray-300 rounded focus:ring-emobilio-green transition-shadow cursor-pointer"/>
                  </div>
                  <div class="ml-4 flex-1 text-sm">
                      <label for="edit-premium" class="font-bold text-emobilio-navy cursor-pointer block select-none" :class="{'opacity-50': !editFlags.premium}">Prämie überschreiben (€):</label>
                      <div class="relative mt-2">
                        <input
                            type="text"
                            v-model="premiumInput"
                            @input="formatInput"
                            :disabled="!editFlags.premium"
                            class="block w-full px-4 py-3 rounded-lg border border-emobilio-navy/10 bg-white text-emobilio-navy focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green font-medium transition-all disabled:opacity-50 disabled:bg-gray-100"
                            placeholder="z.B. 150.00"
                        />
                        <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                            <span class="text-emobilio-navy/30 text-sm font-bold" :class="{'opacity-50': !editFlags.premium}">€</span>
                        </div>
                      </div>
                  </div>
                </div>

                <!-- Assigned User Toggle -->
                <div class="flex items-start bg-gray-50 p-4 rounded-xl border border-gray-100 hover:border-emobilio-navy/10 transition-colors">
                  <div class="flex items-center h-5 mt-1">
                      <input id="edit-assignee" type="checkbox" v-model="editFlags.assignee" class="w-5 h-5 text-emobilio-green border-gray-300 rounded focus:ring-emobilio-green transition-shadow cursor-pointer"/>
                  </div>
                  <div class="ml-4 flex-1 text-sm">
                      <label for="edit-assignee" class="font-bold text-emobilio-navy cursor-pointer block select-none" :class="{'opacity-50': !editFlags.assignee}">Bearbeiter-ID zuweisen:</label>
                      <input
                        type="number"
                        v-model="formData.assigned_user_id"
                        :disabled="!editFlags.assignee"
                        placeholder="Nicht zugewiesen"
                        class="mt-2 block w-full px-4 py-3 rounded-lg border border-emobilio-navy/10 bg-white text-emobilio-navy focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green font-medium transition-all disabled:opacity-50 disabled:bg-gray-100"
                      />
                  </div>
                </div>

                <!-- Payout Date Toggle -->
                <div class="flex items-start bg-gray-50 p-4 rounded-xl border border-gray-100 hover:border-emobilio-navy/10 transition-colors">
                  <div class="flex items-center h-5 mt-1">
                      <input id="edit-date" type="checkbox" v-model="editFlags.date" class="w-5 h-5 text-emobilio-green border-gray-300 rounded focus:ring-emobilio-green transition-shadow cursor-pointer"/>
                  </div>
                  <div class="ml-4 flex-1 text-sm">
                      <label for="edit-date" class="font-bold text-emobilio-navy cursor-pointer block select-none" :class="{'opacity-50': !editFlags.date}">Auszahlungsdatum setzen auf:</label>
                      <input
                        type="date"
                        v-model="formData.payout_date"
                        :disabled="!editFlags.date"
                        class="mt-2 block w-full px-4 py-3 rounded-lg border border-emobilio-navy/10 bg-white text-emobilio-navy focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green font-medium transition-all disabled:opacity-50 disabled:bg-gray-100"
                      />
                  </div>
                </div>

                 <p v-if="errorMsg" class="mt-4 text-sm font-bold text-red-600 flex items-center justify-center p-3 bg-red-50 rounded-xl">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                     </svg>
                    {{ errorMsg }}
                 </p>
              </div>
            </div>
            
            <div class="bg-gray-50 px-6 py-4 sm:px-8 sm:flex sm:flex-row-reverse border-t border-emobilio-navy/5">
              <button 
                type="button" 
                @click="save"
                class="w-full inline-flex justify-center rounded-full border border-transparent shadow-lg shadow-emobilio-green/20 px-6 py-3 bg-emobilio-green text-base font-bold text-white hover:bg-[#00A8AD] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emobilio-green sm:ml-3 sm:w-auto sm:text-sm transition-all"
              >
                {{ enabledCount > 0 ? `Ändere ${enabledCount} Feld(er) bei ${selectedCount} Anträgen` : 'Nichts ausgewählt' }}
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
import { ref, reactive, watch, computed } from 'vue';

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

const editFlags = reactive({
    status: false,
    premium: false,
    assignee: false,
    date: false
});

const premiumInput = ref('');
const errorMsg = ref('');

const formData = reactive({
    status: 'Fahrzeug registriert',
    assigned_user_id: null,
    payout_date: ''
});

const enabledCount = computed(() => {
    let count = 0;
    if (editFlags.status) count++;
    if (editFlags.premium) count++;
    if (editFlags.assignee) count++;
    if (editFlags.date) count++;
    return count;
});

watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        // Reset everything when opening
        editFlags.status = false;
        editFlags.premium = false;
        editFlags.assignee = false;
        editFlags.date = false;
        
        premiumInput.value = '';
        errorMsg.value = '';
        
        formData.status = 'Fahrzeug in Prüfung';
        formData.assigned_user_id = null;
        formData.payout_date = '';
    }
});

const formatInput = (e) => {
    let val = e.target.value;
    val = val.replace(/[^0-9.,]/g, '');
    premiumInput.value = val;
};

const close = () => {
    emit('close');
};

const save = () => {
    errorMsg.value = '';
    const payload = {};
    
    if (enabledCount.value === 0) {
        close();
        return;
    }

    // 1. Validate & Pack Status
    if (editFlags.status) {
        payload.status = formData.status;
    }

    // 2. Validate & Pack Premium
    if (editFlags.premium) {
        if (!premiumInput.value || premiumInput.value.trim() === '') {
            errorMsg.value = 'Prämie ist markiert, aber es fehlt ein Wert.';
            return;
        }
        const cleanVal = premiumInput.value.replace(',', '.');
        const floatVal = parseFloat(cleanVal);
        if (isNaN(floatVal)) {
            errorMsg.value = 'Ungültiges Preisformat bei Prämie.';
            return;
        }
        if (floatVal < 0) {
            errorMsg.value = 'Die Prämie kann nicht negativ sein.';
            return;
        }
        payload.premium_amount_cents = Math.round(floatVal * 100);
    }

    // 3. Pack Assignee
    if (editFlags.assignee) {
        payload.assigned_user_id = formData.assigned_user_id === '' ? null : formData.assigned_user_id;
    }

    // 4. Pack Date
    if (editFlags.date) {
        payload.payout_date = formData.payout_date === '' ? null : formData.payout_date;
    }

    emit('save', payload);
};
</script>

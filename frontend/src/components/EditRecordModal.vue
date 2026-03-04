<template>
  <div v-if="isOpen" class="relative z-50" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- Background backdrop -->
    <div class="fixed inset-0 bg-gray-500/75 transition-opacity" aria-hidden="true" @click="closeModal"></div>

    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <!-- Modal panel -->
        <div class="relative transform border-none rounded-3xl bg-white text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-2xl overflow-hidden">
          <div class="bg-emobilio-navy px-6 py-4 flex items-center justify-between">
            <h3 class="text-lg font-bold text-white flex items-center" id="modal-title">
              <span class="w-8 h-8 bg-emobilio-green rounded-lg flex items-center justify-center mr-3 text-sm shadow-md shadow-emobilio-green/20">e</span>
              Antrag #{{ record?.id }} bearbeiten
            </h3>
            <button @click="closeModal" class="text-white/60 hover:text-white transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="bg-white px-4 pt-5 pb-4 sm:p-8">
            <div class="space-y-8">
              <!-- Section: Status & Information -->
              <div>
                <h4 class="text-xs font-black text-emobilio-navy/40 uppercase tracking-widest mb-4">Status & Zuweisung</h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <!-- Status -->
                  <div class="space-y-1">
                    <label for="status" class="block text-sm font-bold text-emobilio-navy">Aktueller Status</label>
                    <select
                      id="status"
                      v-model="formData.status"
                      class="block w-full px-4 py-3 rounded-xl border border-emobilio-navy/10 bg-emobilio-bg/50 text-emobilio-navy focus:outline-none focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green transition-all font-medium sm:text-sm"
                    >
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

                  <!-- Assigned User -->
                  <div class="space-y-1">
                    <label for="user" class="block text-sm font-bold text-emobilio-navy">Bearbeiter (ID)</label>
                    <input
                      type="number"
                      id="user"
                      v-model="formData.assigned_user_id"
                      placeholder="Nicht zugewiesen"
                      class="block w-full px-4 py-3 rounded-xl border border-emobilio-navy/10 bg-emobilio-bg/50 text-emobilio-navy focus:outline-none focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green transition-all font-medium sm:text-sm"
                    />
                  </div>
                </div>
              </div>

              <!-- Section: Financial Details -->
              <div>
                <h4 class="text-xs font-black text-emobilio-navy/40 uppercase tracking-widest mb-4">Finanzielle Details</h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <!-- Premium -->
                  <div class="space-y-1">
                    <label for="premium" class="block text-sm font-bold text-emobilio-navy">Prämie (in Euro)</label>
                    <div class="relative">
                      <input
                        type="number"
                        step="0.01"
                        id="premium"
                        v-model="displayPremium"
                        class="block w-full px-4 py-3 rounded-xl border border-emobilio-navy/10 bg-emobilio-bg/50 text-emobilio-navy focus:outline-none focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green transition-all font-medium sm:text-sm"
                        placeholder="0,00"
                      />
                      <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                        <span class="text-emobilio-navy/30 text-sm font-bold">€</span>
                      </div>
                    </div>
                  </div>

                  <!-- Payout Date -->
                  <div class="space-y-1">
                    <label for="payout" class="block text-sm font-bold text-emobilio-navy">Auszahlungsdatum</label>
                    <input
                      type="date"
                      id="payout"
                      v-model="formData.payout_date"
                      class="block w-full px-4 py-3 rounded-xl border border-emobilio-navy/10 bg-emobilio-bg/50 text-emobilio-navy focus:outline-none focus:ring-2 focus:ring-emobilio-green/20 focus:border-emobilio-green transition-all font-medium sm:text-sm"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="bg-emobilio-bg/50 px-6 py-6 flex flex-col sm:flex-row-reverse gap-3 sm:px-8 border-t border-emobilio-navy/5">
            <button
              type="button"
              class="btn-primary w-full sm:w-auto"
              @click="save"
            >
              Änderungen Speichern
            </button>
            <button
              type="button"
              class="inline-flex w-full justify-center rounded-full border border-emobilio-navy/10 bg-white px-8 py-3 text-sm font-black text-emobilio-navy shadow-sm hover:bg-gray-50 focus:outline-none transition-all sm:w-auto"
              @click="closeModal"
            >
              Abbrechen
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, ref } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  record: Object
});

const emit = defineEmits(['close', 'save']);

const displayPremium = ref(null);

const formData = reactive({
  status: '',
  premium_amount_cents: null,
  payout_date: '',
  assigned_user_id: null
});

const formatDateForInput = (dateValue) => {
  if (!dateValue || dateValue === '01.01.0001' || dateValue === '0001-01-01') return '';
  
  // If it's a timestamp (number)
  if (typeof dateValue === 'number') {
    // Check if it's a very old date (like 0001-01-01)
    const date = new Date(dateValue);
    if (date.getFullYear() < 100) return '';
    return date.toISOString().split('T')[0];
  }
  
  // If it's already a string, try to parse it or return as is if it matches YYYY-MM-DD
  try {
    const date = new Date(dateValue);
    if (!isNaN(date.getTime())) {
      return date.toISOString().split('T')[0];
    }
  } catch (e) {
    console.error('Error parsing date:', e);
  }
  
  return dateValue;
};

watch(() => props.record, (newRecord) => {
  if (newRecord) {
    formData.status = newRecord.status || '';
    formData.premium_amount_cents = newRecord.premium_amount_cents;
    displayPremium.value = newRecord.premium_amount_cents ? newRecord.premium_amount_cents / 100 : null;
    formData.payout_date = formatDateForInput(newRecord.payout_date);
    formData.assigned_user_id = newRecord.assigned_user_id;
  }
}, { immediate: true });

const closeModal = () => {
  emit('close');
};

const save = () => {
  // Convert display Euro back to cents
  if (displayPremium.value !== null && displayPremium.value !== '') {
    formData.premium_amount_cents = Math.round(parseFloat(displayPremium.value) * 100);
  } else {
    formData.premium_amount_cents = null;
  }

  const payload = { ...formData, id: props.record.id };
  
  // Sanitize fields: convert empty strings to null for the backend
  if (payload.assigned_user_id === '') payload.assigned_user_id = null;
  if (payload.payout_date === '') payload.payout_date = null;

  emit('save', payload);
};
</script>

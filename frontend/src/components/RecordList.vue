<template>
  <div class="w-full">
    <div v-if="loading" class="text-center py-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Lade THG-Anträge...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
      <p class="font-bold">Fehler</p>
      <p>{{ error }}</p>
      <button @click="$emit('refresh')" class="mt-2 text-sm underline hover:text-red-800">Erneut versuchen</button>
    </div>

    <div v-else class="card-premium overflow-x-auto border-none shadow-none rounded-none">
      <table class="min-w-full divide-y divide-emobilio-navy/10">
        <thead class="bg-emobilio-navy text-white">
          <tr>
            <th v-for="header in visibleHeaders" :key="header.key" scope="col" class="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
              {{ header.label }}
            </th>
            <th scope="col" class="sticky right-0 bg-emobilio-navy px-6 py-4 z-10 border-l border-white/10">
              <span class="sr-only">Bearbeiten</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="record in records" :key="record.id" class="hover:bg-gray-50 transition-colors">
            <td v-for="header in visibleHeaders" :key="header.key" class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <template v-if="header.key === 'document_file' && record[header.key]?.url">
                <a :href="record[header.key].url" target="_blank" class="inline-flex items-center text-emobilio-green hover:text-[#00A8AD] font-bold border-b border-emobilio-green/30 hover:border-[#00A8AD] transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Ansehen
                </a>
              </template>
              <template v-else>
                {{ formatValue(record[header.key], header.key) }}
              </template>
            </td>
            <td class="sticky right-0 bg-white px-6 py-4 text-right text-sm font-medium shadow-[-10px_0_20px_-10px_rgba(0,43,73,0.1)] z-10 border-l border-emobilio-navy/5">
              <button @click="$emit('edit', record)" class="inline-flex items-center px-4 py-2 bg-emobilio-green text-white text-xs font-bold rounded-full hover:bg-[#00A8AD] hover:scale-105 active:scale-95 transition-all shadow-md shadow-emobilio-green/20 whitespace-nowrap">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                   <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
                Bearbeiten
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  records: Array,
  loading: Boolean,
  error: String
});

defineEmits(['edit', 'refresh']);

const columnMapping = {
  partner_id: 'Partner ID',
  external_reference: 'Externe Referenz',
  customer_number: 'Kundennummer',
  license_plate: 'Kennzeichen',
  holder_name: 'Fahrzeughalter',
  registration_date: 'Zulassungsdatum',
  vehicle_class: 'Fahrzeugklasse',
  vin: 'FIN',
  bonus_year: 'Bonusjahr',
  document_file: 'Fahrzeugschein',
  document_filename: 'Dateiname',
  status: 'Status',
  assigned_user_id: 'Zugewiesen an',
  agent_notes: 'Notizen',
  backend_reference: 'Backend Referenz',
  premium_amount_cents: 'Prämie',
  payout_date: 'Auszahlungsdatum',
  updated_at: 'Aktualisiert am'
};

const visibleHeaders = computed(() => {
  if (!props.records || props.records.length === 0) return [];
  
  // Get keys from the first record
  const keys = Object.keys(props.records[0]);
  
  // Filter out id and created_at, and map to German labels
  return keys
    .filter(key => key !== 'id' && key !== 'created_at')
    .map(key => ({
      key,
      label: columnMapping[key] || key // Fallback to key name if not mapped
    }));
});

const statusMapping = {
  'Fahrzeug registriert': 'Fahrzeug registriert',
  'Fahrzeug verifiziert': 'Fahrzeug verifiziert',
  'Fahrzeug erneut prüfen': 'Fahrzeug erneut prüfen',
  'Fahrzeug abgelehnt (kein Elektro)': 'Fahrzeug abgelehnt (kein Elektro)',
  'Fahrzeug braucht User Eingabe': 'Fahrzeug braucht User Eingabe',
  'Fahrzeug in Prüfung': 'Fahrzeug in Prüfung',
  'Fahrzeug bestätigt': 'Fahrzeug bestätigt',
  'Fahrzeug abgelehnt': 'Fahrzeug abgelehnt',
  'Zur Auszahlung offen': 'Zur Auszahlung offen',
  'Fahrzeug-Bonus ausgezahlt': 'Fahrzeug-Bonus ausgezahlt',
  'Auszahlungsanspruch verfallen': 'Auszahlungsanspruch verfallen',
  'Fahrzeug ignorieren(spam)': 'Fahrzeug ignorieren(spam)',
  'In Kündigung': 'In Kündigung',
  'Gekündigt': 'Gekündigt',
  'Fahrzeug-Entwurf': 'Fahrzeug-Entwurf'
};

const formatValue = (value, key) => {
  if (key === 'status') return statusMapping[value] || value;
  
  if (key === 'payout_date' && (value === null || value === undefined || value === '' || value === '01.01.0001' || value === '0001-01-01')) {
    return 'offen';
  }

  if (value === null || value === undefined) return '-';

  if (key === 'premium_amount_cents') {
    const euro = (value / 100).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return `${euro} €`;
  }

  if (key === 'updated_at' || key.includes('date')) {
      // Simple date formatting if it's a timestamp or date string
      if (typeof value === 'number') return new Date(value).toLocaleDateString('de-DE');
      return value; 
  }
  return value;
};
</script>

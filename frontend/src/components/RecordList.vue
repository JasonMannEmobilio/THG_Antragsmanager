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

    <div v-else>
      <!-- Bulk Action Bar -->
    <transition enter-active-class="transform transition ease-out duration-300" enter-from-class="translate-y-full opacity-0" enter-to-class="translate-y-0 opacity-100" leave-active-class="transform transition ease-in duration-200" leave-from-class="translate-y-0 opacity-100" leave-to-class="translate-y-full opacity-0">
      <div v-if="selectedIds.size > 0" class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 bg-emobilio-navy text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center space-x-6 border border-white/10 backdrop-blur-lg">
        <div class="flex items-center space-x-2 border-r border-white/20 pr-6">
          <span class="bg-emobilio-green text-white text-xs font-bold px-2 py-1 rounded-full">{{ selectedIds.size }}</span>
          <span class="text-sm font-medium">ausgewählt</span>
        </div>
        
        <div class="flex items-center space-x-3">
          <button @click="handleBulkUpdatePrice" class="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-all text-sm font-bold border border-white/5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emobilio-green" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Prämie setzen</span>
          </button>
          
          <button @click="handleBulkDownload" class="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-all text-sm font-bold border border-white/5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>Anhänge laden</span>
          </button>
          
          <button @click="$emit('export-csv', selectedRecords)" class="flex items-center space-x-2 px-4 py-2 bg-emobilio-green hover:bg-[#00A8AD] rounded-xl transition-all text-sm font-bold shadow-lg shadow-emobilio-green/20">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>Diesen Export (CSV)</span>
          </button>
        </div>
        
        <button @click="selectedIds.clear()" class="ml-4 p-2 hover:bg-white/10 rounded-full transition-colors text-white/40 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </transition>

    <div class="card-premium overflow-x-auto border-none shadow-none rounded-none">

      <table class="min-w-full divide-y divide-emobilio-navy/10 border-separate border-spacing-0">
        <thead class="bg-emobilio-navy text-white">
          <tr>
            <!-- Selection Checkbox Column (Sticky Left) -->
            <th scope="col" class="sticky left-0 z-30 bg-emobilio-navy px-4 py-4 border-b border-white/10 w-10">
              <input 
                type="checkbox" 
                :checked="isAllSelected" 
                @change="toggleSelectAll"
                class="h-4 w-4 rounded border-white/20 text-emobilio-green focus:ring-emobilio-green bg-white/10 cursor-pointer"
              />
            </th>
            <!-- Edit Button Column (Sticky Left) -->
            <th scope="col" class="sticky left-10 z-30 bg-emobilio-navy px-4 py-4 border-b border-white/10 border-r border-white/10 w-32">
              <span class="text-xs font-bold uppercase tracking-wider">Aktion</span>
            </th>
            <!-- Download Column (Sticky Left, after action) -->
            <th scope="col" class="sticky left-[10.5rem] z-30 bg-emobilio-navy px-4 py-4 border-b border-white/10 border-r border-white/10 w-32">
              <span class="text-xs font-bold uppercase tracking-wider">Dokument</span>
            </th>
            <!-- Dynamic Headers -->
            <th v-for="header in filteredVisibleHeaders" :key="header.key" scope="col" class="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider border-b border-white/10">
              <div class="flex items-center space-x-1 cursor-pointer hover:text-emobilio-green transition-colors" @click="sortBy(header.key)">
                <span>{{ header.label }}</span>
                <span v-if="sortKey === header.key" class="text-emobilio-green">
                  {{ sortOrder === 'asc' ? '↑' : '↓' }}
                </span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="record in sortedRecords" :key="record.id" class="transition-colors" :class="isSelected(record.id) ? 'bg-emobilio-green/10' : 'bg-white hover:bg-gray-50'">
            <!-- Row Checkbox (Sticky Left) -->
            <td class="sticky left-0 z-20 bg-inherit px-4 py-4 border-r border-gray-200/50 shadow-[1px_0_0_0_rgba(0,0,0,0.05)]">
              <input 
                type="checkbox" 
                :checked="isSelected(record.id)" 
                @change="toggleSelection(record.id)"
                class="h-4 w-4 rounded border-gray-300 text-emobilio-green focus:ring-emobilio-green cursor-pointer"
              />
            </td>
            <!-- Action Button (Sticky Left) -->
            <td class="sticky left-10 z-20 bg-inherit px-4 py-4 border-r border-gray-200/50 shadow-[1px_0_0_0_rgba(0,0,0,0.05)]">
               <button @click="$emit('edit', record)" class="inline-flex items-center px-3 py-1.5 bg-emobilio-green text-white text-[10px] font-bold rounded-full hover:bg-[#00A8AD] hover:scale-105 active:scale-95 transition-all shadow-sm shadow-emobilio-green/10 whitespace-nowrap">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                   <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
                Bearbeiten
              </button>
            </td>
            <!-- Download Button (Sticky Left) -->
            <td class="sticky left-[10.5rem] z-20 bg-inherit px-4 py-4 border-r border-gray-200/50 shadow-[1px_0_0_0_rgba(0,0,0,0.05)]">
              <a v-if="record.document_file?.url" :href="record.document_file.url" target="_blank" class="inline-flex items-center text-emobilio-green hover:text-[#00A8AD] text-xs font-bold border-b border-emobilio-green/20 hover:border-[#00A8AD] transition-all whitespace-nowrap">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Ansehen
              </a>
              <span v-else class="text-xs text-gray-400">-</span>
            </td>
            <!-- Dynamic Data Columns -->
            <td v-for="header in filteredVisibleHeaders" :key="header.key" class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 border-r border-gray-50 last:border-r-0">
               {{ formatValue(record[header.key], header.key) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    </div>
    
    <!-- Bulk Premium Modal -->
    <BulkPremiumModal
        :is-open="isBulkModalOpen"
        :selected-count="selectedIds.size"
        @close="isBulkModalOpen = false"
        @save="handleBulkModalSave"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import BulkPremiumModal from './BulkPremiumModal.vue';

const props = defineProps({
  records: Array,
  loading: Boolean,
  error: String
});

const emit = defineEmits(['edit', 'refresh', 'bulk-update', 'export-csv']);

// --- Sorting ---
const sortKey = ref('updated_at');
const sortOrder = ref('desc');

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

// --- Selection ---
const selectedIds = ref(new Set());

const isSelected = (id) => selectedIds.value.has(id);

const toggleSelection = (id) => {
  if (selectedIds.value.has(id)) {
    selectedIds.value.delete(id);
  } else {
    selectedIds.value.add(id);
  }
};

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedIds.value.clear();
  } else {
    props.records.forEach(r => selectedIds.value.add(r.id));
  }
};

const isAllSelected = computed(() => {
  return props.records.length > 0 && selectedIds.value.size === props.records.length;
});

const selectedRecords = computed(() => {
  return props.records.filter(r => selectedIds.value.has(r.id));
});

// --- Dynamic Headers ---
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

const filteredVisibleHeaders = computed(() => {
  if (!props.records || props.records.length === 0) return [];
  
  const keys = Object.keys(props.records[0]);
  
  // Filter out id, created_at, and document_file (since it's a fixed column now)
  return keys
    .filter(key => key !== 'id' && key !== 'created_at' && key !== 'document_file')
    .map(key => ({
      key,
      label: columnMapping[key] || key
    }));
});

// --- Records Processing ---
const sortedRecords = computed(() => {
  let items = [...props.records];
  
  if (sortKey.value) {
    items.sort((a, b) => {
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];
      
      // Null handling
      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;
      
      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();
      
      if (valA < valB) return sortOrder.value === 'asc' ? -1 : 1;
      if (valA > valB) return sortOrder.value === 'asc' ? 1 : -1;
      return 0;
    });
  }
  
  return items;
});

const formatValue = (value, key) => {
  if (key === 'status') return value;
  
  if (key === 'payout_date' && (value === null || value === undefined || value === '' || value === '01.01.0001' || value === '0001-01-01')) {
    return 'offen';
  }

  if (value === null || value === undefined) return '-';

  if (key === 'premium_amount_cents') {
    const euro = (parseInt(value, 10) / 100).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return `${euro} €`;
  }

  if (key === 'updated_at' || key.includes('date')) {
      if (typeof value === 'number') return new Date(value).toLocaleDateString('de-DE');
      return value; 
  }
  return value;
};

// --- Bulk Actions ---
const isBulkModalOpen = ref(false);

const handleBulkUpdatePrice = () => {
    isBulkModalOpen.value = true;
};

const handleBulkModalSave = (priceFloat) => {
    const priceCents = Math.round(priceFloat * 100);
    emit('bulk-update', { ids: Array.from(selectedIds.value), data: { premium_amount_cents: priceCents } });
    selectedIds.value.clear();
    isBulkModalOpen.value = false;
};

const handleBulkDownload = async () => {
    for (const record of selectedRecords.value) {
        if (record.document_file?.url) {
            try {
                // Fetching the file locally as a Blob bypasses Cross-Origin popup blockers entirely
                // by creating a same-origin URL that the browser trusts completely for downloads
                const response = await fetch(record.document_file.url);
                if (!response.ok) throw new Error('Fetch failed');
                
                const blob = await response.blob();
                const blobUrl = URL.createObjectURL(blob);
                
                const link = document.createElement('a');
                link.href = blobUrl;
                link.download = record.document_filename || record.document_file.name || `dokument_${record.customer_number || record.id}.pdf`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                // Cleanup
                setTimeout(() => URL.revokeObjectURL(blobUrl), 10000);
            } catch (err) {
                console.error("Blob download failed, falling back to basic link:", err);
                // Fallback in case of strict CORS restrictions from the file server
                const link = document.createElement('a');
                link.href = record.document_file.url;
                link.target = '_blank';
                link.download = record.document_filename || record.document_file.name || 'dokument.pdf';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
            // Delay buffer to not crash the browser and satisfy multi-download heuristics
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    }
};

</script>

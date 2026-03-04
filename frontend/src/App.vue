<template>
  <div class="min-h-screen bg-emobilio-bg font-sans text-emobilio-navy overflow-x-hidden">
    <!-- Unauthenticated View -->
    <template v-if="!isAuthenticated">
      <Login @login-success="handleLoginSuccess" />
    </template>

    <!-- Authenticated View -->
    <template v-else>
      <nav class="nav-blur px-4 py-4 sm:px-6 lg:px-8 mb-8">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center space-x-6">
          <img src="./assets/e_mobilio_logo.jpg" alt="e-mobilio logo" class="h-12 w-auto object-contain" />
          <h1 class="text-2xl font-black tracking-tight text-emobilio-navy">
            <span class="text-emobilio-green ml-2">THG Manager</span>
          </h1>
        </div>
        <div class="flex items-center space-x-4 flex-1 justify-end max-w-sm ml-auto mr-4">
           <div class="relative w-full">
             <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
               <svg class="h-5 w-5 text-emobilio-navy/30" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                 <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
               </svg>
             </div>
             <input 
               v-model="searchQuery" 
               type="text" 
               placeholder="Suchen..." 
               class="block w-full pl-10 pr-3 py-2 border border-emobilio-navy/10 rounded-full leading-5 bg-white/50 placeholder-emobilio-navy/30 focus:outline-none focus:ring-2 focus:ring-emobilio-green focus:border-emobilio-green sm:text-sm transition-all"
             />
           </div>
           <button @click="fetchRecords" class="p-2 hover:bg-emobilio-navy/5 rounded-full transition-colors flex-shrink-0" title="Refresh">
             <div :class="{'animate-spin': loading}">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
               </svg>
             </div>
           </button>
           <button @click="handleLogout" class="flex items-center space-x-2 px-4 py-2 border border-emobilio-navy/10 rounded-full hover:bg-red-50 hover:border-red-100 group transition-all" title="Abmelden">
              <span class="text-sm font-bold text-emobilio-navy/60 group-hover:text-red-600">Abmelden</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emobilio-navy/30 group-hover:text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
           </button>
        </div>
      </div>
    </nav>

    <main class="relative px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div class="card-premium p-6 sm:p-10 mb-10 overflow-hidden">
         <div class="w-full">
            <!-- Removed redundant header -->
            
            <RecordList 
                :records="filteredRecords" 
                :loading="loading" 
                :error="error"
                @edit="openEditModal"
                @refresh="fetchRecords"
            />
         </div>
      </div>
    </main>

    <EditRecordModal
        :is-open="isModalOpen"
        :record="selectedRecord"
        @close="closeEditModal"
        @save="handleSave"
    />

    <NotificationToast
        :show="notification.show"
        :type="notification.type"
        :title="notification.title"
        :message="notification.message"
        @close="notification.show = false"
    />
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import RecordList from './components/RecordList.vue';
import EditRecordModal from './components/EditRecordModal.vue';
import NotificationToast from './components/NotificationToast.vue';
import Login from './components/Login.vue';
import logo from './assets/e_mobilio_logo.jpg';
import { getRecords, updateRecord } from './services/api';

const isAuthenticated = ref(!!localStorage.getItem('authToken'));
const records = ref([]);
const loading = ref(false);
const error = ref(null);
const isModalOpen = ref(false);
const selectedRecord = ref(null);
const searchQuery = ref('');

const filteredRecords = computed(() => {
    if (!searchQuery.value) {
        return records.value;
    }
    const query = searchQuery.value.toLowerCase();
    return records.value.filter(record => {
        // Search across all values in the record
        return Object.values(record).some(val => {
            if (val === null || val === undefined) return false;
            return String(val).toLowerCase().includes(query);
        });
    });
});

const notification = reactive({
    show: false,
    type: 'success',
    title: '',
    message: ''
});

const showNotification = (type, title, message) => {
    notification.type = type;
    notification.title = title;
    notification.message = message;
    notification.show = true;
    setTimeout(() => {
        notification.show = false;
    }, 4000);
};

const handleLoginSuccess = (token) => {
    isAuthenticated.value = true;
    fetchRecords();
};

const handleLogout = () => {
    localStorage.removeItem('authToken');
    isAuthenticated.value = false;
    records.value = [];
};

const fetchRecords = async () => {
    if (!isAuthenticated.value) return;
    loading.value = true;
    error.value = null;
    try {
        records.value = await getRecords();
    } catch (err) {
        error.value = 'Failed to fetch records. ' + (err.message || '');
        console.error(err);
    } finally {
        loading.value = false;
    }
};

const openEditModal = (record) => {
    selectedRecord.value = record;
    isModalOpen.value = true;
};

const closeEditModal = () => {
    isModalOpen.value = false;
    selectedRecord.value = null;
};

const handleSave = async (updatedData) => {
    console.log('App.vue: handleSave called with:', updatedData);
    try {
        await updateRecord(updatedData);
        // Optimistic update or refetch
        const index = records.value.findIndex(r => r.id === updatedData.id);
        if (index !== -1) {
            records.value[index] = { ...records.value[index], ...updatedData };
        }
        closeEditModal();
        showNotification('success', 'Success', 'Record updated successfully!');
    } catch (err) {
        showNotification('error', 'Error', 'Failed to update record: ' + (err.message || ''));
        console.error(err);
    }
};

onMounted(() => {
    fetchRecords();
});
</script>

<template>
  <div class="min-h-screen bg-emobilio-bg flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center mb-6">
        <img src="../assets/e_mobilio_logo.jpg" alt="e-mobilio logo" class="h-16 w-auto object-contain" />
      </div>
      <h2 class="text-center text-3xl font-black text-emobilio-navy tracking-tight">
        Anmeldung zum <span class="text-emobilio-green">THG Manager</span>
      </h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card-premium py-8 px-4 shadow-2xl sm:px-10">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="email" class="block text-sm font-bold text-emobilio-navy">Email-Adresse</label>
            <div class="mt-1">
              <input 
                id="email" 
                v-model="email" 
                name="email" 
                type="email" 
                autocomplete="email" 
                required 
                class="appearance-none block w-full px-4 py-3 border border-emobilio-navy/10 rounded-xl shadow-sm placeholder-emobilio-navy/30 focus:outline-none focus:ring-emobilio-green focus:border-emobilio-green sm:text-sm bg-emobilio-bg/50 transition-all font-medium"
                placeholder="ihre@email.de"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-bold text-emobilio-navy">Passwort</label>
            <div class="mt-1">
              <input 
                id="password" 
                v-model="password" 
                name="password" 
                type="password" 
                autocomplete="current-password" 
                required 
                class="appearance-none block w-full px-4 py-3 border border-emobilio-navy/10 rounded-xl shadow-sm placeholder-emobilio-navy/30 focus:outline-none focus:ring-emobilio-green focus:border-emobilio-green sm:text-sm bg-emobilio-bg/50 transition-all font-medium"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div v-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-red-700">{{ error }}</p>
              </div>
            </div>
          </div>

          <div>
            <button 
              type="submit" 
              :disabled="loading"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-emobilio-green/30 text-base font-black text-white bg-emobilio-green hover:bg-[#2B8C2A] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emobilio-green transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Anmelden
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { login } from '../services/api';

const emit = defineEmits(['login-success']);

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref(null);

const handleLogin = async () => {
    loading.value = true;
    error.value = null;
    try {
        const response = await login({
            email: email.value,
            password: password.value
        });
        localStorage.setItem('authToken', response.authToken);
        emit('login-success', response.authToken);
    } catch (err) {
        error.value = err.message || 'credentials may be wrong';
    } finally {
        loading.value = false;
    }
};
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center overflow-auto bg-gray-500 bg-opacity-75 backdrop-blur-sm" aria-labelledby="modal-title" role="dialog" aria-modal="true" @click.self="$emit('close')">
    <div class="relative bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:max-w-xl sm:w-full m-4">
      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-emobilio-green/10 sm:mx-0 sm:h-10 sm:w-10">
              <svg class="h-6 w-6 text-emobilio-green" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-xl leading-6 font-black text-emobilio-navy" id="modal-title">
                So nutzen Sie den THG Manager
              </h3>
              <div class="mt-4 space-y-4 text-sm text-emobilio-navy/80">
                
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
                  <h4 class="font-bold text-emobilio-green mb-2 flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    Suchen & Filtern
                  </h4>
                  <p>Nutzen Sie die Suchleiste oben, um nach Namen, Kennzeichen, VIN oder Status zu suchen. Die Liste aktualisiert sich sofort.</p>
                </div>

                <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
                  <h4 class="font-bold text-emobilio-green mb-2 flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                    Einträge bearbeiten
                  </h4>
                  <p>Klicken Sie bei einem beliebigen Eintrag auf <strong>Bearbeiten</strong>, um den Status, Betrag oder das Auszahlungsdatum anzupassen.</p>
                </div>

                <div class="bg-gray-50 p-4 rounded-xl border border-gray-100">
                  <h4 class="font-bold text-emobilio-green mb-2 flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                    Aktualisieren
                  </h4>
                  <p>Mit dem kreisförmigen Pfeil-Button neben der Suchleiste können Sie die Daten jederzeit neu von der Datenbank laden.</p>
                </div>

              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse border-t border-gray-100">
          <button type="button" class="w-full inline-flex justify-center rounded-xl border border-transparent shadow-sm px-6 py-2 bg-emobilio-green text-base font-medium text-white hover:bg-emobilio-green/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emobilio-green sm:ml-3 sm:w-auto sm:text-sm transition-colors" @click="$emit('close')">
            Verstanden
          </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
});

defineEmits(['close']);
</script>

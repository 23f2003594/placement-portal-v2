<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="card shadow-sm p-4">
        <h2 class="mb-4">View Applications by Drive</h2>
        <p class="text-muted">Select a placement drive to view the list of student applicants.</p>
        <div class="list-group mt-3">
          <button v-for="drive in allDrives" :key="drive.id" 
            @click="gotoapplicants(drive.id)"
            class="list-group-item list-group-item-action d-flex justify-content-between align-items-center p-3">
            <div>
              <h5 class="mb-1">{{ drive.title }}</h5>
              <small class="text-primary fw-bold">{{ drive.company_name }}</small>
            </div>
            <span class="badge bg-secondary rounded-pill">View Applicants &rarr;</span>
          </button>
          <button class="btn btn-light border me-3" @click="$router.push('/admin/dashboard')">
              <i class="bi bi-chevron-left"></i> Back
          </button>
        </div>
        <div v-if="allDrives.length === 0" class="text-center py-5">
          <p class="text-muted">No approved drives found.</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue';
import api from '../services/api';
const router = useRouter();
const allDrives = ref([]);
const fetchdrives = async()=>{
  try{
    const res =await api.get('/admin/drives');
    const today = new Date();
    allDrives.value = res.data.filter(d =>{
      const isapproved = d.status === 'approved';
      const isdeadline = d.application_deadline && new Date(d.application_deadline) < today;
      const isclosed = d.status === 'closed';
      return isapproved || isdeadline || isclosed;
    });
  }catch(err) { 
    console.error("Error filtering drives:", err); 
  }
};
const gotoapplicants = (id)=>{
  router.push(`/admin/applications/drive/${id}`);
};
onMounted(fetchdrives);
</script>
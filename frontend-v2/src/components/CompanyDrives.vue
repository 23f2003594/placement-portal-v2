<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="mb-0">My Placement Drives</h2>
          <p class="text-muted">Track applications and manage candidate selection.</p>
        </div>
        <button class="btn btn-primary shadow-sm" @click="$router.push('/company/drives/create')">
          <i class="bi bi-plus-lg"></i> Post New Drive
        </button>
        <button class="btn btn-outline-secondary btn-sm" @click="$router.push('/company/dashboard')">
            <i class="bi bi-arrow-left"></i> Back to Dashboard
         </button>
      </div>
      <div class="card shadow-sm border-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-dark">
              <tr>
                <th>Job Title</th>
                <th>Salary</th>
                <th>Status</th>
                <th>Application Funnel</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in drives" :key="drive.id">
                <td class="fw-bold">{{ drive.title }}</td>
                <td>{{ drive.salary }} LPA</td>
                <td>
                  <span :class="statusclass(drive.status)">{{ drive.status }}</span>
                </td>
                <td>
                  <div class="d-flex gap-2">
                    <span class="badge bg-secondary">Total: {{ drive.total_apps }}</span>
                    <span class="badge bg-info text-dark">Shortlisted: {{ drive.shortlisted_count }}</span>
                  </div>
                </td>
                <td class="text-center">
                  <button 
                    v-if="drive.status !== 'pending'"
                    class="btn btn-sm btn-outline-primary px-3" 
                    @click="$router.push(`/company/drives/${drive.id}/applicants`)">
                    Manage Applicants
                  </button>
                  <span v-else class="text-muted small">Awaiting Admin Approval</span>
                </td>
              </tr>
              <tr v-if="drives.length === 0">
                <td colspan="5" class="text-center py-5 text-muted">
                  You haven't posted any drives yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import Navbar from './Navbar.vue';
import api from '../services/api';
const drives = ref([]);
const fetchmydrives = async()=>{
  try{
    const res =await api.get('/company/drives');
    drives.value = res.data;
  }catch(err) {
    console.error("Error loading company drives");
  }
};
const statusclass = (status)=>{
  return {
    'badge bg-warning text-dark': status === 'pending',
    'badge bg-success': status === 'approved',
    'badge bg-danger': status === 'closed'
  };
};
onMounted(fetchmydrives);
</script>
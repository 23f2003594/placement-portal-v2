<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div v-if="data.approval_status !== 'approved'" class="alert alert-warning shadow-sm">
        <h4 class="alert-heading">Pending Approval!</h4>
        <p>Your account is currently <strong>{{ data.approval_status }}</strong>. You will be able to post drives once the Admin approves your profile.</p>
      </div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Welcome, {{ data.company_name }}</h2>
        <button v-if="data.approval_status === 'approved'" 
                class="btn btn-primary" @click="$router.push('/company/drives/create')">
          + Create New Drive
        </button>
      </div>
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card border-0 shadow-sm bg-primary text-white p-3">
            <h6>Total Drives</h6>
            <h2 class="mb-0">{{ data.stats?.total_drives || 0 }}</h2>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm bg-success text-white p-3">
            <h6>Applications Received</h6>
            <h2 class="mb-0">{{ data.stats?.total_apps || 0 }}</h2>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm bg-info text-white p-3">
            <h6>Hired Candidates</h6>
            <h2 class="mb-0">{{ data.stats?.hired || 0 }}</h2>
          </div>
        </div>
      </div>
      <div class="mt-5">
        <h4>Quick Actions</h4>
        <div class="row mt-3">
          <div class="col-md-3">
            <div class="card text-center p-4 action-card" @click="$router.push('/company/drives')">
              <i class="bi bi-megaphone fs-1 mb-2"></i>
              <h6>Manage My Drives</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import Navbar from './Navbar.vue';
import api from '../services/api';
const data = ref({ stats: {} });
const fetchstats = async()=>{
  try{
    const res =await api.get('/company/stats');
    data.value = res.data;
  }catch(err) {
    console.error("Dashboard failed to load");
  }
};
onMounted(fetchstats);
</script>
<style scoped>
.action-card {
  cursor: pointer;
  transition: transform 0.2s;
}
.action-card:hover {
  transform: translateY(-5px);
  background-color: #f8f9fa;
}
</style>
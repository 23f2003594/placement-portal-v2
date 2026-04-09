<template>
  <div>
    <Navbar />
    <div class="container mt-4 mb-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="mb-0 fw-bold">Finalized Placements</h2>
          <p class="text-muted">Master list of students who have accepted job offers.</p>
        </div>
        <button class="btn btn-outline-secondary shadow-sm" @click="$router.push('/admin/dashboard')">
          <i class="bi bi-arrow-left"></i> Back to Dashboard
        </button>
      </div>
      <div class="card shadow-sm border-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Student Name</th>
                <th>Company</th>
                <th>Position</th>
                <th>Package (LPA)</th>
                <th class="text-center">Offer Letter</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in placementrecords" :key="record.id">
                <td class="text-muted fw-bold">#{{ record.id }}</td>
                <td>
                  <div class="fw-bold">{{ record.student_name }}</div>
                </td>
                <td>{{ record.company_name }}</td>
                <td>
                  <span class="badge bg-info-subtle text-info border border-info">
                    {{ record.position }}
                  </span>
                </td>
                <td><span class="fw-bold text-success">{{ record.salary }} LPA</span></td>
                <td class="text-center">
                  <a v-if="record.offer_letter_link" 
                     :href="record.offer_letter_link" 
                     target="_blank" 
                     class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-file-earmark-pdf"></i> View PDF
                  </a>
                  <span v-else class="text-muted small">No link provided</span>
                </td>
              </tr>
              <tr v-if="placementrecords.length === 0">
                <td colspan="6" class="text-center py-5 text-muted">
                  <i class="bi bi-folder-x fs-1 d-block mb-2"></i>
                  No placement records found.
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
const placementrecords = ref([]);
const fetchplacements = async()=>{
  try{
    const res =await api.get('/admin/placements');
    placementrecords.value = res.data;
  }catch(err) {
    console.error("Error fetching placement records:",err);
  }
};
onMounted(fetchplacements);
</script>
<style scoped>
.hover-card { transition: transform 0.2s; cursor: pointer; }
.hover-card:hover { transform: translateY(-5px); }
.icon-circle { 
  width: 60px; height: 60px; display: flex; 
  align-items: center; justify-content: center; border-radius: 50%; 
}
.bg-primary-subtle { background-color: #e3f2fd; }
.bg-info-subtle { background-color: #e0f7fa; }
</style>
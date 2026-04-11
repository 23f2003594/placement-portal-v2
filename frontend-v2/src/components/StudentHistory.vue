<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <h3 class="mb-4">My Application History</h3>
      <button class="btn btn-light border me-3" @click="$router.push('/student/dashboard')">
          <i class="bi bi-chevron-left"></i> Back
      </button>
      <div class="card shadow-sm border-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-dark">
              <tr>
                <th>Company & Role</th>
                <th>Applied Date</th>
                <th>Status</th>
                <th>Interviews / Feedback</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.application_id">
                <td>
                  <div class="fw-bold">{{ app.company_name }}</div>
                  <small class="text-muted">{{ app.title }}</small>
                </td>
                <td>{{ app.applied_date }}</td>
                <td>
                  <span :class="statusbadge(app.status)">{{ app.status.toUpperCase() }}</span>
                </td>
                <td>
                  <div v-if="app.status === 'interview'" class="small">
                    <strong>Date:</strong>{{ app.interview_date }}<br>
                    <strong>Note:</strong>{{ app.feedback }}
                  </div>
                  <span v-else class="text-muted small">--</span>
                </td>
                <td class="text-center">
                  <div v-if="app.status === 'selected'" class="d-grid gap-2">
                    <a :href="app.remarks" target="_blank" class="btn btn-sm btn-outline-info">View Offer</a>
                    <button class="btn btn-sm btn-success" @click="confirmplacement(app.application_id)">Accept & Confirm</button>
                    <button class="btn btn-sm btn-danger" @click="rejectplacement(app.application_id)">Reject</button>
                  </div>
                  <div v-else-if="app.status === 'placed'">
                    <span class="text-success small fw-bold">Placed <i class="bi bi-check-all"></i></span>
                    <a :href="app.offer_letter_link" target="_blank" class="btn btn-sm btn-outline-info">View Offer</a>
                  </div>
                  <span v-else class="text-muted small">Waiting for Company</span>
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
const applications = ref([]);
const fetchhistory = async()=>{
  const res =await api.get('/student/applications');
  applications.value = res.data;
};
const confirmplacement = async(id)=>{
  if (confirm("By accepting, you finalize your placement. You won't be able to apply for other drives.")) {
    await api.post('/student/accept-offer', { application_id: id });
    fetchhistory();
  }
};
const rejectplacement = async(id)=>{
  if (confirm("Are you sure you want to REJECT this offer? This action cannot be undone.")) {
    try{
      const res =await api.post('/student/reject-offer', { application_id: id });
      if (res.data.success) {
        alert("Offer rejected. You can now apply for other drives.");
        fetchhistory();
      }
    }catch(err) {
      console.error("Error rejecting offer:", err);
      alert("Failed to reject offer.");
    }
  }
};
const statusbadge = (s)=> ({
  'badge bg-secondary': s === 'applied',
  'badge bg-info text-dark': s === 'shortlisted',
  'badge bg-warning text-dark': s === 'interview',
  'badge bg-success': s === 'selected' || s === 'placed',
  'badge bg-danger': s === 'rejected'
});
onMounted(fetchhistory);
</script>

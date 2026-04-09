<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="mb-0">{{ driveInfo.title }}</h2>
          <p class="text-muted">Company: <strong>{{ driveInfo.company }}</strong></p>
        </div>
        <button class="btn btn-outline-secondary" @click="$router.push('/admin/applications')">Back to Selection</button>
      </div>
      <div class="table-responsive card shadow-sm">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-dark">
            <tr>
              <th>Roll No</th>
              <th>Student Name</th>
              <th>CGPA</th>
              <th>Status</th>
              <th>Applied Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applicants" :key="app.app_id">
              <td>{{ app.roll_no }}</td>
              <td><strong>{{ app.student_name }}</strong></td>
              <td>{{ app.cgpa }}</td>
              <td>
                <span :class="statusbadge(app.status)">{{ app.status }}</span>
              </td>
              <td>{{ new Date(app.applied_date).toLocaleDateString() }}</td>
              <td>
                <button class="btn btn-sm btn-outline-primary" @click="$router.push(`/admin/students/${app.student_id}`)">
                  View Profile
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="applicants.length === 0" class="text-center py-5">
          No students have applied for this drive yet.
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from './Navbar.vue';
import api from '../services/api';
const route = useRoute();
const applicants = ref([]);
const driveInfo = ref({ title: '', company: '' });
const fetchapplicants = async()=>{
  try{
    const res =await api.get(`/admin/drives/${route.params.id}/applications`);
    applicants.value = res.data.applicants;
    driveInfo.value = { title: res.data.drive_title, company: res.data.company_name };
  }catch(err) { console.error(err); }
};
const statusbadge = (status)=>{
  return {
    'badge bg-secondary': status === 'applied',
    'badge bg-success': status === 'selected',
    'badge bg-danger': status === 'rejected'
  };
};
onMounted(fetchapplicants);
</script>
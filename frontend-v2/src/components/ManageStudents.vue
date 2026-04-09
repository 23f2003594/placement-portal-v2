<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="card shadow-sm p-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>Manage Students</h2>
          <button class="btn btn-outline-secondary" @click="$router.push('/admin/dashboard')">Back</button>
        </div>
        <div class="mb-3">
          <input v-model="searchQuery" @input="fetchstudents" 
                 class="form-control" placeholder="Search by Name, Email, or Roll No..." />
        </div>
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-dark">
              <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in students" :key="s.id">
                <td>{{ s.roll_no }}</td>
                <td><strong>{{ s.name }}</strong></td>
                <td>{{ s.email }}</td>
                <td>
                  <span :class="s.is_blacklisted ? 'badge bg-danger' : 'badge bg-success'">
                    {{ s.is_blacklisted ? 'Blacklisted' : 'Active' }}
                  </span>
                </td>
                <td>
                  <button :class="s.is_blacklisted ? 'btn btn-sm btn-success' : 'btn btn-sm btn-danger'"
                          @click="toggleblacklist(s.id)">
                    {{ s.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
                  </button>
                  <button class="btn btn-sm btn-outline-primary ms-2" @click="viewprofile(s.id)">
                    View Profile
                  </button>
                </td>
              </tr>
              <tr v-if="students.length === 0">
                <td colspan="5" class="text-center py-4 text-muted">No students found.</td>
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
import { useRouter } from 'vue-router';
const router = useRouter();
const students = ref([]);
const searchQuery = ref('');
const fetchstudents = async()=>{
  try{
    const res =await api.get('/admin/students', { params: { q: searchQuery.value } });
    students.value = res.data;
  }catch(err) {
    console.error(err);
  }
};
const toggleblacklist = async(id)=>{
  try{
    await api.post(`/admin/students/${id}/toggle-blacklist`);
    fetchstudents(); 
  }catch(err) {
    alert("Operation failed");
  }
};
const viewprofile = (id)=>{
  router.push(`/admin/students/${id}`);
};
onMounted(fetchstudents);
</script>
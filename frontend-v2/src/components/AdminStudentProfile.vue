<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div v-if="loading" class="text-center">Loading Profile...</div>
      <div v-else-if="student" class="card shadow border-0">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Student Profile: {{ student.name }}</h4>
          <button class="btn btn-light btn-sm" @click="$router.push('/admin/dashboard')">Back</button>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6 mb-4">
              <h5 class="text-muted border-bottom pb-2">Personal & Account Info</h5>
              <p><strong>Roll Number:</strong>{{ student.roll_no }}</p>
              <p><strong>Email:</strong>{{ student.email }}</p>
              <p><strong>Status:</strong> 
                <span :class="student.is_blacklisted ? 'text-danger' : 'text-success'">
                  {{ student.is_blacklisted ? 'Blacklisted' : 'Active' }}
                </span>
              </p>
            </div>
            <div class="col-md-6 mb-4">
              <h5 class="text-muted border-bottom pb-2">Academic Details</h5>
              <p><strong>Branch:</strong>{{ student.branch }}</p>
              <p><strong>Year:</strong>{{ student.year }}</p>
              <p><strong>CGPA:</strong> <span class="badge bg-info text-dark">{{ student.cgpa }}</span></p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12 mb-4">
              <h5 class="text-muted border-bottom pb-2">Background</h5>
              <p><strong>Education:</strong><br>{{ student.education || 'Not provided' }}</p>
              <p><strong>Technical Skills:</strong><br>
                <span v-for="skill in splitskills(student.skills)" :key="skill" class="badge bg-secondary me-1">
                  {{ skill }}
                </span>
              </p>
            </div>
            <div class="col-md-12">
              <div class="alert alert-light border">
                <strong>Resume Link:</strong> 
                <a v-if="student.resume_link" :href="student.resume_link" target="_blank" class="ms-2">View Document</a>
                <span v-else class="text-muted ms-2">No resume uploaded</span>
              </div>
            </div>
          </div>
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
const student = ref(null);
const loading = ref(true);
const fetchprofile = async()=>{
  try{
    const res =await api.get(`/admin/students/${route.params.id}`);
    student.value = res.data;
  }catch(err) {
    alert("Could not load student profile");
  } finally {
    loading.value = false;
  }
};
const splitskills = (skills)=>{
  return skills ? skills.split(',').map(s => s.trim()) : [];
};
onMounted(fetchprofile);
</script>
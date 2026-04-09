<template>
  <div>
    <Navbar />
    <div class="container mt-4 mb-5">
      <div class="card shadow-sm border-0">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center p-3">
          <h4 class="mb-0">Placement Profile</h4>
          <div class="d-flex gap-2">
            <span v-if="student.is_blacklisted" class="badge bg-danger">Blacklisted</span>
            <span v-if="student.status === 'placed'" class="badge bg-light text-success">Officially Placed</span>
          </div>
        </div>
        <div class="card-body p-4">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label fw-bold text-muted">Full Name</label>
              <input :value="student.name" class="form-control bg-light" readonly />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label fw-bold text-muted">Roll Number</label>
              <input :value="student.roll_no" class="form-control bg-light" readonly />
            </div>

            <hr class="my-4">

            <div class="col-md-4 mb-3">
              <label class="form-label fw-bold">Branch / Department</label>
              <input v-model="student.branch" class="form-control bg-light" placeholder="e.g. CSE" readonly/>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label fw-bold">Graduation Year</label>
              <input v-model="student.year" type="number" class="form-control bg-light" placeholder="e.g. 2026" readonly />
            </div>
            <div class="col-md-8 mb-3">
              <label class="form-label fw-bold">Skills</label>
              <input 
                v-model="student.skills" 
                class="form-control" 
                placeholder="e.g. Java, Python, SQL, React" 
                :readonly="userRole !== 'student'"
              />
            </div>
            <div class="col-md-8 mb-3">
              <label class="form-label fw-bold">Education</label>
              <textarea 
                v-model="student.education" 
                class="form-control"  
                placeholder="Current degree details"
                :readonly="userRole !== 'student'"
              ></textarea>
            </div>
            <div class="col-md-8 mb-3">
              <label class="form-label fw-bold">CGPA</label>
              <textarea 
                v-model="student.cgpa" 
                class="form-control"  
                placeholder="Current degree details"
                :readonly="userRole !== 'student'"
              ></textarea>
            </div>
            <div class="col-12 mb-4">
              <label class="form-label fw-bold">Resume Link (URL)</label>
              <div class="input-group">
                <input 
                  v-model="student.resume_link" 
                  class="form-control" 
                  placeholder="https://drive.google.com/..." 
                  :readonly="userRole !== 'student'"
                />
                <a v-if="student.resume_link" :href="student.resume_link" target="_blank" class="btn btn-outline-primary">
                  <i class="bi bi-box-arrow-up-right"></i> View
                </a>
              </div>
            </div>
            <div class="col-12 d-flex justify-content-between align-items-center">
              <button class="btn btn-outline-secondary" @click="$router.push('/student/dashboard')">Back</button>
              <button 
                v-if="userRole === 'student'" 
                class="btn btn-success px-5 shadow-sm" 
                @click="saveprofile" 
                :disabled="saving">
                <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                {{ saving ? 'Saving...' : 'Save Profile Changes' }}
              </button>
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
const student = ref({
  name: '',
  roll_no: '',
  cgpa: null,
  skills: '',
  education: '',
  resume_link: '',
  is_blacklisted: false,
  status: ''
});
const saving = ref(false);
const userRole = ref(localStorage.getItem('role'));
const fetchprofile = async()=>{
  try{
    const res =await api.get('/student/profile');
    student.value = res.data;
  }catch(err) {
    console.error("Failed to load profile.");
  }
};
const saveprofile = async()=>{
  if (!student.value.resume_link) {
    alert("Please provide a resume link before saving.");
    return;
  }
  saving.value = true;
  try{
    const res =await api.post('/student/profile', {
      cgpa: student.value.cgpa,
      skills: student.value.skills,
      education: student.value.education,
      resume_link: student.value.resume_link
    });
    alert(res.data.message || "Profile updated!");
  }catch(err) {
    alert("Error updating profile. Check if all fields are valid.");
  } finally {
    saving.value = false;
  }
};
onMounted(fetchprofile);
</script>
<style scoped>
.form-control:readonly {
  background-color: #f8f9fa;
  cursor: default;
}
</style>
<template>
  <div>
    <Navbar />
    <div class="container mt-4 mb-5">
      <div class="card shadow-sm border-0">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Create New Placement Drive</h4>
          <button class="btn btn-light btn-sm" @click="$router.push('/company/dashboard')">Cancel</button>
        </div>
        <div class="card-body p-4">
          <form @submit.prevent="submitdrive">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-bold">Job Title</label>
                <input v-model="form.title" type="text" class="form-control" placeholder="e.g. Software Engineer Intern" required />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-bold">Salary / CTC</label>
                <input v-model="form.salary" type="text" class="form-control" placeholder="e.g. 12 LPA" required />
              </div>
              <div class="col-12 mb-3">
                <label class="form-label fw-bold">Job Description</label>
                <textarea v-model="form.description" class="form-control" rows="4" placeholder="Describe the role and responsibilities..." required></textarea>
              </div>
              <div class="col-12 mb-3">
                <label class="form-label fw-bold">Skills Required</label>
                <input v-model="form.skills_required" type="text" class="form-control" placeholder="e.g. Java, Python, React, SQL" required />
              </div>
              <hr class="my-4">
              <h5 class="mb-3 text-secondary">Eligibility Criteria</h5>
              <div class="col-md-4 mb-3">
                <label class="form-label fw-bold">Target Branch</label>
                <select v-model="form.eligibility_branch" class="form-select" required>
                  <option value="All">All Branches</option>
                  <option value="CSE">CSE</option>
                  <option value="ECE">ECE</option>
                  <option value="EEE">EEE</option>
                  <option value="IT">IT</option>
                  <option value="CIVIL">CIVIL</option>
                  <option value="MECH">MECH</option>
                  <option value="FASHION">FASHION</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label class="form-label fw-bold">Minimum CGPA</label>
                <input v-model="form.eligibility_cgpa" type="number" step="0.1" class="form-control" placeholder="e.g. 7.5" required />
              </div>
              <div class="col-md-4 mb-3">
                <label class="form-label fw-bold">Passing Year</label>
                <input v-model="form.eligibility_year" type="number" class="form-control" placeholder="e.g. 2026" required />
              </div>
              <div class="col-md-6 mb-4">
                <label class="form-label fw-bold">Application Deadline</label>
                <input v-model="form.application_deadline" type="date" class="form-control" required />
              </div>
              <div class="col-12">
                <button type="submit" class="btn btn-success w-100 py-2 fw-bold" :disabled="loading">
                  {{ loading ? 'Posting Drive...' : 'Post Placement Drive' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue';
import api from '../services/api';
const router = useRouter();
const loading = ref(false);
const form = ref({
  title: '',
  description: '',
  salary: '',
  skills_required: '',
  eligibility_branch: 'All',
  eligibility_cgpa: '',
  eligibility_year: '',
  application_deadline: ''
});
const submitdrive = async()=>{
  loading.value = true;
  try{
    const res =await api.post('/company/drives/create', form.value);
    alert(res.data.message);
    router.push('/company/drives');
  }catch(err) {
    alert(err.response?.data?.message || "Failed to create drive");
  } finally {
    loading.value = false;
  }
};
</script>
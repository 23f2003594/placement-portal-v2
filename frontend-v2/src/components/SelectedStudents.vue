<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>Final Selections: {{ driveTitle }}</h3>
        <button class="btn btn-sm btn-secondary" @click="$router.go(-1)">Back</button>
      </div>
      <div class="row">
        <div v-for="student in selectedList" :key="student.roll_no" class="col-md-4 mb-3">
          <div class="card shadow-sm border-success">
            <div class="card-body">
              <h5 class="card-title">{{ student.name }}</h5>
              <p class="card-text mb-1"><strong>Roll No:</strong>{{ student.roll_no }}</p>
              <p class="card-text mb-1"><strong>Dept:</strong>{{ student.branch }}</p>
              <p class="card-text mb-3"><strong>CGPA:</strong>{{ student.cgpa }}</p>
              <a :href="student.offer_letter_link" target="_blank" class="btn btn-sm btn-success w-100">
                View Offer Letter
              </a>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selectedList.length === 0" class="text-center mt-5">
        <p class="text-muted">No students have been selected for this drive yet.</p>
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
const selectedList = ref([]);
const driveTitle = ref("Placement Drive")
onMounted(async()=>{
  const res =await api.get(`/company/drives/${route.params.id}/selected`);
  selectedList.value = res.data;
});
</script>
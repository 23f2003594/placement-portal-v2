<template>
  <div>
    <Navbar />
    <div class="container mt-4 mb-5">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4 gap-3">
        <div>
          <h2 class="mb-0 fw-bold text-dark">Placement Drives</h2>
          <p class="text-muted mb-0">Opportunities matching your profile and eligibility.</p>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-secondary shadow-sm" @click="$router.push('/student/dashboard')">
            <i class="bi bi-arrow-left"></i> Back
          </button>
          <div class="search-container shadow-sm">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0">
                <i class="bi bi-search text-muted"></i>
              </span>
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control border-start-0 ps-0" 
                placeholder="Search Role or Company..."
              />
            </div>
          </div>
        </div>
      </div>
      <div class="row g-4" v-if="drives.length > 0">
        <div v-for="drive in drives" :key="drive.id" class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 drive-card">
            <div class="card-body p-4 d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title text-primary fw-bold mb-0">{{ drive.title }}</h5>
                <span class="badge bg-success text-white px-2 py-1">
                  {{ drive.salary }} LPA
                </span>
              </div>
              <h6 class="card-subtitle mb-3 text-secondary fw-semibold">
                <i class="bi bi-building me-1"></i>{{ drive.company_name }}
              </h6>
              <p class="mb-2 small text-muted">
                <i class="bi bi-geo-alt-fill text-danger me-1"></i> 
                {{ drive.location || 'Remote / PAN India' }}
              </p>
              <p class="card-text text-secondary small mb-3 text-truncate-3">
                {{ drive.description }}
              </p>
              <button class="btn btn-sm btn-link text-decoration-none p-0 mb-3 text-start" @click="opendescription(drive)">
                Read Full Description...
              </button>
              <div class="mt-auto">
                <div class="d-flex flex-wrap gap-2 mb-3">
                  <span class="badge bg-light text-dark border">
                    CGPA: {{ drive.eligibility_cgpa }}+
                  </span>
                  <span class="badge bg-light text-dark border">
                    {{ drive.eligibility_branch }}
                  </span>
                </div>
                <button 
                  class="btn w-100 fw-bold py-2 shadow-sm" 
                  :class="drive.already_applied ? 'btn-secondary disabled' : 'btn-primary'"
                  @click="handleapply(drive.id)"
                  :disabled="drive.already_applied">
                  <i v-if="drive.already_applied" class="bi bi-check-circle-fill me-2"></i>
                  {{ drive.already_applied ? 'Already Applied' : 'Apply Now' }}
                </button>
              </div>
            </div>
            <div class="card-footer bg-light border-0 py-2">
              <small class="text-muted">
                <i class="bi bi-calendar-x me-1"></i> Deadline: {{ formatDate(drive.application_deadline) }}
              </small>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-5 mt-5">
        <i class="bi bi-clipboard-x fs-1 text-muted"></i>
        <p class="h5 text-muted mt-3">No active drives found.</p>
      </div>
      <div v-if="showModal && selectedDrive" class="modal-overlay" @click.self="closemodal">
        <div class="modal-dialog modal-lg">
          <div class="modal-content shadow-lg border-0 animate-in">
            <div class="modal-header bg-primary text-white p-3">
              <h5 class="modal-title">{{ selectedDrive.title }}</h5>
              <button type="button" class="btn-close btn-close-white" @click="closemodal"></button>
            </div>
            <div class="modal-body p-4">
              <div class="row mb-4">
                <div class="col-sm-6">
                  <label class="text-muted small fw-bold text-uppercase">Company</label>
                  <p class="h6">{{ selectedDrive.company_name }}</p>
                </div>
                <div class="col-sm-6">
                  <label class="text-muted small fw-bold text-uppercase">Salary Package</label>
                  <p class="h6 text-success">{{ selectedDrive.salary }} LPA</p>
                </div>
              </div>
              <hr>
              <h6 class="fw-bold mb-3">Job Description & Requirements</h6>
              <div class="description-box">
                {{ selectedDrive.description }}
              </div>
            </div>
            <div class="modal-footer bg-light">
              <button class="btn btn-secondary" @click="closemodal">Close</button>
              <button 
                v-if="!selectedDrive.already_applied" 
                class="btn btn-primary px-4" 
                @click="handleapply(selectedDrive.id); closemodal()">
                Apply Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue';
import api from '../services/api';
const router = useRouter();
const drives = ref([]);
const searchQuery = ref('');
const selectedDrive = ref(null);
const showModal = ref(false);
const fetchdrives = async()=>{
  try{
    const res =await api.get('/student/drives', {
      params: { search: searchQuery.value }
    });
    drives.value = res.data;
  }catch(err) {
    console.error("Error loading drives:", err);
  }
};
watch(searchQuery, ()=>{
  fetchdrives();
});
const handleapply = async(driveId)=>{
  try{
    const res =await api.post('/student/apply', { drive_id: driveId });
    alert(res.data.message);
    fetchdrives();
  }catch(err) {
    alert(err.response?.data?.message || "Eligibility check failed.");
  }
};
const opendescription = (drive)=>{
  selectedDrive.value = drive;
  showModal.value = true;
  document.body.style.overflow = 'hidden'; 
};
const closemodal = ()=>{
  showModal.value = false;
  selectedDrive.value = null;
  document.body.style.overflow = 'auto';
};
const formatDate = (dateStr)=>{
  if (!dateStr) return 'N/A';
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric'
  });
};
onMounted(fetchdrives);
</script>
<style scoped>
.drive-card { transition: all 0.3s ease; }
.drive-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.12) !important; }
.text-truncate-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 4.5em;
}
.search-container { width: 300px; }
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 20px;
}
.modal-content {
  background: white;
  border-radius: 12px;
  max-height: 90vh;
  overflow: hidden;
}
.description-box {
  white-space: pre-wrap;
  max-height: 400px;
  overflow-y: auto;
  color: #495057;
  line-height: 1.6;
}
.animate-in {
  animation: modalFadeIn 0.3s ease-out;
}
@keyframes modalFadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
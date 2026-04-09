<template>
  <div>
    <Navbar />
    <div class="container mt-4 mb-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="mb-0 fw-bold">Manage Placement Drives</h2>
          <p class="text-muted small">Review, Approve, or Close company recruitment requests.</p>
        </div>
        <button class="btn btn-outline-secondary shadow-sm" @click="$router.push('/admin/dashboard')">
          <i class="bi bi-arrow-left"></i> Back to Dashboard
        </button>
      </div>
      <div class="table-responsive card shadow-sm border-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-dark">
            <tr>
              <th>Job Title</th>
              <th>Company</th>
              <th>Eligibility</th>
              <th>Salary</th>
              <th>Status</th>
              <th class="text-center"> Description & Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in drives" :key="drive.id">
              <td>
                <div class="fw-bold text-primary">{{ drive.title }}</div>
                <small class="text-muted">Deadline: {{ formatDate(drive.application_deadline) }}</small>
              </td>
              <td>{{ drive.company_name }}</td>
              <td>
                <span class="badge bg-info-subtle text-info border border-info me-1">CGPA: {{ drive.eligibility_cgpa }}+</span>
                <span class="badge bg-light text-dark border">{{ drive.eligibility_branch }}</span>
              </td>
              <td><span class="fw-bold">{{ drive.salary }} LPA</span></td>
              <td>
                <span :class="statusbadge(drive.status)">{{ drive.status.toUpperCase() }}</span>
              </td>
              <td class="text-center">
                <div class="btn-group">
                  <button class="btn btn-sm btn-outline-primary" @click="opendescription(drive)">
                    <i class="bi bi-eye"></i> View
                  </button>
                  <button v-if="drive.status === 'pending'" 
                          class="btn btn-sm btn-success" 
                          @click="handleaction(drive.id, 'approve')">
                    Approve
                  </button>
                  <button v-if="drive.status === 'approved'" 
                          class="btn btn-sm btn-outline-danger" 
                          @click="handleaction(drive.id, 'close')">
                    Close
                  </button>
                </div>
                <span v-if="drive.status === 'closed'" class="text-muted small ms-2">Completed</span>
              </td>
            </tr>
            <tr v-if="drives.length === 0">
              <td colspan="6" class="text-center py-4 text-muted">No drives found.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="showModal && selectedDrive" class="modal-overlay" @click.self="closemodal">
        <div class="modal-dialog modal-lg">
          <div class="modal-content shadow-lg border-0 animate-in">
            <div class="modal-header bg-dark text-white">
              <h5 class="modal-title">Drive Details Review</h5>
              <button type="button" class="btn-close btn-close-white" @click="closemodal"></button>
            </div>
            <div class="modal-body p-4">
              <div class="row mb-4">
                <div class="col-md-6">
                  <label class="text-muted small fw-bold">POSTING TITLE</label>
                  <p class="h5 text-primary">{{ selectedDrive.title }}</p>
                </div>
                <div class="col-md-6">
                  <label class="text-muted small fw-bold">COMPANY</label>
                  <p class="h5">{{ selectedDrive.company_name }}</p>
                </div>
              </div>
              <hr>
              <h6 class="fw-bold mb-3">Job Description & Company Requirements</h6>
              <div class="description-box">
                {{ selectedDrive.description }}
              </div>
            </div>
            <div class="modal-footer bg-light">
              <button class="btn btn-secondary" @click="closemodal">Close</button>
              
              <button v-if="selectedDrive.status === 'pending'" 
                      class="btn btn-success px-4" 
                      @click="handleaction(selectedDrive.id, 'approve'); closemodal()">
                Approve Now
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
const drives = ref([]);
const selectedDrive = ref(null);
const showModal = ref(false);
const fetchdrives = async()=>{
  try{
    const res =await api.get('/admin/drives');
    drives.value = res.data;
  }catch(err) {
    console.error("Error loading drives");
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
const handleaction = async(id, action)=>{
  if (confirm(`Are you sure you want to ${action} this drive?`)) {
    try{
      await api.post(`/admin/drives/${id}/${action}`);
      fetchdrives();
    }catch(err) {
      alert("Action failed");
    }
  }
};
const formatDate = (dateStr)=>{
  if (!dateStr) return 'N/A';
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric'
  });
};
const statusbadge = (status)=>{
  return {
    'badge bg-warning text-dark': status === 'pending',
    'badge bg-success': status === 'approved',
    'badge bg-danger': status === 'closed'
  };
};
onMounted(fetchdrives);
</script>
<style scoped>
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
  max-height: 350px;
  overflow-y: auto;
  color: #495057;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}
.animate-in {
  animation: modalFadeIn 0.25s ease-out;
}
@keyframes modalFadeIn {
  from { opacity: 0; transform: scale(0.97); }
  to { opacity: 1; transform: scale(1); }
}
.bg-info-subtle { background-color: #e0f7fa; }
</style>
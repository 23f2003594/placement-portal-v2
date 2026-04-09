<template>
  <div>
    <Navbar />
    <div class="container mt-4 mb-5">
      <div class="card shadow-sm border-0 mb-4 bg-light">
        <div class="card-body d-flex justify-content-between align-items-center">
          <div>
            <h5 class="text-muted mb-1">Managing Applicants for</h5>
            <h2 class="mb-0 text-primary">{{ driveTitle }}</h2>
          </div>
          <div class="btn-group">
            <button class="btn btn-outline-success" @click="gotoselected">
              <i class="bi bi-trophy"></i> View Hired Students
            </button>
            <button class="btn btn-outline-secondary" @click="$router.push('/company/drives')">
              Back to My Drives
            </button>
          </div>
        </div>
      </div>
      <div class="card shadow-sm border-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-dark">
              <tr>
                <th>Student Details</th>
                <th>CGPA</th>
                <th>Status</th>
                <th>Interview Info</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applicants" :key="app.app_id">
                <td>
                  <div class="fw-bold">{{ app.name }}</div>
                  <small class="text-muted">{{ app.roll_no }}</small>
                </td>
                <td>
                  <span class="badge bg-info text-dark">{{ app.cgpa }}</span>
                </td>
                <td>
                  <span :class="statusbadge(app.status)">{{ app.status.toUpperCase() }}</span>
                </td>
                <td>
                  <div v-if="app.status === 'interview'" class="small text-primary fw-bold">
                    <i class="bi bi-calendar3 me-1"></i>
                    {{ formatInterviewDate(app.interview_date) }}
                  </div>
                  <span v-else class="text-muted small">--</span>
                </td>
                <td class="text-center">
                  <div v-if="app.status === 'placed'">
                    <span class="badge bg-success p-2">
                      <i class="bi bi-patch-check-fill"></i> HIRED
                    </span>
                  </div>
                  <div v-else-if="app.status !== 'rejected'" class="btn-group me-2">
                    <button v-if="app.status === 'applied'" 
                            class="btn btn-sm btn-success" @click="handleshortlist(app.app_id)">
                      Shortlist
                    </button>
                    <button v-if="app.status === 'shortlisted'" 
                            class="btn btn-sm btn-info text-white" @click="openinterview(app)">
                      Schedule
                    </button>
                    <button v-if="app.status === 'interview' || app.status === 'shortlisted'" 
                            class="btn btn-sm btn-primary" @click="handleselect(app.app_id)">
                      Select
                    </button>
                    <button v-if="app.status !== 'selected'"class="btn btn-sm btn-outline-danger" @click="handlereject(app.app_id)">
                      Reject
                    </button>
                  </div>
                  <div v-else class="d-inline-block me-2">
                    <span class="text-danger small fw-bold">CLOSED</span>
                  </div>
                  <button class="btn btn-sm btn-outline-dark ms-1" @click="fetchshowprofile(app.student_id)">
                    View Profile
                  </button>
                </td>
              </tr>
              <tr v-if="applicants.length === 0">
                <td colspan="5" class="text-center py-5 text-muted">No applications found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-if="modals.interview" class="modal-overlay">
      <div class="modal-dialog shadow-lg">
        <div class="modal-content p-4">
          <h4>Schedule Interview</h4>
          <p class="text-muted">Candidate: {{ selectedApp?.name }}</p>
          <div class="mb-3">
            <label class="form-label">Date and Time</label>
            <input type="datetime-local" v-model="form.interview_date" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Feedback/Notes</label>
            <textarea v-model="form.feedback" class="form-control" rows="3"></textarea>
          </div>
          <div class="d-flex justify-content-end gap-2">
            <button class="btn btn-secondary" @click="modals.interview = false">Cancel</button>
            <button class="btn btn-primary" @click="confirmschedule">Save Interview</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="modals.profile" class="modal-overlay" @click.self="modals.profile = false">
      <div class="modal-dialog shadow-lg" style="max-width: 500px;">
        <div class="modal-content p-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="mb-0">Student Profile</h4>
            <button class="btn-close" @click="modals.profile = false"></button>
          </div>
          <div v-if="currentStudent">
            <p><strong>Name:</strong>{{ currentStudent.name }}</p>
            <p><strong>Roll No:</strong>{{ currentStudent.roll_no }}</p>
            <p><strong>Email:</strong>{{ currentStudent.email }}</p>
            <p><strong>CGPA:</strong>{{ currentStudent.cgpa }}</p>
            <p><strong>Branch:</strong>{{ currentStudent.branch }}</p>
            <p><strong>Skills:</strong>{{ currentStudent.skills || 'Not specified' }}</p>
            <a :href="currentStudent.resume_link" target="_blank" class="btn btn-sm btn-primary w-100 mt-2">
              Open Resume <i class="bi bi-box-arrow-up-right"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Navbar from './Navbar.vue';
import api from '../services/api'
const route = useRoute();
const router = useRouter();
const applicants = ref([]);
const driveTitle = ref("Drive Applications");
const modals = ref({ interview: false, profile: false });
const selectedApp = ref(null);
const currentStudent = ref(null);
const form = ref({ interview_date: '', feedback: '' });
const fetchapps = async()=>{
  try{
    const res =await api.get(`/company/drives/${route.params.id}/applications`);
    console.log("Fetched Applicants:",res.data);
    applicants.value = res.data;
  }catch(err) { console.error("Fetch Error:", err); }
};
const handleshortlist = async(id)=>{
  if (!id) {
    alert("Application ID is undefined! Check console.");
    return;
  }
  try{
    await api.post(`/company/applications/${id}/shortlist`);
    fetchapps();
  }catch(err) { console.error("Shortlist API Error:", err); }
};
const handlereject = async(id)=>{
  if (!id) return;
  if (confirm("Reject this candidate? This action cannot be undone.")) {
    await api.post(`/company/applications/${id}/reject`);
    fetchapps();
  }
};
const formatInterviewDate = (dateStr)=>{
  if (!dateStr) return "Not Scheduled";
  try{
    const date = new Date(dateStr);
    return date.toLocaleString('en-IN', {
      timeZone : 'Asia/Kolkata',day: '2-digit',month: 'short',hour: '2-digit',minute: '2-digit',hour12: true
    });
  }catch(e){
    return dateStr; 
  }
};
const openinterview = (app)=>{
  selectedApp.value = app;
  modals.value.interview = true;
};
const confirmschedule = async()=>{
  try{
    const appId = selectedApp.value.app_id;
    if (!appId) {
      alert("Error: Application ID is missing.");
      return;
    }
    const res =await api.post(`/company/applications/${appId}/schedule`, {
      interview_date: form.value.interview_date,
      feedback: form.value.feedback
    });

    if (res.data.success) {
      modals.value.interview = false;
      form.value = { interview_date: '', feedback: '' }; 
      await fetchapps(); 
    }
  }catch(err) {
    console.error("Failed to schedule:", err.response?.data || err.message);
    alert("Error: Could not save the interview date.");
  }
};
const handleselect = async(id)=>{
  if (!id) return;
  const link = prompt("Enter Offer Letter Link:");
  if (link) {
    try{
      await api.post(`/company/applications/${id}/select`, { offer_link: link });
      fetchapps();
    }catch(err) {
      alert("Error selecting candidate. Make sure the placement table logic is correct.");
    }
  }
};
const fetchshowprofile = async(studentId)=>{
  const res =await api.get(`/company/students/${studentId}`);
  currentStudent.value = res.data;
  modals.value.profile = true;
};
const gotoselected = ()=>{
  router.push(`/company/drives/${route.params.id}/selected`);
};
const statusbadge = (status)=>{
  return {
    'badge bg-secondary': status === 'applied',
    'badge bg-info text-dark': status === 'shortlisted',
    'badge bg-warning text-dark': status === 'interview',
    'badge bg-success': status === 'selected' || status === 'placed',
    'badge bg-danger': status === 'rejected'
  };
};
onMounted(fetchapps);
</script>
<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.6);
  display: flex; justify-content: center; align-items: center;
  z-index: 1050;
}
.modal-dialog { width: 90%; max-width: 500px; }
.modal-content { background: white; border-radius: 8px; border: none; }
</style>
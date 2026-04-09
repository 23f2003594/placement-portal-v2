<template>
  <div class="dashboard-wrapper">
    <Navbar />
    <div class="container mt-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="card bg-primary text-white shadow-sm border-0 p-4">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h1 class="display-6 mb-1">Welcome, Student!</h1>
                <p class="mb-0 opacity-75">Track your career progress and apply for new opportunities.</p>
              </div>
              <div class="text-end">
                <span class="badge bg-light text-primary px-3 py-2">
                  <i class="bi bi-shield-check"></i> Authenticated
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card h-100 shadow-sm border-0 hover-card" @click="$router.push('/student/drives')">
            <div class="card-body text-center p-4">
              <div class="icon-circle bg-info-subtle text-info mb-3 mx-auto">
                <i class="bi bi-briefcase fs-2"></i>
              </div>
              <h4>Placement Drives</h4>
              <p class="text-muted">Explore and apply to the latest job openings from top companies.</p>
              <button class="btn btn-outline-info w-100">Browse Jobs</button>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card h-100 shadow-sm border-0 hover-card" @click="$router.push('/student/applications')">
            <div class="card-body text-center p-4">
              <div class="icon-circle bg-success-subtle text-success mb-3 mx-auto">
                <i class="bi bi-journal-text fs-2"></i>
              </div>
              <h4>My Applications</h4>
              <p class="text-muted">Check your interview schedules, feedback, and offer letters.</p>
              <button class="btn btn-outline-success w-100">View History</button>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card h-100 shadow-sm border-0 hover-card" @click="$router.push('/student/profile/${userId}')">
            <div class="card-body text-center p-4">
              <div class="icon-circle bg-warning-subtle text-warning mb-3 mx-auto">
                <i class="bi bi-person-gear fs-2"></i>
              </div>
              <h4>My Profile</h4>
              <p class="text-muted">Keep your CGPA, Skills, and Resume link updated for recruiters.</p>
              <button class="btn btn-outline-warning w-100">Update Profile</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue';
const router = useRouter();
const userRole = ref('');
onMounted(()=>{
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  if (!token || role !== 'student') {
    router.push('/');
  } else {
    userRole.value = role;
  }
});
</script>
<style scoped>
.dashboard-wrapper {
  background-color: #f8f9fa;
  min-height: 100vh;
}
.hover-card {
  transition: transform 0.2s, shadow 0.2s;
  cursor: pointer;
}
.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}
.icon-circle {
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}
.bg-info-subtle { background-color: #e0f7fa; }
.bg-success-subtle { background-color: #e8f5e9; }
.bg-warning-subtle { background-color: #fff3e0; }
</style>
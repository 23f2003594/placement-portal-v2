<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4">
    <div class="container">
      <router-link class="navbar-brand fw-bold" :to="dashboardLink">
        Placement Portal
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item" v-if="role === 'admin'">
            <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="role === 'student'">
            <router-link class="nav-link" to="/student/dashboard">My Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="role === 'company'">
            <router-link class="nav-link" to="/company/dashboard">Company Portal</router-link>
          </li>
        </ul>
        <div class="d-flex align-items-center">
          <span class="navbar-text me-3 text-light small">
            Logged in as: <strong>{{ role.toUpperCase() }}</strong>
          </span>
          <button class="btn btn-outline-danger btn-sm" @click="handlelogout">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
const router = useRouter();
const role = ref(localStorage.getItem('role') || '');
const dashboardLink = computed(()=>{
  if (role.value === 'admin') return '/admin/dashboard';
  if (role.value === 'company') return '/company/dashboard';
  return '/student/dashboard';
});
const handlelogout = ()=>{
  localStorage.clear();
  router.push('/');
};
</script>
<style scoped>
.nav-link.router-link-active {
  color: #fff !important;
  font-weight: bold;
}
</style>
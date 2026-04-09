<template>
  <div>
    <Navbar/>
    <div class="container mt-4">
      <h2 class="mb-4">Admin Dashboard</h2>
      <div class="row">
        <div class="col-md-3" v-for="card in stats" :key="card.title">
          <div class="card shadow-sm mb-4 text-center">
            <div class="card-body">
              <h5 class="card-title">{{ card.title }}</h5>
              <h2 class="text-primary">{{ card.value }}</h2>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-md-3">
          <button class="btn btn-outline-success w-100 mb-3"
                  @click="$router.push('/admin/students')">
            Manage Students
          </button>
        </div>
        <div class="col-md-3">
          <button class="btn btn-outline-primary w-100 mb-3"
                  @click="$router.push('/admin/companies')">
            Manage Companies
          </button>
        </div>
        <div class="col-md-3">
          <button class="btn btn-outline-warning w-100 mb-3"
                  @click="$router.push('/admin/drives')">
            Manage Drives
          </button>
        </div>
        <div class="col-md-3">
          <button class="btn btn-outline-dark w-100 mb-3"
                  @click="$router.push('/admin/applications')">
            View Applications
          </button>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100 shadow-sm border-0 hover-card" @click="$router.push('/admin/placements')">
          <div class="card-body text-center p-4">
            <div class="icon-circle bg-primary-subtle text-primary mb-3 mx-auto">
              <i class="bi bi-trophy fs-2"></i>
            </div>
            <h4>Placement Records</h4>
            <p class="text-muted small">View all finalized placements and download offer letters.</p>
            <button class="btn btn-outline-primary w-100 mt-2">View Records</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../components/Navbar.vue"
import api from "../services/api"
export default {
  name: "AdminDashboard",
  components:{Navbar},
  data() {
    return {
      stats: [
        { title: "Students", value: 0 },
        { title: "Companies", value: 0 },
        { title: "Drives", value: 0 },
        { title: "Applications", value: 0 }
      ]
    }
  },
  async mounted() {
    try{
      const res =await api.get("/admin/dashboard")
      console.log(res.data);
      this.stats = [
        { title: "Students", value: res.data.total_students },
        { title: "Companies", value: res.data.total_companies },
        { title: "Drives", value: res.data.total_drives },
        { title: "Applications", value: res.data.total_applications }
      ]
    }catch(err) {
      console.error(err)
    }
  }
}
</script>
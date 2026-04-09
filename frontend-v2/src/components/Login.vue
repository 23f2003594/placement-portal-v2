<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 400px; border-radius: 12px;">
      <h3 class="text-center mb-3">Placement Portal</h3>
      <p class="text-center text-muted">Login to continue</p>
      <div class="mb-3">
        <label>Email</label>
        <input v-model="email" class="form-control" placeholder="Enter email" @keyup.enter="login" />
      </div>
      <div class="mb-3">
        <label>Password</label>
        <input v-model="password" type="password" class="form-control" placeholder="Enter password" @keyup.enter="login" />
      </div>
      <button class="btn btn-primary w-100" @click="login">
        Login
      </button>
      <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
      <hr>
      <div class="text-center">
        <small>
          New user?
          <router-link to="/register/student">Student</router-link> |
          <router-link to="/register/company">Company</router-link>
        </small>
      </div>
    </div>
  </div>
</template>
<script>
import api from "../services/api"
export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      error: ""
    }
  },
  methods: {
    async login() {
      this.error = ""; 
      try{
        const res =await api.post("/login", {
          email: this.email,
          password: this.password
        });
        localStorage.setItem('token',res.data.token);
        localStorage.setItem('role',res.data.role);
        const role = res.data.role;
        if (role === "admin") this.$router.push("/admin/dashboard");
        else if (role === "company") this.$router.push("/company/dashboard");
        else this.$router.push("/student/dashboard");
      }catch(err) {
        this.error = err.response?.data?.message || "Login failed";
      }
    }
  }
}
</script>
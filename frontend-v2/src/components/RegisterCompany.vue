<template>
  <div class="container mt-5">
    <div class="card p-4 shadow" style="max-width: 500px; margin:auto;">
      <h3 class="text-center mb-3">Company Registration</h3>
      <input v-model="form.name" class="form-control mb-2" placeholder="Company Name" />
      <input v-model="form.email" class="form-control mb-2" placeholder="Email" />
      <input v-model="form.password" type="password" class="form-control mb-2" placeholder="Password" />
      <input v-model="form.industry" class="form-control mb-2" placeholder="Industry" />
      <input v-model="form.location" class="form-control mb-2" placeholder="Location" />
      <input v-model="form.hr_contact" class="form-control mb-2" placeholder="HR Contact" />
      <input v-model="form.website" class="form-control mb-2" placeholder="Website" />
      <button class="btn btn-success w-100 mt-2" @click="register">
        Register
      </button>
      <p class="text-danger mt-2">{{ error }}</p>
    </div>
  </div>
</template>
<script>
import api from "../services/api"
export default {
  name: "RegisterCompany",
  data() {
    return {
      form: {
        name: "",
        email: "",
        password: "",
        industry: "",
        location: "",
        hr_contact: "",
        website: ""
      },
      error: ""
    }
  },
  methods: {
    async register() {
      try{
        const res =await api.post("/register/company", this.form)
        alert(res.data.message)
        this.$router.push("/")
      }catch(err) {
        this.error = err.response?.data?.message || "Registration failed"
      }
    }
  }
}
</script>
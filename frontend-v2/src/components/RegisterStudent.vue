<template>
  <div class="container mt-5">
    <div class="card shadow p-4 mx-auto" style="max-width: 500px; border-radius: 12px;">
      <h3 class="text-center">Student Registration</h3>
      <div class="mb-2"><label>Name</label><input v-model="form.name" class="form-control" /></div>
      <div class="mb-2"><label>Email</label><input v-model="form.email" class="form-control" /></div>
      <div class="mb-2"><label>Password</label><input v-model="form.password" type="password" class="form-control" /></div>
      <div class="mb-2"><label>Roll No</label><input v-model="form.roll_no" class="form-control" /></div>
      <div class="mb-2"><label>Branch</label><input v-model="form.branch" class="form-control" /></div>
      <div class="mb-2"><label>Year</label><input v-model="form.year" class="form-control" /></div>
      <div class="mb-2"><label>CGPA</label><input v-model="form.cgpa" class="form-control" /></div>
      <div class="mb-2"><label>Education</label><input v-model="form.education" class="form-control" /></div>
      <div class="mb-2"><label>Skills</label><input v-model="form.skills" class="form-control" /></div>
      <div class="mb-2"><label>Resume_Link</label><input v-model="form.resume_link" class="form-control" /></div>
      </div>
      <button class="btn btn-success w-100 mt-3" @click="handleregister">Register</button>
      <p v-if="msg" :class="success ? 'text-success' : 'text-danger'" class="mt-2 text-center">{{ msg }}</p>
      <router-link to="/" class="d-block text-center mt-2">Back to Login</router-link>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import api from '../services/api';
import { useRouter } from 'vue-router';
const router = useRouter();
const msg = ref('');
const success = ref(false);
const form = ref({ name: '', email: '', password: '', roll_no: '', branch: '', year: '', cgpa: '', education: '', skills: '',resume_link: '' });
const handleregister = async()=>{
  try{
    const res =await api.post('/register/student', form.value);
    msg.value = res.data.message;
    success.value = true;
    setTimeout(()=> router.push('/'), 2000);
  }catch(err) {
    msg.value = err.response?.data?.message || "Error";
    success.value = false;
  }
};
</script>
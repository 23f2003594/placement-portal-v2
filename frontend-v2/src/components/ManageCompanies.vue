<template>
  <div class="container mt-4">
    <div class="card shadow-sm p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Manage Companies</h2>
        <button class="btn btn-outline-secondary" @click="$router.push('/admin/dashboard')">Back to Dashboard</button>
      </div>
      <div class="row mb-3 g-2">
        <div class="col-md-6">
          <input v-model="searchQuery" @input="fetchcompanies" class="form-control" placeholder="Search by name or industry..." />
        </div>
        <div class="col-md-6 text-end">
          <button :class="viewMode === 'all' ? 'btn btn-primary' : 'btn btn-outline-primary'" 
                  @click="setviewmode('all')" class="me-2">All Companies</button>
          <button :class="viewMode === 'pending' ? 'btn btn-warning' : 'btn btn-outline-warning'" 
                  @click="setviewmode('pending')">Pending Approvals</button>
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Company Name</th>
              <th>Industry</th>
              <th>Email</th>
              <th>Status</th>
              <th>System Access</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in filteredCompanies" :key="c.id">
              <td><strong>{{ c.name }}</strong></td>
              <td>{{ c.industry }}</td>
              <td>{{ c.email }}</td>
              <td>
                <span :class="getstatusclass(c.approval_status)">{{ c.approval_status }}</span>
              </td>
              <td>
                <span :class="c.is_active ? 'text-success' : 'text-danger'">
                  {{ c.is_active ? 'Active' : 'Blacklisted' }}
                </span>
              </td>
              <td>
                <div v-if="c.approval_status === 'pending'" class="btn-group btn-group-sm mb-1 d-block">
                  <button class="btn btn-success" @click="handleaction(c.id, 'approve')">Approve</button>
                  <button class="btn btn-danger" @click="handleaction(c.id, 'reject')">Reject</button>
                </div>
                
                <button v-if="c.approval_status === 'approved'" 
                        :class="c.is_active ? 'btn btn-sm btn-outline-danger' : 'btn btn-sm btn-outline-success'"
                        @click="toggleactive(c.user_id)">
                  {{ c.is_active ? 'Blacklist' : 'Unblacklist' }}
                </button>
              </td>
            </tr>
            <tr v-if="filteredCompanies.length === 0">
              <td colspan="6" class="text-center py-4 text-muted">No companies found matching criteria.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
const companies = ref([]);
const searchQuery = ref('');
const viewMode = ref('all'); 
const fetchcompanies = async()=>{
  try{
    const res =await api.get('/admin/companies', { params: { q: searchQuery.value } });
    companies.value = res.data;
  }catch(err) { console.error(err); }
};
const setviewmode = (mode)=>{ viewMode.value = mode; };
const filteredCompanies = computed(()=>{
  if (viewMode.value === 'pending') {
    return companies.value.filter(c => c.approval_status === 'pending');
  }
  return companies.value;
});
const handleaction = async(id, action)=>{
  try{
    await api.post(`/admin/companies/${id}/${action}`);
    fetchcompanies();
  }catch(err) { alert("Action failed"); }
};
const toggleactive = async(userId)=>{
  try{
    await api.post(`/admin/companies/${userId}/toggle-active`);
    fetchcompanies();
  }catch(err) { alert("Status update failed"); }
};
const getstatusclass = (status)=>{
  return {
    'badge bg-warning text-dark': status === 'pending',
    'badge bg-success': status === 'approved',
    'badge bg-danger': status === 'rejected'
  };
};
onMounted(fetchcompanies);
</script>
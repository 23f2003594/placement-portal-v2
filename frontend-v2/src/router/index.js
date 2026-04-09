import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import StudentDashboard from '../components/StudentDashboard.vue';
import RegisterStudent from '../components/RegisterStudent.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import RegisterCompany from '../components/RegisterCompany.vue';
import ManageCompanies from '../components/ManageCompanies.vue';
import ManageStudents from '../components/ManageStudents.vue';
import AdminStudentProfile from '../components/AdminStudentProfile.vue';
import StudentProfile from '../components/StudentProfile.vue';
import ManageDrives from '../components/ManageDrives.vue';
import DriveApplications from '../components/DriveApplications.vue';
import AdminApplications from '../components/AdminApplications.vue';
import CompanyDashboard from '../components/CompanyDashboard.vue';
import CreateDrive from '../components/CreateDrive.vue';
import CompanyDrives from '../components/CompanyDrives.vue';
import ViewApplicants from '../components/ViewApplicants.vue';
import SelectedStudents from '../components/SelectedStudents.vue';
import StudentDrives from '../components/StudentDrives.vue';
import StudentHistory from '../components/StudentHistory.vue';
import AdminPlacements from '../components/AdminPlacements.vue';

const routes = [
  { 
    path: '/', 
    name: 'Login',
    component: Login 
  },
  { 
    path: '/student/dashboard', 
    name: 'StudentDashboard',
    component: StudentDashboard 
  },
  {
    path: '/register/student',
    name: 'RegisterStudent',
    component: RegisterStudent
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/register/company',
    name: 'RegisterCompany',
    component: RegisterCompany
  },
  {
    path: '/admin/companies',
    name: 'ManageCompanies',
    component: ManageCompanies
  },
  {
    path: '/admin/students',
    name: 'ManageStudents',
    component: ManageStudents
  },
  {
    path: '/admin/students/:id',
    name: 'AdminStudentProfile',
    component: AdminStudentProfile
  },
  {
    path: '/student/profile/:id',
    name: 'StudentProfile',
    component: StudentProfile
  },
  {
    path: '/admin/drives',
    name: 'ManageDrives',
    component: ManageDrives
  },
  {
    path: '/admin/applications',
    name: 'AdminApplications',
    component: AdminApplications
  },
  {
    path: '/admin/applications/drive/:id',
    name: 'DriveApplications',
    component: DriveApplications
  },
  {
    path: '/company/dashboard',
    name: 'CompanyDashboard',
    component: CompanyDashboard
  },
  {
    path: '/company/drives/create',
    name: 'CreateDrive',
    component: CreateDrive
  },
  {
    path: '/company/drives',
    name: 'CompanyDrives',
    component: CompanyDrives
  },
  {
    path: '/company/drives/:id/applicants',
    name: 'ViewApplicants',
    component: ViewApplicants
  },
  {
    path: '/company/drives/:id/selected',
    name: 'SelectedStudents',
    component: SelectedStudents
  },
  {
    path: '/student/drives',
    name: 'StudentDrives',
    component: StudentDrives
  },
  {
    path: '/student/applications',
    name: 'StudentHistory',
    component: StudentHistory
  },
  {
    path: '/admin/placements',
    name: 'AdminPlacements',
    component: AdminPlacements
  }
];
const router = createRouter({
  history: createWebHistory(),
  routes
});
export { router };
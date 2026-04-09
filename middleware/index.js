const express = require('express');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());
const JWT_SECRET = "shakthi_secret_key_2026";
const FLASK_URL = "http://localhost:5000";


const verifyAdmin=(req,res,next)=>{
    const authHeader=req.headers['authorization'];
    const token=authHeader && authHeader.split(' ')[1];
    if (!token) return res.status(401).json({message:"No token provided"});
    try{
        const decoded=jwt.verify(token,JWT_SECRET);
        if(decoded.role!=='admin') {
            return res.status(403).json({message:"Admin access required"});
        }
        req.user=decoded;
        next();
    }catch(err){
        res.status(401).json({message:"Invalid token"});
    }
};

const verifyStudent=(req,res,next)=>{
    const authHeader=req.headers['authorization'];
    const token=authHeader && authHeader.split(' ')[1];
    if(!token)return res.status(401).json({message:"No token provided"});
    try{
        const decoded=jwt.verify(token,JWT_SECRET);
        if(decoded.role!=='student'){
            return res.status(403).json({message:"Student access required"});
        }
        req.user = decoded;
        next();
    }catch(err){
        res.status(401).json({message:"Invalid token"});
    }
};

const verifyCompany=(req,res,next)=>{
    const authHeader=req.headers['authorization'];
    const token=authHeader && authHeader.split(' ')[1];
    if (!token)return res.status(401).json({message:"No token provided"});
    try{
        const decoded=jwt.verify(token,JWT_SECRET);
        if(decoded.role!=='company'){
            return res.status(403).json({message:"Company access required"});
        }
        req.user=decoded;
        next();
    }catch(err){
        res.status(401).json({message:"Invalid token"});
    }
};

// --- AUTH & PUBLIC ROUTES ---

app.get('/api/test',(req,res)=>{
    res.json({message:"Express is alive!"});
});

app.post('/api/login',async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/auth/login`,req.body);
        if (response.data.success){
            const userData=response.data.user;
            const token=jwt.sign(userData,JWT_SECRET,{expiresIn:'1h'});
            res.json({success:true,token,role:userData.role});
        }
    }catch(error){
        res.status(error.response?.status || 500).json({
            message: error.response?.data?.message || "Server Error"
        });
    }
});

app.post('/api/register/student',async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/auth/register/student`,req.body);
        res.json(response.data);
    }catch(error){
        res.status(error.response?.status || 500).json({message:"Registration failed"});
    }
});

app.post('/api/register/company',async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/auth/register/company`,req.body);
        res.json(response.data);
    }catch(error){
        res.status(error.response?.status || 500).json({ message:"Company registration failed"});
    }
});

// --- ADMIN ROUTES ---

app.get('/api/admin/dashboard',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/dashboard`);
        res.json(response.data);
    }catch(error){res.status(500).json({ message:"Error contacting Flask"}); }
});

app.get('/api/admin/companies',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/companies`,{params:req.query});
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch companies"}); }
});

app.get('/api/admin/companies/pending',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/companies/pending`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch pending companies"}); }
});

app.post('/api/admin/companies/:id/approve',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/admin/companies/${req.params.id}/approve`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Approval failed"}); }
});

app.post('/api/admin/companies/:id/reject',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/admin/companies/${req.params.id}/reject`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Rejection failed"}); }
});
app.post('/api/admin/companies/:userId/toggle-active',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/admin/companies/${req.params.userId}/toggle-active`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Update failed"}); }
});
app.get('/api/admin/students',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/students`,{params:req.query});
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch students"}); }
});
app.get('/api/admin/students/:id',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/students/${req.params.id}`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch student profile"}); }
});
app.post('/api/admin/students/:id/toggle-blacklist',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/admin/students/${req.params.id}/toggle-blacklist`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Update failed"}); }
});
app.get('/api/admin/drives',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/drives`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch drives"}); }
});
app.post('/api/admin/drives/:id/:action',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/admin/drives/${req.params.id}/${req.params.action}`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Action failed"}); }
});
app.get('/api/admin/drives/:id/applications',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/drives/${req.params.id}/applications`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch applicants"}); }
});
app.get('/api/admin/placements',verifyAdmin,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/admin/placements`);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to fetch placements"}); }
});

// --- COMPANY ROUTES ---
app.get('/api/company/stats',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/company/stats/${req.user.id}`);
        res.json(response.data);
    }catch(error){res.status(401).json({message:"Error fetching stats"}); }
});
app.post('/api/company/drives/create',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/company/drives/create/${req.user.id}`,req.body);
        res.json(response.data);
    }catch(error){res.status(500).json({message:"Failed to create drive"}); }
});
app.get('/api/company/drives',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/company/drives/list/${req.user.id}`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.get('/api/company/drives/:id/applications',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/company/drives/${req.params.id}/applications`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.post('/api/company/applications/:id/shortlist',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/company/applications/${req.params.id}/shortlist`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.post('/api/company/applications/:id/reject',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/company/applications/${req.params.id}/reject`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.post('/api/company/applications/:id/schedule',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/company/applications/${req.params.id}/schedule`, req.body);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.post('/api/company/applications/:id/select',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/company/applications/${req.params.id}/select`, req.body);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.get('/api/company/drives/:id/selected',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/company/drives/${req.params.id}/selected`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.get('/api/company/students/:id',verifyCompany,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/company/students/${req.params.id}`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
// --- STUDENT ROUTES ---

app.all('/api/student/profile',verifyStudent,async(req,res)=>{
    try{
        const url = `${FLASK_URL}/student/profile/${req.user.id}`;
        if (req.method === 'GET') {
            const response=await axios.get(url);
            res.json(response.data);
        } else if (req.method === 'POST') {
            const response=await axios.post(url, req.body);
            res.json(response.data);
        }
    }catch(error) {res.status(500).json({ message: "Profile action failed" }); }
});
app.get('/api/student/drives',verifyStudent,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/student/drives/${req.user.id}`, {
            params: { search: req.query.search || "" }
        });
        res.json(response.data);
    }catch(e){res.status(500).send("Error fetching drives"); }
});
app.post('/api/student/apply',verifyStudent,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/student/apply`, {
            user_id: req.user.id,
            drive_id: req.body.drive_id
        });
        res.json(response.data);
    }catch(e){res.status(500).send("Application failed"); }
});
app.get('/api/student/applications',verifyStudent,async(req,res)=>{
    try{
        const response=await axios.get(`${FLASK_URL}/student/applications/${req.user.id}`);
        res.json(response.data);
    }catch(e){res.status(500).send("Failed to fetch applications"); }
});
app.get('/api/student/applications/:userId',verifyStudent,async(req,res)=>{
    try{
        if (parseInt(req.params.userId) !== req.user.id) {
            return res.status(403).json({ message: "Access denied" });
        }
        const response=await axios.get(`${FLASK_URL}/student/applications/${req.user.id}`);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.post('/api/student/accept-offer',verifyStudent,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/student/accept-offer`, req.body);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});
app.post('/api/student/reject-offer',verifyStudent,async(req,res)=>{
    try{
        const response=await axios.post(`${FLASK_URL}/student/reject-offer`, req.body);
        res.json(response.data);
    }catch(e){res.status(500).send(e.message); }
});

app.listen(3000, ()=> console.log("Express running on port 3000"));
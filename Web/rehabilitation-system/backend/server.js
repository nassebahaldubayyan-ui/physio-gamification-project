const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
const db = require('./db');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' })); // Increased limit for photos

// Test database connection
async function testDBConnection() {
    try {
        const [result] = await db.query('SELECT 1 + 1 AS solution');
        console.log('✅ Connected to MySQL database');
    } catch (error) {
        console.error('❌ Database connection failed:', error.message);
    }
}
testDBConnection();

// Serve static files
app.use(express.static(path.join(__dirname, '../frontend')));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Create uploads directory if it doesn't exist
const fs = require('fs');
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
    console.log('📁 Created uploads directory');
}

// API routes
const authRoutes = require('./routes/auth');
const messageRoutes = require('./routes/messages');
const patientRoutes = require('./routes/patients');

app.use('/api/auth', authRoutes);
app.use('/api/messages', messageRoutes);
app.use('/api/patients', patientRoutes);

// Serve index.html for root path
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`✅ Server running on port ${PORT}`);
});
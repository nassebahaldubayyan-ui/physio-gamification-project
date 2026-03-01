const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../db');

router.post('/register/patient', async (req, res) => {
    try {
        const { name, email, password, phone, dateOfBirth, gender, medicalCondition, therapyType } = req.body;

        if (!name || !email || !password || !phone) {
            return res.status(400).json({ 
                message: 'Please provide all required fields' 
            });
        }

        const [existing] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        if (existing.length > 0) {
            return res.status(400).json({ 
                message: 'Email already exists' 
            });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const [userResult] = await db.query(
            'INSERT INTO users (name, email, password, role, phone) VALUES (?, ?, ?, ?, ?)',
            [name, email, hashedPassword, 'patient', phone]
        );

        const userId = userResult.insertId;

        const patientId = `PT${String(userId).padStart(3, '0')}`;

        await db.query(
            `INSERT INTO patients 
            (user_id, patient_id, date_of_birth, gender, medical_condition, therapy_type) 
            VALUES (?, ?, ?, ?, ?, ?)`,
            [userId, patientId, dateOfBirth || '2000-01-01', gender || 'male', 
             medicalCondition || 'Not specified', therapyType || 'Physical Therapy']
        );

        const token = jwt.sign(
            { id: userId, email, role: 'patient' },
            process.env.JWT_SECRET,
            { expiresIn: process.env.JWT_EXPIRE }
        );

        res.status(201).json({
            success: true,
            message: 'Patient registered successfully',
            token,
            user: {
                id: userId,
                name,
                email,
                role: 'patient',
                patientId
            }
        });

    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ 
            success: false,
            message: 'Server error during registration',
            error: error.message 
        });
    }
});

router.post('/register/doctor', async (req, res) => {
    try {
        const { name, email, password, phone, specialty, licenseNumber, hospital, experience } = req.body;

        if (!name || !email || !password || !phone || !specialty || !licenseNumber || !hospital) {
            return res.status(400).json({ 
                message: 'Please provide all required fields' 
            });
        }

        const [existing] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        if (existing.length > 0) {
            return res.status(400).json({ 
                message: 'Email already exists' 
            });
        }

        const [existingLicense] = await db.query('SELECT * FROM doctors WHERE license_number = ?', [licenseNumber]);
        if (existingLicense.length > 0) {
            return res.status(400).json({ 
                message: 'License number already exists' 
            });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const [userResult] = await db.query(
            'INSERT INTO users (name, email, password, role, phone) VALUES (?, ?, ?, ?, ?)',
            [name, email, hashedPassword, 'doctor', phone]
        );

        const userId = userResult.insertId;

        const doctorId = `DR${String(userId).padStart(3, '0')}`;

        await db.query(
            `INSERT INTO doctors 
            (user_id, doctor_id, specialty, license_number, hospital, experience) 
            VALUES (?, ?, ?, ?, ?, ?)`,
            [userId, doctorId, specialty, licenseNumber, hospital, experience || 0]
        );

        const token = jwt.sign(
            { id: userId, email, role: 'doctor' },
            process.env.JWT_SECRET,
            { expiresIn: process.env.JWT_EXPIRE }
        );

        res.status(201).json({
            success: true,
            message: 'Doctor registered successfully',
            token,
            user: {
                id: userId,
                name,
                email,
                role: 'doctor',
                doctorId
            }
        });

    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ 
            success: false,
            message: 'Server error during registration',
            error: error.message 
        });
    }
});

router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ 
                message: 'Please provide email and password' 
            });
        }

        const [users] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        
        if (users.length === 0) {
            return res.status(401).json({ 
                message: 'Invalid email or password' 
            });
        }

        const user = users[0];

        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ 
                message: 'Invalid email or password' 
            });
        }

        if (!user.is_active) {
            return res.status(403).json({ 
                message: 'Account is deactivated. Please contact support.' 
            });
        }

        await db.query('UPDATE users SET last_login = NOW() WHERE id = ?', [user.id]);

        let additionalData = {};
        if (user.role === 'patient') {
            const [patientData] = await db.query(
                'SELECT * FROM patients WHERE user_id = ?', 
                [user.id]
            );
            if (patientData.length > 0) {
                additionalData = patientData[0];
            }
        } else if (user.role === 'doctor') {
            const [doctorData] = await db.query(
                'SELECT * FROM doctors WHERE user_id = ?', 
                [user.id]
            );
            if (doctorData.length > 0) {
                additionalData = doctorData[0];
            }
        }

        const token = jwt.sign(
            { id: user.id, email: user.email, role: user.role },
            process.env.JWT_SECRET,
            { expiresIn: process.env.JWT_EXPIRE }
        );

        res.json({
            success: true,
            message: 'Login successful',
            token,
            user: {
                id: user.id,
                name: user.name,
                email: user.email,
                role: user.role,
                phone: user.phone,
                avatar: user.avatar,
                ...additionalData
            }
        });

    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ 
            success: false,
            message: 'Server error during login',
            error: error.message 
        });
    }
});

router.get('/me', async (req, res) => {
    try {
        res.status(401).json({ 
            message: 'Authentication required' 
        });
        
    } catch (error) {
        console.error('Profile error:', error);
        res.status(500).json({ 
            message: 'Server error' 
        });
    }
});

module.exports = router;
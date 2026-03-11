const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const db = require('../db');
const { protect } = require('../middleware/auth');

// ============================================
// Get all patients (for doctors)
// ============================================
router.get('/', protect, async (req, res) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;
        const skip = (page - 1) * limit;

        const filter = {};
        if (req.query.status) {
            filter.status = req.query.status;
        }
        if (req.query.condition) {
            filter.condition = req.query.condition;
        }

        const [patients] = await db.query(
            `SELECT u.id, u.name, u.email, u.phone, 
                    p.patient_id, p.date_of_birth, p.gender, p.affected_hand,
                    p.medical_condition, p.therapy_type, p.current_level,
                    p.shoulder_strength, p.elbow_strength, p.wrist_strength,
                    p.grip_strength, p.external_rotation, p.photo_url, p.video_url,
                    p.initial_assessment_date, p.last_assessment_date
             FROM users u
             JOIN patients p ON u.id = p.user_id
             WHERE u.role = 'patient'
             ORDER BY u.created_at DESC
             LIMIT ? OFFSET ?`,
            [limit, skip]
        );

        const [totalResult] = await db.query(
            'SELECT COUNT(*) as total FROM users WHERE role = "patient"'
        );

        res.json({
            success: true,
            data: patients,
            pagination: {
                page,
                limit,
                total: totalResult[0].total,
                pages: Math.ceil(totalResult[0].total / limit)
            }
        });

    } catch (error) {
        console.error('Get patients error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error',
            error: error.message 
        });
    }
});

// ============================================
// Get single patient by ID
// ============================================
router.get('/:patientId', protect, async (req, res) => {
    try {
        const { patientId } = req.params;

        const [patients] = await db.query(
            `SELECT u.id, u.name, u.email, u.phone, u.created_at,
                    p.patient_id, p.date_of_birth, p.gender, p.affected_hand,
                    p.medical_condition, p.therapy_type, p.current_level,
                    p.emergency_contact_name, p.emergency_contact_phone,
                    p.address, p.city, p.country,
                    p.shoulder_strength, p.elbow_strength, p.wrist_strength,
                    p.grip_strength, p.external_rotation,
                    p.photo_url, p.video_url, p.initial_assessment_date, p.last_assessment_date
             FROM users u
             JOIN patients p ON u.id = p.user_id
             WHERE p.patient_id = ?`,
            [patientId]
        );

        if (patients.length === 0) {
            return res.status(404).json({ 
                success: false, 
                message: 'Patient not found' 
            });
        }

        // Get recent game sessions
        const [sessions] = await db.query(
            `SELECT * FROM game_sessions 
             WHERE patient_id = (SELECT id FROM patients WHERE patient_id = ?)
             ORDER BY session_date DESC
             LIMIT 10`,
            [patientId]
        );

        // Get progress tracking
        const [progress] = await db.query(
            `SELECT * FROM progress_tracking 
             WHERE patient_id = (SELECT id FROM patients WHERE patient_id = ?)
             ORDER BY tracking_date DESC
             LIMIT 30`,
            [patientId]
        );

        res.json({
            success: true,
            data: {
                ...patients[0],
                recentSessions: sessions,
                progressHistory: progress
            }
        });

    } catch (error) {
        console.error('Get patient error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error',
            error: error.message 
        });
    }
});

// ============================================
// Register new patient (for doctors)
// ============================================
router.post('/register', protect, async (req, res) => {
    try {
        const { 
            name, email, password, phone, dateOfBirth, 
            gender, affectedHand, medicalCondition, therapyType 
        } = req.body;

        // Check if user exists
        const [existing] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        if (existing.length > 0) {
            return res.status(400).json({ 
                message: 'Email already exists' 
            });
        }

        // Hash password (in real app, use bcrypt)
        const hashedPassword = password; // In production: await bcrypt.hash(password, 10);

        // Insert into users table
        const [userResult] = await db.query(
            'INSERT INTO users (name, email, password, role, phone) VALUES (?, ?, ?, ?, ?)',
            [name, email, hashedPassword, 'patient', phone]
        );

        const userId = userResult.insertId;

        // Generate patient ID
        const patientId = `PT${String(userId).padStart(3, '0')}`;

        // Insert into patients table with new fields
        await db.query(
            `INSERT INTO patients 
            (user_id, patient_id, date_of_birth, gender, affected_hand, 
             medical_condition, therapy_type, current_level,
             shoulder_strength, elbow_strength, wrist_strength, 
             grip_strength, external_rotation) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [userId, patientId, dateOfBirth, gender, affectedHand, 
             medicalCondition, therapyType, 1, 0, 0, 0, 0, 0]
        );

        res.status(201).json({
            success: true,
            message: 'Patient registered successfully',
            patientId
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

// ============================================
// Update patient
// ============================================
router.put('/:patientId', protect, async (req, res) => {
    try {
        const { patientId } = req.params;
        const updates = req.body;

        // Build update query dynamically
        const allowedFields = [
            'name', 'phone', 'date_of_birth', 'gender', 'affected_hand',
            'medical_condition', 'therapy_type', 'current_level',
            'emergency_contact_name', 'emergency_contact_phone',
            'address', 'city', 'country'
        ];

        const updateFields = [];
        const updateValues = [];

        Object.keys(updates).forEach(key => {
            if (allowedFields.includes(key)) {
                updateFields.push(`${key} = ?`);
                updateValues.push(updates[key]);
            }
        });

        if (updateFields.length === 0) {
            return res.status(400).json({ 
                success: false, 
                message: 'No valid fields to update' 
            });
        }

        updateValues.push(patientId);

        await db.query(
            `UPDATE patients SET ${updateFields.join(', ')} WHERE patient_id = ?`,
            updateValues
        );

        res.json({
            success: true,
            message: 'Patient updated successfully'
        });

    } catch (error) {
        console.error('Update patient error:', error);
        res.status(500).json({ 
            success: false,
            message: 'Server error',
            error: error.message 
        });
    }
});

// ============================================
// Upload patient photo
// ============================================
router.post('/upload-photo', protect, async (req, res) => {
    try {
        const { patientId, image } = req.body;

        if (!patientId || !image) {
            return res.status(400).json({ 
                success: false, 
                message: 'Patient ID and image are required' 
            });
        }

        // Create uploads directory if it doesn't exist
        const uploadDir = path.join(__dirname, '../uploads');
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }

        // Convert base64 to file
        const base64Data = image.replace(/^data:image\/jpeg;base64,/, '');
        const timestamp = Date.now();
        const filename = `patient_${patientId}_photo_${timestamp}.jpg`;
        const filepath = path.join(uploadDir, filename);

        // Save file
        fs.writeFileSync(filepath, base64Data, 'base64');

        // Update database
        const photoUrl = `/uploads/${filename}`;
        await db.query(
            'UPDATE patients SET photo_url = ? WHERE patient_id = ?',
            [photoUrl, patientId]
        );

        res.json({ 
            success: true, 
            message: 'Photo saved successfully',
            photoUrl 
        });

    } catch (error) {
        console.error('Error saving photo:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error while saving photo' 
        });
    }
});

// ============================================
// Upload assessment video
// ============================================
router.post('/upload-assessment', protect, async (req, res) => {
    try {
        const { patientId, video } = req.body;

        if (!patientId || !video) {
            return res.status(400).json({ 
                success: false, 
                message: 'Patient ID and video are required' 
            });
        }

        // Create uploads directory if it doesn't exist
        const uploadDir = path.join(__dirname, '../uploads');
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }

        // Convert base64 to file
        const base64Data = video.replace(/^data:video\/webm;base64,/, '');
        const timestamp = Date.now();
        const filename = `patient_${patientId}_assessment_${timestamp}.webm`;
        const filepath = path.join(uploadDir, filename);

        // Save file
        fs.writeFileSync(filepath, base64Data, 'base64');

        // Update database
        const videoUrl = `/uploads/${filename}`;
        await db.query(
            `UPDATE patients SET 
             video_url = ?, 
             initial_assessment_date = NOW(),
             last_assessment_date = NOW() 
             WHERE patient_id = ?`,
            [videoUrl, patientId]
        );

        res.json({ 
            success: true, 
            message: 'Assessment video saved successfully',
            videoUrl 
        });

    } catch (error) {
        console.error('Error saving video:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error while saving video' 
        });
    }
});

// ============================================
// Save initial measurements
// ============================================
router.post('/initial-measurements', protect, async (req, res) => {
    try {
        const { patientId, measurements } = req.body;

        await db.query(
            `UPDATE patients SET 
             shoulder_strength = ?, 
             elbow_strength = ?,
             wrist_strength = ?,
             grip_strength = ?,
             external_rotation = ?,
             initial_assessment_date = NOW()
             WHERE patient_id = ?`,
            [measurements.shoulder, measurements.elbow, measurements.wrist, 
             measurements.grip, measurements.rotation, patientId]
        );

        // Also save to progress tracking
        const [patient] = await db.query(
            'SELECT id FROM patients WHERE patient_id = ?',
            [patientId]
        );

        if (patient.length > 0) {
            await db.query(
                `INSERT INTO progress_tracking 
                (patient_id, tracking_date, shoulder_strength, elbow_strength, 
                 wrist_strength, grip_strength, external_rotation)
                VALUES (?, CURDATE(), ?, ?, ?, ?, ?)`,
                [patient[0].id, measurements.shoulder, measurements.elbow,
                 measurements.wrist, measurements.grip, measurements.rotation]
            );
        }

        res.json({ 
            success: true, 
            message: 'Initial measurements saved' 
        });

    } catch (error) {
        console.error('Error saving measurements:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

// ============================================
// Check if patient has photo
// ============================================
router.get('/:patientId/has-photo', protect, async (req, res) => {
    try {
        const { patientId } = req.params;

        const [result] = await db.query(
            'SELECT photo_url FROM patients WHERE patient_id = ?',
            [patientId]
        );

        if (result.length === 0) {
            return res.status(404).json({ 
                success: false, 
                message: 'Patient not found' 
            });
        }

        const hasPhoto = result[0].photo_url !== null && result[0].photo_url !== '';

        res.json({ 
            success: true, 
            hasPhoto 
        });

    } catch (error) {
        console.error('Error checking photo:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

// ============================================
// Get patient progress data for charts
// ============================================
router.get('/:patientId/progress', protect, async (req, res) => {
    try {
        const { patientId } = req.params;
        const { period = 'week' } = req.query; // week, month, year

        const [patient] = await db.query(
            'SELECT id FROM patients WHERE patient_id = ?',
            [patientId]
        );

        if (patient.length === 0) {
            return res.status(404).json({ 
                success: false, 
                message: 'Patient not found' 
            });
        }

        let dateFilter = '';
        switch (period) {
            case 'week':
                dateFilter = 'tracking_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)';
                break;
            case 'month':
                dateFilter = 'tracking_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)';
                break;
            case 'year':
                dateFilter = 'tracking_date >= DATE_SUB(CURDATE(), INTERVAL 365 DAY)';
                break;
            default:
                dateFilter = 'tracking_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)';
        }

        const [progress] = await db.query(
            `SELECT tracking_date, shoulder_strength, elbow_strength, 
                    wrist_strength, grip_strength, external_rotation
             FROM progress_tracking 
             WHERE patient_id = ? AND ${dateFilter}
             ORDER BY tracking_date ASC`,
            [patient[0].id]
        );

        // Format data for charts
        const labels = progress.map(p => {
            const date = new Date(p.tracking_date);
            return period === 'week' ? 
                date.toLocaleDateString('en-US', { weekday: 'short' }) :
                date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });

        const chartData = {
            labels,
            shoulder: progress.map(p => p.shoulder_strength),
            elbow: progress.map(p => p.elbow_strength),
            wrist: progress.map(p => p.wrist_strength),
            grip: progress.map(p => p.grip_strength),
            rotation: progress.map(p => p.external_rotation)
        };

        res.json({
            success: true,
            data: chartData
        });

    } catch (error) {
        console.error('Error getting progress:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

// ============================================
// Delete patient
// ============================================
router.delete('/:patientId', protect, async (req, res) => {
    try {
        const { patientId } = req.params;

        const [patient] = await db.query(
            'SELECT user_id FROM patients WHERE patient_id = ?',
            [patientId]
        );

        if (patient.length === 0) {
            return res.status(404).json({ 
                success: false, 
                message: 'Patient not found' 
            });
        }

        await db.query('DELETE FROM users WHERE id = ?', [patient[0].user_id]);

        res.json({
            success: true,
            message: 'Patient deleted successfully'
        });

    } catch (error) {
        console.error('Delete patient error:', error);
        res.status(500).json({ 
            success: false,
            message: 'Server error',
            error: error.message 
        });
    }
});

module.exports = router;
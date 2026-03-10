const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const db = require('../db');
const { protect } = require('../middleware/auth');

// ============================================
// Photo Upload Route
// ============================================

/**
 * POST /api/patients/upload-photo
 * Upload patient profile photo
 * Body: { patientId, image (base64) }
 */
router.post('/upload-photo', protect, async (req, res) => {
    try {
        const { patientId, image } = req.body;
        
        // Validate input
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
        // Remove data:image/jpeg;base64, prefix
        const base64Data = image.replace(/^data:image\/jpeg;base64,/, '');
        
        // Generate unique filename
        const timestamp = Date.now();
        const filename = `patient_${patientId}_${timestamp}.jpg`;
        const filepath = path.join(uploadDir, filename);
        
        // Save file to disk
        fs.writeFileSync(filepath, base64Data, 'base64');
        
        // Update database with photo URL
        const photoUrl = `/uploads/${filename}`;
        await db.query(
            'UPDATE patients SET photo_url = ? WHERE patient_id = ?',
            [photoUrl, patientId]
        );
        
        res.json({ 
            success: true, 
            message: 'Photo saved successfully',
            photoUrl: photoUrl
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
// Check if patient has photo
// ============================================

/**
 * GET /api/patients/:patientId/has-photo
 * Check if patient has uploaded a photo
 */
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
            hasPhoto: hasPhoto 
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
// Get patient by ID (updated to include photo_url)
// ============================================

/**
 * GET /api/patients/:id
 * Get patient details by ID
 */
router.get('/:id', protect, async (req, res) => {
    try {
        const patientId = req.params.id;
        
        const [patients] = await db.query(
            `SELECT u.id, u.name, u.email, u.phone, 
                    p.patient_id, p.date_of_birth, p.gender, 
                    p.medical_condition, p.therapy_type, p.current_level,
                    p.shoulder_strength, p.elbow_strength, p.wrist_strength,
                    p.grip_strength, p.external_rotation,
                    p.photo_url
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
        
        res.json({
            success: true,
            data: patients[0]
        });
        
    } catch (error) {
        console.error('Error fetching patient:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

module.exports = router;
USE rehabilitation_system;

-- ============================================
-- ============================================
SELECT '=== Doctor Users IDs ===' as '';
SELECT id, name, email FROM users WHERE role = 'doctor';

-- ============================================
-- ============================================
INSERT INTO doctors (user_id, doctor_id, specialty, license_number, hospital, experience) VALUES
((SELECT id FROM users WHERE email = 'dr.ahmad@clinic.com'), 'DR001', 'Physiotherapy', 'LIC001', 'Central Hospital', 10),
((SELECT id FROM users WHERE email = 'dr.sarah@clinic.com'), 'DR002', 'Occupational Therapy', 'LIC002', 'Rehabilitation Center', 8);

-- ============================================
-- ============================================
SELECT '=== Doctors after insertion ===' as '';
SELECT d.*, u.name, u.email 
FROM doctors d
JOIN users u ON d.user_id = u.id;

-- ============================================
-- ============================================
SELECT '=== Current Patients ===' as '';
SELECT p.*, u.name FROM patients p JOIN users u ON p.user_id = u.id;

-- INSERT INTO patients (user_id, patient_id, date_of_birth, gender, affected_hand, medical_condition, therapy_type, current_level, shoulder_strength, elbow_strength, wrist_strength, grip_strength, external_rotation) VALUES
-- ((SELECT id FROM users WHERE email = 'ali@rehab.com'), 'PT001', '2018-01-15', 'male', 'right', 'Motor Disability', 'Physical Therapy', 4, 85, 78, 82, 79, 92),
-- ((SELECT id FROM users WHERE email = 'sara@rehab.com'), 'PT002', '2019-03-20', 'female', 'left', 'Arm Weakness', 'Occupational Therapy', 3, 92, 88, 86, 89, 88),
-- ((SELECT id FROM users WHERE email = 'omar@rehab.com'), 'PT003', '2017-11-05', 'male', 'both', 'Movement Disorder', 'Developmental Therapy', 5, 88, 85, 90, 85, 96);

SELECT '✅ Database is complete and ready!' as 'Result';
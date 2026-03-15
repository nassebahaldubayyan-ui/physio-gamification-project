USE rehabilitation_system;

SELECT '=== Patients in database ===' as '';
SELECT id, patient_id, medical_condition FROM patients;

SET @ali_id = (SELECT id FROM patients WHERE patient_id = 'PT002');
SET @sara_id = (SELECT id FROM patients WHERE patient_id = 'PT005');
SET @omar_id = (SELECT id FROM patients WHERE patient_id = 'PT004');

SELECT '=== Patient IDs found ===' as '';
SELECT @ali_id as 'Ali ID', @sara_id as 'Sara ID', @omar_id as 'Omar ID';

INSERT INTO progress_tracking (patient_id, tracking_date, shoulder_strength, elbow_strength, wrist_strength, grip_strength, external_rotation) VALUES
(@ali_id, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 80, 73, 76, 74, 85),
(@ali_id, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 81, 74, 77, 75, 86),
(@ali_id, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 82, 75, 78, 76, 88),
(@ali_id, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 83, 76, 79, 77, 89),
(@ali_id, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 84, 77, 80, 78, 90),
(@ali_id, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 85, 78, 81, 79, 91),
(@ali_id, CURDATE(), 85, 78, 82, 79, 92);

INSERT INTO progress_tracking (patient_id, tracking_date, shoulder_strength, elbow_strength, wrist_strength, grip_strength, external_rotation) VALUES
(@sara_id, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 88, 84, 82, 85, 82),
(@sara_id, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 89, 85, 83, 86, 83),
(@sara_id, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 90, 86, 84, 87, 84),
(@sara_id, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 91, 87, 85, 88, 85),
(@sara_id, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 92, 88, 86, 89, 86),
(@sara_id, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 92, 88, 86, 89, 87),
(@sara_id, CURDATE(), 92, 88, 86, 89, 88);

INSERT INTO progress_tracking (patient_id, tracking_date, shoulder_strength, elbow_strength, wrist_strength, grip_strength, external_rotation) VALUES
(@omar_id, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 82, 79, 84, 79, 90),
(@omar_id, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 83, 80, 85, 80, 91),
(@omar_id, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 84, 81, 86, 81, 92),
(@omar_id, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 85, 82, 87, 82, 93),
(@omar_id, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 86, 83, 88, 83, 94),
(@omar_id, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 87, 84, 89, 84, 95),
(@omar_id, CURDATE(), 88, 85, 90, 85, 96);

SELECT '=== Progress tracking data added ===' as '';
SELECT * FROM progress_tracking;

SELECT '✅ All done successfully!' as 'Result';
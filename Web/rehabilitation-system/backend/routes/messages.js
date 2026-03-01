const express = require('express');
const router = express.Router();
const messageController = require('../controllers/messageController');
const { protect } = require('../middleware/auth');

router.use(protect);

router.post('/send', messageController.sendMessage);

router.get('/conversations', messageController.getConversations);

router.get('/conversation/:userId', messageController.getConversation);

router.put('/read/:userId', messageController.markAsRead);

module.exports = router;
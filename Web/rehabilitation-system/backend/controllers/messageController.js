const db = require('../db');

exports.sendMessage = async (req, res) => {
    try {
        const { receiverId, message } = req.body;
        const senderId = req.user.id;

        const [result] = await db.query(
            'INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)',
            [senderId, receiverId, message]
        );

        res.status(201).json({
            success: true,
            message: 'Message sent successfully',
            messageId: result.insertId
        });

    } catch (error) {
        console.error('Error sending message:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
};

exports.getConversation = async (req, res) => {
    try {
        const userId = req.user.id;
        const otherUserId = req.params.userId;

        const [messages] = await db.query(
            `SELECT * FROM messages 
             WHERE (sender_id = ? AND receiver_id = ?) 
                OR (sender_id = ? AND receiver_id = ?)
             ORDER BY created_at ASC`,
            [userId, otherUserId, otherUserId, userId]
        );

        res.json({
            success: true,
            data: messages
        });

    } catch (error) {
        console.error('Error fetching messages:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
};

exports.getConversations = async (req, res) => {
    try {
        const userId = req.user.id;

        const [conversations] = await db.query(
            `SELECT DISTINCT 
                CASE 
                    WHEN sender_id = ? THEN receiver_id 
                    ELSE sender_id 
                END as other_user_id,
                u.name as other_user_name,
                u.role as other_user_role,
                (SELECT message FROM messages 
                 WHERE (sender_id = ? AND receiver_id = u.id) 
                    OR (sender_id = u.id AND receiver_id = ?)
                 ORDER BY created_at DESC LIMIT 1) as last_message,
                (SELECT created_at FROM messages 
                 WHERE (sender_id = ? AND receiver_id = u.id) 
                    OR (sender_id = u.id AND receiver_id = ?)
                 ORDER BY created_at DESC LIMIT 1) as last_message_time,
                (SELECT COUNT(*) FROM messages 
                 WHERE receiver_id = ? AND sender_id = u.id AND is_read = FALSE) as unread_count
             FROM messages m
             JOIN users u ON u.id = CASE 
                                        WHEN sender_id = ? THEN receiver_id 
                                        ELSE sender_id 
                                    END
             WHERE sender_id = ? OR receiver_id = ?
             GROUP BY other_user_id`,
            [userId, userId, userId, userId, userId, userId, userId, userId, userId]
        );

        res.json({
            success: true,
            data: conversations
        });

    } catch (error) {
        console.error('Error fetching conversations:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
};

exports.markAsRead = async (req, res) => {
    try {
        const userId = req.user.id;
        const otherUserId = req.params.userId;

        await db.query(
            'UPDATE messages SET is_read = TRUE WHERE sender_id = ? AND receiver_id = ?',
            [otherUserId, userId]
        );

        res.json({
            success: true,
            message: 'Messages marked as read'
        });

    } catch (error) {
        console.error('Error marking messages as read:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
};
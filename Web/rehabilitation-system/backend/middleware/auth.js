const jwt = require('jsonwebtoken');
const db = require('../db');

exports.protect = async (req, res, next) => {
    try {
        let token;

        if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
            token = req.headers.authorization.split(' ')[1];
        }

        if (!token) {
            return res.status(401).json({ 
                success: false, 
                message: 'Not authorized - No token' 
            });
        }

        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        
        const [users] = await db.query('SELECT id, name, email, role FROM users WHERE id = ?', [decoded.id]);
        
        if (users.length === 0) {
            return res.status(401).json({ 
                success: false, 
                message: 'Not authorized - User not found' 
            });
        }

        req.user = users[0];
        next();

    } catch (error) {
        console.error('Auth error:', error);
        
        if (error.name === 'JsonWebTokenError') {
            return res.status(401).json({ 
                success: false, 
                message: 'Not authorized - Invalid token' 
            });
        }
        
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ 
                success: false, 
                message: 'Not authorized - Token expired' 
            });
        }

        res.status(500).json({ 
            success: false, 
            message: 'Server error in auth' 
        });
    }
};
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { PrismaClient } from '@prisma/client';
import { initializeFirebaseAdmin } from './config/firebase';
import { errorHandler } from './middleware/errorHandler';
import { rateLimiter } from './middleware/rateLimiter';
import { logger } from './utils/logger';

// Routes
import authRoutes from './routes/auth';
import userRoutes from './routes/users';
import serviceRoutes from './routes/services';
import transactionRoutes from './routes/transactions';
import dealRoutes from './routes/deals';
import cvRoutes from './routes/cv';
import ocrRoutes from './routes/ocr';

dotenv.config();

const app = express();
const prisma = new PrismaClient();
const PORT = process.env.PORT || 8080;

// Initialize Firebase Admin
initializeFirebaseAdmin();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(rateLimiter);

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// API Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/users', userRoutes);
app.use('/api/v1/services', serviceRoutes);
app.use('/api/v1/transactions', transactionRoutes);
app.use('/api/v1/deals', dealRoutes);
app.use('/api/v1/cv', cvRoutes);
app.use('/api/v1/ocr', ocrRoutes);

// Error handling
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
    logger.info(`Server running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    logger.info('SIGTERM received, shutting down gracefully');
    await prisma.$disconnect();
    process.exit(0);
});

// backend/src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import { auth } from '../config/firebase';

export interface AuthRequest extends Request {
    user?: {
        uid: string;
        email: string;
        userId: string;
        subscription: string;
    };
}

export const authenticate = async (
    req: AuthRequest,
    res: Response,
    next: NextFunction
) => {
    try {
        const token = req.headers.authorization?.split('Bearer ')[1];

        if (!token) {
            return res.status(401).json({ error: 'No token provided' });
        }

        const decodedToken = await auth.verifyIdToken(token);

        // Get user from database
        const user = await prisma.user.findUnique({
            where: { firebaseUid: decodedToken.uid }
        });

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        req.user = {
            uid: decodedToken.uid,
            email: decodedToken.email!,
            userId: user.id,
            subscription: user.subscriptionType
        };

        // Update last active
        await prisma.user.update({
            where: { id: user.id },
            data: { lastActive: new Date() }
        });

        next();
    } catch (error) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

export const requirePremium = (
    req: AuthRequest,
    res: Response,
    next: NextFunction
) => {
    if (req.user?.subscription !== 'PREMIUM' && req.user?.subscription !== 'FAMILY') {
        return res.status(403).json({ error: 'Premium subscription required' });
    }
    next();
};

// backend/src/routes/services.ts
import { Router } from 'express';
import { PrismaClient } from '@prisma/client';
import { authenticate } from '../middleware/auth';

const router = Router();
const prisma = new PrismaClient();

// Get services near user
router.get('/nearby', authenticate, async (req, res) => {
    try {
        const { lat, lng, radius = 10, type, limit = 20 } = req.query;

        // In production, use PostGIS for geo queries
        // For MVP, filter by city
        const services = await prisma.service.findMany({
            where: {
                city: req.user?.city,
                ...(type && { type: type as any })
            },
            take: Number(limit),
            orderBy: { rating: 'desc' }
        });

        res.json(services);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch services' });
    }
});

// Get service by ID
router.get('/:id', authenticate, async (req, res) => {
    try {
        const service = await prisma.service.findUnique({
            where: { id: req.params.id }
        });

        if (!service) {
            return res.status(404).json({ error: 'Service not found' });
        }

        res.json(service);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch service' });
    }
});

// Search services
router.get('/search', authenticate, async (req, res) => {
    try {
        const { q, province, city, type } = req.query;

        const services = await prisma.service.findMany({
            where: {
                OR: [
                    { name: { contains: q as string, mode: 'insensitive' } },
                    { category: { contains: q as string, mode: 'insensitive' } }
                ],
                ...(province && { province: province as string }),
                ...(city && { city: city as string }),
                ...(type && { type: type as any })
            },
            take: 50
        });

        res.json(services);
    } catch (error) {
        res.status(500).json({ error: 'Search failed' });
    }
});

// Bookmark service
router.post('/:id/bookmark', authenticate, async (req, res) => {
    try {
        const bookmark = await prisma.serviceBookmark.create({
            data: {
                userId: req.user!.userId,
                serviceId: req.params.id
            }
        });

        res.json(bookmark);
    } catch (error) {
        res.status(500).json({ error: 'Failed to bookmark' });
    }
});

export default router;
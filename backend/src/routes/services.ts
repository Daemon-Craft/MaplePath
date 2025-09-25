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
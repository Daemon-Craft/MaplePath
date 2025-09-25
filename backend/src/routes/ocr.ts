import { Router } from 'express';
import { Storage } from '@google-cloud/storage';
import { ImageAnnotatorClient } from '@google-cloud/vision';
import { authenticate, requirePremium } from '../middleware/auth';
import multer from 'multer';

const router = Router();
const storage = new Storage();
const vision = new ImageAnnotatorClient();
const upload = multer({ memory: true, limits: { fileSize: 10 * 1024 * 1024 } });

router.post('/scan', authenticate, upload.single('receipt'), async (req, res) => {
    try {
        // Check scan limit for free users
        if (req.user?.subscription === 'FREE') {
            const scansThisMonth = await prisma.transaction.count({
                where: {
                    userId: req.user.userId,
                    receiptUrl: { not: null },
                    createdAt: {
                        gte: new Date(new Date().setDate(1))
                    }
                }
            });

            if (scansThisMonth >= 3) {
                return res.status(403).json({ error: 'Monthly scan limit reached. Upgrade to Premium!' });
            }
        }

        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        // Upload to Cloud Storage
        const bucket = storage.bucket('settlein-receipts');
        const filename = `${req.user!.userId}/${Date.now()}.jpg`;
        const file = bucket.file(filename);

        await file.save(req.file.buffer, {
            metadata: { contentType: req.file.mimetype }
        });

        const receiptUrl = `https://storage.googleapis.com/settlein-receipts/${filename}`;

        // OCR with Vision API
        const [result] = await vision.textDetection(receiptUrl);
        const text = result.textAnnotations?.[0]?.description || '';

        // Parse receipt (simplified)
        const lines = text.split('\n');
        let merchant = '';
        let total = 0;
        const items: any[] = [];

        for (const line of lines) {
            // Find merchant (usually in first few lines)
            if (!merchant && line.length > 3 && line.length < 50) {
                merchant = line.trim();
            }

            // Find total (look for "total" keyword)
            if (line.toLowerCase().includes('total')) {
                const match = line.match(/[\d,]+\.?\d*/);
                if (match) {
                    total = parseFloat(match[0].replace(',', ''));
                }
            }

            // Find items with prices
            const itemMatch = line.match(/(.+?)\s+([\d,]+\.?\d{2})/);
            if (itemMatch && !line.toLowerCase().includes('total')) {
                items.push({
                    name: itemMatch[1].trim(),
                    price: parseFloat(itemMatch[2].replace(',', ''))
                });
            }
        }

        // Create transaction
        const transaction = await prisma.transaction.create({
            data: {
                userId: req.user!.userId,
                type: 'EXPENSE',
                category: 'Groceries', // AI can improve this
                amount: total || 0,
                merchant: merchant || 'Unknown',
                date: new Date(),
                receiptUrl,
                ocrData: { text },
                items
            }
        });

        res.json({
            transaction,
            parsed: { merchant, total, items, text: text.slice(0, 500) }
        });
    } catch (error) {
        console.error('OCR Error:', error);
        res.status(500).json({ error: 'Failed to process receipt' });
    }
});

export default router;
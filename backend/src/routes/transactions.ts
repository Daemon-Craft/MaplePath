import { Router } from 'express';
import { PrismaClient } from '@prisma/client';
import { authenticate, requirePremium } from '../middleware/auth';
import Joi from 'joi';

const router = Router();
const prisma = new PrismaClient();

// Validation schema
const transactionSchema = Joi.object({
    type: Joi.string().valid('INCOME', 'EXPENSE').required(),
    category: Joi.string().required(),
    amount: Joi.number().positive().required(),
    merchant: Joi.string().required(),
    date: Joi.date().required(),
    notes: Joi.string().optional(),
    tags: Joi.array().items(Joi.string()).optional()
});

// Get user transactions
router.get('/', authenticate, async (req, res) => {
    try {
        const { month, category, type, limit = 50 } = req.query;

        const transactions = await prisma.transaction.findMany({
            where: {
                userId: req.user!.userId,
                ...(type && { type: type as any }),
                ...(category && { category: category as string }),
                ...(month && {
                    date: {
                        gte: new Date(`${month}-01`),
                        lt: new Date(new Date(`${month}-01`).setMonth(new Date(`${month}-01`).getMonth() + 1))
                    }
                })
            },
            orderBy: { date: 'desc' },
            take: Number(limit)
        });

        res.json(transactions);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch transactions' });
    }
});

// Create transaction
router.post('/', authenticate, async (req, res) => {
    try {
        const { error, value } = transactionSchema.validate(req.body);
        if (error) {
            return res.status(400).json({ error: error.details[0].message });
        }

        const transaction = await prisma.transaction.create({
            data: {
                userId: req.user!.userId,
                ...value
            }
        });

        res.status(201).json(transaction);
    } catch (error) {
        res.status(500).json({ error: 'Failed to create transaction' });
    }
});

// Get spending insights
router.get('/insights', authenticate, async (req, res) => {
    try {
        const { month = new Date().toISOString().slice(0, 7) } = req.query;

        // Get transactions for the month
        const transactions = await prisma.transaction.findMany({
            where: {
                userId: req.user!.userId,
                date: {
                    gte: new Date(`${month}-01`),
                    lt: new Date(new Date(`${month}-01`).setMonth(new Date(`${month}-01`).getMonth() + 1))
                }
            }
        });

        // Calculate insights
        const totalIncome = transactions
            .filter(t => t.type === 'INCOME')
            .reduce((sum, t) => sum + t.amount, 0);

        const totalExpenses = transactions
            .filter(t => t.type === 'EXPENSE')
            .reduce((sum, t) => sum + t.amount, 0);

        const byCategory = transactions
            .filter(t => t.type === 'EXPENSE')
            .reduce((acc, t) => {
                acc[t.category] = (acc[t.category] || 0) + t.amount;
                return acc;
            }, {} as Record<string, number>);

        const topMerchants = Object.entries(
            transactions
                .filter(t => t.type === 'EXPENSE')
                .reduce((acc, t) => {
                    acc[t.merchant] = (acc[t.merchant] || 0) + t.amount;
                    return acc;
                }, {} as Record<string, number>)
        )
            .sort(([, a], [, b]) => b - a)
            .slice(0, 5)
            .map(([merchant, amount]) => ({ merchant, amount }));

        res.json({
            month,
            totalIncome,
            totalExpenses,
            savings: totalIncome - totalExpenses,
            savingsRate: totalIncome > 0 ? ((totalIncome - totalExpenses) / totalIncome * 100).toFixed(1) : 0,
            byCategory,
            topMerchants,
            transactionCount: transactions.length
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to generate insights' });
    }
});

export default router;
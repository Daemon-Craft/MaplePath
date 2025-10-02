"""
Script to seed the database with Canadian industries
Run this after migrations: python -m app.data.seed_industries
"""
import asyncio
from app.db.database import database
from app.models.cv import industries
from app.data.canadian_industries import CANADIAN_INDUSTRIES


async def seed_industries():
    """Seed the database with Canadian industries"""
    await database.connect()

    try:
        print("Seeding Canadian industries...")

        for industry_data in CANADIAN_INDUSTRIES:
            # Check if industry already exists
            existing = await database.fetch_one(
                industries.select().where(industries.c.name == industry_data["name"])
            )

            if existing:
                print(f"Industry '{industry_data['name']}' already exists, skipping...")
                continue

            # Insert industry
            query = industries.insert().values(
                name=industry_data["name"],
                name_fr=industry_data.get("name_fr"),
                description=industry_data.get("description"),
                tips=industry_data.get("tips"),
                keywords=industry_data.get("keywords"),
                is_active=True
            )

            await database.execute(query)
            print(f"✓ Created industry: {industry_data['name']}")

        print(f"\n✅ Successfully seeded {len(CANADIAN_INDUSTRIES)} industries!")

    except Exception as e:
        print(f"❌ Error seeding industries: {str(e)}")
    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_industries())

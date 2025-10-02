"""
Pre-loaded Canadian industries with job-specific tips and keywords
"""

CANADIAN_INDUSTRIES = [
    {
        "name": "Information Technology",
        "name_fr": "Technologies de l'information",
        "description": "Software development, IT services, cybersecurity, and technology consulting",
        "tips": [
            "Highlight technical certifications (AWS, Azure, CompTIA, etc.)",
            "Include programming languages and frameworks with proficiency levels",
            "Quantify your impact: system performance improvements, cost savings, user growth",
            "Mention Agile/Scrum experience and project management tools",
            "Showcase GitHub portfolio or technical blog if available"
        ],
        "keywords": [
            "Python", "Java", "JavaScript", "React", "Node.js", "AWS", "Docker",
            "Kubernetes", "CI/CD", "Agile", "Scrum", "DevOps", "Cloud Computing",
            "Machine Learning", "API Development", "Microservices", "Git"
        ]
    },
    {
        "name": "Healthcare",
        "name_fr": "Soins de santé",
        "description": "Medical professionals, nursing, healthcare administration, and allied health",
        "tips": [
            "List all relevant licenses and certifications (RN, MD, etc.)",
            "Emphasize patient care outcomes and quality metrics",
            "Include EMR/EHR system experience (Epic, Cerner, etc.)",
            "Highlight compliance with healthcare regulations (PHIPA, HIPAA)",
            "Mention continuing education and professional development"
        ],
        "keywords": [
            "Patient Care", "Clinical Assessment", "Electronic Medical Records",
            "Healthcare Compliance", "Medical Documentation", "PHIPA", "CPR",
            "Emergency Response", "Healthcare Quality", "Patient Safety"
        ]
    },
    {
        "name": "Finance & Banking",
        "name_fr": "Finance et Banque",
        "description": "Banking, investment, accounting, financial planning, and insurance",
        "tips": [
            "Include professional designations (CPA, CFA, CFP, etc.)",
            "Quantify achievements: revenue growth, cost reductions, portfolio performance",
            "Highlight regulatory compliance experience",
            "Mention financial software proficiency (SAP, Oracle, QuickBooks)",
            "Emphasize risk management and analytical skills"
        ],
        "keywords": [
            "Financial Analysis", "Risk Management", "Budgeting", "Forecasting",
            "Financial Reporting", "CPA", "CFA", "Accounting", "Auditing",
            "Compliance", "Investment Strategy", "Portfolio Management", "Excel"
        ]
    },
    {
        "name": "Engineering",
        "name_fr": "Ingénierie",
        "description": "Civil, mechanical, electrical, software, and other engineering disciplines",
        "tips": [
            "List P.Eng. or EIT designation prominently",
            "Include project management experience (PMP, PRINCE2)",
            "Quantify project scope, budgets, and timelines",
            "Highlight CAD/technical software proficiency",
            "Mention adherence to engineering standards and codes"
        ],
        "keywords": [
            "P.Eng", "EIT", "Project Management", "AutoCAD", "SolidWorks",
            "Technical Design", "Quality Assurance", "Engineering Standards",
            "Budget Management", "Risk Assessment", "Construction Management"
        ]
    },
    {
        "name": "Education & Training",
        "name_fr": "Éducation et Formation",
        "description": "Teachers, professors, instructional designers, and educational administrators",
        "tips": [
            "List OCT certification or equivalent teaching credentials",
            "Highlight curriculum development experience",
            "Include student achievement metrics and outcomes",
            "Mention technology integration in teaching",
            "Emphasize inclusive and differentiated instruction experience"
        ],
        "keywords": [
            "Curriculum Development", "Lesson Planning", "Classroom Management",
            "Student Assessment", "Educational Technology", "Differentiated Instruction",
            "OCT", "B.Ed", "Teaching Certification", "Learning Management Systems"
        ]
    },
    {
        "name": "Retail & Sales",
        "name_fr": "Vente au détail",
        "description": "Retail management, sales representatives, customer service, and merchandising",
        "tips": [
            "Quantify sales achievements with percentages and dollar amounts",
            "Highlight customer satisfaction scores and metrics",
            "Include CRM software experience (Salesforce, HubSpot)",
            "Emphasize team leadership and training experience",
            "Mention inventory management and POS system proficiency"
        ],
        "keywords": [
            "Sales Performance", "Customer Service", "CRM", "Salesforce",
            "Team Leadership", "Revenue Growth", "Client Relations",
            "Merchandising", "Inventory Management", "POS Systems"
        ]
    },
    {
        "name": "Hospitality & Tourism",
        "name_fr": "Hôtellerie et Tourisme",
        "description": "Hotels, restaurants, tourism services, and event management",
        "tips": [
            "Highlight customer service excellence and ratings",
            "Include Smart Serve or food safety certifications",
            "Quantify occupancy rates, revenue, or guest satisfaction scores",
            "Mention experience with booking systems and hotel software",
            "Emphasize multilingual abilities if applicable"
        ],
        "keywords": [
            "Customer Service", "Guest Relations", "Smart Serve", "Food Safety",
            "Hotel Management", "Event Planning", "Revenue Management",
            "Booking Systems", "Hospitality Operations", "Multilingual"
        ]
    },
    {
        "name": "Construction & Trades",
        "name_fr": "Construction et Métiers",
        "description": "Skilled trades, construction management, and general contracting",
        "tips": [
            "List Red Seal certification or journeyperson status",
            "Include WHMIS, First Aid, and safety certifications",
            "Quantify project completion rates and timelines",
            "Highlight adherence to building codes and safety standards",
            "Mention equipment operation certifications"
        ],
        "keywords": [
            "Red Seal", "Journeyperson", "WHMIS", "Construction Safety",
            "Building Codes", "Project Management", "Blueprint Reading",
            "Equipment Operation", "Quality Control", "Site Supervision"
        ]
    },
    {
        "name": "Marketing & Communications",
        "name_fr": "Marketing et Communications",
        "description": "Digital marketing, public relations, content creation, and brand management",
        "tips": [
            "Highlight campaign results with metrics (ROI, engagement, conversions)",
            "Include digital marketing tools experience (Google Analytics, SEMrush)",
            "Showcase content creation and copywriting skills",
            "Mention social media management and paid advertising experience",
            "Include portfolio or campaign examples if possible"
        ],
        "keywords": [
            "Digital Marketing", "SEO", "SEM", "Content Marketing", "Social Media",
            "Google Analytics", "Campaign Management", "Brand Strategy",
            "Copywriting", "Email Marketing", "Marketing Automation", "ROI Analysis"
        ]
    },
    {
        "name": "Human Resources",
        "name_fr": "Ressources Humaines",
        "description": "HR management, recruitment, talent development, and employee relations",
        "tips": [
            "List CHRP, CHRL, or SHRM certifications",
            "Highlight experience with HRIS systems (Workday, ADP, Ceridian)",
            "Quantify recruitment metrics and employee retention rates",
            "Emphasize knowledge of employment law and compliance",
            "Include change management and organizational development experience"
        ],
        "keywords": [
            "CHRP", "CHRL", "Recruitment", "Talent Acquisition", "HRIS",
            "Employee Relations", "Performance Management", "Compensation",
            "Benefits Administration", "Employment Law", "Organizational Development"
        ]
    },
    {
        "name": "Transportation & Logistics",
        "name_fr": "Transport et Logistique",
        "description": "Supply chain, warehousing, trucking, and logistics coordination",
        "tips": [
            "Include relevant licenses (Class A/D, FAST card, etc.)",
            "Highlight safety record and compliance",
            "Quantify efficiency improvements and cost savings",
            "Mention logistics software and WMS experience",
            "Emphasize route optimization and inventory management"
        ],
        "keywords": [
            "Supply Chain Management", "Logistics Coordination", "Inventory Control",
            "Warehouse Management", "Transportation", "Safety Compliance",
            "Route Optimization", "Distribution", "Freight Management", "WMS"
        ]
    },
    {
        "name": "Legal Services",
        "name_fr": "Services Juridiques",
        "description": "Lawyers, paralegals, legal assistants, and law clerks",
        "tips": [
            "List bar admission and good standing status",
            "Highlight areas of legal specialization",
            "Include case management and legal research experience",
            "Mention litigation and negotiation achievements",
            "Emphasize legal technology proficiency"
        ],
        "keywords": [
            "Legal Research", "Case Management", "Litigation", "Contract Review",
            "Legal Writing", "Client Relations", "Negotiation", "Compliance",
            "Due Diligence", "Legal Technology", "Bar Admission"
        ]
    }
]

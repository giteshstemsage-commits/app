from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Models
class Resource(BaseModel):
    title: str
    url: str
    type: str  # video, article, course

class Milestone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    order: int
    resources: List[Resource]
    estimated_days: int

class CareerPath(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
    color: str
    milestones: List[Milestone]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    career_path_id: str
    completed_milestones: List[str] = []
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProgressUpdate(BaseModel):
    milestone_id: str
    completed: bool

# Career Paths Data
CAREER_PATHS_DATA = [
    {
        "id": "software-dev",
        "name": "Software Development",
        "description": "Master full-stack development and build scalable applications",
        "icon": "code",
        "color": "#10B981",
        "milestones": [
            {
                "id": "sd-1",
                "title": "Programming Fundamentals",
                "description": "Learn core programming concepts, data structures, and algorithms",
                "order": 1,
                "estimated_days": 45,
                "resources": [
                    {"title": "CS50 - Harvard", "url": "https://cs50.harvard.edu/x/", "type": "course"},
                    {"title": "Python for Beginners", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "type": "video"},
                    {"title": "Data Structures Guide", "url": "https://www.geeksforgeeks.org/data-structures/", "type": "article"}
                ]
            },
            {
                "id": "sd-2",
                "title": "Frontend Development",
                "description": "Master HTML, CSS, JavaScript, and modern frameworks like React",
                "order": 2,
                "estimated_days": 60,
                "resources": [
                    {"title": "MDN Web Docs", "url": "https://developer.mozilla.org/", "type": "article"},
                    {"title": "React Official Tutorial", "url": "https://react.dev/learn", "type": "course"},
                    {"title": "Frontend Roadmap", "url": "https://www.youtube.com/watch?v=9He4UBLyk8Y", "type": "video"}
                ]
            },
            {
                "id": "sd-3",
                "title": "Backend Development",
                "description": "Learn server-side programming, databases, and API design",
                "order": 3,
                "estimated_days": 60,
                "resources": [
                    {"title": "Node.js Guide", "url": "https://nodejs.org/en/docs/guides/", "type": "article"},
                    {"title": "FastAPI Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "course"},
                    {"title": "Database Design", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "type": "video"}
                ]
            },
            {
                "id": "sd-4",
                "title": "DevOps & Deployment",
                "description": "Master CI/CD, containerization, and cloud platforms",
                "order": 4,
                "estimated_days": 40,
                "resources": [
                    {"title": "Docker Getting Started", "url": "https://docs.docker.com/get-started/", "type": "course"},
                    {"title": "Kubernetes Basics", "url": "https://kubernetes.io/docs/tutorials/", "type": "article"},
                    {"title": "CI/CD Pipeline", "url": "https://www.youtube.com/watch?v=scEDHsr3APg", "type": "video"}
                ]
            },
            {
                "id": "sd-5",
                "title": "System Design",
                "description": "Design scalable, distributed systems and architecture",
                "order": 5,
                "estimated_days": 50,
                "resources": [
                    {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "article"},
                    {"title": "Designing Data-Intensive Apps", "url": "https://dataintensive.net/", "type": "course"},
                    {"title": "System Design Interview", "url": "https://www.youtube.com/watch?v=UzLMhqg3_Wc", "type": "video"}
                ]
            }
        ]
    },
    {
        "id": "cybersecurity",
        "name": "Cybersecurity",
        "description": "Protect systems and networks from digital threats",
        "icon": "shield",
        "color": "#EF4444",
        "milestones": [
            {
                "id": "cs-1",
                "title": "Security Fundamentals",
                "description": "Understand core security principles, threats, and vulnerabilities",
                "order": 1,
                "estimated_days": 40,
                "resources": [
                    {"title": "CompTIA Security+", "url": "https://www.comptia.org/certifications/security", "type": "course"},
                    {"title": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/", "type": "article"},
                    {"title": "Cybersecurity Basics", "url": "https://www.youtube.com/watch?v=inWWhr5tnEA", "type": "video"}
                ]
            },
            {
                "id": "cs-2",
                "title": "Network Security",
                "description": "Secure networks, firewalls, and network protocols",
                "order": 2,
                "estimated_days": 45,
                "resources": [
                    {"title": "Network+ Guide", "url": "https://www.professormesser.com/network-plus/n10-008/n10-008-video/n10-008-training-course/", "type": "course"},
                    {"title": "Wireshark Tutorial", "url": "https://www.wireshark.org/docs/", "type": "article"},
                    {"title": "Network Security", "url": "https://www.youtube.com/watch?v=qiQR5rTSshw", "type": "video"}
                ]
            },
            {
                "id": "cs-3",
                "title": "Ethical Hacking",
                "description": "Learn penetration testing and vulnerability assessment",
                "order": 3,
                "estimated_days": 55,
                "resources": [
                    {"title": "TryHackMe", "url": "https://tryhackme.com/", "type": "course"},
                    {"title": "HackTheBox", "url": "https://www.hackthebox.com/", "type": "course"},
                    {"title": "Metasploit Guide", "url": "https://www.offensive-security.com/metasploit-unleashed/", "type": "article"}
                ]
            },
            {
                "id": "cs-4",
                "title": "Security Operations",
                "description": "Master SOC operations, SIEM, and incident response",
                "order": 4,
                "estimated_days": 50,
                "resources": [
                    {"title": "Splunk Fundamentals", "url": "https://www.splunk.com/en_us/training.html", "type": "course"},
                    {"title": "Incident Response Guide", "url": "https://www.sans.org/white-papers/", "type": "article"},
                    {"title": "SOC Analyst Path", "url": "https://www.youtube.com/watch?v=bwj7GFUcn50", "type": "video"}
                ]
            },
            {
                "id": "cs-5",
                "title": "Advanced Security",
                "description": "Cloud security, malware analysis, and forensics",
                "order": 5,
                "estimated_days": 60,
                "resources": [
                    {"title": "AWS Security", "url": "https://aws.amazon.com/security/", "type": "course"},
                    {"title": "Malware Analysis", "url": "https://www.malware-traffic-analysis.net/", "type": "article"},
                    {"title": "Digital Forensics", "url": "https://www.youtube.com/watch?v=NG9Cg_vBKOg", "type": "video"}
                ]
            }
        ]
    },
    {
        "id": "ai-ml",
        "name": "AI & Machine Learning",
        "description": "Build intelligent systems that learn from data",
        "icon": "brain",
        "color": "#8B5CF6",
        "milestones": [
            {
                "id": "ai-1",
                "title": "Mathematics & Statistics",
                "description": "Master linear algebra, calculus, probability, and statistics",
                "order": 1,
                "estimated_days": 50,
                "resources": [
                    {"title": "Khan Academy Math", "url": "https://www.khanacademy.org/math", "type": "course"},
                    {"title": "3Blue1Brown Linear Algebra", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "type": "video"},
                    {"title": "Statistics for ML", "url": "https://www.statlearning.com/", "type": "article"}
                ]
            },
            {
                "id": "ai-2",
                "title": "Python for Data Science",
                "description": "Learn NumPy, Pandas, Matplotlib, and data manipulation",
                "order": 2,
                "estimated_days": 40,
                "resources": [
                    {"title": "Python Data Science Handbook", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "type": "article"},
                    {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "type": "course"},
                    {"title": "Data Analysis Tutorial", "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8", "type": "video"}
                ]
            },
            {
                "id": "ai-3",
                "title": "Machine Learning Basics",
                "description": "Supervised and unsupervised learning algorithms",
                "order": 3,
                "estimated_days": 60,
                "resources": [
                    {"title": "Andrew Ng ML Course", "url": "https://www.coursera.org/learn/machine-learning", "type": "course"},
                    {"title": "Scikit-learn Docs", "url": "https://scikit-learn.org/stable/tutorial/index.html", "type": "article"},
                    {"title": "ML Crash Course", "url": "https://www.youtube.com/watch?v=i_LwzRVP7bg", "type": "video"}
                ]
            },
            {
                "id": "ai-4",
                "title": "Deep Learning",
                "description": "Neural networks, CNNs, RNNs, and transformers",
                "order": 4,
                "estimated_days": 70,
                "resources": [
                    {"title": "Deep Learning Specialization", "url": "https://www.coursera.org/specializations/deep-learning", "type": "course"},
                    {"title": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "type": "article"},
                    {"title": "Neural Networks Explained", "url": "https://www.youtube.com/watch?v=aircAruvnKk", "type": "video"}
                ]
            },
            {
                "id": "ai-5",
                "title": "Advanced AI & MLOps",
                "description": "Production ML, model deployment, and LLMs",
                "order": 5,
                "estimated_days": 55,
                "resources": [
                    {"title": "MLOps Guide", "url": "https://ml-ops.org/", "type": "article"},
                    {"title": "Hugging Face Course", "url": "https://huggingface.co/course", "type": "course"},
                    {"title": "LLM Applications", "url": "https://www.youtube.com/watch?v=zjkBMFhNj_g", "type": "video"}
                ]
            }
        ]
    },
    {
        "id": "data-science",
        "name": "Data Scientist",
        "description": "Extract insights from data and make data-driven decisions",
        "icon": "chart",
        "color": "#3B82F6",
        "milestones": [
            {
                "id": "ds-1",
                "title": "Data Analysis Fundamentals",
                "description": "SQL, data wrangling, and exploratory analysis",
                "order": 1,
                "estimated_days": 45,
                "resources": [
                    {"title": "SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "course"},
                    {"title": "Pandas Guide", "url": "https://pandas.pydata.org/docs/user_guide/index.html", "type": "article"},
                    {"title": "Data Cleaning Tutorial", "url": "https://www.youtube.com/watch?v=iYie42M1ZyU", "type": "video"}
                ]
            },
            {
                "id": "ds-2",
                "title": "Statistical Analysis",
                "description": "Hypothesis testing, A/B testing, and statistical modeling",
                "order": 2,
                "estimated_days": 50,
                "resources": [
                    {"title": "Statistics by Example", "url": "https://www.statisticsbyjim.com/", "type": "article"},
                    {"title": "A/B Testing Guide", "url": "https://www.optimizely.com/optimization-glossary/ab-testing/", "type": "article"},
                    {"title": "Statistics Course", "url": "https://www.youtube.com/watch?v=xxpc-HPKN28", "type": "video"}
                ]
            },
            {
                "id": "ds-3",
                "title": "Data Visualization",
                "description": "Create compelling visualizations with Tableau, Power BI",
                "order": 3,
                "estimated_days": 35,
                "resources": [
                    {"title": "Tableau Public", "url": "https://public.tableau.com/app/resources/learn", "type": "course"},
                    {"title": "Matplotlib Tutorial", "url": "https://matplotlib.org/stable/tutorials/index.html", "type": "article"},
                    {"title": "Data Viz Best Practices", "url": "https://www.youtube.com/watch?v=8EMW7io4rSI", "type": "video"}
                ]
            },
            {
                "id": "ds-4",
                "title": "Machine Learning for Data Science",
                "description": "Predictive modeling and feature engineering",
                "order": 4,
                "estimated_days": 60,
                "resources": [
                    {"title": "Feature Engineering Book", "url": "https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/", "type": "article"},
                    {"title": "Applied ML", "url": "https://www.coursera.org/learn/applied-machine-learning", "type": "course"},
                    {"title": "Model Selection", "url": "https://www.youtube.com/watch?v=EuBBz3bI-aA", "type": "video"}
                ]
            },
            {
                "id": "ds-5",
                "title": "Big Data & Production",
                "description": "Spark, data pipelines, and cloud data platforms",
                "order": 5,
                "estimated_days": 55,
                "resources": [
                    {"title": "Apache Spark Guide", "url": "https://spark.apache.org/docs/latest/", "type": "article"},
                    {"title": "Data Engineering", "url": "https://www.datacamp.com/tracks/data-engineer", "type": "course"},
                    {"title": "Big Data Tutorial", "url": "https://www.youtube.com/watch?v=9aEsXRTs1Ms", "type": "video"}
                ]
            }
        ]
    },
    {
        "id": "web3",
        "name": "Web3 Developer",
        "description": "Build decentralized applications on blockchain",
        "icon": "cube",
        "color": "#F59E0B",
        "milestones": [
            {
                "id": "w3-1",
                "title": "Blockchain Basics",
                "description": "Understand blockchain, crypto, and distributed systems",
                "order": 1,
                "estimated_days": 40,
                "resources": [
                    {"title": "Blockchain Fundamentals", "url": "https://www.coursera.org/learn/blockchain-basics", "type": "course"},
                    {"title": "Bitcoin Whitepaper", "url": "https://bitcoin.org/bitcoin.pdf", "type": "article"},
                    {"title": "Blockchain Explained", "url": "https://www.youtube.com/watch?v=SSo_EIwHSd4", "type": "video"}
                ]
            },
            {
                "id": "w3-2",
                "title": "Solidity & Smart Contracts",
                "description": "Write and deploy smart contracts on Ethereum",
                "order": 2,
                "estimated_days": 55,
                "resources": [
                    {"title": "Solidity Docs", "url": "https://docs.soliditylang.org/", "type": "article"},
                    {"title": "CryptoZombies", "url": "https://cryptozombies.io/", "type": "course"},
                    {"title": "Smart Contract Tutorial", "url": "https://www.youtube.com/watch?v=M576WGiDBdQ", "type": "video"}
                ]
            },
            {
                "id": "w3-3",
                "title": "DApp Development",
                "description": "Build frontend interfaces with Web3.js and Ethers.js",
                "order": 3,
                "estimated_days": 50,
                "resources": [
                    {"title": "Web3.js Guide", "url": "https://web3js.readthedocs.io/", "type": "article"},
                    {"title": "Ethers.js Docs", "url": "https://docs.ethers.org/", "type": "article"},
                    {"title": "Full Stack DApp", "url": "https://www.youtube.com/watch?v=a0osIaAOFSE", "type": "video"}
                ]
            },
            {
                "id": "w3-4",
                "title": "DeFi & NFTs",
                "description": "Decentralized finance protocols and NFT marketplaces",
                "order": 4,
                "estimated_days": 60,
                "resources": [
                    {"title": "DeFi Developer Roadmap", "url": "https://github.com/OffcierCia/DeFi-Developer-Road-Map", "type": "article"},
                    {"title": "NFT School", "url": "https://nftschool.dev/", "type": "course"},
                    {"title": "Build NFT Marketplace", "url": "https://www.youtube.com/watch?v=GKJBEEXUha0", "type": "video"}
                ]
            },
            {
                "id": "w3-5",
                "title": "Advanced Web3",
                "description": "Layer 2, cross-chain, and advanced protocols",
                "order": 5,
                "estimated_days": 55,
                "resources": [
                    {"title": "Layer 2 Guide", "url": "https://ethereum.org/en/layer-2/", "type": "article"},
                    {"title": "Hardhat Tutorial", "url": "https://hardhat.org/tutorial", "type": "course"},
                    {"title": "Advanced Solidity", "url": "https://www.youtube.com/watch?v=gyMwXuJrbJQ", "type": "video"}
                ]
            }
        ]
    },
    {
        "id": "cloud-engineering",
        "name": "Cloud Engineering",
        "description": "Design and manage scalable cloud infrastructure",
        "icon": "cloud",
        "color": "#06B6D4",
        "milestones": [
            {
                "id": "ce-1",
                "title": "Cloud Fundamentals",
                "description": "Learn cloud concepts, services, and deployment models",
                "order": 1,
                "estimated_days": 35,
                "resources": [
                    {"title": "AWS Cloud Practitioner", "url": "https://aws.amazon.com/certification/certified-cloud-practitioner/", "type": "course"},
                    {"title": "Cloud Computing Basics", "url": "https://www.cloudflare.com/learning/cloud/what-is-the-cloud/", "type": "article"},
                    {"title": "Cloud Overview", "url": "https://www.youtube.com/watch?v=M988_fsOSWo", "type": "video"}
                ]
            },
            {
                "id": "ce-2",
                "title": "AWS/Azure/GCP",
                "description": "Master compute, storage, and networking services",
                "order": 2,
                "estimated_days": 60,
                "resources": [
                    {"title": "AWS Solutions Architect", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "type": "course"},
                    {"title": "Azure Fundamentals", "url": "https://learn.microsoft.com/en-us/training/azure/", "type": "course"},
                    {"title": "GCP Tutorial", "url": "https://www.youtube.com/watch?v=4D3X6Xl5c_Y", "type": "video"}
                ]
            },
            {
                "id": "ce-3",
                "title": "Infrastructure as Code",
                "description": "Terraform, CloudFormation, and automated provisioning",
                "order": 3,
                "estimated_days": 45,
                "resources": [
                    {"title": "Terraform Tutorial", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "course"},
                    {"title": "IaC Best Practices", "url": "https://www.hashicorp.com/resources/what-is-infrastructure-as-code", "type": "article"},
                    {"title": "CloudFormation Guide", "url": "https://www.youtube.com/watch?v=9Xpuprxg7aY", "type": "video"}
                ]
            },
            {
                "id": "ce-4",
                "title": "Container Orchestration",
                "description": "Kubernetes, ECS, and serverless architectures",
                "order": 4,
                "estimated_days": 55,
                "resources": [
                    {"title": "Kubernetes Official", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "course"},
                    {"title": "AWS Lambda Guide", "url": "https://aws.amazon.com/lambda/getting-started/", "type": "article"},
                    {"title": "Serverless Tutorial", "url": "https://www.youtube.com/watch?v=vxJobGtqKVM", "type": "video"}
                ]
            },
            {
                "id": "ce-5",
                "title": "Cloud Security & Monitoring",
                "description": "Implement security, monitoring, and cost optimization",
                "order": 5,
                "estimated_days": 50,
                "resources": [
                    {"title": "AWS Security Best Practices", "url": "https://aws.amazon.com/architecture/security-identity-compliance/", "type": "article"},
                    {"title": "CloudWatch & Monitoring", "url": "https://aws.amazon.com/cloudwatch/", "type": "course"},
                    {"title": "Cloud Cost Optimization", "url": "https://www.youtube.com/watch?v=XQFweGjK_-o", "type": "video"}
                ]
            }
        ]
    }
]

# Routes
@api_router.get("/")
async def root():
    return {"message": "SUPERCHARGE API - Career Roadmap Platform"}

@api_router.get("/career-paths", response_model=List[CareerPath])
async def get_career_paths():
    """Get all career paths"""
    return CAREER_PATHS_DATA

@api_router.get("/career-paths/{path_id}", response_model=CareerPath)
async def get_career_path(path_id: str):
    """Get a specific career path"""
    for path in CAREER_PATHS_DATA:
        if path["id"] == path_id:
            return path
    raise HTTPException(status_code=404, detail="Career path not found")

@api_router.get("/progress/{user_id}", response_model=List[UserProgress])
async def get_user_progress(user_id: str):
    """Get user's progress across all career paths"""
    progress_list = await db.user_progress.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    
    for progress in progress_list:
        if isinstance(progress.get('updated_at'), str):
            progress['updated_at'] = datetime.fromisoformat(progress['updated_at'])
    
    return progress_list

@api_router.get("/progress/{user_id}/{path_id}")
async def get_path_progress(user_id: str, path_id: str):
    """Get user's progress for a specific career path"""
    progress = await db.user_progress.find_one(
        {"user_id": user_id, "career_path_id": path_id},
        {"_id": 0}
    )
    
    if not progress:
        # Return empty progress if none exists
        return {
            "user_id": user_id,
            "career_path_id": path_id,
            "completed_milestones": [],
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    
    if isinstance(progress.get('updated_at'), str):
        progress['updated_at'] = datetime.fromisoformat(progress['updated_at'])
    
    return progress

@api_router.post("/progress/{user_id}/{path_id}")
async def update_progress(user_id: str, path_id: str, update: ProgressUpdate):
    """Update milestone completion status"""
    # Find existing progress
    existing = await db.user_progress.find_one(
        {"user_id": user_id, "career_path_id": path_id}
    )
    
    if existing:
        completed = existing.get("completed_milestones", [])
        
        if update.completed and update.milestone_id not in completed:
            completed.append(update.milestone_id)
        elif not update.completed and update.milestone_id in completed:
            completed.remove(update.milestone_id)
        
        await db.user_progress.update_one(
            {"user_id": user_id, "career_path_id": path_id},
            {
                "$set": {
                    "completed_milestones": completed,
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    else:
        # Create new progress entry
        new_progress = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "career_path_id": path_id,
            "completed_milestones": [update.milestone_id] if update.completed else [],
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.user_progress.insert_one(new_progress)
    
    return {"success": True, "milestone_id": update.milestone_id, "completed": update.completed}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
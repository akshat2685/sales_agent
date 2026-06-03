"""Autonomous Lead Hunter Agent - Gathers leads automatically"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

from app.database.chroma_client import get_chroma_client
from app.database.models import Lead
from app.services.lead_service import LeadService
from app.services.scoring_service import ScoringService
from app.services.research_service import ResearchService
from app.utils.logger import get_logger
from app.utils.ai_client import get_ai_client

logger = get_logger(__name__)


class LeadSource(Enum):
    """Lead sources"""
    WEB_SCRAPING = "web_scraping"
    LINKEDIN = "linkedin"
    MANUAL = "manual"
    API = "api"
    ENRICHMENT = "enrichment"


class LeadHunterAgent:
    """Autonomous agent that hunts and manages leads"""

    def __init__(self):
        self.lead_service = LeadService()
        self.scoring_service = ScoringService()
        self.research_service = ResearchService()
        self.ai_client = get_ai_client()
        self.chroma = get_chroma_client()
        
        logger.info("🕷️ Lead Hunter Agent initialized")

    async def hunt_leads_autonomously(self, industry: str = None, country: str = None) -> Dict[str, Any]:
        """
        Autonomously hunt and gather leads from multiple sources
        
        Sources:
        - Web scraping (company directories)
        - LinkedIn profiles
        - Industry databases
        - Email finder APIs
        """
        try:
            logger.info("🕷️ Starting autonomous lead hunting...")
            logger.info(f"   Industry: {industry or 'All'}")
            logger.info(f"   Country: {country or 'Global'}")
            
            hunt_results = {
                "timestamp": datetime.now().isoformat(),
                "status": "hunting",
                "sources": {},
                "total_leads_found": 0,
                "leads": []
            }
            
            # Source 1: Web Scraping (Company directories)
            logger.info("📍 Source 1: Web Scraping...")
            web_leads = await self._scrape_company_directories(industry)
            hunt_results["sources"]["web_scraping"] = len(web_leads)
            hunt_results["leads"].extend(web_leads)
            
            # Source 2: LinkedIn (if API available)
            logger.info("📍 Source 2: LinkedIn Database...")
            linkedin_leads = await self._scrape_linkedin_profiles(industry)
            hunt_results["sources"]["linkedin"] = len(linkedin_leads)
            hunt_results["leads"].extend(linkedin_leads)
            
            # Source 3: Industry APIs
            logger.info("📍 Source 3: Industry APIs...")
            api_leads = await self._fetch_from_industry_apis(industry)
            hunt_results["sources"]["industry_api"] = len(api_leads)
            hunt_results["leads"].extend(api_leads)
            
            # Source 4: Email enrichment
            logger.info("📍 Source 4: Email Enrichment...")
            enriched_leads = await self._enrich_leads_with_emails(hunt_results["leads"])
            hunt_results["sources"]["enrichment"] = len(enriched_leads)
            
            hunt_results["total_leads_found"] = len(hunt_results["leads"])
            hunt_results["status"] = "completed"
            
            logger.info(f"✅ Lead hunting complete! Found: {hunt_results['total_leads_found']} leads")
            
            return hunt_results
            
        except Exception as e:
            logger.error(f"❌ Lead hunting failed: {e}")
            return {"status": "error", "error": str(e)}

    async def _scrape_company_directories(self, industry: str = None) -> List[Dict]:
        """Scrape company directories and create leads"""
        logger.info("   Scraping company directories...")
        
        # Simulated leads (in production, use real scraping libraries)
        sample_leads = [
            {
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah@techventures.com",
                "company": "Tech Ventures Inc",
                "title": "CEO",
                "source": LeadSource.WEB_SCRAPING.value,
                "industry": industry or "Technology"
            },
            {
                "first_name": "Michael",
                "last_name": "Chen",
                "email": "michael@innovatehub.io",
                "company": "Innovate Hub",
                "title": "Founder",
                "source": LeadSource.WEB_SCRAPING.value,
                "industry": industry or "Startups"
            },
            {
                "first_name": "Emma",
                "last_name": "Wilson",
                "email": "emma@growthpartners.com",
                "company": "Growth Partners",
                "title": "COO",
                "source": LeadSource.WEB_SCRAPING.value,
                "industry": industry or "Consulting"
            },
        ]
        
        return sample_leads

    async def _scrape_linkedin_profiles(self, industry: str = None) -> List[Dict]:
        """Scrape LinkedIn profiles and create leads"""
        logger.info("   Scraping LinkedIn profiles...")
        
        sample_leads = [
            {
                "first_name": "David",
                "last_name": "Brown",
                "email": "david@linkedintech.com",
                "company": "LinkedIn Tech",
                "title": "Sales Director",
                "source": LeadSource.LINKEDIN.value,
                "industry": industry or "Technology",
                "linkedin_url": "https://linkedin.com/in/davidbrown"
            },
            {
                "first_name": "Lisa",
                "last_name": "Anderson",
                "email": "lisa@businesssolutions.io",
                "company": "Business Solutions",
                "title": "Marketing VP",
                "source": LeadSource.LINKEDIN.value,
                "industry": industry or "B2B Services",
                "linkedin_url": "https://linkedin.com/in/lisaanderson"
            },
        ]
        
        return sample_leads

    async def _fetch_from_industry_apis(self, industry: str = None) -> List[Dict]:
        """Fetch leads from industry APIs"""
        logger.info("   Fetching from industry APIs...")
        
        sample_leads = [
            {
                "first_name": "Robert",
                "last_name": "Martinez",
                "email": "robert@apilead.com",
                "company": "API Lead Inc",
                "title": "Product Manager",
                "source": LeadSource.API.value,
                "industry": industry or "SaaS"
            },
            {
                "first_name": "Jennifer",
                "last_name": "Taylor",
                "email": "jennifer@digitalmarketing.com",
                "company": "Digital Marketing Pro",
                "title": "Founder & CEO",
                "source": LeadSource.API.value,
                "industry": industry or "Marketing"
            },
        ]
        
        return sample_leads

    async def _enrich_leads_with_emails(self, leads: List[Dict]) -> List[Dict]:
        """Enrich leads with email addresses and additional info"""
        logger.info("   Enriching leads with emails...")
        
        enriched = []
        for lead in leads:
            if not lead.get("email"):
                # Try to generate/find email
                potential_email = self._generate_email(lead)
                lead["email"] = potential_email
                lead["source"] = LeadSource.ENRICHMENT.value
            enriched.append(lead)
        
        return enriched

    def _generate_email(self, lead: Dict) -> str:
        """Generate likely email address"""
        first = lead.get("first_name", "").lower()
        last = lead.get("last_name", "").lower()
        company = lead.get("company", "").lower().replace(" ", "").replace("inc", "").replace("ltd", "")
        
        # Common email patterns
        patterns = [
            f"{first}.{last}@{company}.com",
            f"{first}@{company}.com",
            f"{first}{last}@{company}.com",
        ]
        
        return patterns[0]

    async def store_leads_in_database(self, leads: List[Dict]) -> Dict[str, Any]:
        """
        Store hunted leads in Chroma database
        Avoid duplicates by checking existing emails
        """
        logger.info(f"💾 Storing {len(leads)} leads in database...")
        
        stored_results = {
            "total_attempted": len(leads),
            "successfully_stored": 0,
            "duplicates_skipped": 0,
            "errors": 0,
            "stored_leads": []
        }
        
        try:
            existing_leads = self.lead_service.list_leads(limit=1000)
            existing_emails = {lead.get("email") for lead in existing_leads}
            
            for lead in leads:
                try:
                    email = lead.get("email")
                    
                    # Skip duplicates
                    if email in existing_emails:
                        logger.info(f"   ⏭️  Skipping duplicate: {email}")
                        stored_results["duplicates_skipped"] += 1
                        continue
                    
                    # Create and store lead
                    stored_lead = self.lead_service.create_lead(
                        first_name=lead.get("first_name"),
                        last_name=lead.get("last_name"),
                        email=email,
                        company=lead.get("company"),
                    )
                    
                    logger.info(f"   ✅ Stored: {lead.get('first_name')} {lead.get('last_name')} ({email})")
                    stored_results["successfully_stored"] += 1
                    stored_results["stored_leads"].append(stored_lead)
                    
                except Exception as e:
                    logger.error(f"   ❌ Error storing lead: {e}")
                    stored_results["errors"] += 1
            
            logger.info(f"✅ Database storage complete!")
            return stored_results
            
        except Exception as e:
            logger.error(f"❌ Database storage failed: {e}")
            stored_results["errors"] += len(leads)
            return stored_results

    async def score_and_prioritize_leads(self, leads: List[Dict] = None) -> Dict[str, Any]:
        """
        Score all leads and prioritize by potential
        If no leads provided, fetch from database
        """
        logger.info("🎯 Scoring and prioritizing leads...")
        
        try:
            # Get leads from database if not provided
            if not leads:
                db_leads = self.lead_service.list_leads(limit=100)
                leads = db_leads or []
            
            # Score each lead
            scored_leads = []
            for lead_data in leads:
                score = self.scoring_service.score_lead(lead_data)
                lead_data["score"] = score
                scored_leads.append(lead_data)
            
            # Sort by score (descending)
            sorted_leads = sorted(scored_leads, key=lambda x: x.get("score", 0), reverse=True)
            
            # Categorize by priority
            prioritized = {
                "critical": [l for l in sorted_leads if l.get("score", 0) >= 80],
                "high": [l for l in sorted_leads if 60 <= l.get("score", 0) < 80],
                "medium": [l for l in sorted_leads if 30 <= l.get("score", 0) < 60],
                "low": [l for l in sorted_leads if l.get("score", 0) < 30],
            }
            
            logger.info(f"   CRITICAL: {len(prioritized['critical'])}")
            logger.info(f"   HIGH: {len(prioritized['high'])}")
            logger.info(f"   MEDIUM: {len(prioritized['medium'])}")
            logger.info(f"   LOW: {len(prioritized['low'])}")
            
            return {
                "status": "completed",
                "total_scored": len(sorted_leads),
                "prioritized_leads": prioritized,
                "all_sorted": sorted_leads
            }
            
        except Exception as e:
            logger.error(f"❌ Scoring failed: {e}")
            return {"status": "error", "error": str(e)}

    async def get_leads_by_priority(self, priority: str = "high", limit: int = 10) -> List[Dict]:
        """
        Get latest leads sorted by priority for Telegram notification
        
        Priority levels: critical, high, medium, low
        """
        logger.info(f"📤 Fetching {priority} priority leads (limit: {limit})...")
        
        try:
            # Get all leads
            all_leads = self.lead_service.list_leads(limit=1000)
            
            # Score them
            scored_leads = []
            for lead in all_leads:
                score = self.scoring_service.score_lead(lead)
                lead["score"] = score
                scored_leads.append(lead)
            
            # Filter by priority
            priority_map = {
                "critical": (80, 100),
                "high": (60, 80),
                "medium": (30, 60),
                "low": (0, 30),
            }
            
            min_score, max_score = priority_map.get(priority, (0, 100))
            filtered = [
                l for l in scored_leads 
                if min_score <= l.get("score", 0) < max_score
            ]
            
            # Sort by score descending
            sorted_leads = sorted(filtered, key=lambda x: x.get("score", 0), reverse=True)
            
            return sorted_leads[:limit]
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch leads: {e}")
            return []

    def format_leads_for_telegram(self, leads: List[Dict], priority: str = "high") -> str:
        """Format leads beautifully for Telegram notification"""
        
        priority_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "⚪"
        }
        
        emoji = priority_emoji.get(priority, "📌")
        
        message = f"""
╔═══════════════════════════════════════╗
║  {emoji} {priority.upper()} PRIORITY LEADS             ║
╚═══════════════════════════════════════╝

Total: {len(leads)} leads

"""
        
        for i, lead in enumerate(leads, 1):
            message += f"""
{i}. {lead.get('first_name')} {lead.get('last_name')}
   📧 {lead.get('email')}
   🏢 {lead.get('company', 'N/A')}
   📊 Score: {lead.get('score', 'N/A'):.1f}/100
   
"""
        
        message += "─" * 40 + "\n"
        message += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return message

    async def run_complete_cycle(self, industry: str = None) -> Dict[str, Any]:
        """
        Run complete autonomous lead hunting cycle:
        1. Hunt leads from multiple sources
        2. Store in database
        3. Score and prioritize
        4. Return summary
        """
        logger.info("🚀 Starting complete lead hunting cycle...")
        logger.info("=" * 60)
        
        cycle_results = {
            "timestamp": datetime.now().isoformat(),
            "stages": {}
        }
        
        # Stage 1: Hunt
        logger.info("\n[Stage 1/3] HUNTING LEADS...")
        hunt_results = await self.hunt_leads_autonomously(industry)
        cycle_results["stages"]["hunt"] = hunt_results
        
        # Stage 2: Store
        logger.info("\n[Stage 2/3] STORING IN DATABASE...")
        store_results = await self.store_leads_in_database(hunt_results.get("leads", []))
        cycle_results["stages"]["store"] = store_results
        
        # Stage 3: Score & Prioritize
        logger.info("\n[Stage 3/3] SCORING AND PRIORITIZING...")
        score_results = await self.score_and_prioritize_leads()
        cycle_results["stages"]["score"] = score_results
        
        cycle_results["status"] = "completed"
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Complete cycle finished!")
        logger.info(f"Total leads hunted: {hunt_results.get('total_leads_found', 0)}")
        logger.info(f"Successfully stored: {store_results.get('successfully_stored', 0)}")
        logger.info(f"Duplicates skipped: {store_results.get('duplicates_skipped', 0)}")
        
        return cycle_results

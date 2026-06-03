"""Telegram bot command handlers - Showcase intelligent orchestrator"""

from telegram import Update
from telegram.ext import ContextTypes
from app.agent.orchestrator import HermesOrchestrator
from app.utils.logger import get_logger

logger = get_logger(__name__)
orchestrator = HermesOrchestrator()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    welcome_message = """
╔═══════════════════════════════════════╗
║   🧠 HERMES SALES AGENT 🧠           ║
║  AI-Powered Lead Intelligence        ║
╚═══════════════════════════════════════╝

Welcome! I'm your intelligent sales orchestrator.

Available commands:
/help - Show all commands
/add_lead - Add a new lead
/list_leads - View recent leads
/analytics - Get campaign analytics

Type /help for more details.
"""
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
╔═══════════════════════════════════════╗
║        HERMES COMMANDS                ║
╚═══════════════════════════════════════╝

🚀 LEAD MANAGEMENT
/add_lead <first_name> <last_name> <email> [company]
  → Add a new lead with intelligent processing
  → Example: /add_lead John Doe john@example.com "TechCorp"

/list_leads
  → View your recent leads

/search_leads <query>
  → Search leads by name or company

📊 ANALYTICS
/analytics
  → Get detailed campaign analytics
  → Conversion rates, lead scores, statistics

🎯 CAMPAIGN
/campaign <count>
  → Run a sample campaign with multiple leads

❓ HELP
/help - Show this message
/start - Show welcome message

═══════════════════════════════════════

The orchestrator automatically:
✓ Analyzes lead data
✓ Decides optimal processing strategy
✓ Calls appropriate services
✓ Scores and qualifies leads
✓ Generates personalized outreach
✓ Formats comprehensive responses
"""
    await update.message.reply_text(help_text)


async def add_lead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a new lead using orchestrator"""
    try:
        if len(context.args) < 3:
            await update.message.reply_text(
                "❌ Usage: /add_lead <first_name> <last_name> <email> [company]\\n"
                "Example: /add_lead John Doe john@example.com TechCorp"
            )
            return
        
        first_name = context.args[0]
        last_name = context.args[1]
        email = context.args[2]
        company = context.args[3] if len(context.args) > 3 else None
        
        # Show processing status
        await update.message.reply_text("🔄 Processing lead with orchestrator...", parse_mode="HTML")
        
        # Call orchestrator
        result = orchestrator.process_lead(first_name, last_name, email, company)
        
        # Format response
        formatted_response = orchestrator.format_response(result)
        
        await update.message.reply_text(formatted_response, parse_mode="HTML")
        
        # If ready to send, show next steps
        if result.get("status") == "ready_to_send":
            next_steps = """
✅ Lead is ready for outreach!

Next steps:
→ Review the message above
→ Send via email/LinkedIn
→ Update lead status as interactions occur
            """
            await update.message.reply_text(next_steps)
        
    except Exception as e:
        logger.error(f"Failed to add lead: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def list_leads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all leads"""
    try:
        leads = orchestrator.lead_service.list_leads(limit=10)
        
        if not leads:
            await update.message.reply_text("📭 No leads found yet. Use /add_lead to add one!")
            return
        
        message = "📋 RECENT LEADS\\n\\n"
        message += "=" * 40 + "\\n"
        
        for i, lead in enumerate(leads[:5], 1):
            message += f"\\n{i}. {lead.get('first_name')} {lead.get('last_name')}\\n"
            message += f"   📧 {lead.get('email')}\\n"
            message += f"   🏢 {lead.get('company', 'N/A')}\\n"
            message += f"   📊 Score: {lead.get('score', 'N/A')}/100\\n"
            message += f"   📍 Status: {lead.get('status', 'new')}\\n"
        
        message += "\\n" + "=" * 40
        
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Failed to list leads: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def search_leads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search leads by query"""
    try:
        if not context.args:
            await update.message.reply_text("Usage: /search_leads <query>")
            return
        
        query = " ".join(context.args)
        results = orchestrator.lead_service.search_leads(query, n_results=5)
        
        if not results or not results.get("metadatas"):
            await update.message.reply_text(f"❌ No leads found for '{query}'")
            return
        
        message = f"🔍 SEARCH RESULTS for '{query}'\\n\\n"
        for i, metadata in enumerate(results["metadatas"][:5], 1):
            message += f"{i}. {metadata.get('first_name')} {metadata.get('last_name')}\\n"
            message += f"   📧 {metadata.get('email')}\\n\\n"
        
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get analytics report"""
    try:
        await update.message.reply_text("📊 Generating analytics report...", parse_mode="HTML")
        
        analytics_data = orchestrator.get_analytics()
        
        stats = analytics_data.get("analytics", {}).get("statistics", {})
        metrics = analytics_data.get("analytics", {}).get("metrics", {})
        
        message = """
╔═══════════════════════════════════════╗
║      CAMPAIGN ANALYTICS               ║
╚═══════════════════════════════════════╝

📈 LEAD STATISTICS:
Total Leads: {}
├─ New: {}
├─ Contacted: {}
├─ Qualified: {}
└─ Converted: {}

📊 CONVERSION METRICS:
Conversion Rate: {:.2f}%
Average Score: {:.2f}/100
Contacted Leads: {}

═══════════════════════════════════════
        """.format(
            stats.get('total_leads', 0),
            stats.get('new_leads', 0),
            stats.get('contacted', 0),
            stats.get('qualified', 0),
            stats.get('converted', 0),
            metrics.get('conversion_rate', 0),
            metrics.get('average_score', 0),
            metrics.get('total_leads', 0),
        )
        
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Analytics failed: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def campaign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run a sample campaign with multiple leads"""
    try:
        count = int(context.args[0]) if context.args else 3
        
        if count > 10:
            await update.message.reply_text("⚠️ Max 10 leads per campaign for demo")
            count = 10
        
        await update.message.reply_text(f"🚀 Starting campaign with {count} sample leads...\\n(This may take a moment)")
        
        # Sample leads for demo
        sample_leads = [
            {"first_name": "Alice", "last_name": "Johnson", "email": "alice@techcorp.com", "company": "TechCorp"},
            {"first_name": "Bob", "last_name": "Smith", "email": "bob@innovate.com", "company": "Innovate Inc"},
            {"first_name": "Carol", "last_name": "Williams", "email": "carol@startup.io", "company": "StartupIO"},
            {"first_name": "David", "last_name": "Brown", "email": "david@enterprise.com", "company": "Enterprise Co"},
            {"first_name": "Eva", "last_name": "Martinez", "email": "eva@growth.com", "company": "Growth Labs"},
        ]
        
        leads_to_process = sample_leads[:count]
        
        # Run campaign through orchestrator
        campaign_result = orchestrator.run_campaign(leads_to_process)
        
        # Format results
        summary = campaign_result.get("summary", {})
        message = f"""
╔═══════════════════════════════════════╗
║      CAMPAIGN RESULTS                 ║
╚═══════════════════════════════════════╝

✅ Campaign Completed!

📊 LEAD BREAKDOWN:
🔴 CRITICAL: {summary.get('critical', 0)}
🟠 HIGH: {summary.get('high', 0)}
🟡 MEDIUM: {summary.get('medium', 0)}
⚪ LOW: {summary.get('low', 0)}

Total Processed: {campaign_result.get('total_leads', 0)}

Strategy Used: {campaign_result.get('strategy', 'N/A').upper()}

═══════════════════════════════════════

Check individual leads with /list_leads or /search_leads
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Campaign failed: {e}")
        await update.message.reply_text(f"❌ Campaign error: {str(e)}")

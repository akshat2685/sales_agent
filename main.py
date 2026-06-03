"""Main entry point - CEO Lead Management System"""

import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
)
from app.config.settings import settings
from app.utils.logger import get_logger
from app.bot.telegram_handlers import (
    start,
    help_command,
    hunt,
    hunt_industry,
    critical_leads,
    high_leads,
    medium_leads,
    low_leads,
    lead_summary,
    recent_leads,
)

logger = get_logger(__name__)


async def main():
    """Main function to start the CEO lead management bot"""
    logger.info("\n" + "="*70)
    logger.info("🚀 AUTONOMOUS LEAD HUNTER AGENT - STARTING")
    logger.info("="*70)
    logger.info(f"⏰ Timestamp: {logger}")
    logger.info(f"🔐 Configuration:")
    logger.info(f"   Debug Mode: {settings.DEBUG}")
    logger.info(f"   Log Level: {settings.LOG_LEVEL}")
    logger.info(f"   AI Model: {settings.MODEL_CHOICE}")
    logger.info(f"   Database: Chroma Cloud")
    logger.info(f"   Host: {settings.CHROMA_HOST}")
    logger.info("="*70)
    
    try:
        # Create bot application
        app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        logger.info("\n📝 Registering command handlers...")
        
        # Register all handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        
        # Hunting commands
        app.add_handler(CommandHandler("hunt", hunt))
        app.add_handler(CommandHandler("hunt_industry", hunt_industry))
        
        # Priority-based retrieval
        app.add_handler(CommandHandler("critical_leads", critical_leads))
        app.add_handler(CommandHandler("high_leads", high_leads))
        app.add_handler(CommandHandler("medium_leads", medium_leads))
        app.add_handler(CommandHandler("low_leads", low_leads))
        
        # Analytics
        app.add_handler(CommandHandler("lead_summary", lead_summary))
        app.add_handler(CommandHandler("recent_leads", recent_leads))
        
        logger.info("✅ All command handlers registered successfully!")
        logger.info(f"📱 Bot Token: {settings.TELEGRAM_BOT_TOKEN[:20]}...")
        logger.info(f"💬 Chat ID: {settings.TELEGRAM_CHAT_ID}")
        
        logger.info("\n" + "="*70)
        logger.info("🤖 BOT IS READY FOR COMMANDS")
        logger.info("="*70)
        logger.info("\n📋 Available Commands:")
        logger.info("   /hunt - Start autonomous lead hunting")
        logger.info("   /hunt_industry <industry> - Hunt in specific industry")
        logger.info("   /critical_leads - Get critical priority leads")
        logger.info("   /high_leads - Get high priority leads")
        logger.info("   /medium_leads - Get medium priority leads")
        logger.info("   /low_leads - Get low priority leads")
        logger.info("   /lead_summary - Get statistics")
        logger.info("   /recent_leads - View recent leads")
        logger.info("\n🕷️ LISTENING FOR COMMANDS...\n")
        logger.info("="*70 + "\n")
        
        # Start polling
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n" + "="*70)
        logger.info("🛑 BOT SHUTDOWN BY USER")
        logger.info("="*70)
    except Exception as e:
        logger.error(f"\n❌ CRITICAL ERROR: {e}")
        logger.error("="*70)

#!/usr/bin/env python3
"""
AI Business Opportunity Agent - Main Orchestrator
Usage: python src/main.py [telegram|email|test]
"""
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.collector import OpportunityCollector
from src.analyzer import OpportunityAnalyzer
from src.delivery import deliver

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def run_agent(delivery_method: str = "telegram"):
    start = datetime.now()
    logger.info("=" * 50)
    logger.info("AI BUSINESS OPPORTUNITY AGENT")
    logger.info("=" * 50)

    try:
        logger.info("[1/3] Collecting opportunities...")
        articles = OpportunityCollector().collect_all()

        if not articles:
            logger.warning("No articles found. Exiting.")
            return

        logger.info(f"Collected {len(articles)} opportunities")

        logger.info("[2/3] AI Analysis...")
        analyzer = OpportunityAnalyzer()
        briefing = analyzer.analyze(articles)
        briefing = analyzer.add_disclaimer(briefing)

        if delivery_method == "test":
            logger.info("[3/3] TEST MODE:")
            print("\n" + "=" * 50)
            print(briefing[:2000])
            print("\n... [truncated]")
            print("=" * 50)
        else:
            logger.info(f"[3/3] Delivering via {delivery_method}...")
            success = deliver(briefing, method=delivery_method)
            elapsed = (datetime.now() - start).total_seconds()
            if success:
                logger.info(f"SUCCESS! Delivered in {elapsed:.1f}s")
            else:
                logger.error("Delivery failed")

    except Exception as e:
        logger.error(f"Agent failed: {e}", exc_info=True)

    logger.info("=" * 50)


if __name__ == "__main__":
    method = sys.argv[1] if len(sys.argv) > 1 else "test"
    run_agent(delivery_method=method)

#!/usr/bin/env python3
"""
AI Agent Sweep CLI

Command-line interface for running sweep operations.

Usage:
    python backend/sweep_cli.py [options]

Options:
    --auto-fix          Enable automatic fixes for detected issues
    --format FORMAT     Output format: json, markdown (default: markdown)
    --output FILE       Save report to file instead of stdout
    --verbose           Enable verbose logging
"""

import sys
import os
import argparse
import asyncio
import logging

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.sweep import SweepAgent


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI Agent Sweep & Auto-Fix Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Enable automatic fixes for detected issues'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'markdown'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Save report to file instead of stdout'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting AI Agent Sweep...")
    logger.info(f"Auto-fix: {'enabled' if args.auto_fix else 'disabled'}")
    
    # Create and run sweep agent
    agent = SweepAgent(auto_fix=args.auto_fix)
    report = await agent.run_full_sweep()
    
    # Generate output
    if args.format == 'json':
        output = report.to_json()
    else:
        output = report.to_markdown()
    
    # Save or print output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        logger.info(f"Report saved to: {args.output}")
    else:
        print("\n" + "="*80)
        print(output)
        print("="*80)
    
    # Exit code based on errors
    report_dict = report.to_dict()
    if report_dict['summary']['total_errors'] > 0:
        logger.warning(f"Sweep completed with {report_dict['summary']['total_errors']} errors")
        return 1
    else:
        logger.info("Sweep completed successfully with no errors")
        return 0


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

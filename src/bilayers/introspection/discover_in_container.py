"""Entry point for running discovery inside a Docker container."""

import argparse
import sys
from pathlib import Path

from .discovery import discover_callables, save_discovery_results


def main():
    """Main entry point for containerized discovery."""
    parser = argparse.ArgumentParser(description="Discover functions in a module (containerized)")

    parser.add_argument("module", help="Module name to introspect")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file path")
    parser.add_argument("--include-private", action="store_true", help="Include private functions")
    parser.add_argument("--filter", help="Regex pattern to filter function names")

    args = parser.parse_args()

    try:
        # Run discovery
        results = discover_callables(
            args.module,
            include_private=args.include_private,
            filter_pattern=args.filter,
        )

        # Save results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_discovery_results(results, output_path)

        print(f"Discovered {len(results)} functions from {args.module}")
        print(f"Results saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

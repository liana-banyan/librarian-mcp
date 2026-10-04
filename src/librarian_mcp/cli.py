"""

"""


def main() -> None:
    """Run the stdio server, or import benchmark measurements with --import."""
    import sys

    from librarian_mcp.metrics import import_measurements

    if len(sys.argv) >= 2 and sys.argv[1] == "--import":
        if len(sys.argv) != 3:
            print("Usage: librarian-mcp --import path/to/results.jsonl", file=sys.stderr)
            raise SystemExit(2)

        imported, skipped = import_measurements(sys.argv[2])
        print(f"Imported {imported} records, skipped {skipped} malformed lines")
        return

    from librarian_mcp.server import main as serve

    serve()


if __name__ == "__main__":
    main()

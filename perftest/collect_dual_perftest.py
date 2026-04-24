import argparse
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master-source")
    parser.add_argument("--pr-source")
    parser.add_argument("--builds-root")
    parser.parse_args()

    timestamp = datetime.now().strftime("%a %d %b %Y %H:%M:%S %Z")
    print(f"body=Time now: {timestamp}")


if __name__ == "__main__":
    main()

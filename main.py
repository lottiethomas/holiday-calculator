import argparse
import json
import sys
from pathlib import Path

from dtos.user_dto import UserDto


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load a JSON file representing a user and calculate their cost for a holiday."
    )
    parser.add_argument(
        "user",
        type=Path,
        help="Path to the JSON file representing a user",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path: Path = args.user

    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"Error: not a file: {path}", file=sys.stderr)
        return 2

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {path} at line {e.lineno}, column {e.colno}", file=sys.stderr)
        return 3
    except OSError as e:
        print(f"Error: could not read {path}: {e}", file=sys.stderr)
        return 4

    # User details from the JSON file
    user = UserDto.model_validate(data).to_user()

    print(f"Cost for holidays in 2025/2026: {user.get_cost_for_holidays_in_holiday_year_starting_in(2025)}")
    print(f"Hours left in 2025/2026: {user.get_remaining_allowance_for_year_starting_in(2025)}")
    print(f"Cost for holidays in 2026/2027: {user.get_cost_for_holidays_in_holiday_year_starting_in(2026)}")
    print(f"Hours left in 2026/2027: {user.get_remaining_allowance_for_year_starting_in(2026)}")

    print(f'Days left in 2026/2027: {user.get_remaining_allowance_for_year_starting_in(2026)/8}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

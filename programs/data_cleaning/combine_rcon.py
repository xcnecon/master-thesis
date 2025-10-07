import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def normalize_key(value: str) -> str:
    """Normalize key field values for matching. Currently trims whitespace only."""
    if value is None:
        return ""
    return str(value).strip()


def resolve_column_name_case_insensitive(columns: Iterable[str], target: str) -> str:
    """Return the actual column name from columns that case-insensitively matches target."""
    normalized_to_actual: Dict[str, str] = {str(c).strip().lower(): c for c in columns}
    target_norm = target.strip().lower()
    if target_norm not in normalized_to_actual:
        raise KeyError(f"Required column '{target}' not found. Available columns: {list(columns)}")
    return normalized_to_actual[target_norm]


def read_headers(csv_path: Path) -> List[str]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"CSV '{csv_path}' appears to be empty – no header row found.")
    return header


def index_rows_by_keys(
    csv_path: Path,
    key_col_1: str,
    key_col_2: str,
) -> Dict[Tuple[str, str], Dict[str, str]]:
    """Load rows from csv_path into a dict keyed by (key1, key2). Last occurrence wins."""
    index: Dict[Tuple[str, str], Dict[str, str]] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            k1 = normalize_key(row.get(key_col_1))
            k2 = normalize_key(row.get(key_col_2))
            index[(k1, k2)] = row
    return index


def merge_rcon(
    rcon1_path: Path,
    rcon2_path: Path,
    output_path: Path,
    key1: str = "rssd9001",
    key2: str = "wrdsreportdate",
) -> None:
    # Inspect headers and resolve actual key column names (case-insensitive)
    rcon1_header = read_headers(rcon1_path)
    rcon2_header = read_headers(rcon2_path)

    rcon1_key1 = resolve_column_name_case_insensitive(rcon1_header, key1)
    rcon1_key2 = resolve_column_name_case_insensitive(rcon1_header, key2)

    rcon2_key1 = resolve_column_name_case_insensitive(rcon2_header, key1)
    rcon2_key2 = resolve_column_name_case_insensitive(rcon2_header, key2)

    # Determine which columns from rcon2 are NEW relative to rcon1 (excluding keys)
    rcon1_cols_set = set(rcon1_header)
    new_cols_from_rcon2: List[str] = [
        c
        for c in rcon2_header
        if c not in rcon1_cols_set and c not in {rcon2_key1, rcon2_key2}
    ]

    # Build index of rcon2 by (key1, key2)
    rcon2_index = index_rows_by_keys(rcon2_path, rcon2_key1, rcon2_key2)

    # Prepare output header: rcon1 columns first, then the NEW columns from rcon2
    output_header = list(rcon1_header) + new_cols_from_rcon2

    # Perform a LEFT JOIN: keep all rcon1 rows; add only NEW columns from rcon2
    total_rows = 0
    matched_rows = 0
    with rcon1_path.open("r", encoding="utf-8-sig", newline="") as f_in, output_path.open(
        "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=output_header)
        writer.writeheader()

        for row in reader:
            total_rows += 1
            k1 = normalize_key(row.get(rcon1_key1))
            k2 = normalize_key(row.get(rcon1_key2))
            r2 = rcon2_index.get((k1, k2))
            if r2 is not None:
                matched_rows += 1
                for col in new_cols_from_rcon2:
                    row[col] = r2.get(col, "")
            else:
                for col in new_cols_from_rcon2:
                    row[col] = ""
            writer.writerow(row)

    # Basic progress info
    print(
        f"Merged {total_rows} rows from rcon1 with {len(rcon2_index)} indexed rows from rcon2. "
        f"Matches found: {matched_rows}. Output: {output_path}"
    )


def main() -> None:
    # Fixed paths and keys (no CLI arguments)
    rcon1_path = Path("data") / "raw" / "rcon1.csv"
    rcon2_path = Path("data") / "raw" / "rcon2.csv"
    output_path = Path("data") / "raw" / "rcon_full.csv"

    # Validate inputs
    if not rcon1_path.exists():
        raise FileNotFoundError(f"rcon1 does not exist: {rcon1_path}")
    if not rcon2_path.exists():
        raise FileNotFoundError(f"rcon2 does not exist: {rcon2_path}")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    merge_rcon(
        rcon1_path=rcon1_path,
        rcon2_path=rcon2_path,
        output_path=output_path,
        key1="rssd9001",
        key2="wrdsreportdate",
    )


if __name__ == "__main__":
    main()



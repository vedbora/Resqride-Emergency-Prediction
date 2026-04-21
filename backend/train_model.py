from pathlib import Path
import argparse
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def resolve_dataset_path(backend_dir: Path, provided_path: str | None) -> Path:
    """
    Resolve dataset path from CLI arg or common filenames.
    """
    if provided_path:
        candidate = Path(provided_path)
        if not candidate.is_absolute():
            candidate = backend_dir / candidate
        if candidate.is_dir():
            # If a directory is provided, try to locate likely dataset CSV file inside it.
            preferred_names = ["911.csv", "911calls.csv", "911_calls.csv", "calls_911.csv"]
            for name in preferred_names:
                preferred = candidate / name
                if preferred.exists():
                    return preferred

            csv_files = sorted(candidate.glob("*.csv"))
            if len(csv_files) == 1:
                return csv_files[0]
            if len(csv_files) > 1:
                # Prefer files containing "911" in the filename.
                with_911 = [f for f in csv_files if "911" in f.name.lower()]
                if with_911:
                    return with_911[0]
                return csv_files[0]
        return candidate

    common_names = ["911.csv", "911calls.csv", "911_calls.csv", "calls_911.csv"]
    for name in common_names:
        candidate = backend_dir / name
        if candidate.exists():
            return candidate

    return backend_dir / "911.csv"


def train_and_save_model(dataset_arg: str | None = None):
    """
    Train Decision Tree model using 911 Calls data and save as model.pkl.
    Expected dataset columns: title, lat, lng
    """
    backend_dir = Path(__file__).resolve().parent
    dataset_path = resolve_dataset_path(backend_dir, dataset_arg)
    model_path = backend_dir / "model.pkl"

    if not dataset_path.exists():
        raise FileNotFoundError(
            "Dataset file not found.\n"
            "Place CSV in backend folder (e.g. 911.csv) OR pass path explicitly:\n"
            "python train_model.py --data \"C:/path/to/911.csv\""
        )

    df = pd.read_csv(dataset_path)

    required_columns = {"title", "lat", "lng"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}"
        )

    # Extract reason from title (e.g. 'EMS: BACK PAINS/INJURY' -> 'EMS')
    df["reason"] = df["title"].astype(str).str.split(":").str[0].str.strip()

    # Keep only known classes for consistent behavior.
    df = df[df["reason"].isin(["EMS", "Fire", "Traffic"])].copy()
    df = df.dropna(subset=["lat", "lng", "reason"])

    if df.empty:
        raise ValueError("No valid training rows found after preprocessing.")

    x = df[["lat", "lng"]]
    y = df["reason"]

    model = DecisionTreeClassifier(random_state=42)
    model.fit(x, y)

    joblib.dump(model, model_path)
    print(f"Model trained successfully and saved to: {model_path}")
    print(f"Training rows used: {len(df)}")
    print("Classes:", sorted(df["reason"].unique().tolist()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train ResQride model using 911 calls CSV dataset."
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Optional dataset path. If not provided, script searches common CSV names in backend folder.",
    )
    args = parser.parse_args()
    train_and_save_model(args.data)

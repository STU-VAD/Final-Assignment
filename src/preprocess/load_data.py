import pandas as pd
import json
from pathlib import Path

def load_co2_data(csv_path: str) -> dict:
    """Load CO2 data and return as dictionary."""
    df = pd.read_csv(csv_path, comment='#')
    return {
        'years': df['year'].tolist(),
        'mean': df['mean'].tolist(),
        'unc': df['unc'].tolist()
    }

def load_temperature_data(csv_path: str) -> dict:
    """Load temperature data and return as dictionary."""
    df = pd.read_csv(csv_path)
    lat_bands = [col for col in df.columns if col not in ['Year', 'Glob', 'NHem', 'SHem']]
    return {
        'years': df['Year'].tolist(),
        'latitudeBands': lat_bands,
        'anomalies': df[lat_bands].values.tolist()
    }

def save_json(data: dict, output_path: str):
    """Save data as JSON file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

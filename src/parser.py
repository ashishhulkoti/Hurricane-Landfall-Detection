import pandas as pd

def parse_hurdat2(file_path: str) -> pd.DataFrame:
    """
    Parse the NOAA HURDAT2 dataset into a structured pandas DataFrame.

    Each storm entry begins with a header line containing metadata,
    followed by multiple data lines representing 6-hour interval track data.

    Returns:
        pd.DataFrame: A structured DataFrame with columns:
            ['storm_id', 'name', 'datetime', 'year', 'lat', 'lon', 'wind', 'status', 'landfall']
    """
    records = []
    storm_id, name = None, None

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ The file {file_path} could not be found.")
    except Exception as e:
        raise RuntimeError(f"❌ Error reading HURDAT2 file: {e}")

    for line in lines:
        parts = line.strip().split(',')

        # Header line: contains storm ID and name
        if len(parts) == 4:
            storm_id = parts[0]
            name = parts[1].strip()
            continue

        # Data line: contains date/time, position, and intensity info
        try:
            date = parts[0].strip()
            time = parts[1].strip()
            year = int(date[:4])
            if year < 1900:
                continue  # Skip pre-1900 data

            lat = float(parts[4][:-1]) * (1 if parts[4][-1] == 'N' else -1)
            lon = float(parts[5][:-1]) * (-1 if parts[5][-1] == 'W' else 1)
            wind = int(parts[6].strip())
            landfall = parts[2].strip()
            status = parts[3].strip()

            records.append([
                storm_id, name,
                pd.to_datetime(date + time, format="%Y%m%d%H%M"),
                year, lat, lon, wind, status, landfall
            ])
        except (IndexError, ValueError):
            # Skip malformed lines but log them for debugging
            print(f"⚠️ Skipping malformed line: {line.strip()}")

    df = pd.DataFrame(
        records,
        columns=['storm_id', 'name', 'datetime', 'year', 'lat', 'lon', 'wind', 'status', 'landfall']
    )

    if df.empty:
        raise ValueError("❌ Parsed DataFrame is empty. Check file format or parsing logic.")

    return df

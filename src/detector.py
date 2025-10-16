import pandas as pd
from src.geoutil import is_in_state

def detect_landfalls_by_path(df: pd.DataFrame, state_polygon):
    """
    Detect hurricane landfalls algorithmically by checking when a storm's
    path crosses from ocean to land within the specified state boundary.

    Args:
        df (pd.DataFrame): Parsed HURDAT2 DataFrame.
        state_polygon (Polygon): Geometry of the state (e.g., Florida).

    Returns:
        pd.DataFrame: All landfall events with metadata, sorted by datetime.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty. Cannot detect landfalls.")

    landfalls = []
    for storm_id, group in df.groupby('storm_id'):
        group = group.sort_values('datetime').reset_index(drop=True)
        name = group['name'].iloc[0]
        prev_in_state = False

        for i in range(1, len(group)):
            try:
                curr_in_state = is_in_state(group.loc[i, 'lat'], group.loc[i, 'lon'], state_polygon)
                is_hurricane = group.loc[i, 'status'] == "HU"

                # Landfall condition: hurricane enters state boundary
                if not prev_in_state and curr_in_state and is_hurricane:
                    landfalls.append({
                        'storm_id': storm_id,
                        'name': name,
                        'datetime': group.loc[i, 'datetime'],
                        'lat': group.loc[i, 'lat'],
                        'lon': group.loc[i, 'lon'],
                        'wind': group.loc[i, 'wind'],
                        'status': group.loc[i, 'status'],
                        'landfall_indicator': group.loc[i, 'landfall']
                    })
                prev_in_state = curr_in_state
            except Exception as e:
                print(f"⚠️ Error processing storm {storm_id}: {e}")

    results = pd.DataFrame(landfalls)
    if not results.empty:
        results = results.sort_values(by='datetime', ascending=True).reset_index(drop=True)

    return results


def detect_landfalls_by_indicator(df: pd.DataFrame, state_polygon):
    """
    Detect hurricane landfalls using the official 'L' indicator from HURDAT2.

    Args:
        df (pd.DataFrame): Parsed HURDAT2 DataFrame.
        state_polygon (Polygon): Geometry of the state (e.g., Florida).

    Returns:
        pd.DataFrame: Landfalls with the 'L' indicator within the given state.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty. Cannot detect landfalls.")

    landfalls = []
    for storm_id, group in df.groupby('storm_id'):
        group = group.sort_values('datetime').reset_index(drop=True)
        name = group['name'].iloc[0]

        for i in range(1, len(group)):
            try:
                curr_in_state = is_in_state(group.loc[i, 'lat'], group.loc[i, 'lon'], state_polygon)
                is_hurricane = group.loc[i, 'status'] == "HU"
                has_indicator = group.loc[i, 'landfall'] == "L"

                if has_indicator and curr_in_state and is_hurricane:
                    landfalls.append({
                        'storm_id': storm_id,
                        'name': name,
                        'datetime': group.loc[i, 'datetime'],
                        'lat': group.loc[i, 'lat'],
                        'lon': group.loc[i, 'lon'],
                        'wind': group.loc[i, 'wind'],
                        'status': group.loc[i, 'status'],
                        'landfall_indicator': group.loc[i, 'landfall']
                    })
            except Exception as e:
                print(f"⚠️ Error in indicator-based detection for {storm_id}: {e}")

    results = pd.DataFrame(landfalls)
    if not results.empty:
        results = results.sort_values(by='datetime', ascending=True).reset_index(drop=True)

    return results

from shapely.geometry import Point
import geopandas as gpd

def load_state_polygon(shapefile_path: str, state_name: str):
    """
    Load a specific U.S. state's boundary polygon from a shapefile.

    Args:
        shapefile_path (str): Path to the shapefile containing all U.S. states.
        state_name (str): Name of the state to extract (e.g., 'Florida').

    Returns:
        shapely.geometry.Polygon: The state's boundary polygon.
    """
    try:
        states = gpd.read_file(shapefile_path)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to read shapefile: {e}")

    if 'NAME' not in states.columns:
        raise ValueError("❌ Shapefile must contain a 'NAME' column for state names.")

    if state_name not in states['NAME'].values:
        raise ValueError(f"❌ State '{state_name}' not found in shapefile.")

    return states.loc[states['NAME'] == state_name, 'geometry'].iloc[0]


def is_in_state(lat: float, lon: float, state_polygon) -> bool:
    """
    Check if a (lat, lon) point lies within the given state polygon.

    Args:
        lat (float): Latitude in decimal degrees.
        lon (float): Longitude in decimal degrees.
        state_polygon (Polygon): The state's geometry.

    Returns:
        bool: True if the point is inside the polygon, else False.
    """
    try:
        return state_polygon.contains(Point(lon, lat))
    except Exception:
        # Defensive fallback in case of malformed coordinates
        return False

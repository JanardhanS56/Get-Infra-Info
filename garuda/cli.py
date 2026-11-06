import sys
import json
import click
from rich.console import Console
from rich.prompt import Prompt

from .engine import analyze_sector
from .ui import display_banner, display_report
from .geo import validate_coordinates

console = Console()

PRESETS = {
    "1": ("Bengaluru (India)", 12.9716, 77.5946),
    "2": ("New York City (USA)", 40.7580, -73.9855),
    "3": ("London (UK)", 51.5074, -0.1278),
    "4": ("Tokyo (Japan)", 35.6580, 139.7016),
    "5": ("Paris (France)", 48.8566, 2.3522),
    "6": ("Sydney (Australia)", -33.8688, 151.2093),
}


def export_report(report, export_format: str, output_path: str):
    """Exports the generated analysis to JSON or Markdown."""
    if export_format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        console.print(f"[bold green]✓ Report exported successfully to JSON:[/] [cyan]{output_path}[/]")
    elif export_format == "md":
        md_content = f"""# Garuda Geospatial Reconnaissance Report (100 km²)

**Timestamp:** {report.analysis_timestamp}  
**Center Coordinates:** ({report.bbox.center_lat}, {report.bbox.center_lon})  
**Sector Scope:** 10.0 km × 10.0 km ({report.bbox.area_sq_km} km²)  
**Bounding Box:** South {report.bbox.south}° | North {report.bbox.north}° | West {report.bbox.west}° | East {report.bbox.east}°  

## 1. Geographic & Administrative Position
- **Location:** {report.place.display_name}
- **Elevation:** {report.place.elevation_m} m AMSL
- **Climate Conditions:** {report.place.current_temp_c}°C ({report.place.weather_condition})

## 2. Housing & Built Footprint
- **Total Buildings:** {report.buildings.total_buildings:,} ({report.buildings.building_density_per_sq_km} / km²)
- **Residential Houses:** {report.buildings.residential_buildings:,}
- **Apartment Complexes:** {report.buildings.apartments:,}
- **Commercial & Industrial:** {report.buildings.commercial_industrial:,}

## 3. Road & Mobility Network
- **Total Highway Segments:** {report.roads.total_road_segments:,} ({report.roads.road_density_per_sq_km} / km²)
- **Arterial Corridors & Expressways:** {report.roads.motorway_trunk:,}
- **Primary & Secondary Corridors:** {report.roads.primary_secondary:,}
- **Residential & Local Streets:** {report.roads.tertiary_residential:,}
- **Service & Living Streets:** {report.roads.service_living_street:,}
- **Pedestrian & Cycleways:** {report.roads.pedestrian_cycleways:,}
- **Railway Infrastructure:** {report.roads.railways:,}

## 4. Critical & Emergency Infrastructure
- **Hospitals & Medical Centers:** {report.critical_infra.hospitals:,}
- **Clinics & Outpatient Care:** {report.critical_infra.clinics:,}
- **Pharmacies:** {report.critical_infra.pharmacies:,}
- **Police Stations:** {report.critical_infra.police_stations:,}
- **Fire & Rescue Stations:** {report.critical_infra.fire_stations:,}
- **Schools (K-12):** {report.critical_infra.schools:,}
- **Colleges & Universities:** {report.critical_infra.colleges_universities:,}

## 5. Civic & Natural Environment
- **Waterways & Water Bodies:** {report.civic_env.water_bodies_ways:,}
- **Parks & Green Reserves:** {report.civic_env.parks_and_green:,}
- **Financial Access (Banks & ATMs):** {report.civic_env.banks_and_atms:,}
- **Fuel & Charging Stations:** {report.civic_env.fuel_charging_stations:,}

## 6. Strategic Assessment
- **Urban Classification:** {report.urbanization_index}
- **Infrastructure Maturity Score:** {report.infrastructure_score}
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        console.print(f"[bold green]✓ Report exported successfully to Markdown:[/] [cyan]{output_path}[/]")


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--lat", type=float, default=None, help="Latitude of the center point (-90.0 to 90.0)")
@click.option("--lon", type=float, default=None, help="Longitude of the center point (-180.0 to 180.0)")
@click.option("--size", type=float, default=10.0, help="Square side length in kilometers (default: 10.0)")
@click.option("--export", type=click.Choice(["json", "md"], case_sensitive=False), default=None, help="Export format")
@click.option("--output", type=str, default=None, help="Path for exported report")
def main(lat, lon, size, export, output):
    """
    GARUDA: 10km Square Geospatial Intelligence CLI
    
    Takes latitude and longitude and performs deep reconnaissance on a 10km × 10km sector.
    """
    display_banner()

    # Interactive mode if coordinates not specified
    if lat is None or lon is None:
        console.print("[bold yellow]No coordinates supplied. Select an option or enter custom coordinates:[/]\n")
        for key, (name, p_lat, p_lon) in PRESETS.items():
            console.print(f"  [bold cyan][{key}][/] {name} -> ({p_lat}, {p_lon})")
        console.print("  [bold cyan][C][/] Enter custom Latitude & Longitude\n")

        choice = Prompt.ask("Select option", default="1").strip()
        if choice in PRESETS:
            _, lat, lon = PRESETS[choice]
        else:
            raw_lat = Prompt.ask("Enter Latitude (e.g. 12.9716)").strip()
            raw_lon = Prompt.ask("Enter Longitude (e.g. 77.5946)").strip()
            try:
                lat = float(raw_lat)
                lon = float(raw_lon)
            except ValueError:
                console.print("[bold red]ERR: invalid coordinates. Latitude and longitude must be numbers.[/]")
                sys.exit(1)

    # Validate coordinates
    valid, err_msg = validate_coordinates(lat, lon)
    if not valid:
        console.print(f"[bold red]ERR: {err_msg}[/]")
        sys.exit(1)

    console.print(f"\n[bold green]► Initiating 10km Sector Analysis for ({lat:.6f}, {lon:.6f})...[/]")

    with console.status("[bold cyan]Querying OpenStreetMap, Nominatim & Open-Meteo...", spinner="dots"):
        try:
            report = analyze_sector(lat=lat, lon=lon, side_length_km=size)
        except Exception as e:
            console.print(f"[bold red]ERR: failed to complete sector analysis: {e}[/]")
            sys.exit(1)

    # Display Report in Terminal
    display_report(report)

    # Handle Export if requested
    if export:
        if not output:
            output = f"garuda_report_{lat:.4f}_{lon:.4f}.{export.lower()}"
        export_report(report, export.lower(), output)
    else:
        # Prompt for optional export
        save_opt = Prompt.ask("\nWould you like to export this intelligence report?", choices=["y", "n"], default="n")
        if save_opt.lower() == "y":
            fmt = Prompt.ask("Export format", choices=["json", "md"], default="md")
            out_file = f"garuda_sector_{lat:.4f}_{lon:.4f}.{fmt}"
            export_report(report, fmt, out_file)


if __name__ == "__main__":
    main()

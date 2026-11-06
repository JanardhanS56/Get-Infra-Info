from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from .models import AreaAnalysisReport

console = Console()


def display_banner():
    banner = Text(
        "🦅 GARUDA SPATIAL INTELLIGENCE\n"
        "10 km x 10 km (100 km²) Precision Area Reconnaissance",
        style="bold cyan",
        justify="center",
    )
    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))


def display_report(report: AreaAnalysisReport):
    bbox = report.bbox
    place = report.place
    bld = report.buildings
    roads = report.roads
    crit = report.critical_infra
    civic = report.civic_env

    # 1. Location & Geo Panel
    geo_text = Text()
    geo_text.append(f"• Location Name: ", style="bold yellow")
    geo_text.append(f"{place.display_name}\n", style="white")

    geo_text.append(f"• Admin Scope:   ", style="bold yellow")
    admin_parts = [p for p in [place.suburb, place.city, place.district, place.state, place.country] if p]
    geo_text.append(f"{' ➔ '.join(admin_parts) if admin_parts else 'N/A'}\n", style="cyan")

    geo_text.append(f"• Coordinates:   ", style="bold yellow")
    geo_text.append(f"Center ({bbox.center_lat:.6f}, {bbox.center_lon:.6f})\n", style="green")

    geo_text.append(f"• 10km Square:   ", style="bold yellow")
    geo_text.append(
        f"South {bbox.south:.4f}° | North {bbox.north:.4f}° | West {bbox.west:.4f}° | East {bbox.east:.4f}°\n",
        style="bright_white"
    )

    geo_text.append(f"• Area & Span:   ", style="bold yellow")
    elev_str = f"{place.elevation_m} m AMSL" if place.elevation_m is not None else "N/A"
    temp_str = f"{place.current_temp_c}°C ({place.weather_condition})" if place.current_temp_c is not None else "N/A"
    geo_text.append(
        f"10.0 km × 10.0 km (Total: {bbox.area_sq_km} km²) | Elevation: {elev_str} | Weather: {temp_str}",
        style="magenta"
    )

    console.print(Panel(geo_text, title="📍 GEOGRAPHIC POSITION & ADMINISTRATIVE SCOPE", border_style="yellow"))

    # 2. Table: Housing & Buildings
    bld_table = Table(title="🏢 Housing & Built Footprint", box=box.ROUNDED, expand=True, header_style="bold blue")
    bld_table.add_column("Category / Feature", style="cyan")
    bld_table.add_column("Count", justify="right", style="bold green")
    bld_table.add_column("Density / Context", style="dim white")

    bld_table.add_row("Total Building Structures", f"{bld.total_buildings:,}", f"{bld.building_density_per_sq_km:.1f} per km²")
    bld_table.add_row("Residential Houses & Homes", f"{bld.residential_buildings:,}", "Single family, detached, terrace")
    bld_table.add_row("Multi-Family / Apartments", f"{bld.apartments:,}", "High-density residential complexes")
    bld_table.add_row("Commercial & Industrial", f"{bld.commercial_industrial:,}", "Offices, retail, warehouses, plants")
    bld_table.add_row("Other / Unclassified Structures", f"{bld.other_buildings:,}", "Civic, sheds, outbuildings")

    # 3. Table: Roads & Mobility Network
    road_table = Table(title="🛣️ Road Expansion & Mobility", box=box.ROUNDED, expand=True, header_style="bold magenta")
    road_table.add_column("Highway Network Tier", style="cyan")
    road_table.add_column("Segments", justify="right", style="bold green")
    road_table.add_column("Connectivity Role", style="dim white")

    road_table.add_row("Total Road Network", f"{roads.total_road_segments:,}", f"{roads.road_density_per_sq_km:.1f} segments/km²")
    road_table.add_row("Expressways & Arterial Trunks", f"{roads.motorway_trunk:,}", "Intercity / regional transit corridors")
    road_table.add_row("Primary & Secondary Roads", f"{roads.primary_secondary:,}", "Urban thoroughfares & commercial avenues")
    road_table.add_row("Residential & Local Streets", f"{roads.tertiary_residential:,}", "Neighborhood & internal access streets")
    road_table.add_row("Service Roads & Living Streets", f"{roads.service_living_street:,}", "Alleys, parking & shared zones")
    road_table.add_row("Tracks & Rural Roads", f"{roads.track_unclassified:,}", "Agricultural / unpaved connectors")
    road_table.add_row("Pedestrian Walkways & Cycleways", f"{roads.pedestrian_cycleways:,}", "Active non-motorized infrastructure")
    road_table.add_row("Bridges & Overpasses", f"{roads.bridges:,}", "Grade-separated river/rail crossings")
    road_table.add_row("Tunnels & Underpasses", f"{roads.tunnels:,}", "Sub-surface vehicular conduits")
    road_table.add_row("Railway Lines & Tracks", f"{roads.railways:,}", "Heavy rail, metro & light rail routes")

    console.print(Columns([bld_table, road_table], equal=True))

    # 4. Table: Critical Emergency & Health Infrastructure
    crit_table = Table(title="🚑 Critical & Emergency Infrastructure", box=box.ROUNDED, expand=True, header_style="bold red")
    crit_table.add_column("Facility", style="cyan")
    crit_table.add_column("Count", justify="right", style="bold green")
    crit_table.add_column("Operational Status", style="dim white")

    crit_table.add_row("Hospitals & Medical Centers", f"{crit.hospitals:,}", "Emergency care & surgical facilities")
    crit_table.add_row("Clinics & Health Centers", f"{crit.clinics:,}", "Outpatient & primary health clinics")
    crit_table.add_row("Pharmacies & Dispensaries", f"{crit.pharmacies:,}", "Pharmaceutical retail access")
    crit_table.add_row("Police Stations & Posts", f"{crit.police_stations:,}", "Law enforcement & public security")
    crit_table.add_row("Fire & Rescue Stations", f"{crit.fire_stations:,}", "Firefighting & disaster response")
    crit_table.add_row("Schools (Primary & Secondary)", f"{crit.schools:,}", "K-12 educational institutions")
    crit_table.add_row("Colleges & Universities", f"{crit.colleges_universities:,}", "Higher education campuses")

    # 5. Table: Civic, Amenities & Natural Environment
    civic_table = Table(title="🌳 Civic Amenities & Natural Environment", box=box.ROUNDED, expand=True, header_style="bold green")
    civic_table.add_column("Feature / Amenity", style="cyan")
    civic_table.add_column("Count", justify="right", style="bold green")
    civic_table.add_column("Ecological & Social Role", style="dim white")

    civic_table.add_row("Waterways & Water Bodies", f"{civic.water_bodies_ways:,}", "Lakes, rivers, canals & reservoirs")
    civic_table.add_row("Parks, Gardens & Green Cover", f"{civic.parks_and_green:,}", "Urban green lung & recreation")
    civic_table.add_row("Banks & ATM Terminals", f"{civic.banks_and_atms:,}", "Financial services distribution")
    civic_table.add_row("Fuel Stations & EV Chargers", f"{civic.fuel_charging_stations:,}", "Energy & mobility fueling points")
    civic_table.add_row("Places of Worship", f"{civic.places_of_worship:,}", "Community & cultural sanctuaries")
    civic_table.add_row("Supermarkets & Food Markets", f"{civic.supermarkets_markets:,}", "Essential food supply nodes")

    console.print(Columns([crit_table, civic_table], equal=True))

    # 6. Strategic Assessment Panel
    summary_text = Text()
    summary_text.append("• Urban Classification:    ", style="bold white")
    summary_text.append(f"{report.urbanization_index}\n", style="bold cyan")

    summary_text.append("• Infrastructure Maturity:  ", style="bold white")
    summary_text.append(f"{report.infrastructure_score}\n", style="bold green")

    summary_text.append("• Tactical Area Summary:   ", style="bold white")
    summary_text.append(
        f"This 100 km² sector encompasses {bld.total_buildings:,} buildings "
        f"and {roads.total_road_segments:,} active road segments with {crit.healthcare_total:,} healthcare sites, "
        f"{crit.emergency_services_total:,} emergency response hubs, and {civic.water_bodies_ways:,} mapped water features.",
        style="white"
    )

    console.print(Panel(summary_text, title="⚡ STRATEGIC ASSESSMENT", border_style="bold magenta"))

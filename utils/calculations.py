def calculate_foam_requirements(length, width, height,
                                target_density=23.6,
                                polyol_weight=300.0,
                                c_pentane_weight=43.0,
                                mdi_weight=152.0,
                                polyol_mix_weight=114.2):
    """
    Calculate foam shot mass for given dimensions and material ratios.
    
    Returns a dictionary with foam volume, required materials, and thickening time.
    """
    # Foam volume
    volume_cm3 = length * width * height
    volume_m3 = volume_cm3 / 1e6  # m³

    # Total mass required
    total_mass_kg = target_density * volume_m3
    total_mass_g = total_mass_kg * 1000

    # Fractions based on lab test
    polyol_fraction = polyol_mix_weight / (polyol_mix_weight + mdi_weight)
    mdi_fraction = mdi_weight / (polyol_mix_weight + mdi_weight)
    c_pentane_fraction = c_pentane_weight / polyol_weight

    # Calculate required materials
    required_polyol = total_mass_g * polyol_fraction / (1 + c_pentane_fraction)
    required_c_pentane = required_polyol * c_pentane_fraction
    required_mdi = total_mass_g * mdi_fraction

    # Thickening time (lab reference)
    thickening_time_sec = 45  # ±4 sec at 25°C

    return {
        "volume_cm3": volume_cm3,
        "volume_m3": volume_m3,
        "total_mass_g": total_mass_g,
        "total_mass_kg": total_mass_kg,
        "required_polyol": required_polyol,
        "required_c_pentane": required_c_pentane,
        "required_mdi": required_mdi,
        "thickening_time_sec": thickening_time_sec,
        "target_density": target_density
    }

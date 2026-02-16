"""Physics constants for space engineering. These NEVER change.

Usage from any skill tool:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
    from constants import G0, MU_EARTH, AU
"""

# Gravitational
G0 = 9.80665              # m/s^2, standard gravity
G_CONST = 6.67430e-11     # m^3 kg^-1 s^-2, gravitational constant

# Earth
MU_EARTH = 3.986004418e5  # km^3/s^2
R_EARTH = 6371.0           # km, mean radius
J2_EARTH = 1.08263e-3      # Earth oblateness

# Sun
MU_SUN = 1.32712440018e11 # km^3/s^2
AU = 1.496e8               # km, astronomical unit

# Planetary mu (km^3/s^2)
MU = {
    "mercury": 2.2032e4,
    "venus": 3.24859e5,
    "earth": 3.986004418e5,
    "moon": 4.9048695e3,
    "mars": 4.282837e4,
    "jupiter": 1.26687e8,
    "saturn": 3.7931e7,
    "uranus": 5.794e6,
    "neptune": 6.8351e6,
}

# Planetary semi-major axes (km from Sun)
SMA = {
    "mercury": 5.791e7,
    "venus": 1.082e8,
    "earth": 1.496e8,
    "mars": 2.279e8,
    "jupiter": 7.786e8,
    "saturn": 1.4335e9,
    "uranus": 2.8725e9,
    "neptune": 4.4951e9,
}

# Speed of light
C = 299792.458  # km/s

# Boltzmann
K_BOLTZMANN = 1.380649e-23  # J/K

# Stefan-Boltzmann
SIGMA_SB = 5.670374419e-8   # W m^-2 K^-4

# Solar flux at 1 AU
SOLAR_FLUX_1AU = 1361.0  # W/m^2

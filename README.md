# Atom Simulation

Atom Simulation is an interactive Pygame desktop app for exploring basic atomic structure. It keeps the original animated electron idea, then adds richer educational views for shells, orbital probability clouds, emission spectra, ions, isotopes, and simplified energy transitions.

## Features

- Animated Bohr-style shell model.
- Probability-inspired electron cloud view with measurement markers.
- Representative visible spectrum lines for selected elements.
- Hydrogen-like energy transition lab with emitted photons, wavelength, and eV readout.
- First 20 elements with clickable picker tiles.
- Ion charge controls that update electron count and shell layout.
- Isotope controls that update neutron count and nucleus display.
- Keyboard and mouse controls for fast exploration.

## Requirements

- Python 3.10 or newer.
- Pygame.

Install Pygame:

```powershell
python -m pip install pygame
```

## Run

From the project root:

```powershell
python main.py
```

## Controls

| Action | Control |
| --- | --- |
| Select first ten elements | `1`-`9`, `0` |
| Cycle elements | `Left` / `Right` or `A` / `D` |
| Switch modes | Click top tabs or press `B`, `C`, `S`, `E` |
| Cycle mode | `M` |
| Pause / resume | `Space` |
| Change animation speed | `+` / `-` |
| Change ion charge | `[` / `]` |
| Change neutron count | `,` / `.` |
| Measure cloud probability | Click in Cloud mode or press `X` |
| Energy transition level | `Up` / `Down` |
| Energy transition target | `T` |
| Emit photon | `Enter` |
| Help overlay | `H` |
| Quit | `Esc` or `Q` |

## Educational Notes

This is a teaching simulator, not a numerical quantum chemistry package. Shells, orbital clouds, and multi-electron energy transitions are simplified visual models intended to build intuition. The energy transition view uses hydrogen-like equations and is exact only for one-electron atoms or ions.

Representative spectral lines are included for classroom-style visualization. They should not be treated as calibration-grade spectroscopy data.

## Development Checks

Compile check:

```powershell
python -m py_compile main.py
```

Headless smoke run:

```powershell
$env:SDL_VIDEODRIVER='dummy'
$env:ATOM_SIM_SMOKE='1'
python main.py
```

## Project Structure

```text
.
├── main.py
├── LICENSE
├── README.md
├── SECURITY.md
└── CONTRIBUTING.md
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.

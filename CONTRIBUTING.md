# Contributing

Thanks for improving Atom Simulation. Contributions should keep the app simple to run, educational, and understandable for learners.

## Getting Started

1. Fork or clone the repository.
2. Install Python 3.10 or newer.
3. Install Pygame:

```powershell
python -m pip install pygame
```

4. Run the app:

```powershell
python main.py
```

## Development Workflow

Before opening a pull request, run:

```powershell
python -m py_compile main.py
```

For a quick headless smoke test:

```powershell
$env:SDL_VIDEODRIVER='dummy'
$env:ATOM_SIM_SMOKE='1'
python main.py
```

## Contribution Ideas

- Improve UI layout and accessibility.
- Add more accurate or better documented atomic data.
- Add more element spectra while clearly citing the source.
- Improve cloud and energy model explanations.
- Add tests for helper functions such as wavelength conversion, isotope labels, and shell filling.
- Package the app for easier installation.

## Code Style

- Keep the app easy to run as a single-file Pygame project unless there is a strong reason to split modules.
- Use clear names for physics and UI concepts.
- Prefer small helper functions over repeated drawing logic.
- Keep comments short and useful.
- Avoid adding dependencies unless they materially improve the project.

## Scientific Accuracy

This project uses simplified educational models. When adding physics behavior:

- Clearly distinguish exact formulas from teaching approximations.
- Cite authoritative sources for atomic data.
- Avoid presenting visual intuition as a full quantum mechanical solver.
- Keep UI wording honest about limitations.

## Pull Request Checklist

- The app starts with `python main.py`.
- `python -m py_compile main.py` passes.
- New controls are documented in `README.md`.
- New data sources are documented where relevant.
- Generated files are not committed.
- Changes are focused and do not remove existing features unless discussed first.

## License

By contributing, you agree that your contributions will be licensed under the MIT License used by this project.

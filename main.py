from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass

import pygame


WINDOW_SIZE = (1180, 820)
FPS = 60

BACKGROUND = (14, 16, 20)
PANEL = (29, 33, 39)
PANEL_ALT = (38, 43, 50)
BORDER = (58, 67, 80)
SURFACE = (17, 20, 25)
SURFACE_ALT = (23, 27, 33)
TEXT = (235, 239, 245)
MUTED = (155, 164, 178)
FAINT = (78, 88, 102)
ORBIT = (86, 100, 118)
PROTON = (235, 90, 86)
NEUTRON = (108, 128, 152)
ELECTRON = (94, 210, 255)
ACCENT = (250, 184, 75)
GOOD = (111, 220, 154)


@dataclass(frozen=True)
class Element:
    atomic_number: int
    symbol: str
    name: str
    mass_number: int
    shells: tuple[int, ...]
    electron_config: str
    category: str
    color: tuple[int, int, int]
    spectrum_nm: tuple[float, ...]
    note: str

    @property
    def neutron_count(self) -> int:
        return max(0, self.mass_number - self.atomic_number)

    @property
    def valence_electrons(self) -> int:
        return self.shells[-1]


ELEMENTS: list[Element] = [
    Element(1, "H", "Hydrogen", 1, (1,), "1s1", "Reactive nonmetal", (92, 190, 255), (410.2, 434.0, 486.1, 656.3), "Balmer lines shown in spectrum mode."),
    Element(2, "He", "Helium", 4, (2,), "1s2", "Noble gas", (180, 156, 255), (447.1, 471.3, 492.2, 501.6, 587.6, 667.8, 706.5), "Closed first shell."),
    Element(3, "Li", "Lithium", 7, (2, 1), "1s2 2s1", "Alkali metal", (255, 138, 112), (610.4, 670.8), "One valence electron."),
    Element(4, "Be", "Beryllium", 9, (2, 2), "1s2 2s2", "Alkaline earth metal", (255, 199, 95), (), "Second shell has an s pair."),
    Element(5, "B", "Boron", 11, (2, 3), "1s2 2s2 2p1", "Metalloid", (130, 220, 160), (), "First p electron."),
    Element(6, "C", "Carbon", 12, (2, 4), "1s2 2s2 2p2", "Reactive nonmetal", (118, 235, 210), (), "Four valence electrons."),
    Element(7, "N", "Nitrogen", 14, (2, 5), "1s2 2s2 2p3", "Reactive nonmetal", (118, 170, 255), (), "Half-filled p subshell."),
    Element(8, "O", "Oxygen", 16, (2, 6), "1s2 2s2 2p4", "Reactive nonmetal", (245, 116, 116), (), "Six valence electrons."),
    Element(9, "F", "Fluorine", 19, (2, 7), "1s2 2s2 2p5", "Halogen", (133, 235, 119), (), "One electron short of neon."),
    Element(10, "Ne", "Neon", 20, (2, 8), "1s2 2s2 2p6", "Noble gas", (255, 118, 178), (585.2, 614.3, 640.2, 650.7, 703.2), "Closed second shell."),
    Element(11, "Na", "Sodium", 23, (2, 8, 1), "[Ne] 3s1", "Alkali metal", (255, 198, 74), (589.0, 589.6), "Classic yellow doublet."),
    Element(12, "Mg", "Magnesium", 24, (2, 8, 2), "[Ne] 3s2", "Alkaline earth metal", (122, 224, 178), (516.7, 517.3, 518.4), "Third-shell s pair."),
    Element(13, "Al", "Aluminium", 27, (2, 8, 3), "[Ne] 3s2 3p1", "Post-transition metal", (146, 184, 215), (), "First third-shell p electron."),
    Element(14, "Si", "Silicon", 28, (2, 8, 4), "[Ne] 3s2 3p2", "Metalloid", (120, 210, 176), (), "Semiconductor element."),
    Element(15, "P", "Phosphorus", 31, (2, 8, 5), "[Ne] 3s2 3p3", "Reactive nonmetal", (238, 150, 91), (), "Half-filled 3p subshell."),
    Element(16, "S", "Sulfur", 32, (2, 8, 6), "[Ne] 3s2 3p4", "Reactive nonmetal", (248, 212, 92), (), "Six valence electrons."),
    Element(17, "Cl", "Chlorine", 35, (2, 8, 7), "[Ne] 3s2 3p5", "Halogen", (130, 225, 130), (), "One electron short of argon."),
    Element(18, "Ar", "Argon", 40, (2, 8, 8), "[Ne] 3s2 3p6", "Noble gas", (155, 166, 255), (696.5, 706.7, 738.4), "Closed third shell."),
    Element(19, "K", "Potassium", 39, (2, 8, 8, 1), "[Ar] 4s1", "Alkali metal", (196, 150, 255), (404.4, 766.5, 769.9), "A fourth shell starts."),
    Element(20, "Ca", "Calcium", 40, (2, 8, 8, 2), "[Ar] 4s2", "Alkaline earth metal", (125, 217, 194), (393.4, 396.8, 422.7), "Fourth-shell s pair."),
]


ORBITAL_SEQUENCE = (
    ("1s", 2, "s", 1),
    ("2s", 2, "s", 2),
    ("2p", 6, "p", 2),
    ("3s", 2, "s", 3),
    ("3p", 6, "p", 3),
    ("4s", 2, "s", 4),
)


@dataclass
class ElectronParticle:
    shell_index: int
    slot: int
    angle: float
    angular_speed: float
    color: tuple[int, int, int]


@dataclass
class CloudPoint:
    x: float
    y: float
    color: tuple[int, int, int]
    size: int
    phase: float


@dataclass
class Measurement:
    x: float
    y: float
    probability: float
    age: float = 0.0


@dataclass
class Photon:
    x: float
    y: float
    vx: float
    vy: float
    color: tuple[int, int, int]
    wavelength_nm: float
    energy_ev: float
    age: float = 0.0
    life: float = 1.8


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    amount = clamp(amount, 0.0, 1.0)
    return (
        int(a[0] + (b[0] - a[0]) * amount),
        int(a[1] + (b[1] - a[1]) * amount),
        int(a[2] + (b[2] - a[2]) * amount),
    )


def wavelength_to_rgb(wavelength_nm: float) -> tuple[int, int, int]:
    """Approximate visible wavelength as display RGB."""
    wavelength_nm = clamp(wavelength_nm, 380.0, 780.0)
    gamma = 0.8

    if wavelength_nm < 440:
        r, g, b = -(wavelength_nm - 440) / 60, 0.0, 1.0
    elif wavelength_nm < 490:
        r, g, b = 0.0, (wavelength_nm - 440) / 50, 1.0
    elif wavelength_nm < 510:
        r, g, b = 0.0, 1.0, -(wavelength_nm - 510) / 20
    elif wavelength_nm < 580:
        r, g, b = (wavelength_nm - 510) / 70, 1.0, 0.0
    elif wavelength_nm < 645:
        r, g, b = 1.0, -(wavelength_nm - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0

    if wavelength_nm < 420:
        factor = 0.3 + 0.7 * (wavelength_nm - 380) / 40
    elif wavelength_nm < 701:
        factor = 1.0
    else:
        factor = 0.3 + 0.7 * (780 - wavelength_nm) / 80

    return (
        int(255 * (r * factor) ** gamma),
        int(255 * (g * factor) ** gamma),
        int(255 * (b * factor) ** gamma),
    )


def draw_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    pos: tuple[int, int],
    color: tuple[int, int, int] = TEXT,
) -> pygame.Rect:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)
    return rect


def draw_centered_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    center: tuple[int, int],
    color: tuple[int, int, int] = TEXT,
) -> pygame.Rect:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)
    return rect


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int] = PANEL,
    border: tuple[int, int, int] = BORDER,
    radius: int = 8,
) -> None:
    shadow = rect.move(0, 3)
    pygame.draw.rect(surface, (7, 9, 12), shadow, border_radius=radius)
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 1, border_radius=radius)


def draw_fit_right(
    surface: pygame.Surface,
    fonts: tuple[pygame.font.Font, ...],
    text: str,
    right: int,
    y: int,
    color: tuple[int, int, int],
    max_width: int,
) -> None:
    for font in fonts:
        rendered = font.render(text, True, color)
        if rendered.get_width() <= max_width:
            surface.blit(rendered, (right - rendered.get_width(), y))
            return

    font = fonts[-1]
    clipped = text
    while clipped and font.size(clipped + "...")[0] > max_width:
        clipped = clipped[:-1]
    rendered = font.render((clipped + "...") if clipped else "...", True, color)
    surface.blit(rendered, (right - rendered.get_width(), y))


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def orbital_occupancy(electrons: int) -> list[tuple[str, int, str, int]]:
    occupancy: list[tuple[str, int, str, int]] = []
    remaining = electrons
    for label, capacity, orbital_type, principal in ORBITAL_SEQUENCE:
        if remaining <= 0:
            break
        count = min(capacity, remaining)
        occupancy.append((label, count, orbital_type, principal))
        remaining -= count
    return occupancy


def shells_for_electrons(electrons: int) -> tuple[int, ...]:
    shells: list[int] = []
    remaining = max(0, electrons)
    for capacity in (2, 8, 8, 2):
        if remaining <= 0:
            break
        shells.append(min(capacity, remaining))
        remaining -= shells[-1]
    return tuple(shells) if shells else (0,)


def ion_label(charge: int) -> str:
    if charge == 0:
        return "neutral"
    sign = "+" if charge > 0 else "-"
    amount = abs(charge)
    return f"{sign}" if amount == 1 else f"{amount}{sign}"


def isotope_label(element: Element, neutron_count: int) -> str:
    return f"{element.name}-{element.atomic_number + neutron_count}"


def hydrogenic_transition(z: int, high_n: int, low_n: int) -> tuple[float, float]:
    energy_ev = 13.605693 * z * z * ((1 / (low_n * low_n)) - (1 / (high_n * high_n)))
    wavelength_nm = 1239.841984 / energy_ev
    return energy_ev, wavelength_nm


def wavelength_band(wavelength_nm: float) -> str:
    if wavelength_nm < 380:
        return "UV"
    if wavelength_nm <= 780:
        return "visible"
    return "IR"


class AtomSimulation:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Atom Simulation")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.show_help = False
        self.current_index = 0
        self.mode_index = 0
        self.modes = ("Shell", "Cloud", "Spectrum", "Energy")
        self.speed_scale = 1.0
        self.time = 0.0
        self.frame_count = 0
        self.ion_charge = 0
        self.neutron_delta = 0
        self.excited_level = 3
        self.transition_target = 2
        self.periodic_buttons: list[tuple[pygame.Rect, int]] = []
        self.mode_buttons: list[tuple[pygame.Rect, int]] = []
        self.measurements: list[Measurement] = []
        self.photons: list[Photon] = []

        self.font_small = pygame.font.SysFont("segoeui", 15)
        self.font = pygame.font.SysFont("segoeui", 18)
        self.font_bold = pygame.font.SysFont("segoeui", 18, bold=True)
        self.font_medium = pygame.font.SysFont("segoeui", 26, bold=True)
        self.font_large = pygame.font.SysFont("segoeui", 52, bold=True)

        self.electrons: list[ElectronParticle] = []
        self.cloud_points: list[CloudPoint] = []
        self.rebuild_particles()

    @property
    def current_element(self) -> Element:
        return ELEMENTS[self.current_index]

    @property
    def current_mode(self) -> str:
        return self.modes[self.mode_index]

    @property
    def electron_count(self) -> int:
        return int(clamp(self.current_element.atomic_number - self.ion_charge, 0, 20))

    @property
    def neutron_count(self) -> int:
        base = self.current_element.neutron_count + self.neutron_delta
        return int(clamp(base, 0, 30))

    @property
    def active_shells(self) -> tuple[int, ...]:
        return shells_for_electrons(self.electron_count)

    def rebuild_particles(self) -> None:
        self.create_electrons()
        self.create_cloud_points()
        self.measurements.clear()

    def create_electrons(self) -> None:
        element = self.current_element
        self.electrons.clear()
        rng = random.Random(element.atomic_number * 137 + self.electron_count * 17)
        palette = (
            ELECTRON,
            mix(element.color, (255, 255, 255), 0.25),
            mix(element.color, ACCENT, 0.35),
        )

        for shell_index, count in enumerate(self.active_shells):
            for slot in range(count):
                spacing = math.tau / max(1, count)
                jitter = rng.uniform(-0.12, 0.12)
                angle = spacing * slot + jitter
                direction = -1 if (slot + shell_index) % 2 else 1
                angular_speed = direction * (0.72 / (shell_index + 1) + rng.uniform(0.02, 0.08))
                self.electrons.append(
                    ElectronParticle(shell_index, slot, angle, angular_speed, palette[slot % len(palette)])
                )

    def create_cloud_points(self) -> None:
        element = self.current_element
        self.cloud_points.clear()
        rng = random.Random(element.atomic_number * 4001 + self.electron_count * 31)

        for label, count, orbital_type, principal in orbital_occupancy(self.electron_count):
            point_count = 90 * count
            base = 28 + principal * 36

            if orbital_type == "s":
                for _ in range(point_count):
                    angle = rng.uniform(0, math.tau)
                    ring_bias = 1.0 + 0.28 * math.sin(principal * rng.uniform(0, math.tau))
                    radius = abs(rng.gauss(base * ring_bias, 16 + principal * 6))
                    self.cloud_points.append(
                        CloudPoint(
                            radius * math.cos(angle),
                            radius * math.sin(angle),
                            mix(element.color, ELECTRON, rng.random() * 0.45),
                            rng.choice((1, 1, 2)),
                            rng.uniform(0, math.tau),
                        )
                    )
            else:
                axes = (0.0, math.pi / 2, math.pi / 4)
                for i in range(point_count):
                    axis = axes[i % len(axes)]
                    side = -1 if rng.random() < 0.5 else 1
                    center = base * 1.35 * side
                    along = rng.gauss(center, 22 + principal * 5)
                    across = rng.gauss(0, 11 + principal * 3)
                    x = along * math.cos(axis) - across * math.sin(axis)
                    y = along * math.sin(axis) + across * math.cos(axis)
                    self.cloud_points.append(
                        CloudPoint(
                            x,
                            y,
                            mix(element.color, (255, 255, 255), rng.random() * 0.35),
                            rng.choice((1, 1, 2)),
                            rng.uniform(0, math.tau),
                        )
                    )

    def set_element(self, index: int) -> None:
        self.current_index = index % len(ELEMENTS)
        self.ion_charge = 0
        self.neutron_delta = 0
        self.rebuild_particles()

    def cycle_mode(self, delta: int = 1) -> None:
        self.mode_index = (self.mode_index + delta) % len(self.modes)

    def adjust_charge(self, delta: int) -> None:
        element = self.current_element
        self.ion_charge = int(clamp(self.ion_charge + delta, -3, element.atomic_number))
        self.rebuild_particles()

    def adjust_neutrons(self, delta: int) -> None:
        base = self.current_element.neutron_count
        new_total = int(clamp(base + self.neutron_delta + delta, 0, 30))
        self.neutron_delta = new_total - base

    def cloud_screen_position(self, point: CloudPoint) -> tuple[float, float]:
        rect = self.simulation_rect()
        spin = self.time * 0.07
        x = point.x * math.cos(spin) - point.y * math.sin(spin)
        y = point.x * math.sin(spin) + point.y * math.cos(spin)
        return rect.centerx + x, rect.centery + 4 + y

    def probability_at(self, x: float, y: float) -> float:
        if not self.cloud_points:
            return 0.0

        density = 0.0
        for point in self.cloud_points[:: max(1, len(self.cloud_points) // 450)]:
            px, py = self.cloud_screen_position(point)
            distance_sq = (px - x) ** 2 + (py - y) ** 2
            density += math.exp(-distance_sq / 1500.0)
        return clamp(density / 18.0, 0.0, 1.0)

    def measure_cloud_at(self, pos: tuple[int, int]) -> None:
        if self.current_mode != "Cloud" or not self.simulation_rect().collidepoint(pos):
            return

        probability = self.probability_at(float(pos[0]), float(pos[1]))
        self.measurements.append(Measurement(float(pos[0]), float(pos[1]), probability))
        self.measurements = self.measurements[-8:]

    def sample_cloud_measurement(self) -> None:
        if not self.cloud_points:
            return

        point = random.choice(self.cloud_points)
        x, y = self.cloud_screen_position(point)
        self.measurements.append(Measurement(x, y, self.probability_at(x, y)))
        self.measurements = self.measurements[-8:]

    def trigger_transition(self) -> None:
        high = max(self.excited_level, self.transition_target + 1)
        low = min(self.transition_target, high - 1)
        energy_ev, wavelength_nm = hydrogenic_transition(self.current_element.atomic_number, high, low)
        color = wavelength_to_rgb(wavelength_nm)
        rect = self.simulation_rect()
        y = rect.y + 82 + (6 - high) * 58
        self.photons.append(
            Photon(
                x=rect.x + 156,
                y=y,
                vx=250 + 18 * high,
                vy=-28 + 16 * (low - 1),
                color=color,
                wavelength_nm=wavelength_nm,
                energy_ev=energy_ev,
            )
        )
        self.photons = self.photons[-10:]

    def handle_key(self, key: int) -> None:
        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.set_element(self.current_index + 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.set_element(self.current_index - 1)
        elif key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_m:
            self.cycle_mode()
        elif key == pygame.K_b:
            self.mode_index = 0
        elif key == pygame.K_c:
            self.mode_index = 1
        elif key == pygame.K_s:
            self.mode_index = 2
        elif key == pygame.K_e:
            self.mode_index = 3
        elif key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
            self.speed_scale = clamp(self.speed_scale + 0.15, 0.15, 3.0)
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self.speed_scale = clamp(self.speed_scale - 0.15, 0.15, 3.0)
        elif key == pygame.K_LEFTBRACKET:
            self.adjust_charge(-1)
        elif key == pygame.K_RIGHTBRACKET:
            self.adjust_charge(1)
        elif key == pygame.K_COMMA:
            self.adjust_neutrons(-1)
        elif key == pygame.K_PERIOD:
            self.adjust_neutrons(1)
        elif key == pygame.K_x:
            self.sample_cloud_measurement()
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.trigger_transition()
        elif key == pygame.K_UP:
            self.excited_level = int(clamp(self.excited_level + 1, 2, 6))
            self.transition_target = min(self.transition_target, self.excited_level - 1)
        elif key == pygame.K_DOWN:
            self.excited_level = int(clamp(self.excited_level - 1, 2, 6))
            self.transition_target = min(self.transition_target, self.excited_level - 1)
        elif key == pygame.K_t:
            self.transition_target += 1
            if self.transition_target >= self.excited_level:
                self.transition_target = 1
        elif key == pygame.K_r:
            self.rebuild_particles()
            self.photons.clear()
        elif key == pygame.K_h:
            self.show_help = not self.show_help
        elif pygame.K_1 <= key <= pygame.K_9:
            self.set_element(key - pygame.K_1)
        elif key == pygame.K_0:
            self.set_element(9)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, index in self.mode_buttons:
                    if rect.collidepoint(event.pos):
                        self.mode_index = index
                        break
                else:
                    self.measure_cloud_at(event.pos)
                    for rect, index in self.periodic_buttons:
                        if rect.collidepoint(event.pos):
                            self.set_element(index)
                            break

    def update(self, dt: float) -> None:
        if self.paused:
            return

        self.time += dt * self.speed_scale
        for electron in self.electrons:
            electron.angle += electron.angular_speed * dt * self.speed_scale

        for measurement in self.measurements:
            measurement.age += dt
        self.measurements = [measurement for measurement in self.measurements if measurement.age < 5.0]

        for photon in self.photons:
            photon.age += dt
            photon.x += photon.vx * dt * self.speed_scale
            photon.y += photon.vy * dt * self.speed_scale
        self.photons = [photon for photon in self.photons if photon.age < photon.life]

    def draw_background(self) -> None:
        self.screen.fill(BACKGROUND)
        width, height = self.screen.get_size()
        for y in range(0, height, 4):
            amount = y / height
            color = mix((15, 18, 23), (27, 29, 35), amount)
            pygame.draw.rect(self.screen, color, (0, y, width, 4))

        for x in range(32, width - 390, 32):
            pygame.draw.line(self.screen, (22, 27, 34), (x, 92), (x, height - 178), 1)
        for y in range(116, height - 178, 32):
            pygame.draw.line(self.screen, (22, 27, 34), (28, y), (width - 405, y), 1)

    def simulation_rect(self) -> pygame.Rect:
        return pygame.Rect(24, 104, 748, 520)

    def nucleus_center(self) -> tuple[int, int]:
        rect = self.simulation_rect()
        return rect.centerx, rect.centery + 4

    def shell_radius(self, shell_index: int) -> int:
        return 70 + shell_index * 54

    def draw_header(self) -> None:
        element = self.current_element
        self.mode_buttons.clear()
        draw_text(self.screen, self.font_medium, "Atom Simulation", (24, 16))
        draw_text(
            self.screen,
            self.font_small,
            f"{element.name} ({element.symbol})  |  {ion_label(self.ion_charge)}  |  {isotope_label(element, self.neutron_count)}",
            (26, 52),
            MUTED,
        )

        nav_x = 388
        nav_y = 20
        tab_w = 106
        tab_h = 40
        for index, mode in enumerate(self.modes):
            rect = pygame.Rect(nav_x + index * (tab_w + 8), nav_y, tab_w, tab_h)
            selected = index == self.mode_index
            fill = mix(element.color, (23, 27, 33), 0.35) if selected else SURFACE_ALT
            border = mix(element.color, (255, 255, 255), 0.25) if selected else BORDER
            pygame.draw.rect(self.screen, fill, rect, border_radius=8)
            pygame.draw.rect(self.screen, border, rect, 2 if selected else 1, border_radius=8)
            draw_centered_text(self.screen, self.font_bold if selected else self.font, mode, rect.center, TEXT if selected else MUTED)
            self.mode_buttons.append((rect, index))

        speed_rect = pygame.Rect(850, 25, 112, 30)
        pygame.draw.rect(self.screen, SURFACE_ALT, speed_rect, border_radius=7)
        draw_centered_text(self.screen, self.font_small, f"{self.speed_scale:.2f}x speed", speed_rect.center, MUTED)

        status = "Paused" if self.paused else "Running"
        pill = pygame.Rect(1056, 24, 100, 32)
        pygame.draw.rect(self.screen, GOOD if not self.paused else ACCENT, pill, border_radius=8)
        draw_centered_text(self.screen, self.font_bold, status, pill.center, (15, 18, 22))

    def draw_nucleus(self) -> None:
        element = self.current_element
        cx, cy = self.nucleus_center()
        radius = 34
        pygame.draw.circle(self.screen, mix(element.color, (255, 255, 255), 0.18), (cx, cy), radius + 3)
        pygame.draw.circle(self.screen, (36, 41, 48), (cx, cy), radius + 1)

        particles = [PROTON] * element.atomic_number + [NEUTRON] * self.neutron_count
        rng = random.Random(element.atomic_number * 311)
        for i, color in enumerate(particles[:44]):
            local_radius = radius * math.sqrt(rng.random()) * 0.82
            angle = rng.uniform(0, math.tau) + i * 0.37
            px = cx + int(local_radius * math.cos(angle))
            py = cy + int(local_radius * math.sin(angle))
            pygame.draw.circle(self.screen, color, (px, py), 4)

        draw_centered_text(self.screen, self.font_medium, element.symbol, (cx, cy - 2))
        draw_centered_text(self.screen, self.font_small, f"Z={element.atomic_number}", (cx, cy + 25), MUTED)

    def draw_shell_model(self) -> None:
        element = self.current_element
        cx, cy = self.nucleus_center()
        rect = self.simulation_rect()
        draw_panel(self.screen, rect, SURFACE, BORDER)

        for shell_index, count in enumerate(self.active_shells):
            radius = self.shell_radius(shell_index)
            shell_color = mix(ORBIT, element.color, 0.2 + shell_index * 0.08)
            pygame.draw.circle(self.screen, shell_color, (cx, cy), radius, 1)
            draw_text(
                self.screen,
                self.font_small,
                f"n={shell_index + 1}  e={count}",
                (cx + radius + 8, cy - 8),
                MUTED,
            )

        for electron in self.electrons:
            radius = self.shell_radius(electron.shell_index)
            ex = cx + radius * math.cos(electron.angle)
            ey = cy + radius * math.sin(electron.angle)
            pygame.draw.circle(self.screen, mix(electron.color, (255, 255, 255), 0.45), (int(ex), int(ey)), 8)
            pygame.draw.circle(self.screen, electron.color, (int(ex), int(ey)), 5)

        self.draw_nucleus()
        self.draw_simulation_caption("Bohr-style shell view keeps the original moving electrons while ion controls change the electron count.")

    def draw_cloud_model(self) -> None:
        element = self.current_element
        rect = self.simulation_rect()
        cx, cy = self.nucleus_center()
        draw_panel(self.screen, rect, (12, 15, 20), BORDER)

        cloud = pygame.Surface(rect.size, pygame.SRCALPHA)
        spin = self.time * 0.07
        pulse = 0.75 + 0.25 * math.sin(self.time * 2.0)
        local_center = (rect.width // 2, rect.height // 2 + 4)

        for point in self.cloud_points:
            x = point.x * math.cos(spin) - point.y * math.sin(spin)
            y = point.x * math.sin(spin) + point.y * math.cos(spin)
            alpha = int(36 + 75 * (0.5 + 0.5 * math.sin(self.time * 2.4 + point.phase)) * pulse)
            pygame.draw.circle(
                cloud,
                (*point.color, alpha),
                (int(local_center[0] + x), int(local_center[1] + y)),
                point.size,
            )

        self.screen.blit(cloud, rect.topleft)

        for label, count, orbital_type, principal in orbital_occupancy(self.electron_count):
            if orbital_type == "s":
                radius = 28 + principal * 36
                pygame.draw.circle(self.screen, (58, 68, 82), (cx, cy), radius, 1)

        self.draw_nucleus()
        labels = ", ".join(f"{label}{count}" for label, count, _, _ in orbital_occupancy(self.electron_count)) or "no bound electrons"
        draw_text(self.screen, self.font_bold, f"Orbitals: {labels}", (rect.x + 18, rect.y + 16), TEXT)

        for measurement in self.measurements:
            fade = 1.0 - measurement.age / 5.0
            radius = int(12 + measurement.age * 28)
            color = mix(ACCENT, GOOD, measurement.probability)
            mx, my = int(measurement.x), int(measurement.y)
            pygame.draw.circle(self.screen, color, (mx, my), max(3, radius), 1)
            pygame.draw.line(self.screen, color, (mx - 9, my), (mx + 9, my), 1)
            pygame.draw.line(self.screen, color, (mx, my - 9), (mx, my + 9), 1)
            label = f"P~{measurement.probability:.2f}"
            rendered = self.font_small.render(label, True, mix(MUTED, color, fade))
            self.screen.blit(rendered, (mx + 12, my - 8))

        self.draw_simulation_caption("Cloud view now supports measurement: click in the cloud or press X to sample likely electron locations.")

    def draw_spectrum_model(self) -> None:
        element = self.current_element
        rect = self.simulation_rect()
        draw_panel(self.screen, rect, (9, 11, 15), BORDER)

        title_y = rect.y + 18
        draw_text(self.screen, self.font_bold, f"{element.name} representative visible emission lines", (rect.x + 18, title_y))

        spectrum_rect = pygame.Rect(rect.x + 38, rect.y + 128, rect.width - 76, 135)
        pygame.draw.rect(self.screen, (2, 3, 5), spectrum_rect, border_radius=6)

        for x in range(spectrum_rect.width):
            nm = 380 + (x / spectrum_rect.width) * 400
            color = wavelength_to_rgb(nm)
            pygame.draw.line(
                self.screen,
                tuple(max(0, c // 4) for c in color),
                (spectrum_rect.x + x, spectrum_rect.y),
                (spectrum_rect.x + x, spectrum_rect.bottom),
            )

        if element.spectrum_nm:
            for nm in element.spectrum_nm:
                line_x = spectrum_rect.x + int((nm - 380) / 400 * spectrum_rect.width)
                color = wavelength_to_rgb(nm)
                pygame.draw.line(self.screen, mix(color, (255, 255, 255), 0.35), (line_x, spectrum_rect.y - 5), (line_x, spectrum_rect.bottom + 5), 3)
                draw_centered_text(self.screen, self.font_small, f"{nm:.1f}", (line_x, spectrum_rect.bottom + 22), MUTED)
        else:
            draw_centered_text(
                self.screen,
                self.font,
                "No representative visible lines saved for this element yet.",
                spectrum_rect.center,
                MUTED,
            )

        for nm in (400, 500, 600, 700):
            x = spectrum_rect.x + int((nm - 380) / 400 * spectrum_rect.width)
            pygame.draw.line(self.screen, FAINT, (x, spectrum_rect.bottom + 36), (x, spectrum_rect.bottom + 45), 1)
            draw_centered_text(self.screen, self.font_small, f"{nm} nm", (x, spectrum_rect.bottom + 58), MUTED)

        mini_center = (rect.x + 115, rect.y + 398)
        pygame.draw.circle(self.screen, mix(element.color, (255, 255, 255), 0.1), mini_center, 46)
        draw_centered_text(self.screen, self.font_large, element.symbol, mini_center)

        lines = wrap_text(
            "Spectrum mode adds a research-data angle: atoms have element-specific transition lines, so the visual model can connect structure to observation.",
            self.font,
            445,
        )
        y = rect.y + 360
        for line in lines:
            draw_text(self.screen, self.font, line, (rect.x + 190, y), MUTED)
            y += 24

        self.draw_simulation_caption("Line wavelengths are representative classroom references, not a calibration-grade spectrometer.")

    def draw_energy_model(self) -> None:
        element = self.current_element
        rect = self.simulation_rect()
        draw_panel(self.screen, rect, (11, 14, 19), BORDER)

        high = max(self.excited_level, self.transition_target + 1)
        low = min(self.transition_target, high - 1)
        energy_ev, wavelength_nm = hydrogenic_transition(element.atomic_number, high, low)
        band = wavelength_band(wavelength_nm)
        color = wavelength_to_rgb(wavelength_nm)

        draw_text(self.screen, self.font_bold, "Hydrogen-like transition lab", (rect.x + 18, rect.y + 16), TEXT)
        draw_text(
            self.screen,
            self.font_small,
            f"Using Z={element.atomic_number}; exact for one-electron atoms/ions, approximate as a teaching model for neutral atoms.",
            (rect.x + 18, rect.y + 43),
            MUTED,
        )

        level_x1 = rect.x + 150
        level_x2 = rect.x + 560
        y_for_n: dict[int, int] = {}

        for n in range(1, 7):
            y = rect.y + 82 + (6 - n) * 58
            y_for_n[n] = y
            energy = -13.605693 * element.atomic_number * element.atomic_number / (n * n)
            selected = n in (high, low)
            line_color = mix(color, (255, 255, 255), 0.18) if selected else FAINT
            width = 4 if selected else 2
            pygame.draw.line(self.screen, line_color, (level_x1, y), (level_x2, y), width)
            draw_text(self.screen, self.font_small, f"n={n}", (level_x1 - 48, y - 9), TEXT if selected else MUTED)
            draw_text(self.screen, self.font_small, f"{energy:.2f} eV", (level_x2 + 18, y - 9), MUTED)

        electron_y = y_for_n[high]
        electron_x = level_x1 + 52 + 8 * math.sin(self.time * 3.0)
        pygame.draw.circle(self.screen, mix(ELECTRON, color, 0.28), (int(electron_x), electron_y), 10)
        pygame.draw.circle(self.screen, ELECTRON, (int(electron_x), electron_y), 5)

        arrow_x = level_x1 + 235
        pygame.draw.line(self.screen, color, (arrow_x, y_for_n[high]), (arrow_x, y_for_n[low]), 3)
        direction = -1 if y_for_n[low] < y_for_n[high] else 1
        pygame.draw.polygon(
            self.screen,
            color,
            (
                (arrow_x, y_for_n[low]),
                (arrow_x - 8, y_for_n[low] + 14 * direction),
                (arrow_x + 8, y_for_n[low] + 14 * direction),
            ),
        )

        info_rect = pygame.Rect(rect.x + 34, rect.bottom - 132, rect.width - 68, 82)
        pygame.draw.rect(self.screen, PANEL_ALT, info_rect, border_radius=8)
        pygame.draw.rect(self.screen, (58, 68, 82), info_rect, 1, border_radius=8)
        draw_text(self.screen, self.font_bold, f"n={high} -> n={low}", (info_rect.x + 18, info_rect.y + 14), TEXT)
        draw_text(self.screen, self.font, f"{energy_ev:.3f} eV photon", (info_rect.x + 150, info_rect.y + 13), TEXT)
        draw_text(self.screen, self.font, f"{wavelength_nm:.1f} nm ({band})", (info_rect.x + 360, info_rect.y + 13), mix(color, (255, 255, 255), 0.25))
        draw_text(self.screen, self.font_small, "Up/Down selects excited level, T changes target level, Enter emits photons.", (info_rect.x + 18, info_rect.y + 49), MUTED)

        for photon in self.photons:
            fade = 1.0 - photon.age / photon.life
            alpha_color = mix(BACKGROUND, photon.color, fade)
            pygame.draw.circle(self.screen, alpha_color, (int(photon.x), int(photon.y)), 7)
            pygame.draw.circle(self.screen, mix(alpha_color, (255, 255, 255), 0.4), (int(photon.x), int(photon.y)), 3)
            label = f"{photon.wavelength_nm:.0f} nm"
            draw_text(self.screen, self.font_small, label, (int(photon.x) + 12, int(photon.y) - 8), MUTED)

        self.draw_simulation_caption("Energy mode turns spectra into a cause-and-effect transition model instead of a static color strip.")

    def draw_simulation_caption(self, text: str) -> None:
        rect = self.simulation_rect()
        lines = wrap_text(text, self.font_small, rect.width - 36)
        y = rect.bottom - 44
        for line in lines:
            draw_text(self.screen, self.font_small, line, (rect.x + 18, y), MUTED)
            y += 18

    def draw_info_panel(self) -> None:
        element = self.current_element
        rect = pygame.Rect(792, 104, 364, 520)
        draw_panel(self.screen, rect, PANEL, BORDER)

        badge = pygame.Rect(rect.x + 22, rect.y + 20, 78, 78)
        pygame.draw.ellipse(self.screen, mix(element.color, (255, 255, 255), 0.08), badge)
        pygame.draw.ellipse(self.screen, element.color, badge, 2)
        draw_centered_text(self.screen, self.font_large, element.symbol, badge.center, TEXT)

        draw_text(self.screen, self.font_medium, element.name, (rect.x + 118, rect.y + 22))
        detail_lines = wrap_text(f"{element.category} | {ion_label(self.ion_charge)} | {isotope_label(element, self.neutron_count)}", self.font_small, 214)
        y = rect.y + 58
        for line in detail_lines[:2]:
            draw_text(self.screen, self.font_small, line, (rect.x + 120, y), MUTED)
            y += 19

        isotope_state = "common isotope"
        if self.neutron_delta < 0:
            isotope_state = "neutron-poor"
        elif self.neutron_delta > 0:
            isotope_state = "neutron-rich"
        rows = (
            ("Atomic #", str(element.atomic_number)),
            ("Isotope", isotope_label(element, self.neutron_count)),
            ("Nucleus", f"{element.atomic_number}p / {self.neutron_count}n"),
            ("Charge", ion_label(self.ion_charge)),
            ("Electrons", str(self.electron_count)),
            ("Shells", "-".join(str(shell) for shell in self.active_shells)),
            ("Valence", str(self.active_shells[-1])),
            ("State", isotope_state),
        )

        col_gap = 10
        card_w = (rect.width - 44 - col_gap) // 2
        card_h = 46
        start_y = rect.y + 112
        for index, (label, value) in enumerate(rows):
            col = index % 2
            row = index // 2
            card = pygame.Rect(rect.x + 18 + col * (card_w + col_gap), start_y + row * 54, card_w, card_h)
            pygame.draw.rect(self.screen, PANEL_ALT, card, border_radius=7)
            pygame.draw.rect(self.screen, (46, 53, 62), card, 1, border_radius=7)
            draw_text(self.screen, self.font_small, label, (card.x + 10, card.y + 5), MUTED)
            draw_fit_right(
                self.screen,
                (self.font_bold, self.font_small),
                value,
                card.right - 10,
                card.y + 23,
                TEXT,
                card.width - 20,
            )

        note_y = rect.y + 334
        draw_text(self.screen, self.font_bold, "Element note", (rect.x + 18, note_y), TEXT)
        for index, line in enumerate(wrap_text(element.note, self.font_small, rect.width - 36)[:2]):
            draw_text(self.screen, self.font_small, line, (rect.x + 18, note_y + 26 + index * 18), MUTED)

        draw_text(self.screen, self.font_bold, "Shortcuts", (rect.x + 18, rect.bottom - 104), TEXT)
        chips = [
            "Mode B/C/S/E",
            "Elem A/D",
            "Ion [ ]",
            "N ,/.",
            "P Click/X",
            "E Enter/T",
        ]
        chip_w = (rect.width - 36 - 16) // 3
        chip_h = 28
        chip_y = rect.bottom - 70
        for index, label in enumerate(chips):
            col = index % 3
            row = index // 3
            chip = pygame.Rect(rect.x + 18 + col * (chip_w + 8), chip_y + row * 32, chip_w, chip_h)
            pygame.draw.rect(self.screen, SURFACE_ALT, chip, border_radius=7)
            draw_centered_text(self.screen, self.font_small, label, chip.center, TEXT)

    def draw_periodic_picker(self) -> None:
        self.periodic_buttons.clear()
        base = pygame.Rect(24, 648, 1132, 144)
        draw_panel(self.screen, base, PANEL, BORDER)
        draw_text(self.screen, self.font_bold, "First 20 elements", (base.x + 18, base.y + 18), TEXT)
        draw_text(self.screen, self.font_small, "Click tiles or use keys.", (base.x + 18, base.y + 48), MUTED)

        selected = self.current_element
        selected_rect = pygame.Rect(base.x + 18, base.y + 82, 206, 38)
        pygame.draw.rect(self.screen, SURFACE_ALT, selected_rect, border_radius=7)
        draw_text(self.screen, self.font_small, "Selected", (selected_rect.x + 12, selected_rect.y + 10), MUTED)
        draw_fit_right(
            self.screen,
            (self.font_bold, self.font_small),
            f"{selected.atomic_number} {selected.symbol} {selected.name}",
            selected_rect.right - 12,
            selected_rect.y + 9,
            TEXT,
            122,
        )

        tile_w = 58
        tile_h = 42
        gap = 6
        start_x = base.x + 258
        start_y = base.y + 25

        for i, element in enumerate(ELEMENTS):
            col = i % 10
            row = i // 10
            rect = pygame.Rect(start_x + col * (tile_w + gap), start_y + row * (tile_h + 13), tile_w, tile_h)
            is_selected = i == self.current_index
            fill = mix(element.color, (24, 28, 34), 0.72 if not is_selected else 0.12)
            border = element.color if is_selected else (60, 68, 78)
            pygame.draw.rect(self.screen, fill, rect, border_radius=6)
            pygame.draw.rect(self.screen, border, rect, 2 if is_selected else 1, border_radius=6)
            draw_text(self.screen, self.font_small, str(element.atomic_number), (rect.x + 6, rect.y + 4), (20, 24, 30) if is_selected else MUTED)
            draw_centered_text(self.screen, self.font_bold, element.symbol, (rect.centerx, rect.centery + 8), TEXT)
            self.periodic_buttons.append((rect, i))

    def draw_help_overlay(self) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.screen.blit(overlay, (0, 0))

        rect = pygame.Rect(196, 82, 708, 560)
        pygame.draw.rect(self.screen, (28, 32, 38), rect, border_radius=10)
        pygame.draw.rect(self.screen, (72, 82, 96), rect, 1, border_radius=10)
        draw_text(self.screen, self.font_medium, "Help", (rect.x + 28, rect.y + 24))

        help_lines = [
            "Shell model: animated shell electrons, preserving the original app idea.",
            "Cloud model: probability-inspired orbital clouds with s and p shapes plus measurement.",
            "Spectrum model: representative visible emission lines for selected elements.",
            "Energy model: hydrogen-like transitions with emitted photons and wavelength math.",
            "",
            "Keys: 1-4 keep Hydrogen, Helium, Lithium, Beryllium from the old version.",
            "Keys: 1-9 and 0 select the first ten elements. Use Left/Right for all 20.",
            "M cycles views. B, C, S, and E jump to Shell, Cloud, Spectrum, and Energy.",
            "[] changes ion charge. Comma/period changes neutron count.",
            "Cloud: click inside the cloud or press X to add probability measurements.",
            "Energy: Up/Down picks excited level, T picks lower level, Enter emits.",
            "Space pauses. +/- changes animation speed. R regenerates the view.",
            "",
            "The cloud and multi-electron energy model are educational approximations.",
        ]

        y = rect.y + 78
        for line in help_lines:
            if line:
                draw_text(self.screen, self.font, line, (rect.x + 30, y), MUTED)
            y += 27

        draw_text(self.screen, self.font_small, "Press H to close.", (rect.x + 30, rect.bottom - 42), ACCENT)

    def draw(self) -> None:
        self.draw_background()
        self.draw_header()

        if self.current_mode == "Shell":
            self.draw_shell_model()
        elif self.current_mode == "Cloud":
            self.draw_cloud_model()
        elif self.current_mode == "Spectrum":
            self.draw_spectrum_model()
        else:
            self.draw_energy_model()

        self.draw_info_panel()
        self.draw_periodic_picker()

        if self.show_help:
            self.draw_help_overlay()

        pygame.display.flip()

    def run(self) -> None:
        smoke = os.environ.get("ATOM_SIM_SMOKE") == "1"
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
            self.frame_count += 1

            if smoke and self.frame_count >= 3:
                self.running = False

        pygame.quit()


def main() -> None:
    AtomSimulation().run()


if __name__ == "__main__":
    main()

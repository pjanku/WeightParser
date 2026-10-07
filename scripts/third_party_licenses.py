"""Vygeneruje THIRD_PARTY_LICENSES.txt pro knihovny zabalené do Vazenky.exe.

Texty licencí se čtou z nainstalovaných balíčků, takže vždy odpovídají
verzím, které PyInstaller skutečně zabalil.
"""

import sys
import sysconfig
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

# Balíčky, které končí uvnitř exe (ne build-time závislosti PyInstalleru).
# PyInstaller je tu kvůli bootloaderu, který je součástí exe.
BUNDLED_PACKAGES: tuple[str, ...] = ("pypdf", "openpyxl", "et_xmlfile", "pyinstaller")

LICENSE_MARKERS: tuple[str, ...] = ("LICEN", "COPYING")
SEPARATOR = "=" * 79


class LicenseCollectionError(Exception):
    """Licenci některé ze zabalených komponent se nepodařilo najít."""


def package_section(name: str) -> str:
    """Vrátí sekci s názvem, verzí a texty licencí jednoho balíčku."""
    try:
        dist = distribution(name)
    except PackageNotFoundError as exc:
        raise LicenseCollectionError(f"Balíček {name} není nainstalovaný.") from exc

    license_files = sorted(
        (
            file
            for file in dist.files or []
            if ".dist-info" in str(file)
            and any(marker in file.name.upper() for marker in LICENSE_MARKERS)
        ),
        key=str,
    )
    if not license_files:
        raise LicenseCollectionError(f"Balíček {name} neobsahuje soubor s licencí.")

    texts = [
        Path(dist.locate_file(file)).read_text(encoding="utf-8")
        for file in license_files
    ]
    header = f"{dist.metadata['Name']} {dist.version}"
    return "\n".join([SEPARATOR, header, SEPARATOR, "", *texts])


def python_section() -> str:
    """Vrátí licenci Python runtime (na Windows obsahuje i Tcl/Tk, OpenSSL apod.)."""
    candidates = (
        Path(sys.base_prefix) / "LICENSE.txt",
        Path(sysconfig.get_paths()["stdlib"]) / "LICENSE.txt",
    )
    for path in candidates:
        if path.is_file():
            header = f"Python {sys.version.split()[0]}"
            return "\n".join(
                [SEPARATOR, header, SEPARATOR, "", path.read_text(encoding="utf-8")]
            )
    raise LicenseCollectionError("Soubor LICENSE.txt Pythonu nebyl nalezen.")


def main() -> None:
    """Zapíše THIRD_PARTY_LICENSES.txt do cesty z argumentu (výchozí aktuální složka)."""
    output = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path("THIRD_PARTY_LICENSES.txt")
    )
    intro = (
        "Vazenky.exe obsahuje následující software třetích stran.\n"
        "Níže jsou uvedeny jejich licence a copyright.\n"
    )
    sections = [
        intro,
        *(package_section(name) for name in BUNDLED_PACKAGES),
        python_section(),
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n\n".join(sections), encoding="utf-8")
    print(f"Zapsáno: {output}")


if __name__ == "__main__":
    main()

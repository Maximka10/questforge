from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.tools'
PACKWIZ = TOOLS / 'packwiz'
PACKWIZ_ZIP = TOOLS / 'packwiz.zip'
PACKWIZ_URL = 'https://nightly.link/packwiz/packwiz/workflows/go/main/Linux%2064-bit%20x86.zip'
FORGE_URL = 'https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.23/forge-1.20.1-47.4.23-installer.jar'
FORGE_SHA1 = 'ed31ce02ac69176f34353235cb2508d5a0f1e0881'
FORGE_INSTALLER = TOOLS / 'forge-installer.jar'


def run(*args: str, cwd: Path = ROOT) -> None:
    print('+', ' '.join(args), flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f'Downloading {url}', flush=True)
    with urllib.request.urlopen(url, timeout=120) as r, dest.open('wb') as f:
        shutil.copyfileobj(r, f)


def ensure_packwiz() -> None:
    if PACKWIZ.exists():
        return
    if PACKWIZ_ZIP.exists():
        PACKWIZ_ZIP.unlink()
    download(PACKWIZ_URL, PACKWIZ_ZIP)
    extracted = TOOLS / 'packwiz-extracted'
    if extracted.exists():
        shutil.rmtree(extracted)
    extracted.mkdir(parents=True)
    with zipfile.ZipFile(PACKWIZ_ZIP) as zf:
        zf.extractall(extracted)
    candidates = list(extracted.rglob('packwiz'))
    if not candidates:
        raise RuntimeError('packwiz executable was not found in the official artifact')
    shutil.copy2(candidates[0], PACKWIZ)
    PACKWIZ.chmod(PACKWIZ.stat().st_mode | 0o111)


def install_mods() -> None:
    manifest = ROOT / 'scripts' / 'mods.txt'
    for raw in manifest.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        source, slug = [x.strip() for x in line.split('|', 1)]
        if source == 'mr':
            run(str(PACKWIZ), 'mr', 'install', slug, '-y')
        elif source == 'cf':
            run(str(PACKWIZ), 'cf', 'install', slug, '-y')
        else:
            raise RuntimeError(f'Unsupported manifest source: {source}')


def main() -> int:
    ensure_packwiz()
    run(str(PACKWIZ), '--version')
    run(str(PACKWIZ), 'init', '--reinit', '-y', '--name', 'QuestForge', '--author', 'Maximka10', '--version', '0.1.0', '--mc-version', '1.20.1', '--modloader', 'forge', '--forge-version', '47.4.23')
    install_mods()

    run(sys.executable, str(ROOT / 'scripts' / 'generate_quests.py'))
    run(str(PACKWIZ), 'refresh')
    run(str(PACKWIZ), 'modrinth', 'export', '-o', 'QuestForge.mrpack')

    download(FORGE_URL, FORGE_INSTALLER)
    actual = sha1(FORGE_INSTALLER)
    if actual != FORGE_SHA1:
        raise RuntimeError(f'Forge installer SHA1 mismatch: expected {FORGE_SHA1}, got {actual}')

    minecraft = ROOT / '.minecraft'
    if minecraft.exists():
        shutil.rmtree(minecraft)
    minecraft.mkdir()
    run('java', '-Djava.awt.headless=true', '-jar', str(FORGE_INSTALLER), '--installClient', '--targetDir', str(minecraft))

    version_dir = minecraft / 'versions' / '1.20.1-forge-47.4.23'
    if not (version_dir / '1.20.1-forge-47.4.23.json').exists():
        raise RuntimeError(f'Forge version JSON missing: {version_dir}')
    if not (version_dir / '1.20.1-forge-47.4.23.jar').exists():
        raise RuntimeError(f'Forge version JAR missing: {version_dir}')

    drop = ROOT / 'drop-in'
    if drop.exists():
        shutil.rmtree(drop)
    for rel in ('mods', 'config', 'defaultconfigs', 'kubejs', 'resourcepacks', 'shaderpacks', 'versions'):
        (drop / rel).mkdir(parents=True, exist_ok=True)

    for rel in ('mods', 'config', 'defaultconfigs', 'kubejs', 'resourcepacks', 'shaderpacks'):
        src = ROOT / rel
        if src.exists():
            shutil.copytree(src, drop / rel, dirs_exist_ok=True)
    shutil.copytree(minecraft / 'versions', drop / 'versions', dirs_exist_ok=True)

    (drop / 'INSTALL.txt').write_text(
        'QuestForge 0.1.0\n'
        'Minecraft 1.20.1\n'
        'Forge 47.4.23\n'
        'Java 17 x64\n\n'
        'Copy everything inside this folder into %APPDATA%\\.minecraft.\n'
        'The versions\\1.20.1-forge-47.4.23 folder is already included.\n'
        'The official launcher may download missing vanilla libraries/assets on first run.\n'
        'Recommended RAM: 8-10 GB.\n'
        'Start with a fresh world.\n',
        encoding='utf-8',
    )

    output = ROOT / 'QuestForge-1.20.1-Forge-47.4.23-ready.zip'
    if output.exists():
        output.unlink()
    shutil.make_archive(str(output.with_suffix('')), 'zip', ROOT, 'drop-in')
    print(f'Created {output} ({output.stat().st_size} bytes)', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

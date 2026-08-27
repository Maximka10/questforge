from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.tools'
PACKWIZ = Path(shutil.which('packwiz') or (Path.home() / 'go' / 'bin' / 'packwiz'))
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
    run('curl', '-fL', '--retry', '4', '--retry-all-errors', '--retry-delay', '2', '-A', 'Mozilla/5.0 QuestForgeBuilder/1.0', url, '-o', str(dest))


def ensure_packwiz() -> None:
    global PACKWIZ
    found = shutil.which('packwiz')
    if found:
        PACKWIZ = Path(found)
    if not PACKWIZ.exists():
        raise RuntimeError('packwiz is not installed; CI must install an official packwiz binary first')
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


def test_server() -> None:
    server = ROOT / 'server-test'
    if server.exists():
        shutil.rmtree(server)
    server.mkdir()
    installer = server / 'forge-installer.jar'
    shutil.copy2(FORGE_INSTALLER, installer)
    run('java', '-Djava.awt.headless=true', '-jar', str(installer), '--installServer', str(server))

    client_only = {
        'jei', 'embeddium', 'oculus', 'entityculling', 'controlling', 'mouse-tweaks',
        'xaeros-minimap', 'xaeros-world-map', 'appleskin'
    }
    mods_dst = server / 'mods'
    mods_dst.mkdir(exist_ok=True)
    for jar in (ROOT / 'mods').glob('*.jar'):
        name = jar.name.lower()
        if any(token in name for token in client_only):
            continue
        shutil.copy2(jar, mods_dst / jar.name)
    for rel in ('config', 'defaultconfigs', 'kubejs'):
        src = ROOT / rel
        if src.exists():
            shutil.copytree(src, server / rel, dirs_exist_ok=True)
    (server / 'eula.txt').write_text('eula=true\n', encoding='utf-8')
    (server / 'user_jvm_args.txt').touch(exist_ok=True)
    unix_args = server / 'libraries' / 'net' / 'minecraftforge' / 'forge' / '1.20.1-47.4.23' / 'unix_args.txt'
    if not unix_args.exists():
        raise RuntimeError(f'Forge server args missing: {unix_args}')

    log = server / 'server.log'
    with log.open('w', encoding='utf-8') as fh:
        proc = subprocess.Popen(
            ['java', '@user_jvm_args.txt', '@libraries/net/minecraftforge/forge/1.20.1-47.4.23/unix_args.txt', 'nogui'],
            cwd=server, stdout=fh, stderr=subprocess.STDOUT,
        )
        try:
            code = proc.wait(timeout=150)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
            code = 124
    text = log.read_text(encoding='utf-8', errors='replace')
    print(text[-12000:], flush=True)
    bad = [line for line in text.splitlines() if any(x in line for x in ('ModLoadingException', 'Exception in server tick loop', 'FATAL', 'ERROR'))]
    if bad:
        raise RuntimeError('Dedicated server reported fatal/error lines:\n' + '\n'.join(bad[-30:]))
    if code not in (0, 124):
        raise RuntimeError(f'Dedicated server exited unexpectedly with code {code}')


def main() -> int:
    TOOLS.mkdir(parents=True, exist_ok=True)
    ensure_packwiz()
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
    if not (version_dir / '1.20.1-forge-47.4.23.json').exists() or not (version_dir / '1.20.1-forge-47.4.23.jar').exists():
        raise RuntimeError(f'Forge client profile incomplete: {version_dir}')

    test_server()

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
        'QuestForge 0.1.0\nMinecraft 1.20.1\nForge 47.4.23\nJava 17 x64\n\n'
        'Copy everything inside this folder into %APPDATA%\\.minecraft.\n'
        'The versions\\1.20.1-forge-47.4.23 folder is already included.\n'
        'The official launcher may download missing vanilla libraries/assets on first run.\n'
        'Recommended RAM: 8-10 GB.\nStart with a fresh world.\n',
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

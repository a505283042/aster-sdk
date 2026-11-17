"""Public target release metadata. Contains no pins, DTS, flash or RTOS build rules."""
import json
import os
from pathlib import Path
from runtime_paths import sdk_root

ROOT = sdk_root()
API = json.loads((ROOT / "contract/api.json").read_text())
AOT_BACKENDS = API["aot_backends"]
ORIENTATIONS = {"portrait", "landscape"}


def targets():
    return {p.stem: json.loads(p.read_text()) for p in (ROOT / "targets").glob("*.json")}


def get(name=None):
    name = name or os.environ.get("ASTER_TARGET")
    all_targets = targets()
    if name not in all_targets:
        raise SystemExit("Select --target: " + ", ".join(sorted(all_targets)))
    target = all_targets[name]
    target["model"] = name
    target["console"] = os.environ.get("ASTER_CONSOLE", target["deployment"].get("console", ""))
    target["data"] = {"glob": os.environ.get("ASTER_CDC", target["deployment"].get("data_glob", ""))}
    return target


def pack_key_for(backend):
    if backend not in AOT_BACKENDS:
        raise SystemExit("Unsupported AOT backend: " + str(backend))
    return AOT_BACKENDS[backend]


def data_glob(name=None):
    return get(name)["data"]["glob"]


def hardware():
    """Firmware-authored physical boards, separate from compiler CPU targets."""
    return {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in (ROOT / 'hardware').glob('*.json')}


def get_hardware(name, target=None):
    boards = hardware()
    if name not in boards:
        raise SystemExit("Select --hardware: " + ", ".join(sorted(boards)))
    board = boards[name]
    if target and target != board['cpu']:
        raise SystemExit("--hardware " + name + " requires --target " + board['cpu'])
    selected = get(board['cpu'])
    if selected['aot_target'] != board['aot_target'] or (board.get('aot_profile') and selected.get('aot_profile') != board['aot_profile']):
        raise SystemExit("Hardware AOT profile differs from compiler target")
    for field in ('display', 'memory', 'capabilities', 'deployment', 'system', 'soc'):
        if field in board:
            selected[field] = board[field]
    selected['console'] = os.environ.get('ASTER_CONSOLE', selected['deployment'].get('console', ''))
    selected['data'] = {'glob': os.environ.get('ASTER_CDC', selected['deployment'].get('data_glob', ''))}
    selected['hardware_id'] = board['id']
    selected['board_id'] = board.get('board_id', board['id'])
    selected['hardware_name'] = board.get('name', board['id'])
    return selected

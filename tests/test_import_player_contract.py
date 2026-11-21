import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from import_contract import platform_files


class PlatformImport(unittest.TestCase):
    def test_riscv_profile_and_cpu_survive_contract_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'toolchains').mkdir()
            (root / 'toolchains/catalog.json').write_text(
                json.dumps({'boards': {'riscv': {'cpu': 'riscv32', 'aot_backend': 'riscv32'}}})
            )
            api = {
                'product': 'aster',
                'abi': '4.4.0',
                'feature_bits': {'display': 0, 'media-player': 23},
            }

            def record(board):
                return json.dumps(
                    {
                        'id': board,
                        'cpu': 'riscv',
                        'aot_target': 'riscv32',
                        'aot_profile': 'rv32-ilp32f-interruptible',
                        'system': 'esp-idf',
                    }
                ).encode()

            files = {
                'contract/api.json': json.dumps(api).encode(),
                'targets/p4.json': record('p4'),
                'targets/s31.json': record('s31'),
            }
            result = platform_files(files, root)
            target = json.loads(result['targets/riscv.json'])
            self.assertEqual(target['cpu'], 'riscv32')
            self.assertEqual(target['aot_profile'], 'rv32-ilp32f-interruptible')
            self.assertIn('media-player', target['capabilities'])
            self.assertNotIn('targets/s31.json', result)
            self.assertEqual(json.loads(result['hardware/p4.json'])['id'], 'p4')
            self.assertEqual(json.loads(result['hardware/s31.json'])['id'], 's31')
            (root / 'targets').mkdir()
            target['status'] = 'hardware-verified'
            path = root / 'targets/riscv.json'
            path.write_text(json.dumps(target))
            refreshed = json.loads(platform_files(files, root)['targets/riscv.json'])
            self.assertEqual(refreshed['status'], 'hardware-verified')
            target['aot_profile'] = 'previous-profile'
            path.write_text(json.dumps(target))
            refreshed = json.loads(platform_files(files, root)['targets/riscv.json'])
            self.assertEqual(refreshed['status'], 'build-supported')
            bad = json.loads(files['targets/s31.json'])
            bad['aot_profile'] = 'different-profile'
            files['targets/s31.json'] = json.dumps(bad).encode()
            with self.assertRaisesRegex(ValueError, 'profiles differ'):
                platform_files(files, root)

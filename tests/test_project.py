"""Exercise media-path handling independently of a local copyrighted dump."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("hotel_build",ROOT/"tools/build.py")
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class MediaPaths(unittest.TestCase):
    def test_cue_resolves_from_its_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            binary=root/"a game.bin"
            binary.write_bytes(b"test")
            cue=root/"a game.cue"
            cue.write_text('FILE "a game.bin" BINARY\n TRACK 01 MODE2/2352\n INDEX 01 00:00:00\n')
            self.assertEqual(build.disc_binary(cue),binary.resolve())

    def test_multi_file_cue_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            cue=Path(directory)/"invalid.cue"
            cue.write_text('FILE "a.bin" BINARY\nFILE "b.bin" BINARY\n')
            with self.assertRaises(ValueError):build.disc_binary(cue)

if __name__=="__main__":unittest.main()

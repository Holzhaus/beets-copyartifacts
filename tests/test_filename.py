import os
import sys

# Use unittest2 on Python < 2.7
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from helper import CopyArtifactsTestCase
from beets import config

class CopyArtifactsFilename(CopyArtifactsTestCase):
    """
    Tests to check handling of artifacts with filenames containing unicode characters
    """
    def setUp(self):
        super(CopyArtifactsFilename, self).setUp()

        self._set_import_dir()
        self.album_path = os.path.join(self.import_dir, 'the_album')
        os.makedirs(self.album_path)

        self._setup_import_session(autotag=False)

        config['copyartifacts']['extensions'] = '.file'

    def test_import_dir_with_unicode_character_in_artifact_name_copy(self):
        open(os.path.join(self.album_path, u'\xe4rtifact.file'), 'a').close()
        medium = self._create_medium(os.path.join(self.album_path, 'track_1.mp3'), 'full.mp3')
        self.import_media = [medium]

        self._run_importer()

        self.assert_in_lib_dir('Tag Artist', 'Tag Album', u'\xe4rtifact.file')

    def test_import_dir_with_unicode_character_in_artifact_name_move(self):
        config['import']['move'] = True

        open(os.path.join(self.album_path, u'\xe4rtifact.file'), 'a').close()
        medium = self._create_medium(os.path.join(self.album_path, 'track_1.mp3'), 'full.mp3')
        self.import_media = [medium]

        self._run_importer()

        self.assert_in_lib_dir('Tag Artist', 'Tag Album', u'\xe4rtifact.file')

    def test_import_dir_with_illegal_character_in_album_name(self):
        config['paths']['ext:file'] = unicode('$albumpath/$artist - $album')

        # Create import directory, illegal filename character used in the album name
        open(os.path.join(self.album_path, u'artifact.file'), 'a').close()
        medium = self._create_medium(os.path.join(self.album_path, 'track_1.mp3'),
                                     'full.mp3',
                                     'Tag Album?')
        self.import_media = [medium]

        self._run_importer()

        self.assert_in_lib_dir('Tag Artist', 'Tag Album_', u'Tag Artist - Tag Album_.file')


if __name__ == '__main__':
    unittest.main()


import os.path
import shutil
import tarfile
import tempfile

from .base import Command
from ..npm import Client


class Install(Command):
    """Download and install the vendored packages and their dependencies."""

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-y', '--yes', action='store_true', default=False,
                            dest='ignore', help="Ignore all prompts.")

    def handle(self, options):
        config = self.get_config(options)
        client = Client(config.metadata_dir, config.registry)

        if not options.ignore:
            print(f'Proceeding may erase files in {config.location_dir}.')
            confirm = input('Are you sure you want to do this? [y/N] ')
            if confirm.lower() in ['', 'n', 'no']:
                return

        # Get pacakge metadata
        for package in config.packages:
            client.get_metadata(package['package'])

        # Download archives and checksum against lockfile
        for package in config.packages:
            archive = client.get_archive(package['package'], package['version'])
            if not client.checksum(archive, package['shasum']):
                package, version = package['package'], package['version']
                raise RuntimeError(f"Checksum failure for {package}@{version}. "
                                   f"Archive and lockfile shasums do not match. ")

        # Clear existing directories in install location and untar the archives
        os.makedirs(config.location_dir, exist_ok=True)
        for package in config.packages:
            archive = client.get_archive(package['package'], package['version'])
            install = os.path.join(config.location_dir, package['package'])

            with tempfile.TemporaryDirectory() as unpack:
                with tarfile.open(archive, 'r:gz') as tar:
                    def is_within_directory(directory, target):
                        
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)
                    
                        prefix = os.path.commonprefix([abs_directory, abs_target])
                        
                        return prefix == abs_directory
                    
                    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")
                    
                        tar.extractall(path, members, numeric_owner=numeric_owner) 
                        
                    
                    safe_extract(tar, unpack)

                if os.path.exists(install):
                    shutil.rmtree(install)
                shutil.move(os.path.join(unpack, 'package'), install)

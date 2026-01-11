import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional

from snowflake.cli.api.exceptions import CliError

log = logging.getLogger(__name__)

SNOWFLAKE_PROJECT_FILE = "snowflake.yml"


@dataclass
class ProjectInfo:
    """Information about a Snowflake project."""

    name: str
    path: str

    def to_dict(self) -> dict:
        """Convert to dictionary for output."""
        return {
            "name": self.name,
            "path": self.path,
        }


class FileManager:
    """Manager for file system operations."""

    def __init__(self, root_folder: Optional[Path] = None):
        self._root_folder = root_folder

    @property
    def root_folder(self) -> Path:
        """Returns the configured root folder."""
        if self._root_folder is None:
            raise CliError(
                "Root folder not configured. Please provide a --root-folder path."
            )
        return self._root_folder

    @root_folder.setter
    def root_folder(self, value: Path) -> None:
        """Sets the root folder."""
        self._root_folder = value

    def _validate_root_folder(self) -> None:
        """Validates that the root folder exists and is a directory."""
        folder = self.root_folder
        if not folder.exists():
            raise CliError(f"Root folder does not exist: {folder}")
        if not folder.is_dir():
            raise CliError(f"Root folder path is not a directory: {folder}")

    def list_projects(self) -> Generator[dict, None, None]:
        """
        Recursively searches for Snowflake projects in the root folder.

        A Snowflake project is identified by the presence of a snowflake.yml file.

        Yields:
            Dictionary containing project information (name and path).
        """
        self._validate_root_folder()
        folder = self.root_folder

        log.debug("Searching for Snowflake projects in: %s", folder)

        # Recursively find all snowflake.yml files
        for snowflake_yml in sorted(folder.glob(f"**/{SNOWFLAKE_PROJECT_FILE}")):
            try:
                project_folder = snowflake_yml.parent
                project_info = ProjectInfo(
                    name=project_folder.name,
                    path=str(project_folder.relative_to(folder)),
                )
                log.debug("Found project: %s at %s", project_info.name, project_info.path)
                yield project_info.to_dict()
            except OSError as e:
                log.warning("Could not access project at %s: %s", snowflake_yml.parent, e)
                continue

# models.py
"""
CheatSheet Model
Handles CRUD operations for cheatsheets stored as YAML files.
Includes validation, sanitization, and atomic file operations.
"""

import os
import re
import shutil
import tempfile
from typing import Any, Dict, List, Optional

import yaml
from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate
from werkzeug.utils import secure_filename


class CategoryItemSchema(Schema):
    """Schema for validating individual items within a category."""

    command = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    component = fields.Str(allow_none=True, validate=validate.Length(max=100))

    class Meta:
        unknown = EXCLUDE


class CategorySchema(Schema):
    """Schema for validating cheatsheet categories."""

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    column = fields.Int(required=True, validate=validate.Range(min=1, max=6))
    component = fields.Str(allow_none=True, validate=validate.Length(max=100))
    items = fields.List(fields.Nested(CategoryItemSchema), required=True)

    class Meta:
        unknown = EXCLUDE


class CheatSheetSchema(Schema):
    """Schema for validating complete cheatsheet data."""

    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    columns = fields.Int(required=True, validate=validate.Range(min=1, max=6))
    categories = fields.List(fields.Nested(CategorySchema), required=True)

    class Meta:
        unknown = EXCLUDE


class CheatSheet:
    """
    CheatSheet model for managing individual cheatsheets.

    Attributes:
        name (str): Safe filename for the cheatsheet
        file_path (str): Full path to the YAML file
        data (dict): Cheatsheet content
        columns (int): Number of display columns
        categories (list): List of category dictionaries
    """

    # Allowed cheatsheet name pattern
    NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,50}$")

    def __init__(
        self,
        name: str,
        data: Optional[Dict[str, Any]] = None,
        cheatsheets_folder: str = None,
    ):
        """
        Initialize a CheatSheet instance.

        Args:
            name: Cheatsheet identifier
            data: Optional cheatsheet data dictionary
            cheatsheets_folder: Path to cheatsheets storage directory

        Raises:
            ValueError: If name contains invalid characters
        """
        self.name = self._sanitize_name(name)
        self.cheatsheets_folder = cheatsheets_folder or os.path.join(
            os.getcwd(), "cheatsheets"
        )
        self.file_path = os.path.join(self.cheatsheets_folder, f"{self.name}.yaml")
        self.data = data or {}
        self.columns = self.data.get("columns", 1)
        self.categories = self.data.get("categories", [])

    @classmethod
    def _sanitize_name(cls, name: str) -> str:
        """
        Sanitize and validate the cheatsheet name.

        Args:
            name: Raw cheatsheet name

        Returns:
            Sanitized safe name

        Raises:
            ValueError: If name is invalid or contains unsafe characters
        """
        if not name:
            raise ValueError("Cheatsheet name cannot be empty")

        # Remove any path separators and whitespace
        name = name.strip().replace("/", "").replace("\\", "").replace(" ", "-")

        # Use werkzeug's secure_filename as additional safety
        name = secure_filename(name)

        # Validate against our pattern
        if not cls.NAME_PATTERN.match(name):
            raise ValueError(
                f"Invalid cheatsheet name: '{name}'. "
                "Only alphanumeric characters, hyphens, and underscores allowed (1-50 chars)."
            )

        return name

    def validate_data(self) -> None:
        """
        Validate cheatsheet data against schema.

        Raises:
            ValidationError: If data doesn't match schema
        """
        schema = CheatSheetSchema()
        schema.load(self.data)  # Will raise ValidationError if invalid

    def load(self) -> "CheatSheet":
        """
        Load cheatsheet data from YAML file.

        Returns:
            Self for method chaining

        Raises:
            FileNotFoundError: If cheatsheet file doesn't exist
            yaml.YAMLError: If YAML parsing fails
            ValidationError: If loaded data is invalid
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"Cheat sheet '{self.name}' not found at {self.file_path}"
            )

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                # Use safe_load to prevent arbitrary code execution
                self.data = yaml.safe_load(file)

                if self.data is None:
                    self.data = {}

                # Validate loaded data
                self.validate_data()

                self.columns = self.data.get("columns", 1)
                self.categories = self.data.get("categories", [])

        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML for '{self.name}': {str(e)}")

        return self

    def save(self) -> None:
        """
        Save cheatsheet data to YAML file atomically.

        Uses atomic write pattern: write to temp file, then move to destination.
        This prevents file corruption if the process is interrupted.

        Raises:
            ValidationError: If data is invalid before saving
            IOError: If file operations fail
        """
        # Validate before saving
        self.validate_data()

        # Ensure directory exists
        os.makedirs(self.cheatsheets_folder, exist_ok=True)

        # Atomic write: write to temp file first
        fd, temp_path = tempfile.mkstemp(
            dir=self.cheatsheets_folder, prefix=f".{self.name}_", suffix=".yaml.tmp"
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as temp_file:
                yaml.safe_dump(
                    self.data,
                    temp_file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            # Atomic move (on same filesystem)
            shutil.move(temp_path, self.file_path)

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise IOError(f"Failed to save cheatsheet '{self.name}': {str(e)}")

    def delete(self) -> None:
        """
        Delete the cheatsheet file.

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Cheat sheet '{self.name}' not found")

        os.remove(self.file_path)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert cheatsheet to dictionary for API responses.

        Returns:
            Dictionary with cheatsheet data
        """
        return {
            "name": self.name,
            "columns": self.columns,
            "categories": self.categories,
            "data": self.data,
        }

    @staticmethod
    def list_all(cheatsheets_folder: str = None) -> List[str]:
        """
        List all available cheatsheets.

        Args:
            cheatsheets_folder: Path to cheatsheets directory

        Returns:
            List of cheatsheet names (without .yaml extension)
        """
        folder = cheatsheets_folder or os.path.join(os.getcwd(), "cheatsheets")

        if not os.path.exists(folder):
            return []

        cheatsheets = []
        for file_name in os.listdir(folder):
            if file_name.endswith(".yaml") and not file_name.startswith("."):
                cheatsheet_name = os.path.splitext(file_name)[0]
                cheatsheets.append(cheatsheet_name)

        return sorted(cheatsheets)

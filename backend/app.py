# app.py
"""
CheatSheeter Flask API
RESTful API for managing programming cheatsheets.
"""

import logging
import os
from functools import wraps

from config import config
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import ValidationError
from models import CheatSheet

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)
app.config.from_object(config[os.environ.get("FLASK_ENV", "development")])

# Enable CORS with specific origins in production
if app.config["ENV"] == "production":
    CORS(app, origins=app.config.get("ALLOWED_ORIGINS", ["http://localhost:8080"]))
else:
    CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Ensure the cheatsheets directory exists
os.makedirs(app.config["CHEATSHEETS_FOLDER"], exist_ok=True)


def handle_errors(f):
    """
    Decorator for consistent error handling across endpoints.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return jsonify({"error": "Invalid input", "message": str(e)}), 400
        except ValidationError as e:
            logger.warning(f"Schema validation error: {e.messages}")
            return jsonify({"error": "Validation failed", "details": e.messages}), 400
        except FileNotFoundError as e:
            logger.info(f"Resource not found: {str(e)}")
            return jsonify({"error": "Not found", "message": str(e)}), 404
        except PermissionError as e:
            logger.error(f"Permission error: {str(e)}")
            return jsonify(
                {"error": "Permission denied", "message": "Cannot access resource"}
            ), 403
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return jsonify(
                {
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                }
            ), 500

    return decorated_function


# =============================================================================
# API Routes
# =============================================================================


@app.route("/")
def index():
    """Serve the main application page."""
    return send_from_directory(app.template_folder, "index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify(
        {
            "status": "healthy",
            "version": "1.0.0",
            "cheatsheets_folder": app.config["CHEATSHEETS_FOLDER"],
        }
    ), 200


@app.route("/api/cheatsheets", methods=["GET"])
@limiter.limit("30 per minute")
@handle_errors
def get_cheatsheets():
    """
    Get list of all cheatsheets.

    Returns:
        JSON array of cheatsheet names
    """
    cheatsheets = CheatSheet.list_all(app.config["CHEATSHEETS_FOLDER"])
    logger.info(f"Retrieved {len(cheatsheets)} cheatsheets")
    return jsonify({"cheatsheets": cheatsheets}), 200


@app.route("/api/cheatsheets/<string:name>", methods=["GET"])
@limiter.limit("60 per minute")
@handle_errors
def get_cheatsheet(name):
    """
    Get a specific cheatsheet by name.

    Args:
        name: Cheatsheet identifier

    Returns:
        JSON object with cheatsheet data
    """
    cheatsheet = CheatSheet(
        name, cheatsheets_folder=app.config["CHEATSHEETS_FOLDER"]
    ).load()
    logger.info(f"Retrieved cheatsheet: {name}")
    return jsonify(cheatsheet.to_dict()), 200


@app.route("/api/cheatsheets", methods=["POST"])
@limiter.limit("10 per minute")
@handle_errors
def create_cheatsheet():
    """
    Create a new cheatsheet.

    Expected JSON body:
        {
            "name": "string",
            "data": {
                "title": "string",
                "columns": integer,
                "categories": [...]
            }
        }

    Returns:
        JSON with success message and created cheatsheet data
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    content = data.get("data", {})

    if not name:
        return jsonify({"error": "Cheat sheet name is required"}), 400

    # Check if already exists
    cheatsheet = CheatSheet(name, cheatsheets_folder=app.config["CHEATSHEETS_FOLDER"])
    if os.path.exists(cheatsheet.file_path):
        return jsonify({"error": f"Cheatsheet '{name}' already exists"}), 409

    cheatsheet.data = content
    cheatsheet.save()

    logger.info(f"Created cheatsheet: {name}")
    return jsonify(
        {
            "message": "Cheat sheet created successfully",
            "cheatsheet": cheatsheet.to_dict(),
        }
    ), 201


@app.route("/api/cheatsheets/<string:name>", methods=["PUT"])
@limiter.limit("20 per minute")
@handle_errors
def update_cheatsheet(name):
    """
    Update an existing cheatsheet.

    Args:
        name: Cheatsheet identifier

    Expected JSON body:
        {
            "data": {
                "title": "string",
                "columns": integer,
                "categories": [...]
            }
        }

    Returns:
        JSON with success message and updated cheatsheet data
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    content = data.get("data", {})

    # Load existing to ensure it exists
    cheatsheet = CheatSheet(
        name, cheatsheets_folder=app.config["CHEATSHEETS_FOLDER"]
    ).load()

    # Update with new data
    cheatsheet.data = content
    cheatsheet.columns = content.get("columns", 1)
    cheatsheet.categories = content.get("categories", [])
    cheatsheet.save()

    logger.info(f"Updated cheatsheet: {name}")
    return jsonify(
        {
            "message": "Cheat sheet updated successfully",
            "cheatsheet": cheatsheet.to_dict(),
        }
    ), 200


@app.route("/api/cheatsheets/<string:name>", methods=["DELETE"])
@limiter.limit("10 per minute")
@handle_errors
def delete_cheatsheet(name):
    """
    Delete a cheatsheet.

    Args:
        name: Cheatsheet identifier

    Returns:
        JSON with success message
    """
    cheatsheet = CheatSheet(name, cheatsheets_folder=app.config["CHEATSHEETS_FOLDER"])
    cheatsheet.delete()

    logger.info(f"Deleted cheatsheet: {name}")
    return jsonify({"message": f"Cheat sheet '{name}' deleted successfully"}), 200


# =============================================================================
# Error Handlers
# =============================================================================


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify(
        {"error": "Not found", "message": "The requested resource was not found"}
    ), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify(
        {
            "error": "Method not allowed",
            "message": "The HTTP method is not allowed for this endpoint",
        }
    ), 405


@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit exceeded."""
    return jsonify(
        {
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
        }
    ), 429


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return jsonify(
        {"error": "Internal server error", "message": "An unexpected error occurred"}
    ), 500


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", False),
    )

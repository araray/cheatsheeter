/**
 * api.js
 * API module for communicating with the CheatSheeter backend.
 * Uses jQuery AJAX for HTTP requests.
 */

(function(window) {
    'use strict';

    const API_BASE = '/api';

    /**
     * API client object
     */
    const API = {
        /**
         * Get all cheatsheets
         * @returns {Promise}
         */
        getAllCheatsheets: function() {
            return $.ajax({
                url: `${API_BASE}/cheatsheets`,
                method: 'GET',
                dataType: 'json',
                timeout: 10000
            });
        },

        /**
         * Get a specific cheatsheet by name
         * @param {string} name - Cheatsheet name
         * @returns {Promise}
         */
        getCheatsheet: function(name) {
            return $.ajax({
                url: `${API_BASE}/cheatsheets/${encodeURIComponent(name)}`,
                method: 'GET',
                dataType: 'json',
                timeout: 10000
            });
        },

        /**
         * Create a new cheatsheet
         * @param {string} name - Cheatsheet name
         * @param {Object} data - Cheatsheet data
         * @returns {Promise}
         */
        createCheatsheet: function(name, data) {
            return $.ajax({
                url: `${API_BASE}/cheatsheets`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    name: name,
                    data: data
                }),
                dataType: 'json',
                timeout: 15000
            });
        },

        /**
         * Update an existing cheatsheet
         * @param {string} name - Cheatsheet name
         * @param {Object} data - Cheatsheet data
         * @returns {Promise}
         */
        updateCheatsheet: function(name, data) {
            return $.ajax({
                url: `${API_BASE}/cheatsheets/${encodeURIComponent(name)}`,
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                    data: data
                }),
                dataType: 'json',
                timeout: 15000
            });
        },

        /**
         * Delete a cheatsheet
         * @param {string} name - Cheatsheet name
         * @returns {Promise}
         */
        deleteCheatsheet: function(name) {
            return $.ajax({
                url: `${API_BASE}/cheatsheets/${encodeURIComponent(name)}`,
                method: 'DELETE',
                dataType: 'json',
                timeout: 10000
            });
        },

        /**
         * Health check
         * @returns {Promise}
         */
        healthCheck: function() {
            return $.ajax({
                url: `${API_BASE}/health`,
                method: 'GET',
                dataType: 'json',
                timeout: 5000
            });
        }
    };

    // Expose API to global scope
    window.CheatSheetAPI = API;

})(window);

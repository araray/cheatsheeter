/**
 * theme.js
 * Theme management module for CheatSheeter.
 * Handles theme switching and persistence.
 */

(function(window, $) {
    'use strict';

    const THEME_KEY = 'cheatsheeter-theme';
    const DEFAULT_THEME = 'default';

    /**
     * Theme Manager
     */
    const ThemeManager = {
        /**
         * Initialize theme system
         */
        init: function() {
            this.loadSavedTheme();
            this.attachEventListeners();
        },

        /**
         * Load theme from localStorage
         */
        loadSavedTheme: function() {
            const savedTheme = localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
            this.applyTheme(savedTheme, false);
            $('#theme-select').val(savedTheme);
        },

        /**
         * Apply a theme
         * @param {string} themeName - Name of the theme to apply
         * @param {boolean} save - Whether to save to localStorage
         */
        applyTheme: function(themeName, save = true) {
            const themeStylesheet = $('#theme-stylesheet');
            const newHref = `/static/themes/${themeName}.css`;

            // Only reload if different
            if (themeStylesheet.attr('href') !== newHref) {
                themeStylesheet.attr('href', newHref);
            }

            // Update body class for theme-specific styling
            $('body').removeClass(function(index, className) {
                return (className.match(/(^|\s)theme-\S+/g) || []).join(' ');
            });
            $('body').addClass(`theme-${themeName}`);

            // Save to localStorage
            if (save) {
                try {
                    localStorage.setItem(THEME_KEY, themeName);
                } catch (e) {
                    console.warn('Failed to save theme to localStorage:', e);
                }
            }
        },

        /**
         * Attach event listeners for theme selection
         */
        attachEventListeners: function() {
            const self = this;

            $('#theme-select').on('change', function() {
                const selectedTheme = $(this).val();
                self.applyTheme(selectedTheme);
            });
        },

        /**
         * Get current theme name
         * @returns {string}
         */
        getCurrentTheme: function() {
            return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
        }
    };

    // Expose ThemeManager to global scope
    window.ThemeManager = ThemeManager;

})(window, jQuery);

/**
 * app.js
 * Main application logic for CheatSheeter.
 * Handles UI interactions, routing, and data management.
 */

(function(window, $) {
    'use strict';

    /**
     * Main Application Object
     */
    const App = {
        // Current state
        currentView: 'list',
        currentCheatsheet: null,
        categoryCounter: 0,

        /**
         * Initialize the application
         */
        init: function() {
            console.log('CheatSheeter initializing...');

            // Initialize theme manager
            ThemeManager.init();

            // Attach event listeners
            this.attachGlobalEventListeners();

            // Load initial view
            this.showView('list');
            this.loadCheatsheetsList();

            console.log('CheatSheeter ready!');
        },

        /**
         * Attach global event listeners
         */
        attachGlobalEventListeners: function() {
            const self = this;

            // Navigation links
            $('[data-view]').on('click', function(e) {
                e.preventDefault();
                const view = $(this).data('view');
                self.showView(view);
            });

            // Brand link - go home
            $('#brand-link').on('click', function(e) {
                e.preventDefault();
                self.showView('list');
            });

            // Back to list buttons
            $('#back-to-list, #cancel-edit, #cancel-edit-2').on('click', function(e) {
                e.preventDefault();
                self.showView('list');
            });

            // Search functionality
            $('#search-input').on('input', function() {
                self.filterCheatsheets($(this).val());
            });

            // Form submission
            $('#cheatsheet-form').on('submit', function(e) {
                e.preventDefault();
                self.handleFormSubmit();
            });

            // Add category button
            $('#add-category-btn').on('click', function() {
                self.addCategory();
            });
        },

        /**
         * Show a specific view
         * @param {string} viewName - Name of the view to show
         */
        showView: function(viewName) {
            this.currentView = viewName;

            // Hide all views
            $('.view-container').hide();

            // Update navigation active state
            $('.navbar-nav .nav-link').removeClass('active');
            $(`.navbar-nav .nav-link[data-view="${viewName}"]`).addClass('active');

            // Show requested view
            switch(viewName) {
                case 'list':
                    $('#list-view').show();
                    this.loadCheatsheetsList();
                    break;
                case 'create':
                    this.showEditView();
                    break;
                case 'view':
                    $('#view-cheatsheet-view').show();
                    break;
                default:
                    $('#list-view').show();
            }
        },

        /**
         * Show loading spinner
         */
        showLoading: function() {
            $('#loading-spinner').show();
        },

        /**
         * Hide loading spinner
         */
        hideLoading: function() {
            $('#loading-spinner').hide();
        },

        /**
         * Show alert message
         * @param {string} message - Alert message
         * @param {string} type - Alert type (success, danger, warning, info)
         */
        showAlert: function(message, type = 'info') {
            const alertHtml = `
                <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;

            const $alert = $(alertHtml);
            $('#alert-container').append($alert);

            // Auto-dismiss after 5 seconds
            setTimeout(function() {
                $alert.alert('close');
            }, 5000);
        },

        /**
         * Load and display list of cheatsheets
         */
        loadCheatsheetsList: function() {
            const self = this;
            self.showLoading();

            CheatSheetAPI.getAllCheatsheets()
                .done(function(response) {
                    self.renderCheatsheetsList(response.cheatsheets || []);
                })
                .fail(function(xhr) {
                    self.showAlert('Failed to load cheatsheets. Please try again.', 'danger');
                    console.error('Failed to load cheatsheets:', xhr);
                })
                .always(function() {
                    self.hideLoading();
                });
        },

        /**
         * Render cheatsheets list
         * @param {Array} cheatsheets - Array of cheatsheet names
         */
        renderCheatsheetsList: function(cheatsheets) {
            const self = this;
            const $container = $('#cheatsheets-container');
            $container.empty();

            if (cheatsheets.length === 0) {
                $('#empty-state').show();
                return;
            }

            $('#empty-state').hide();

            cheatsheets.forEach((name) => {
                const cardHtml = `
                    <div class="col-md-6 col-lg-4 cheatsheet-card" data-name="${name}">
                        <div class="card h-100 shadow-sm hover-shadow">
                            <div class="card-body">
                                <h5 class="card-title">
                                    <i class="bi bi-file-code text-primary"></i> ${self.formatName(name)}
                                </h5>
                                <p class="card-text text-muted">
                                    <small><i class="bi bi-tag"></i> ${name}</small>
                                </p>
                            </div>
                            <div class="card-footer bg-transparent border-top-0">
                                <div class="d-flex gap-2">
                                    <button class="btn btn-sm btn-primary flex-grow-1 view-cheatsheet-btn"
                                            data-name="${name}">
                                        <i class="bi bi-eye"></i> View
                                    </button>
                                    <button class="btn btn-sm btn-outline-secondary edit-cheatsheet-btn"
                                            data-name="${name}">
                                        <i class="bi bi-pencil"></i> Edit
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger delete-cheatsheet-btn"
                                            data-name="${name}">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                $container.append(cardHtml);
            });

            // Attach event listeners for buttons
            $('.view-cheatsheet-btn').on('click', function() {
                const name = $(this).data('name');
                self.viewCheatsheet(name);
            });

            $('.edit-cheatsheet-btn').on('click', function() {
                const name = $(this).data('name');
                self.editCheatsheet(name);
            });

            $('.delete-cheatsheet-btn').on('click', function() {
                const name = $(this).data('name');
                self.deleteCheatsheet(name);
            });
        },

        /**
         * Filter cheatsheets by search term
         * @param {string} searchTerm - Search term
         */
        filterCheatsheets: function(searchTerm) {
            const term = searchTerm.toLowerCase();

            $('.cheatsheet-card').each(function() {
                const name = $(this).data('name').toLowerCase();
                if (name.includes(term)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        },

        /**
         * Format cheatsheet name for display
         * @param {string} name - Raw name
         * @returns {string} Formatted name
         */
        formatName: function(name) {
            return name
                .replace(/[-_]/g, ' ')
                .replace(/\b\w/g, function(char) {
                    return char.toUpperCase();
                });
        },

        /**
         * View a specific cheatsheet
         * @param {string} name - Cheatsheet name
         */
        viewCheatsheet: function(name) {
            const self = this;
            self.showLoading();

            CheatSheetAPI.getCheatsheet(name)
                .done(function(response) {
                    self.currentCheatsheet = response;
                    self.renderCheatsheetView(response);
                    self.showView('view');
                })
                .fail(function(xhr) {
                    self.showAlert('Failed to load cheatsheet. Please try again.', 'danger');
                    console.error('Failed to load cheatsheet:', xhr);
                })
                .always(function() {
                    self.hideLoading();
                });
        },

        /**
         * Render cheatsheet view
         * @param {Object} cheatsheet - Cheatsheet data
         */
        renderCheatsheetView: function(cheatsheet) {
            const self = this;

            // Set title
            $('#cheatsheet-title').text(cheatsheet.data.title || cheatsheet.name);

            // Set up edit and delete buttons
            $('#edit-cheatsheet-btn').off('click').on('click', function() {
                self.editCheatsheet(cheatsheet.name);
            });

            $('#delete-cheatsheet-btn').off('click').on('click', function() {
                self.deleteCheatsheet(cheatsheet.name);
            });

            // Render content
            const $content = $('#cheatsheet-content');
            $content.empty();

            const columns = cheatsheet.columns || 1;
            const categoriesByColumn = {};

            // Group categories by column
            for (let i = 1; i <= columns; i++) {
                categoriesByColumn[i] = [];
            }

            (cheatsheet.categories || []).forEach((category) => {
                const col = category.column || 1;
                if (categoriesByColumn[col]) {
                    categoriesByColumn[col].push(category);
                }
            });

            // Render columns
            for (let i = 1; i <= columns; i++) {
                const categories = categoriesByColumn[i];
                const colWidth = Math.floor(12 / columns);

                const $col = $(`<div class="col-md-${colWidth}"></div>`);

                categories.forEach((category) => {
                    const categoryHtml = self.renderCategoryCard(category);
                    $col.append(categoryHtml);
                });

                $content.append($col);
            }

            if ((cheatsheet.categories || []).length === 0) {
                $content.append(`
                    <div class="col-12 text-center text-muted py-5">
                        <i class="bi bi-inbox display-4"></i>
                        <p class="mt-3">This cheatsheet has no categories yet.</p>
                    </div>
                `);
            }
        },

        /**
         * Render a category card
         * @param {Object} category - Category data
         * @returns {string} HTML string
         */
        renderCategoryCard: function(category) {
            const self = this;
            const items = (category.items || []).map((item) => {
                return `
                    <li class="list-group-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <code class="text-primary">${self.escapeHtml(item.command)}</code>
                                <p class="mb-0 mt-1 text-muted small">${self.escapeHtml(item.description)}</p>
                            </div>
                        </div>
                    </li>
                `;
            }).join('');

            return `
                <div class="card mb-3 shadow-sm">
                    <div class="card-header bg-light">
                        <h5 class="mb-0">${self.escapeHtml(category.name)}</h5>
                    </div>
                    <ul class="list-group list-group-flush">
                        ${items || '<li class="list-group-item text-muted">No items</li>'}
                    </ul>
                </div>
            `;
        },

        /**
         * Show edit view for creating or editing a cheatsheet
         * @param {string} name - Optional cheatsheet name for edit mode
         */
        showEditView: function(name = null) {
            const self = this;

            // Reset form
            $('#cheatsheet-form')[0].reset();
            $('#categories-container').empty();
            self.categoryCounter = 0;

            if (name) {
                // Edit mode
                $('#edit-view-title').text('Edit Cheatsheet');
                $('#edit-mode').val('edit');
                $('#edit-cheatsheet-name').val(name);
                $('#cheatsheet-name-input').prop('disabled', true);

                // Load cheatsheet data
                self.showLoading();

                CheatSheetAPI.getCheatsheet(name)
                    .done(function(response) {
                        self.populateEditForm(response);
                    })
                    .fail(function(xhr) {
                        self.showAlert('Failed to load cheatsheet for editing.', 'danger');
                        self.showView('list');
                    })
                    .always(function() {
                        self.hideLoading();
                    });
            } else {
                // Create mode
                $('#edit-view-title').text('Create Cheatsheet');
                $('#edit-mode').val('create');
                $('#cheatsheet-name-input').prop('disabled', false);
                $('#no-categories').show();
            }

            $('#edit-view').show();
        },

        /**
         * Populate edit form with cheatsheet data
         * @param {Object} cheatsheet - Cheatsheet data
         */
        populateEditForm: function(cheatsheet) {
            const self = this;

            $('#cheatsheet-name-input').val(cheatsheet.name);
            $('#cheatsheet-title-input').val(cheatsheet.data.title || '');
            $('#cheatsheet-columns').val(cheatsheet.data.columns || 1);

            (cheatsheet.data.categories || []).forEach((category) => {
                self.addCategory(category);
            });

            if (cheatsheet.data.categories && cheatsheet.data.categories.length > 0) {
                $('#no-categories').hide();
            }
        },

        /**
         * Add a category to the form
         * @param {Object} data - Optional category data
         */
        addCategory: function(data = null) {
            const self = this;
            const id = ++self.categoryCounter;

            const categoryHtml = `
                <div class="card mb-3 category-card" data-category-id="${id}">
                    <div class="card-header bg-light d-flex justify-content-between align-items-center">
                        <strong>Category ${id}</strong>
                        <button type="button" class="btn btn-sm btn-danger remove-category-btn"
                                data-category-id="${id}">
                            <i class="bi bi-trash"></i> Remove
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="row mb-3">
                            <div class="col-md-8">
                                <label class="form-label">Category Name *</label>
                                <input type="text" class="form-control category-name"
                                       value="${data ? self.escapeHtml(data.name) : ''}"
                                       placeholder="e.g., Basics" required>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Column *</label>
                                <input type="number" class="form-control category-column"
                                       value="${data ? data.column : 1}"
                                       min="1" max="6" required>
                            </div>
                        </div>

                        <div class="items-container" data-category-id="${id}">
                            <!-- Items will be added here -->
                        </div>

                        <button type="button" class="btn btn-sm btn-outline-primary add-item-btn"
                                data-category-id="${id}">
                            <i class="bi bi-plus-lg"></i> Add Item
                        </button>
                    </div>
                </div>
            `;

            $('#categories-container').append(categoryHtml);
            $('#no-categories').hide();

            // Add event listeners
            $(`.remove-category-btn[data-category-id="${id}"]`).on('click', function() {
                self.removeCategory(id);
            });

            $(`.add-item-btn[data-category-id="${id}"]`).on('click', function() {
                self.addItem(id);
            });

            // Add existing items if data provided
            if (data && data.items) {
                data.items.forEach((item) => {
                    self.addItem(id, item);
                });
            }
        },

        /**
         * Remove a category
         * @param {number} categoryId - Category ID
         */
        removeCategory: function(categoryId) {
            $(`.category-card[data-category-id="${categoryId}"]`).remove();

            if ($('.category-card').length === 0) {
                $('#no-categories').show();
            }
        },

        /**
         * Add an item to a category
         * @param {number} categoryId - Category ID
         * @param {Object} data - Optional item data
         */
        addItem: function(categoryId, data = null) {
            const self = this;
            const itemId = Date.now() + Math.random();

            const itemHtml = `
                <div class="card mb-2 item-card" data-item-id="${itemId}">
                    <div class="card-body">
                        <div class="row mb-2">
                            <div class="col-md-6">
                                <label class="form-label small">Command *</label>
                                <input type="text" class="form-control form-control-sm item-command"
                                       value="${data ? self.escapeHtml(data.command) : ''}"
                                       placeholder="e.g., git commit" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small">Description *</label>
                                <input type="text" class="form-control form-control-sm item-description"
                                       value="${data ? self.escapeHtml(data.description) : ''}"
                                       placeholder="e.g., Commit changes" required>
                            </div>
                        </div>
                        <button type="button" class="btn btn-sm btn-outline-danger remove-item-btn"
                                data-item-id="${itemId}">
                            <i class="bi bi-x-lg"></i> Remove
                        </button>
                    </div>
                </div>
            `;

            $(`.items-container[data-category-id="${categoryId}"]`).append(itemHtml);

            // Add event listener
            $(`.remove-item-btn[data-item-id="${itemId}"]`).on('click', function() {
                $(`.item-card[data-item-id="${itemId}"]`).remove();
            });
        },

        /**
         * Handle form submission
         */
        handleFormSubmit: function() {
            const self = this;

            // Collect form data
            const name = $('#cheatsheet-name-input').val().trim();
            const title = $('#cheatsheet-title-input').val().trim();
            const columns = parseInt($('#cheatsheet-columns').val());
            const mode = $('#edit-mode').val();

            // Validate
            if (!name || !title) {
                self.showAlert('Please fill in all required fields.', 'warning');
                return;
            }

            // Collect categories
            const categories = [];
            $('.category-card').each(function() {
                const $category = $(this);
                const categoryName = $category.find('.category-name').val().trim();
                const column = parseInt($category.find('.category-column').val());

                if (!categoryName) {
                    return; // Skip empty categories
                }

                const items = [];
                $category.find('.item-card').each(function() {
                    const $item = $(this);
                    const command = $item.find('.item-command').val().trim();
                    const description = $item.find('.item-description').val().trim();

                    if (command && description) {
                        items.push({
                            command: command,
                            description: description
                        });
                    }
                });

                categories.push({
                    name: categoryName,
                    column: column,
                    items: items
                });
            });

            const data = {
                title: title,
                columns: columns,
                categories: categories
            };

            // Submit
            self.showLoading();

            let apiCall;
            if (mode === 'edit') {
                const editName = $('#edit-cheatsheet-name').val();
                apiCall = CheatSheetAPI.updateCheatsheet(editName, data);
            } else {
                apiCall = CheatSheetAPI.createCheatsheet(name, data);
            }

            apiCall
                .done(function(response) {
                    self.showAlert(
                        mode === 'edit' ? 'Cheatsheet updated successfully!' : 'Cheatsheet created successfully!',
                        'success'
                    );
                    self.showView('list');
                })
                .fail(function(xhr) {
                    const error = xhr.responseJSON && xhr.responseJSON.message
                        ? xhr.responseJSON.message
                        : 'Failed to save cheatsheet. Please try again.';
                    self.showAlert(error, 'danger');
                })
                .always(function() {
                    self.hideLoading();
                });
        },

        /**
         * Edit a cheatsheet
         * @param {string} name - Cheatsheet name
         */
        editCheatsheet: function(name) {
            this.showEditView(name);
        },

        /**
         * Delete a cheatsheet
         * @param {string} name - Cheatsheet name
         */
        deleteCheatsheet: function(name) {
            const self = this;

            if (!confirm(`Are you sure you want to delete "${name}"? This action cannot be undone.`)) {
                return;
            }

            self.showLoading();

            CheatSheetAPI.deleteCheatsheet(name)
                .done(function() {
                    self.showAlert('Cheatsheet deleted successfully!', 'success');

                    // If viewing this cheatsheet, go back to list
                    if (self.currentView === 'view' && self.currentCheatsheet && self.currentCheatsheet.name === name) {
                        self.showView('list');
                    } else {
                        self.loadCheatsheetsList();
                    }
                })
                .fail(function(xhr) {
                    self.showAlert('Failed to delete cheatsheet. Please try again.', 'danger');
                })
                .always(function() {
                    self.hideLoading();
                });
        },

        /**
         * Escape HTML to prevent XSS
         * @param {string} text - Text to escape
         * @returns {string} Escaped text
         */
        escapeHtml: function(text) {
            if (!text) return '';
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, function(m) { return map[m]; });
        }
    };

    // Initialize app when document is ready
    $(document).ready(function() {
        App.init();
    });

    // Expose App to global scope for debugging
    window.CheatSheetApp = App;

})(window, jQuery);

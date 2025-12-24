
document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // The protection level is read. If not defined, 'full' is used for security.
    const level = window.protectionLevel || 'full';

    // --- Level 'full': Total block ---
    // Blocks context menu, copy shortcuts, and text selection.
    if (level === 'full') {
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        }, false);

        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && (e.key === 'c' || e.key === 'x' || e.key === 'a' || e.key === 'p' || e.key === 'u')) {
                e.preventDefault();
            }
            if (e.key === 'F12') {
                e.preventDefault();
            }
        });

        // Apply CSS styles to disable text selection
        document.body.style.userSelect = 'none';
        document.body.style.webkitUserSelect = 'none';
        document.body.style.mozUserSelect = 'none';
        document.body.style.msUserSelect = 'none';
    }

    // --- Level 'annotations': Partial block for Study Room ---
    // Blocks context menu and shortcuts, but ALLOWS text selection for annotating.
    if (level === 'annotations') {
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        }, false);

        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && (e.key === 'c' || e.key === 'x' || e.key === 'a' || e.key === 'p' || e.key === 'u')) {
                e.preventDefault();
            }
            if (e.key === 'F12') {
                e.preventDefault();
            }
        });
        // NOTE: Text selection (user-select) is deliberately not blocked.
    }

    // --- Level 'none': No protection ---
    // No restrictions are applied. Ideal for editing forms.
    if (level === 'none') {
        // No blocking action is executed.
    }
});
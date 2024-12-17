document.addEventListener('DOMContentLoaded', function () {
    const actionSelect = document.getElementById('action');
    const resizeOptions = document.getElementById('resize-options');
    const dpiOptions = document.getElementById('dpi-options');

    actionSelect.addEventListener('change', function () {
        const action = actionSelect.value;

        resizeOptions.style.display = action === 'resize' ? 'block' : 'none';
        dpiOptions.style.display = action === 'change_dpi' ? 'block' : 'none';
    });
});

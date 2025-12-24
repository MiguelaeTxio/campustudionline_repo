document.addEventListener('DOMContentLoaded', function() {
    // Asegurarnos de que el código solo se ejecute en la página de cambio de ContentMaterial
    if (document.body.classList.contains('change-form') && document.body.id === 'contentmaterial_form') {

        const masterCategorySelect = document.querySelector('#id_master_category');
        const subCategorySelect = document.querySelector('#id_sub_category');
        const ajaxURL = '/admin/contents/ajax/load-subcategories/';

        if (masterCategorySelect && subCategorySelect) {
            masterCategorySelect.addEventListener('change', function() {
                const masterId = this.value;

                // Limpiar opciones de subcategoría
                subCategorySelect.innerHTML = '<option value="">---------</option>';

                if (masterId) {
                    fetch(`${ajaxURL}?master_category_id=${masterId}`)
                        .then(response => response.json())
                        .then(data => {
                            data.forEach(function(subcategory) {
                                const option = new Option(subcategory.name, subcategory.id);
                                subCategorySelect.add(option);
                            });
                        })
                        .catch(error => console.error('Error al cargar subcategorías:', error));
                }
            });
        }
    }
});

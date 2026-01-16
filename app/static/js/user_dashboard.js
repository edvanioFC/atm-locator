document.addEventListener('DOMContentLoaded', function () {
    const deleteBtn = document.querySelector('.btn-danger');

    if (deleteBtn) {
        deleteBtn.addEventListener('click', function (e) {
            const confirmed = confirm("Tens a certeza que desejas eliminar a tua conta? Esta ação não pode ser desfeita.");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    }

    console.log("User Dashboard JS carregado com sucesso.");
});
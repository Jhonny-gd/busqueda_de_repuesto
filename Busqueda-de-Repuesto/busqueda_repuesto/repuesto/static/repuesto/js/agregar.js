document.addEventListener('DOMContentLoaded', function () {
    // Limpiar compatibilidad al cargar (solo en agregar)
    const select = document.getElementById('compatibilidad');
    if (select) {
        select.innerHTML = '';
    }

    // Ocultar tabla de vehículos hasta que se busque
    const tablaContenedor = document.getElementById('tabla-contenedor');
    if (tablaContenedor) {
        tablaContenedor.style.display = 'none';
    }

    // Mostrar tabla cuando se hace búsqueda
    document.getElementById('btnBuscar').addEventListener('click', function () {
        const modelo = document.getElementById('modelo_buscar').value;
       fetch(`/repuesto/buscar_vehiculo/?modelo_buscar=${encodeURIComponent(modelo)}`)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#tablavehiculos tbody');
                tbody.innerHTML = '';

                if (data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7">No hay vehículos registrados.</td></tr>';
                } else {
                    tablaContenedor.style.display = 'block';

                    data.forEach(v => {
                        const fila = `
                            <tr>
                                <td>${v.id_auto}</td>
                                <td>${v.tipo}</td>
                                <td>${v.marca}</td>
                                <td>${v.modelo}</td>
                                <td>${v.transmision}</td>
                                <td>${v.anio}</td>
                                <td>
                                    <input type="checkbox" class="select-vehiculo"
                                        data-id="${v.id_auto}"
                                        data-marca="${v.marca}"
                                        data-modelo="${v.modelo}"
                                        data-anio="${v.anio}"
                                        data-transmision="${v.transmision}">
                                </td>
                            </tr>`;
                        tbody.innerHTML += fila;
                    });
                }
            })
            .catch(error => console.error('Error al buscar vehículos:', error));
    });
});
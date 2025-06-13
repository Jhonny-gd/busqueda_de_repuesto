document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('btnBuscar').addEventListener('click', function () {
        const modelo = document.getElementById('modelo_buscar').value;
        fetch(`/repuesto/buscar_vehiculo/?modelo_buscar=${encodeURIComponent(modelo)}`)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#tablavehiculos tbody');
                tbody.innerHTML = ''; // Limpiar resultados anteriores

                if (data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7">No hay vehículos registrados.</td></tr>';
                    return;
                }
                //Mostrar la tabla de resultados
                document.getElementById('contenedor-tabla-vehiculos').style.display = 'block';
                // Llenar la tabla con los datos de los vehículos

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
                                    data-anio="${v.anio}">
                            </td>
                        </tr>`;
                    tbody.innerHTML += fila;
                });
            })
            .catch(error => {
                console.error('Error al buscar vehículos:', error);
            });
    });
//boton añadir a compatibilidad
    // Añadir vehículos seleccionados a la compatibilidad
    document.getElementById('btnAñadir').addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.select-vehiculo:checked');
        const compatibilidadSelect = document.getElementById('compatibilidad');

        checkboxes.forEach(checkbox => {
            const id = checkbox.getAttribute('data-id');
            const marca = checkbox.getAttribute('data-marca');
            const modelo = checkbox.getAttribute('data-modelo');
            const anio = checkbox.getAttribute('data-anio');

            // Evitar duplicados
            if (![...compatibilidadSelect.options].some(opt => opt.value === id)) {
                const option = document.createElement('option');
                option.value = id;
               option.text = `${marca} - ${modelo} - (${anio} ${transmision})`;
                compatibilidadSelect.appendChild(option);
            }
        });
    });
});
  
// ------------------------------
// RELOJ
// ------------------------------

function actualizarReloj() {

    const reloj = document.getElementById("reloj");

    if (!reloj) {

        return;

    }

    const ahora = new Date();

    reloj.innerHTML = ahora.toLocaleTimeString(
        "es-CO",
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}

actualizarReloj();

setInterval(
    actualizarReloj,
    1000
);

// ------------------------------
// SELECTORES
// ------------------------------

const form = document.getElementById("formBusqueda");

const sede = document.getElementById("id_sede");

const edificio = document.getElementById("id_edificio");

const aula = document.getElementById("id_aula");

const docente = document.getElementById("id_docente");

const hora = document.getElementById("id_hora");

// ------------------------------
// CARGAR EDIFICIOS
// ------------------------------

async function cargarEdificios() {

    if (!sede) {

        return;

    }

    if (sede.value === "") {

        edificio.innerHTML =
            '<option value="">Todos</option>';

        aula.innerHTML =
            '<option value="">Todas</option>';


        return;

    }

    const respuesta = await fetch(

        "/obtener-edificios/?sede_id=" +
        sede.value

    );

    const datos = await respuesta.json();

    edificio.innerHTML =
        '<option value="">Todos</option>';

    datos.forEach(function (e) {

        edificio.innerHTML +=
            `<option value="${e.id}">${e.nombre}</option>`;

    });

    aula.innerHTML =
        '<option value="">Todas</option>';

    form.submit();

}

// ------------------------------
// CARGAR AULAS
// ------------------------------

async function cargarAulas() {

    if (!edificio) {

        return;

    }

    if (edificio.value === "") {

        aula.innerHTML =
            '<option value="">Todas</option>';

        return;

    }

    const respuesta = await fetch(

        "/obtener-aulas/?edificio_id=" +
        edificio.value

    );

    const datos = await respuesta.json();

    aula.innerHTML =
        '<option value="">Todas</option>';

    datos.forEach(function (a) {

        aula.innerHTML +=
            `<option value="${a.id}">${a.nombre}</option>`;

    });

    form.submit();

}

// ------------------------------
// EVENTOS
// ------------------------------

if (sede) {

    sede.addEventListener(
        "change",
        cargarEdificios
    );

}

if (edificio) {

    edificio.addEventListener(
        "change",
        cargarAulas
    );

}

if (aula) {

    aula.addEventListener(
        "change",
        function () {

            form.submit();

        }
    );

}

if (docente) {

    docente.addEventListener(
        "change",
        function () {

            form.submit();

        }
    );

}

if (hora) {

    hora.addEventListener(
        "change",
        function () {

            form.submit();

        }
    );

}
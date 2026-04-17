from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos, Maestros, Curso, Inscripcion
from . import consultas_bp

@consultas_bp.route("/consultas", methods=["GET"])
def consultas():
    return render_template("consultas/index.html")

@consultas_bp.route("/consultas/alumnos-por-curso", methods=["GET"])
def alumnos_por_curso():
    cursos = Curso.query.all()
    selected_curso_id = request.args.get('curso_id')
    alumnos = []
    curso_seleccionado = None
    if selected_curso_id:
        curso_seleccionado = db.session.get(Curso, int(selected_curso_id))
        if curso_seleccionado:
            alumnos = curso_seleccionado.alumnos
    return render_template("consultas/alumnos_por_curso.html", cursos=cursos, alumnos=alumnos, curso_seleccionado=curso_seleccionado)

@consultas_bp.route("/consultas/cursos-por-maestro", methods=["GET"])
def cursos_por_maestro():
    maestros = Maestros.query.all()
    selected_maestro_matricula = request.args.get('maestro_matricula')
    cursos = []
    maestro_seleccionado = None
    if selected_maestro_matricula:
        maestro_seleccionado = db.session.get(Maestros, int(selected_maestro_matricula))
        if maestro_seleccionado:
            cursos = maestro_seleccionado.cursos
    return render_template("consultas/cursos_por_maestro.html", maestros=maestros, cursos=cursos, maestro_seleccionado=maestro_seleccionado)

@consultas_bp.route("/consultas/alumnos-sin-cursos", methods=["GET"])
def alumnos_sin_cursos():
    # Alumnos que no están inscritos en ningún curso
    alumnos_con_cursos = db.session.query(Inscripcion.alumno_id).distinct().subquery()
    alumnos = Alumnos.query.filter(~Alumnos.id.in_(alumnos_con_cursos)).all()
    return render_template("consultas/alumnos_sin_cursos.html", alumnos=alumnos)

@consultas_bp.route("/consultas/inscripciones", methods=["GET"])
def inscripciones():
    cursos = Curso.query.all()
    selected_curso_id = request.args.get('curso_id')
    curso_seleccionado = None
    query = Inscripcion.query.join(Alumnos).join(Curso).order_by(Inscripcion.fecha_inscripcion.desc())

    if selected_curso_id:
        try:
            curso_id = int(selected_curso_id)
            curso_seleccionado = db.session.get(Curso, curso_id)
            if curso_seleccionado:
                query = query.filter(Inscripcion.curso_id == curso_id)
        except ValueError:
            curso_seleccionado = None

    inscripciones = query.all()
    return render_template(
        "consultas/inscripciones.html",
        cursos=cursos,
        inscripciones=inscripciones,
        curso_seleccionado=curso_seleccionado
    )


@consultas_bp.route("/consultas/inscripciones-por-alumno", methods=["GET"])
def inscripciones_por_alumno():
    alumnos = Alumnos.query.all()
    selected_alumno_id = request.args.get('alumno_id')
    alumno_seleccionado = None
    cursos = []

    if selected_alumno_id:
        try:
            alumno_id = int(selected_alumno_id)
            alumno_seleccionado = db.session.get(Alumnos, alumno_id)
            if alumno_seleccionado:
                cursos = alumno_seleccionado.cursos
        except ValueError:
            alumno_seleccionado = None

    return render_template(
        "consultas/inscripciones_por_alumno.html",
        alumnos=alumnos,
        cursos=cursos,
        alumno_seleccionado=alumno_seleccionado
    )


@consultas_bp.route("/consultas/estadisticas", methods=["GET"])
def estadisticas():
    total_alumnos = Alumnos.query.count()
    total_maestros = Maestros.query.count()
    total_cursos = Curso.query.count()
    total_inscripciones = Inscripcion.query.count()
    return render_template("consultas/estadisticas.html", 
                          total_alumnos=total_alumnos,
                          total_maestros=total_maestros,
                          total_cursos=total_cursos,
                          total_inscripciones=total_inscripciones)
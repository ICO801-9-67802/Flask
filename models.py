from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    inscripciones = db.relationship('Inscripcion', back_populates='alumno', cascade='all, delete-orphan')

    @property
    def cursos(self):
        return [i.curso for i in self.inscripciones]


class Maestros(db.Model):
    __tablename__ = 'maestros'

    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    cursos = db.relationship('Curso', back_populates='maestro', cascade='all, delete-orphan')


class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    maestro_id = db.Column(
        db.Integer,
        db.ForeignKey('maestros.matricula'),
        nullable=False
    )

    maestro = db.relationship('Maestros', back_populates='cursos')
    inscripciones = db.relationship('Inscripcion', back_populates='curso', cascade='all, delete-orphan')

    @property
    def alumnos(self):
        return [i.alumno for i in self.inscripciones]


class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(
        db.Integer,
        db.ForeignKey('alumnos.id'),
        nullable=False
    )

    curso_id = db.Column(
        db.Integer,
        db.ForeignKey('cursos.id'),
        nullable=False
    )

    alumno = db.relationship('Alumnos', back_populates='inscripciones')
    curso = db.relationship('Curso', back_populates='inscripciones')

    fecha_inscripcion = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    __table_args__ = (
        db.UniqueConstraint('alumno_id', 'curso_id', name='uq_alumno_curso'),
    )
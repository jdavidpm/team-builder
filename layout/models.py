from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime


# Ramas de conocimiento
class Rama(models.Model):
    nombre = models.CharField(max_length=128, null=False, blank=False, unique=True)


# Lenguajes de programación
class Lenguaje(models.Model):
    nombre = models.CharField(max_length=45, null=False, blank=False, unique=True)


# Frameworks de programación
class Framework(models.Model):
    nombre = models.CharField(max_length=45, null=False, blank=False, unique=True)


# Herramientas de trabajo
class Herramienta(models.Model):
    nombre = models.CharField(max_length=45, null=False, blank=False, unique=True)


# Distribuciones de sistemas operativos
class Distribucion(models.Model):
    nombre = models.CharField(max_length=45, null=False, blank=False, unique=True)


class Usuario(models.Model):
    # Llave primaria y foránea que hace referencia a la tabla "auth_user" creada por Django
    id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    matricula = models.CharField(max_length=10, null=True, default='0', blank=False, unique=True)

    # Cocientes de dimensiones de personalidad, con 2 dígitos para decimales y 3 dígitos en total
    personalidad_h = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personalidad_e = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personalidad_x = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personalidad_a = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personalidad_c = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personalidad_o = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    # Crea tablas en la BD para las relaciones M a N entre Usuario y Rama
    experiencia = models.ManyToManyField(Rama, related_name='experiencia')
    intereses = models.ManyToManyField(Rama, related_name='intereses')
    lenguajes = models.ManyToManyField(Lenguaje)
    frameworks = models.ManyToManyField(Framework)
    herramientas_sw = models.ManyToManyField(Herramienta, related_name='herramientas_sw')
    herarmientas_hw = models.ManyToManyField(Herramienta, related_name='herramientas_hw')
    distribuciones_so = models.ManyToManyField(Distribucion)

    # Relación M a N entre usuarios para invitaciones a unirse a equipos
    invitaciones = models.ManyToManyField(
        'self',
        through = 'Invitacion',
        through_fields = ('destinatario', 'remitente'),
        symmetrical = False
    )


# Crea tabla para el campo multivaluado: Trabajos Previos
class TrabajoPrevio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    trabajo = models.CharField(max_length=128, null=False, blank=False)

    # crea constraint de valores en par únicos en la base de datos (simulando llave primaria compuesta)
    class Meta:
        unique_together = ('usuario', 'trabajo')


class Carrera(models.Model):
    nombre = models.CharField(max_length=64, null=False, blank=False, unique=True)


class Alumno(models.Model):
    # Opciones para elegir el año de ingreso, desde 15 años atrás hasta la actualidad
    OPCIONES_AÑOS = [(y, y) for y in range(datetime.date.today().year, datetime.date.today().year-15, -1)]

    # Opciones para elegir el semestre de ingreso, para después calcular el semestre actual del usuario
    OPCIONES_SEMESTRES = [
        ('agosto', 'Agosto - Diciembre'),
        ('enero', 'Enero - Junio')
    ]
    
    # Fields
    id = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    año_de_ingreso = models.IntegerField(
        choices=OPCIONES_AÑOS,
        null=False,
        blank=False,
    )
    semestre_de_ingreso = models.CharField(max_length=6, choices=OPCIONES_SEMESTRES, null=False, blank=False)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)


class Academia(models.Model):
    nombre = models.CharField(max_length=64, null=False, blank=False, unique=True)


class UnidadAprendizaje(models.Model):
    nombre = models.CharField(max_length=64, null=False, blank=False, unique=True)
    academia = models.ForeignKey(Academia, on_delete=models.PROTECT)

    # Crea tabla para relaciones M a N entre usuarios profesores y Unidades de Aprendizaje
    profesores = models.ManyToManyField(Usuario)

    # Crea tabla para relaciones M a N entre Unidades de Aprendizaje y Ramas
    ramas = models.ManyToManyField(Rama)


class Proyecto(models.Model):
    # Opciones para estado del proyecto
    OPCIONES_ESTADO = [
        ('propuesto', 'Propuesto'),
        ('en desarrollo', 'En desarrollo'),
        ('finalizado', 'Finalizado')
    ]

    # Opciones para la visibilidad del proyecto
    OPCIONES_VISIBILIDAD = [
        ('privado', 'Privado'),
        ('publico', 'Público')
    ]

    autor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='autor_proyecto')

    # fecha y hora de creación del proyecto
    fecha = models.DateTimeField(auto_now=True, null=False)

    nombre = models.CharField(max_length=64, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)

    estado = models.CharField(
        max_length = 13,
        choices = OPCIONES_ESTADO,
        default = 'creado',
        null = False
    )

    visibilidad = models.CharField(
        max_length = 7,
        choices = OPCIONES_VISIBILIDAD,
        default='publico',
        null=False
    )

    evaluacion = models.DecimalField(
        max_digits = 4,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(10.0)],
        null=True
    )

    # Crea tabla para registro de actividad en el proyecto
    actividad = models.ManyToManyField(
        Usuario,
        through = 'ActividadProyecto',
        through_fields = ('proyecto', 'usuario')
    )

    ramas = models.ManyToManyField(Rama)

    class Meta:
        unique_together = ('autor', 'nombre')


class Equipo(models.Model):

    # El usuario que crea el equipo
    fundador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='fundador')

    # fecha y hora de creación del equipo
    fecha = models.DateTimeField(auto_now=True, null=False)

    nombre = models.CharField(max_length=32, null=False, blank=False)
    
    integrantes = models.ManyToManyField(
        Usuario,
        through = 'Integrante',
        through_fields = ('equipo', 'usuario'),
        related_name = 'integrantes'
    )

    # solicitudes de usuarios para integrarse al equipo
    solicitudes = models.ManyToManyField(
        Usuario,
        through = 'Solicitud',
        through_fields = ('equipo', 'usuario'),
        related_name = 'solicitudes'
    )

    # Proyectos en los que el equipo trabaja
    proyectos = models.ManyToManyField(Proyecto)

    # evaluaciones de procesos operativos
    evaluacion_p1 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluacion_p2 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluacion_p3 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluacion_p4 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluacion_p5 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluacion_p6 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluacion_p7 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    class Meta:
        unique_together = ('fundador', 'nombre')


class Integrante(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True, null=False)
    invitador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="invitador",
        null=True
    )


class Solicitud(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True, null=False)


class Invitacion(models.Model):
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destinatario')
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='remitente')
    
    equipo = models.ForeignKey(
        Equipo,
        on_delete = models.CASCADE,
        null = False
    )

    fecha = models.DateTimeField(auto_now=True, null=False)


class ActividadProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True, null=False)
    descripcion = models.CharField(max_length=256, null=False)


class Tarea(models.Model):
    # Opciones para el estado de la tarea
    OPCIONES_ESTADO = [
        ('pendiente', 'Pendiente'),
        ('en desarrollo', 'En desarrollo'),
        ('en revision', 'Lista para revisión'),
        ('completada', 'Completada')
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='autor_tarea')
    fecha = models.DateTimeField(auto_now=True, null=False)
    nombre = models.CharField(max_length=64, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    vencimiento = models.DateTimeField(null=False, blank=False)

    estado = models.CharField(
        choices = OPCIONES_ESTADO,
        max_length = 13,
        default = 'pendiente',
        blank = False,
        null = False
    )
    
    responsables = models.ManyToManyField(Usuario, related_name='responsables')

    actividad = models.ManyToManyField(
        Usuario,
        through = 'ActividadTarea',
        through_fields= ('tarea', 'usuario')
    )


class ActividadTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True, null=False)
    descripcion = models.CharField(max_length=256, null=False)


class Asociacion(models.Model):
    antecedente = models.CharField(max_length=6, null=False)
    consecuente = models.CharField(max_length=6, null=False)
    
    confianza = models.DecimalField(
        max_digits = 4,
        decimal_places = 3,
        null = False
    )

    soporte = models.DecimalField(
        max_digits = 4,
        decimal_places = 3,
        null = False
    )

    lift = models.DecimalField(
        max_digits = 6,
        decimal_places = 3,
        null = False
    )

    class Meta:
        unique_together = ('antecedente', 'consecuente')
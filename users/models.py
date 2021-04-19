from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
import datetime


# Ramas de conocimiento
class Field(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.name}'

# Lenguajes de programación
class Language(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.name}'

# Frameworks de programación
class Framework(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.name}'

# Herramientas de trabajo
class Tool(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.name}'

# Distribuciones de sistemas operativos
class Distribution(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.name}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    school_register = models.CharField(max_length=10, null=True, blank=True, unique=True) #Is really necessary the default=0?

    # Cocientes de dimensiones de personalidad, con 2 dígitos para decimales y 3 dígitos en total
    personality_h = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personality_e = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personality_x = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personality_a = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personality_c = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    personality_o = models.DecimalField(
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    # Crea tablas en la BD para las relaciones M a N entre Usuario y Rama
    #Every field below now has blank to True
    experience = models.ManyToManyField(Field, related_name='experience', blank=True)
    interests = models.ManyToManyField(Field, related_name='interests', blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    frameworks = models.ManyToManyField(Framework, blank=True)
    sw_tools = models.ManyToManyField(Tool, related_name='sw_tools', blank=True)
    hw_tools = models.ManyToManyField(Tool, related_name='hw_tools', blank=True)
    distributions = models.ManyToManyField(Distribution, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Crea tabla para el campo multivaluado: Trabajos Previos Destacados
class FeaturedWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.CharField(max_length=128, null=False, blank=False)

    # crea constraint de valores en par únicos en la base de datos (simulando llave primaria compuesta)
    class Meta:
        unique_together = ('user', 'work')


class Career(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.name}'


class Student(models.Model):
    # Opciones para elegir el año de ingreso, desde 15 años atrás hasta la actualidad
    YEAR_CHOICES = [(y, y) for y in range(datetime.date.today().year, datetime.date.today().year-15, -1)]

    # Opciones para elegir el semestre de ingreso, para después calcular el semestre actual del usuario
    SEMESTER_CHOICES = [
        ('agosto', 'Agosto - Diciembre'),
        ('enero', 'Enero - Junio')
    ]
    
    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    income_year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=False,
        blank=False,
    )
    income_semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES, null=False, blank=False)
    career = models.ForeignKey(Career, on_delete=models.PROTECT)


class Academy(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)


class Subject(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    academy = models.ForeignKey(Academy, on_delete=models.PROTECT)

    # Crea tabla para relaciones M a N entre usuarios profesores y Unidades de Aprendizaje
    teachers = models.ManyToManyField(User)

    # Crea tabla para relaciones M a N entre Unidades de Aprendizaje y Ramas
    fields = models.ManyToManyField(Field)


class Project(models.Model):
    # Opciones para estado del proyecto
    STATUS_CHOICES = [
        ('propuesto', 'Propuesto'),
        ('en desarrollo', 'En desarrollo'),
        ('finalizado', 'Finalizado')
    ]

    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_author')

    # fecha y hora de creación del proyecto
    creation_date = models.DateTimeField(auto_now=True, null=False)

    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    
    # Visibilidad del proyecto
    # (para determinar si otros pueden ver el nombre, descripción y ramas del proyecto)
    private = models.BooleanField(default=False, null=False)

    status = models.CharField(
        max_length = 13,
        choices = STATUS_CHOICES,
        default = 'propuesto',
        null = False
    )

    evaluation = models.DecimalField(
        max_digits = 4,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(10.0)],
        null=True
    )

    # Crea tabla para registro de actividad en el proyecto
    activity = models.ManyToManyField(
        User,
        through = 'ProjectActivity',
        through_fields = ('project', 'user')
    )

    fields = models.ManyToManyField(Field)

    class Meta:
        unique_together = ('author', 'name')


class Team(models.Model):

    # El usuario que crea el equipo
    founder = models.ForeignKey(User, on_delete=models.PROTECT, related_name='founder')

    # fecha y hora de creación del equipo
    creation_date = models.DateTimeField(auto_now=True, null=False)

    name = models.CharField(max_length=32, null=False, blank=False)
    
    members = models.ManyToManyField(
        User,
        through = 'Membership',
        through_fields = ('team', 'user'),
        related_name = 'membership'
    )

    # solicitudes de usuarios para integrarse al equipo
    join_requests = models.ManyToManyField(
        User,
        through = 'JoinRequest',
        through_fields = ('team', 'user'),
        related_name = 'join_requests'
    )

    # Proyectos en los que el equipo trabaja
    projects = models.ManyToManyField(Project)

    # evaluaciones de procesos operativos
    evaluation_p1 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluation_p2 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluation_p3 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluation_p4 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluation_p5 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluation_p6 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    evaluation_p7 = models.DecimalField(
        max_digits = 3,
        decimal_places = 2,
        validators = [MinValueValidator(0.0), MaxValueValidator(5.0)],
        null = True
    )

    class Meta:
        unique_together = ('founder', 'name')


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
    creation_date = models.DateTimeField(auto_now=True, null=False)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="invited_by",
        null=True
    )


class JoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)


class JoinInvitation(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    
    team = models.ForeignKey(
        Team,
        on_delete = models.CASCADE,
        null = False
    )

    date = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        unique_together = ('to_user', 'from_user')


class ProjectActivity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    description = models.CharField(max_length=256, null=False)


class Task(models.Model):
    # Opciones para el estado de la tarea
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en desarrollo', 'En desarrollo'),
        ('en revision', 'Lista para revisión'),
        ('completada', 'Completada')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='task_author')
    creation_date = models.DateTimeField(auto_now=True, null=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=False, blank=False)

    stauts = models.CharField(
        choices = STATUS_CHOICES,
        max_length = 13,
        default = 'pendiente',
        blank = False,
        null = False
    )
    
    assigned_members = models.ManyToManyField(User, related_name='assigned_members')

    activity = models.ManyToManyField(
        User,
        through = 'TaskActivity',
        through_fields= ('task', 'user')
    )


class TaskActivity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    description = models.CharField(max_length=256, null=False)


class Association(models.Model):
    antecedent = models.CharField(max_length=6, null=False)
    consequent = models.CharField(max_length=6, null=False)
    
    confidence = models.DecimalField(
        max_digits = 4,
        decimal_places = 3,
        null = False
    )

    support = models.DecimalField(
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
        unique_together = ('antecedent', 'consequent')

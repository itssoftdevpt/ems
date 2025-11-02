import uuid

from django.conf import settings
from django.db import models


class Programme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    recommended_class_size = models.PositiveIntegerField(default=40)

    class Meta:
        ordering = ('order',)
        unique_together = ('programme', 'name')

    def __str__(self) -> str:
        return f"{self.programme.name} - {self.name}"


class AcademicLevel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        unique_together = ('section', 'name')

    def __str__(self) -> str:
        return f"{self.section.name} - {self.name}"


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.ForeignKey(AcademicLevel, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    workload_hours = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('name',)
        unique_together = ('level', 'code')

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class GradingScheme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='grading_schemes')
    min_score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    grade = models.CharField(max_length=5)
    remark = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ('-min_score',)

    def __str__(self) -> str:
        return f"{self.grade}: {self.min_score}-{self.max_score}"


class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.ForeignKey(AcademicLevel, on_delete=models.CASCADE, related_name='classrooms')
    name = models.CharField(max_length=100)
    stream = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(default=40)
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coordinated_classrooms',
    )
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='homeroom_classrooms',
    )

    class Meta:
        unique_together = ('level', 'name', 'stream')
        ordering = ('level__order', 'name', 'stream')

    def __str__(self) -> str:
        stream = f" {self.stream}" if self.stream else ''
        return f"{self.level.name}{stream}"


class SubjectAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subject_allocations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='allocations')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subject_allocations')
    weekly_periods = models.PositiveIntegerField(default=4)

    class Meta:
        unique_together = ('classroom', 'subject')

    def __str__(self) -> str:
        return f"{self.subject} -> {self.teacher}"


class LessonPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson_plans')
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    objectives = models.TextField()
    resources = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('subject', 'week_number', 'title')
        ordering = ('subject', 'week_number')

    def __str__(self) -> str:
        return f"{self.subject.name} - Week {self.week_number}"


class SyllabusProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name='progress_entries')
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('updated_at',)

    def __str__(self) -> str:
        return f"{self.lesson_plan} - {self.completion_percentage}%"

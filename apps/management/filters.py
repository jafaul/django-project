import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from .models import Course

User = get_user_model()


class CourseFilterSet(django_filters.FilterSet):
    tags = django_filters.ChoiceFilter(
        label=_("Tag"),
        method='filter_tags', choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})

    )
    teacher = django_filters.ModelChoiceFilter(
        label=_("Teacher"),
        method='filter_teacher', queryset=User.objects.filter(position='teacher').all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_datetime = django_filters.DateFilter(
        label=_("Start Date"),
        method='filter_start', lookup_expr='gte',
        widget = forms.DateTimeInput(attrs={
            "type": "date",
            "class": "form-control",
            "id": "start-datetime",
        })
    )

    class Meta:
        model = Course
        fields = ['tags', 'teacher', 'start_datetime']

        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tags = Course.objects.values_list("tags", flat=True).distinct()
        unique_tags = sorted(set(tag for tag_list in tags for tag in tag_list))
        print(unique_tags)
        self.filters['tags'].extra.update({'choices': [(tag, tag) for tag in unique_tags]})

    def filter_tags(self, queryset, name, value):
        return queryset.filter(**{f"{name}__icontains": value})

    def filter_teacher(self, queryset, name, value):
        return queryset.filter(teacher__email=value)

    def filter_start(self, queryset, name, value):
        return queryset.filter(start_datetime__gte=value)


class RatingFilter(django_filters.FilterSet):
    avg_mark = django_filters.NumberFilter(
        label=_("Avg Mark"),
        method='filter_avg_mark',
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "id": "avg-mark",
        })
    )
    sum_mark = django_filters.NumberFilter(
        label=_("Sum Mark"),
        method='filter_sum_mark',
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "id": "sum-mark",
        })
    )

    tasks_done = django_filters.NumberFilter(
        label=_("Tasks Done"),
        method='filter_tasks_done',
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "id": "tasks-done",
        })
    )

    class Meta:
        model = Course
        fields = ['avg_mark', 'sum_mark', 'tasks_done']

    def filter_avg_mark(self, queryset, name, value):
        queryset.filter(

        )


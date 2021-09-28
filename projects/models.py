import uuid
from django.db import models
from django.urls import reverse
from users.models import Profile


class Project(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    owner = models.ForeignKey(
        Profile,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    demo_link = models.URLField(max_length=400, blank=True)
    source_link = models.URLField(max_length=400, blank=True)
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='projects')
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'id': self.id})
    
    def get_update_url(self):
        return reverse('projects:update_project', kwargs={'id': self.id})
    
    def get_delete_url(self):
        return reverse('projects:delete_project', kwargs={'id': self.id})

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-date_created', 'title']
    
    @property
    def image_URL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    
    @property
    def reviewers(self):
        queryset = self.reviews.all().values_list('owner__id', flat=True)
        return queryset

    def update_vote_count(self):
        reviews = self.reviews.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()
        ratio = up_votes / total_votes * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        (None, ''),
        ('up', 'Up Vote'),
        ('down', 'Down Vote'))

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='reviews')
    body = models.TextField(blank=True)
    value = models.CharField(
        max_length=100,
        choices=VOTE_TYPE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [
            ['owner', 'project']
        ]


class Tag(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from __future__ import print_function

from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from taggit.models import Tag

from .models import Note

from oauth2client import client
from googleapiclient import sample_tools


class NotesIndexView(generic.ListView):
    template_name = 'blog_app/notes_index.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date')[:50]


def note_details_view(request, url):
    note = get_object_or_404(Note, url=url)
    return render(request, 'blog_app/note_details.html', {'note': note})


def tag_notes(request, slug):
    ctx = {
        'tag': get_object_or_404(Tag, slug=slug),
        'notes': Note.objects.filter(tags__slug=slug),
    }
    return render(request, 'blog_app/notes_index.html', ctx)


def import_view(request):
    # Authenticate and construct service.
    scope = 'https://www.googleapis.com/auth/blogger'
    service, flags = sample_tools.init([], 'blogger', 'v3', __doc__, __file__,
                                       scope=scope)

    try:
        users = service.users()

        # Retrieve this user's profile information
        thisuser = users.get(userId='self').execute()
        print('This user\'s display name is: %s' % thisuser['displayName'])

        blogs = service.blogs()

        # Retrieve the list of Blogs this user has write privileges on
        thisusersblogs = blogs.listByUser(userId='self').execute()
        blog = thisusersblogs['items'][0]
        print('The blog named \'%s\' is at: %s' % (blog['name'], blog['url']))
        posts = service.posts()
        request = posts.list(blogId=blog['id'])
        while request != None:
            posts_doc = request.execute()
            if 'items' in posts_doc and not (posts_doc['items'] is None):
                for post in posts_doc['items']:
                    note = Note(title=post['title'], pub_date = post[
                        'published'], body_html = post['content'])
                    for tag in post['labels']:
                        note.tags.add(tag)
                    note.save()
                request = posts.list_next(request, posts_doc)

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize')

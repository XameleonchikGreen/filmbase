from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Country, Film, Genre, Person, Group, Conversation, Message, Membership
from .forms import CountryForm, GenreForm, FilmForm, PersonForm, ConversationForm, MessageForm
from .helpers import paginate
from django.contrib import messages
from django.utils import timezone


def check_admin(user):
    return user.is_superuser


def check_superuser_or_admin(user, group):
    memberships = user.membership_set.filter(group=group)
    if memberships.count() == 0:
        return user.is_superuser
    return user.is_superuser or memberships[0].is_admin


def check_superuser_or_participant(user, group):
    memberships = user.membership_set.filter(group=group)
    return (user.is_superuser or
            (memberships.count() > 0 and not memberships[0].is_waiter))


def check_superuser_author_admin(user, message):
    return (check_superuser_or_admin(user, message.conversation.group)
            or user == message.user)


def country_list(request):
    countries = Country.objects.all()
    return render(request, 'films/country/list.html', {'countries': countries})


def country_detail(request, id):
    country = get_object_or_404(Country, id=id)
    films = Film.objects.filter(country=country)

    films = paginate(request, films)
    return render(request, 'films/country/detail.html',
                  {'country': country, 'films': films})


@user_passes_test(check_admin)
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            messages.success(request, 'Страна добавлена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm()
    return render(request, 'films/country/create.html', {'form': form})


@user_passes_test(check_admin)
def country_update(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, 'Страна изменена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm(instance=country)
    return render(request, 'films/country/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def country_delete(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        country.delete()
        messages.success(request, 'Страна удалена')
        return redirect('films:country_list')
    return render(request, 'films/country/delete.html',
                  {'country': country})


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'films/genre/list.html', {'genres': genres})


def genre_detail(request, id):
    genre = get_object_or_404(Genre, id=id)
    films = Film.objects.filter(genres=genre)

    films = paginate(request, films)
    return render(request, 'films/genre/detail.html',
                  {'genre': genre, 'films': films})


@user_passes_test(check_admin)
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, 'Жанр добавлен')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm()
    return render(request, 'films/genre/create.html', {'form': form})


@user_passes_test(check_admin)
def genre_update(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Жанр изменён')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm(instance=genre)
    return render(request, 'films/genre/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def genre_delete(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Жанр удалён')
        return redirect('films:genre_list')
    return render(request, 'films/genre/delete.html',
                  {'genre': genre})


def film_list(request):
    films = Film.objects.all()
    query = request.GET.get('query', '')
    if query:
        films = films.filter(name__icontains=query)
    films = paginate(request, films)
    return render(request, 'films/film/list.html', {'films': films,
                                                    'query': query})


def film_detail(request, id):
    queryset = Film.objects.prefetch_related("country", "genres", "director",
                                             "people")
    film = get_object_or_404(queryset, id=id)
    return render(request, 'films/film/detail.html',
                  {'film': film})


@user_passes_test(check_admin)
def film_create(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            messages.success(request, 'Фильм добавлен')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm()
    return render(request, 'films/film/create.html', {'form': form})


@user_passes_test(check_admin)
def film_update(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм изменён')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm(instance=film)
    return render(request, 'films/film/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def film_delete(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        film.delete()
        messages.success(request, 'Фильм удалён')
        return redirect('films:film_list')
    return render(request, 'films/film/delete.html',
                  {'film': film})


def person_list(request):
    people = Person.objects.all()
    query = request.GET.get('query', '')
    if query:
        people = people.filter(name__icontains=query)
    people = paginate(request, people)
    return render(request, 'films/person/list.html', {'people': people,
                                                      'query': query})


def person_detail(request, id):
    queryset = Person.objects.prefetch_related("film_set", "directed_films")
    person = get_object_or_404(queryset, id=id)
    return render(request, 'films/person/detail.html',
                  {'person': person})


@user_passes_test(check_admin)
def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            messages.success(request, 'Персона добавлена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm()
    return render(request, 'films/person/create.html', {'form': form})


@user_passes_test(check_admin)
def person_update(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Персона изменена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'films/person/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def person_delete(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Персона удалена')
        return redirect('films:person_list')
    return render(request, 'films/person/delete.html',
                  {'person': person})


@login_required
def group_create(request, id):
    film = get_object_or_404(Film, id=id)

    group = Group.objects.create(
        name=film.name + ' группа',
        film=film
    )
    group.save()

    member = Membership.objects.create(
        user=request.user,
        group=group
    )
    member.is_admin = True
    member.is_waiter = False
    member.save()

    messages.success(request, 'Группа создана')
    return redirect('films:film_detail', id=id)


def group_detail(request, id):
    group = get_object_or_404(Group, id=id)

    convs = group.conversation_set.all()
    convs = paginate(request, convs, per=6)

    memberships = group.membership_set.all()

    admins = memberships.filter(is_admin=True)
    admins = paginate(request, admins, per=5)

    members = memberships.filter(is_admin=False, is_waiter=False)
    members = paginate(request, members, per=5)

    waiters = memberships.filter(is_waiter=True)
    waiters = paginate(request, waiters, per=5)

    return render(request, 'films/group/detail.html',
                  {'group': group, 'admins': admins, 'members': members,
                   'waiters': waiters, 'convs': convs})


@login_required
def group_wait(request, id):
    group = get_object_or_404(Group, id=id)

    member = Membership.objects.create(
        user=request.user,
        group=group
    )
    member.save()

    messages.success(request, 'Ваш запрос отправлен')
    return redirect('films:group_detail', id=group.id)


def group_add_user(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=group_id)

    member = get_object_or_404(Membership, id=member_id)
    member.is_waiter = False
    member.save()

    messages.success(request, 'Пользователь добавлен в группу')
    return redirect('films:group_detail', id=group_id)


def group_delete_user(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=group_id)

    member = get_object_or_404(Membership, id=member_id)

    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Пользователь удалён из группы')
        return redirect('films:group_detail', id=group_id)
    return render(request, 'films/group/delete_user.html',
                  {'group': group, 'member': member})


def group_new_admin(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=group_id)

    new_admin = get_object_or_404(Membership, id=member_id)

    if request.method == 'POST':
        new_admin.is_admin = True
        new_admin.save()
        messages.success(request, 'Администратор добавлен')
        return redirect('films:group_detail', id=group_id)
    return render(request, 'films/group/new_admin.html',
                  {'group': group, 'new_admin': new_admin})


def group_delete_admin(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=group_id)

    new_admin = get_object_or_404(Membership, id=member_id)

    if request.method == 'POST':
        new_admin.is_admin = False
        new_admin.save()
        messages.success(request, 'Администратор удалён')
        return redirect('films:group_detail', id=group_id)
    return render(request, 'films/group/delete_admin.html',
                  {'group': group, 'new_admin': new_admin})


def group_delete(request, id):
    film = get_object_or_404(Film, id=id)
    group = film.group

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:film_detail', id=id)

    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Группа удалена')
        return redirect('films:film_detail', id=id)
    return render(request, 'films/group/delete.html',
                  {'film': film})


def conversation_create(request, id):
    group = get_object_or_404(Group, id=id)

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=group.film.id)

    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            conv = form.save(commit=False)
            conv.group = group
            conv.save()
            messages.success(request, 'Обсуждение создано')
            return redirect('films:group_detail', id=group.id)
    else:
        form = ConversationForm()
    return render(request, 'films/conv/create.html',
                  {'group': group, 'form': form})


def conversation_detail(request, id):
    conv = get_object_or_404(Conversation, id=id)

    messes = conv.message_set.filter(deleted_at=None)
    messes = paginate(request, messes)

    form = MessageForm()
    return render(request, 'films/conv/detail.html',
                  {'conv': conv, 'form': form, 'messes': messes})


def conversation_update(request, id):
    conv = get_object_or_404(Conversation, id=id)

    if not check_superuser_or_admin(request.user, conv.group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=conv.group)

    if request.method == 'POST':
        form = ConversationForm(request.POST, instance=conv)
        if form.is_valid():
            form.save()
            messages.success(request, 'Обсуждение переименовано')
            return redirect('films:group_detail', id=conv.group.id)
    else:
        form = ConversationForm(instance=conv)
    return render(request, 'films/conv/update.html',
                  {'conv': conv, 'form': form})


def conversation_close(request, id):
    conv = get_object_or_404(Conversation, id=id)

    if not check_superuser_or_admin(request.user, conv.group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:conversation_detail', id=id)

    if request.method == 'POST':
        conv.closed_at = timezone.now()
        conv.save()
        messages.success(request, 'Обсуждение закрыто')
        return redirect('films:conversation_detail', id=id)
    return render(request, 'films/conv/close.html',
                  {'conv': conv})


def conversation_open(request, id):
    conv = get_object_or_404(Conversation, id=id)

    if not check_superuser_or_admin(request.user, conv.group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:conversation_detail', id=id)

    if request.method == 'POST':
        conv.closed_at = None
        conv.save()
        messages.success(request, 'Обсуждение открыто')
        return redirect('films:conversation_detail', id=id)
    return render(request, 'films/conv/open.html',
                  {'conv': conv})


def conversation_delete(request, id):
    conv = get_object_or_404(Conversation, id=id)
    group = conv.group

    if not check_superuser_or_admin(request.user, group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:group_detail', id=group.id)

    if request.method == 'POST':
        conv.delete()
        messages.success(request, 'Обсуждение удалено')
        return redirect('films:group_detail', id=group.id)
    return render(request, 'films/conv/delete.html',
                  {'conv': conv})


def message_create(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)

    if not check_superuser_or_participant(request.user, conv.group):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:conversation_detail', id=conv_id)

    form = MessageForm(request.POST, request.FILES)

    if form.is_valid():
        message = form.save(commit=False)
        message.user = request.user
        message.conversation = conv
        message.save()
        messages.success(request, 'Сообщение добавлено')

    return redirect('films:conversation_detail', id=conv_id)


def message_update(request, id):
    message = get_object_or_404(Message, id=id)

    if request.user != message.user:
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:conversation_detail', id=message.conversation.id)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение изменено')
            return redirect('films:conversation_detail', id=message.conversation.id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'films/comment/update.html',
                  {'mess': message, 'form': form})


def message_delete(request, id):
    message = get_object_or_404(Message, id=id)
    conv = message.conversation

    if not check_superuser_author_admin(request.user, message):
        messages.error(request, 'У вас недостаточно прав')
        return redirect('films:conversation_detail', id=conv.id)

    if request.method == 'POST':
        message.deleted_at = timezone.now()
        message.save()
        messages.success(request, 'Сообщение удалено')
        return redirect('films:conversation_detail', id=conv.id)
    return render(request, 'films/comment/delete.html',
                  {'mess': message})


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        people = Person.objects.all()
        if self.q:
            people = people.filter(name__istartswith=self.q)
        return people


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        countries = Country.objects.all()
        if self.q:
            countries = countries.filter(name__istartswith=self.q)
        return countries

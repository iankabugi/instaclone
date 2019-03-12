from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.


def insta(request):
    images = Image.all_images()
    return render(request, 'index.html', {"images": images})


def search_results(request):

    if 'image' in request.GET and request.GET["image"]:
        profile = request.GET.get("image")
        searched_images = Image.search_by_profile(profile)
        message = f"{profile}"
        return render(request, 'all-posts/search.html', {"message": message, "images": category})
    else:
        message = "No photos under this profile exist"
        return render(request, 'all-posts/search.html', {"message": message})
    return render(request, "all-posts/search.html")


def image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "all-posts/image.html", {"image": image})


@login_required(login_url='/accounts/login/')
def image(request, image_id):
    try:
        article = Article.objects.get(id=image_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "all-posts/post.html", {"image": image})


@login_required(login_url='/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('')

    else:
        form = NewIamgeForm()
    return render(request, 'all-news/new_post.html', {"form": form})

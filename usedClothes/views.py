from django.shortcuts import render
from .forms import ClothForm, ImageForm


def sell_home(request):
    form = ClothForm()
    image_form = ImageForm()
    context = {'form': form, 'image_form': image_form}
    if request.method == 'POST':
        image_form = ImageForm(request.POST)
        form = ClothForm(request.POST)
        if form.is_valid() and image_form.is_valid():
            print(form.cleaned_data, image_form.cleaned_data)
            context['message'] = 'The form is submitted'
    return render(request, 'usedClothes/sell_home.html', context=context)

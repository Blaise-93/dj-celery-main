from django.shortcuts import render, get_object_or_404
from .models import Project, Report,  Product
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from profiles.models import Profile, UserProfile
from django.http import JsonResponse
from reports.utils import get_report_image
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReportModelForm
import requests


def products(request):

    products = Product.objects.all()
    context = {"products":products}
    return render(request, "reports/product.html", context)

def load_products(request):
    context = None

    url = 'https://fakestoreapi.com/products'
    fake_products = requests.get(url)
    print(fake_products.json())
    product = fake_products.json()

    for res in product:
        products = Product.objects.create(
            title=res['title'],
            description=res['description'],
            price=res['price'],
            image=res['image']
        )

        context = {
            "products": products
        }
    

    return render(request, "reports/load_products.html", context)


def project_stats(request):

    queryset = Project.objects.all()
    # using list comprehension
    data = [
        {
            "Project": x.name,
            "Start": x.start_date,
            "Finish": x.end_date,
            "Responsible": x.responsible.user.userprofile
        } for x in queryset
    ]

    df = pd.DataFrame(data)
    figure = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Project",
        color="Responsible"
    )

    figure.update_yaxes(autorange="reversed")
    gannt_plot = plot(figure, output_type="div")

    context = {"plot_div": gannt_plot}

    return render(request, "reports/project_stats.html", context)



class ReportList(LoginRequiredMixin, generic.ListView):
    pass


# another approach with ModelForm
def generate_report_view(request):

    form = ReportModelForm(request.POST or None)
    if request.headers.get("X-requested-With") == "XMLHttpRequest":

        image = request.POST.get("image")
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)
        if form.is_valid():

            report = form.save(commit=False)
            report.image = img
            report.author = author
            report.save()

        data = {
            "report_success": {
                "excl": f"Hello {request.user}",
                "phrase": "Your report was successfully saved!"
            }}

        return JsonResponse(data, safe=False)


class ReportCreateView(LoginRequiredMixin,
                        generic.CreateView):

    def post(self, request):

        if request.headers.get("X-requested-With") == "XMLHttpRequest":
            name = self.request.POST.get("name")
            remarks = self.request.POST.get("remarks")
            image = self.request.POST.get("image")
            img = get_report_image(image)

            author = Profile.objects.get(user=self.request.user)

            # instantiate the field and save the report to the db
            report = Report()
            report.name = name
            report.remarks = remarks
            report.image = img
            report.author = author
            report.save()

        data = {
            "report_success": {
                "excl": f"Hello {request.user}",
                "phrase": "Your report was successfully saved!"
            }}
        return JsonResponse((data), safe=False)


""" def generate_report(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img = get_report_image(image)
        print(img)

        author = Profile.objects.get(user=request.user)
        # create report
        Report.objects.create(
            name=name,
            image=img,
            remarks=remarks,
            author=author
        )
        context = {
            "report_success": {
                "excl": request.user.username,
                "phrase": "Your report was successfully saved!"
            }
        }
        messages.info(request, context)
        return JsonResponse({"msg": "Your report was successfully saved"})
    return JsonResponse({})
 """
def bulky_batch(request):
    # example of how to handle a bulky query instances
    sent_favorites = set()
    existing_favorites = set()
    current_favorites = {}

    bulk_inserts, bulk_updates, bulk_deletes = [], [], []

    favorites = {} # an instance of a model 

    for favorite_number in sent_favorites - existing_favorites:
        bulk_inserts.append(Report(
            author=request.user.userprofile, **favorites.get(favorite_number))
            )


    for favorite_number in existing_favorites - sent_favorites:
        bulk_deletes.append(favorite_number)


    for favorite_number in sent_favorites.intersection(existing_favorites):
        favorite = current_favorites.get(favorite_number)
        favorite.order = favorites.get(favorite_number).get("order")
        bulk_updates.append(favorite)


    if bulk_inserts:
        Report.objects.bulk_create(bulk_inserts, batch_size=1000)

    if bulk_updates:
        Report.objects.bulk_update(bulk_updates, ['order'], batch_size=1000)

    if bulk_deletes:
        Report.objects.filter(
            author=request.user.userprofile, name__in=bulk_deletes).delete() 
        
    return render(request, "")



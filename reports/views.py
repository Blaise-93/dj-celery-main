from django.shortcuts import render
from .models import Project
import pandas as pd
from plotly.offline import plot
import plotly.express as px


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


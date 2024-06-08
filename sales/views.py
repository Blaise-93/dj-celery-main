from django.shortcuts import render, redirect
from django.views import generic
from .models import Sales
from .forms import SalesSearchForm
import pandas as pd
from customers.models import Customer
from utils import (
    get_customer_from_id,
    get_salesman_from_id,
    convert_date_to_dd_mm_yy,
    convert_date,
    get_chart,
)
from django.contrib import messages
from reports.forms import ReportModelForm

#  source env/bin/activate
# python manage.py runserver


def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    main_df = None
    chart = None
    no_data = None
    sales_form = SalesSearchForm(request.POST or None)

    report_form = ReportModelForm()

    # salesman = request.user.userprofile
    # customer = Customer.objects.get(name=customer)
    # customer_id = Sales.objects.filter(customer=customer)

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_by = request.POST.get("result_by")

        # access the date_created object
        sales = Sales.objects.filter(
            date_created__lte=date_to, date_created__gte=date_from)[:10]

        if len(sales) > 0:
            sales_df = pd.DataFrame(sales.values())
            sales_df["customer_id"] = sales_df["customer_id"].\
                apply(get_customer_from_id)
            sales_df["salesman_id"] = sales_df["salesman_id"].\
                apply(get_salesman_from_id)

            # modify date_created
            def date_in_yy_mm_dd(x): return x.strftime("%y/%m/%d")

            sales_df['date_created'] = sales_df["date_created"].\
                apply(((date_in_yy_mm_dd)))

            sales_df["date_updated"] = sales_df['date_updated'].\
                apply(date_in_yy_mm_dd)

            # modify salesdf colum
            sales_df.rename(
                {"customer_id": "customer",
                 "salesman_id": "salesman",
                 "id": "sales_id"
                 },

                axis=1, inplace=True)

            # create additional column in the sales_df
            # sales_df["sales_id"] = sales_df["id"]

            # Position DF logic
            positions_data = []

            for sale in sales:
                for position in sale.get_positions():
                    obj = {
                        "position_id": position.id,
                        "product": position.product.name,
                        "quantity": position.quantity,
                        "price": position.price,
                        "sales_id": position.get_sales_id()

                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)

            # MERGE DF OF SALES AND POSITION TABLE USING PD
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            # GROUP TRANSACTIONS IDS BY TOTAL PRICE, you can use any args you want eg price
            main_df = merged_df.groupby(
                "transaction_id",
                as_index=False)['total_price'].agg("sum")

            # Charts Logic

            # for grouped or merged dataframe - practice section
            """
            labels = main_df['transaction_id'].values
            chart = get_chart(chart_type, main_df,
                              labels=labels)
            """

            chart = get_chart(chart_type, sales_df, result_by)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            main_df = main_df.to_html()

        else:
            context = {
                "no_data": {
                    "excl": "Holy Molly",
                    'phrase': "No data available in this date range."
                }
            }
            return render(request, "sales/index.html",context)

        # print(date_from, date_to, chart_type)
    context = {

        "sales_form": sales_form,
        "sales_df": sales_df,
        "positions_df": positions_df,
        "merged_df": merged_df,
        "main_df": main_df,
        "chart": chart,
        "report_form": report_form


    }

    return render(request, "sales/index.html", context)


class SaleListView(generic.ListView):

    queryset = Sales.objects.all()
    context_object_name = "sales"
    template_name = 'sales/sales_list.html'


""" class SalesDetailView(generic.DetailView):
    queryset = Sales.objects.all()
    context_object_name = "sales"
    template_name = 'sales/sales_detail.html' """


def sales_detail(request, **kwargs):

    sales = Sales.objects.get(pk=kwargs['pk'])
    context = {"sales": sales}

    return render(request, 'sales/sales_detail.html', context)


def sales_delete(request, pk):

    print(pk)
    sales = Sales.objects.get(pk=pk)
    context = {"sales": sales}

    return render(request, 'sales/sales_delete.html', context)

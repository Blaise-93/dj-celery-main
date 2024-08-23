import random
import string
import uuid
from customers.models import Customer
from profiles.models import Profile
import pandas as pd
from datetime import datetime
import re
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import seaborn as sns


def slug_modifier():
    """
    Generate a random string code as an adjunct to the patients' slug to
    mask it from the user or any other person viewing the URI. 
    So, we don't want the set slug to be easily identified.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))


def files(file):
    """ A helper function to upload and read individual file when sending emails to
    the user. """
    with open(file, "r", encoding="utf8") as f:
        data = f.read()
        return data


def generate_patient_unique_code():
    """
    Generate a random, unique order number using UUID for our patients
    """
    code = uuid.uuid4().hex.upper()
    return code[0:10]


def generate_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    # code = uuid.uuid4().hex.lower()[:12]

    return code


def get_salesman_from_id(value):
    salesman = Profile.objects.get(id=value)
    return salesman.user.username


def get_customer_from_id(value):

    customer = Customer.objects.get(id=value)
    return customer


def get_graph():
    """ used to get the graph after using the buffer """

    buffer = BytesIO()

    plt.savefig(buffer, format='png')
    # set the cursor in the beginning of
    # the stream
    buffer.seek(0)

    # retrieve entire content of the file
    image_png = buffer.getvalue()
    # use base 64 to encode the byte
    graph = base64.b64encode(image_png)
    # override the grph variable
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_key(result_by):
    if result_by == "#1":
        key = 'transaction_id'
        return key
    elif result_by == "#2":
        key = "date_created"
        return key
    # return key


def get_chart(chart_type, data, result_by, **kwargs):

    # backends is respnsible for drawing our plots, switching backends is the func we shall use.
    # is cool ANti Geometric Backend (AGG), and Switch Backend in Jupyter
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(10, 4))

    key = get_key(result_by)

    result_data = data.groupby(
        key, as_index=False
    )['total_price'].agg("sum")

    # refer to the forms chart_type numbers here
    if chart_type == "#1":
        print("Bar chart")
        # with matplotlib
        """  plt.bar(data["transaction_id"], data['total_price']) # you can use any of the data key as you want - eg price
        """
        # using result by
        plt.bar(result_data[key], result_data["total_price"])
        # with seaborn
        """ sns.barplot(x="transaction_id", y='total_price', data=data)
        """
        # with results_ by
        """ sns.barplot(x=key, y="total_price", data=result_data) """
    elif chart_type == "#2":
        print("Pie chart")
        # kwargs - are passed from main_df of the view
        """ 
        labels = kwargs.get("labels")
        print(labels)
      
        plt.pie(data=data, x="total_price", labels=labels)
        """
        # by (results by)
        plt.pie(data=result_data, x="total_price", labels=result_data[key].values )
    elif chart_type == "#3":
        print("Line chart")
        # with matplotlib
        # plt.plot(data["transaction_id"], data["total_price"], color="green", marker="o", linestyle="dashed")
        plt.plot(result_data[key], result_data["total_price"],
                 color="green", marker="+", linestyle="dashed")
    else:
        print("Oops! Failed to identify the chart type")
    # this will adjust the size of our chart to the fig size
    plt.tight_layout()
   # plt.title(f"Basic charts: {chart_type}")
    chart = get_graph()
    return chart


def convert_date_to_dd_mm_yy(date):
    date = pd.to_datetime(date, format="%y/%m/%d").strftime("%d/%m/%y")
    return date


today = "24/05/03"
print(convert_date_to_dd_mm_yy(today))


def convert_date(date):
    converted_date = datetime.strptime(date, "%y/%m/%d").strftime("%d/%m/%y")
    return converted_date


def change_date_format(dt):
    return re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\3/\2/\1', dt)


input_date = "24/05/03"
converted_date = change_date_format(input_date)








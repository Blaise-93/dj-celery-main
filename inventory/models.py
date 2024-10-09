from django.db import models
from utils import (
    generate_code,
    generate_patient_unique_code as slug_modifier,
    convert_date_to_dd_mm_yy
)
from .regexes import *
from django.utils import timezone
from django.utils.text import slugify


class Product(models.Model):
    """
    Represents a product with details such as name, group,
    description, pricing, and user association.
    """
    GROUP_CHOICES = (
        ("Antibiotics", 'Antibiotics'),
        ("Hypertensive_Drugs", 'Hypertensive Drugs'),
        ("Analgesics", 'Analgesics'),
        ("Supplements", 'Supplements'),
        ("Diabetic_Drugs", 'Diabetic Drugs'),
        ("Cough Syrups", 'Cough Syrups'),
        ("COPDS", 'COPDS'),
        ("Medical Lozenges", 'Medical Lozenges'),
        ("Injectables", 'Injectables'),
        ("Ashmatic_Drugs", 'Ashmatic Drugs'),
        ("Antihistamines", 'Antihistamines'),
        ("Haemanitics", 'Haemanitics'),
        ("Vital_Signs_Machine", 'Vital Signs Machine'),
        ("Ulcer_Drugs", 'Ulcer Drugs'),
        ("Antipsycotics", 'Antipsycotics'),
        ("Topicals", 'Topicals'),
        ("Suppositories", 'Suppositories'),
        ("Ophthalmic Drugs", 'Ophthalmic Drugs'),
        ("Nasal Drugs", 'Nasal Drugs'),
        ("Antivirals", 'Antivirals'),
        ("Anticancer", 'Anticancer'),
        ("Antilipidemia Drugs", 'Antilipidemia Drugs'),
        ("Libido_Enhancers", 'Libido Enhancers'),
        ("Contraceptives", 'Contraceptives'),
        ("Fertility_Medications", 'Fertility Medications'),
        ("Sedatives", 'Sedatives'),
        ("Dressings", 'Dressings'),
        ("Surgicals", 'Surgicals'),

        # Non pharmaceuticals
        ("Cosmetics", 'Cosmetics'),
        ("Beverages_and_Drinks", 'Beverages and Drinks'),
        ("Snacks_and_Biscuits", 'Snacks_and_Biscuits'),
        ("Toiletry", 'Toiletry'),

    )

    UNIT_CHOICES = (
        ("Pack", "Pack"),
        ("Satchets", "Satchets"),
        ("Units", "Units"),

    )

    name = models.CharField(max_length=100, unique=True)
    group_name = models.CharField(max_length=30, choices=GROUP_CHOICES)
    description = models.TextField()
    alt_description = models.CharField(
        editable=False, max_length=150, blank=True)
    unit = models.CharField(max_length=30, choices=UNIT_CHOICES)
    sales_price = models.DecimalField(decimal_places=2, max_digits=18)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=18)
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, editable=False,
                            help_text="Leave this field blank; it will be \
            automatically generated for you.",)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self) -> str:
        return f'{self.name} was created by {self.user}'

    def get_alt_description(self):
        if self.description <= 100:
            self.alt_description = f'{self.description}'
            return self.alt_description
        self.alt_description = f'{self.description[:97]}...'
        return self.alt_description


class Stock(models.Model):
    """
    Represents the stock details of a product, including quantity,
    stock level, and expiration dates.
    """
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    stock_level = models.IntegerField(null=True, blank=True)
    in_stock = models.BooleanField(
        default=False,
        help_text="Leave this field blank; it will be \
            automatically generated for you.")
    expiration_date = models.DateField(db_comment='the expiration date of the product')
    manufactured_date = models.DateField(db_comment="the date the stocked product was manufactured")
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, editable=False,
                            help_text="Leave this field blank; it will be \
            automatically generated for you.")
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self) -> str:
        return f'{self.item.name} stock level is {self.stock_level}'

    def get_stock_available(self):
        """ check and get the stock available
            based on the orders made by
            the customer. """

        if self.stock_level is not None:
            if self.stock_level <= 0:
                self.in_stock = False
            else:
                self.in_stock = True
            available_stock = self.stock_level
            return available_stock
        else:
            return 0  # as a default

    def save(self, *args, **kwargs):
        """ override the original save method to set the price
        according to if it has it is in-stock or not"""

        self.stock_level = self.get_stock_available()
        self.slug = slugify(self.item.name)[:51] + slug_modifier()[:5]
        super().save(*args, **kwargs)


class StockMovement(models.Model):
    """
    Represents the movement of stock between different branches or locations.
    """

    stock = models.ManyToManyField(Stock)
    quantity = models.IntegerField()
    branch_name = models.CharField(max_length=100)
    branch_location = models.CharField(
        max_length=100, verbose_name="location/Warehouse")
    timestamp = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, editable=False,
                            help_text="Leave this field blank; it will be \
            automatically generated for you.",)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)

    def __str__(self) -> str:
        return f'''{self.quantity} items was moved to
        {self.branch_name} on {convert_date_to_dd_mm_yy(self.date_created.date())}'''

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Stock Movement'

    # TODO
    def add_available_stock(self, pk):

        item = Product.objects.get(id=pk)
        stock_qs = Stock.objects.filter(item=item)
        if stock_qs.exists():
            stock = stock_qs[0]
            if stock.item.objects.filter(item__slug=item.slug).exists():
                for product in self.stock.all():
                    current_stock = product.stock_level - self.quantity
                if current_stock > 1:
                    self.quantity += 1
                    stock.save()
                    product.stock_level -= 1
                    item.save()

        if self.quantity:
            for product in self.stock.all():
                current_stock = product.stock_level - self.quantity
                print(current_stock)
            return current_stock

    def save(self, *args, **kwargs):
        """ override the original save method to set the price
        according to if it has it is in-stock or not"""

        self.slug = slugify(self.branch_name)[:51] + slug_modifier()[:3]

        super().save(*args, **kwargs)


class Supplier(models.Model):
    """
    Model representing a supplier.

    Attributes:
        companies_choices (tuple): Choices for the sector of the company.
        first_name (str): First name of the supplier.
        last_name (str): Last name of the supplier.
        email (str): Email address of the supplier.
        phone_number (str): Phone number of the supplier.
        address (str): Address of the supplier.
        companies_sector (str): Sector of the company.
        company_of_the_supplier (str): Name of the supplier's company.
        slug (str): Slug for the supplier.
        date_supplied (date): Date when the supplier was supplied.
        date_created (datetime): Date when the supplier record was created.
        date_updated (datetime): Date when the supplier record was last updated.
    """

    COMPANIES_CHOICES = (
        ("Pharmaceuticals", "Pharmaceuticals"),
        ("Cosmetics", "Cosmetics"),
        ("Food_and_Beverages", "Food and Beverages"),
        ("Medical_Devices", "Medical Devices"),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100, validators=[PHONE_REGEX])
    address = models.CharField(max_length=100)
    companies_sector = models.CharField(
        max_length=100, choices=COMPANIES_CHOICES)
    company_of_the_supplier = models.CharField(max_length=100)
    slug = models.SlugField(
        blank=True, null=True,
        editable=False,
        help_text="Leave this field blank; it will be \
            automatically generated for you.",)
    date_supplied = models.DateField(blank=True, editable=False)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the full name of the supplier.

        Returns:
            str: Full name of the supplier.
        """
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """
        Saves the supplier instance.

        Sets the date_supplied to the current date and generates a slug.
        """
        self.date_supplied = timezone.now().date()
        self.slug = slugify(self.get_full_name()) + slug_modifier()[:5]
        return super().save(*args, **kwargs)


class PurchaseOrder(models.Model):

    """
    Model representing an order.

    Attributes:
        status_choices (tuple): Choices for the status of the order.
        supplier (ForeignKey): Reference to the supplier.
        status (str): Status of the order.
        order_number (str): Number of the order.
        user (ForeignKey): Reference to the user profile.
        slug (str): Slug for the order.
        ordered (bool): Whether the order has been placed.
        date_supplied (date): Date when the order was supplied.
        date_created (datetime): Date when the order record was created.
        date_updated (datetime): Date when the order record was last updated.
    """

    STATUS_CHOICES = (
        ("placed", 'Placed'),
        ("pending", 'Pending'),
        ("confirmed", 'Confirmed'),
        ("processing", 'Processing'),
        ("shipped", 'Shipped'),
        ("in_transit", 'In transit'),
        ("delivered", 'Delivered'),
        ("cancelled", 'cancelled'),
        ("requested_refund", 'requested_refund'),
        ("refund_granted", 'refund_granted'),
        ("returned", 'returned'),

    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    order_number = models.CharField(
        max_length=15, blank=True,
        help_text="Leave this field blank; it will be \
            automatically generated for you.")
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, editable=False,
                            help_text="Leave this field blank; it will be \
            automatically generated for you.",)
    total_cost = models.DecimalField(max_digits=18, decimal_places=2)
    ordered = models.BooleanField(
        default=False,
        help_text="Tick the checkbox if ordered")
    date_supplied = models.DateField(blank=True, editable=False)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'''Order placed from {self.supplier.get_full_name()}
          of {self.supplier.company_of_the_supplier} with order code: {self.order_number}'''

    def save(self, *args, **kwargs):
        """
        Saves the order instance.

        Sets the date_supplied to the current date, generates a slug,
        and assigns an order number if not provided.

        """
        self.date_supplied = timezone.now().date()
        self.slug = slug_modifier()
        if self.order_number == '':
            self.order_number = generate_code()
        return super().save(*args, **kwargs)


class OrderItem(models.Model):

    """
    Order item manages item-level inventory and manage order
    fulfillment and shipping.

    ## Benefits: 
       Order item table allows:
        - Easy addition or removal of items from an order
        - Simple updates to item quantities or prices
        - avoidance of data duplication
        - avoidance of data inconsistency




    Attributes:

        purchase order (ForeignKey): Reference to the purchase order.
        product (ForeignKey): Reference to the product.
        quantity (int): Quantity of the ordered item purchased.
        unit price (int): Unit price of the order item.
        user (ForeignKey): Reference to the user profile.
        slug (str): Slug for the order.
        date_supplied (date): Date when the order was supplied.
        date_created (datetime): Date when the order record was created.
        date_updated (datetime): Date when the order record was last updated.

    """
    class Meta:
        ordering = ['-date_created']

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=18)
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    slug = models.SlugField(
        blank=True, null=True,
        editable=False,
        help_text="Leave this field blank; it will be \
            automatically generated for you.",
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.purchase_order.order_number}'


class Refund(models.Model):
    """
    Model representing a refund.

    Attributes:
        order (ForeignKey): Reference to the order.
        reason (str): Reason for the refund.
        accepted (bool): Whether the refund is accepted.
        email (str): Email address of the user requesting the refund.
        user (ForeignKey): Reference to the user profile.
        date_created (datetime): Date when the refund record was created.
        date_updated (datetime): Date when the refund record was last updated.
    """
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    customer_full_name = models.CharField(max_length=30)
    reason = models.TextField()
    accepted = models.BooleanField(
        default=False, help_text="Tick the checkbox if accepted")
    email = models.EmailField()
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    slug = models.SlugField(
        blank=True, null=True,
        editable=False,
        help_text="Leave this field blank; it will be \
            automatically generated for you.",
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.customer_full_name

    def save(self, *args, **kwargs):
        """
        Saves the supplier instance.

        Sets the date_supplied to the current date and generates a slug.
        """

        self.slug = slug_modifier()
        return super().save(*args, **kwargs)


from mongoengine import Document, StringField, DecimalField

class Product(Document):
  name = StringField(required=True)
  description = StringField()
  price = DecimalField(precision=2)

from cbslogistic.models import Article, Supplier, Order, Detail

Supplier1=Supplier(supplier_name="Kellner und Kunz")
Supplier2=Supplier(supplier_name="Bauhaus")

Article1=Article(article_label="Hammer", article_sensor_no = 1, article_sensor_status = "True")
Article2=Article(article_label="Nagel", article_sensor_no = 2, article_sensor_status = "True")
Article3=Article(article_label="Topf", article_sensor_no = 3, article_sensor_status = "True")

Supplier1.save()
Supplier2.save()
Article1.save()
Article2.save()


# 作者      : pengcheng
# 创建时间  : 2020/11/25 14:21 

from xeger import Xeger
import exrex
from faker import Faker
import rstr
from strgen import StringGenerator

x = Xeger(limit=10)
# print(x.xeger("^[a-z](?=.*[\u4E00-\u9FA5])[^\*/])"))

# print(exrex.getone("(^[a-z](?=.*[\u4E00-\u9FA5])[^\*/])",limit=10))
# fake = Faker("zh_CN")
# print(fake.name())
# print(fake.address())
# print(fake.ssn())
# print(fake.phone_number())
# print(fake.user_agent())
# print(fake.text(max_nb_chars=5))
# print(exrex.getone('[1-9]([^0-9]{4,10})'))
print(exrex.getone('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))


# print(rstr.rstr('[a-zA-Z]',10,include='1$%'))
# print(StringGenerator('[爱到覅据我i恩京拉萨大家发xdfgbdf]{10}&[\p]{2}').render_list(5,unique=True))
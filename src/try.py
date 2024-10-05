import tika
tika.initVM()
from tika import parser
parsed = parser.from_file('./files/sample.eml' ) ## , xmlContent=True)
print(parsed)

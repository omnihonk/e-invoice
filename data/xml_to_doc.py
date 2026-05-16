from drafthorse.models.document import Document
samplexml = open(
    "ZF_Extended_Maschinen-Serial_NR__BT-X-307.xml", "rb").read()
doc = Document.parse(samplexml, strict=False)
print(doc.trade.agreement.seller.name)

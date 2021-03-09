from lxml import etree, objectify
from lxml.etree import tostring
from lxml.builder import E
from io import BytesIO

class Node():
    @staticmethod
    def childTexts(node):
        texts={}
        for child in list(node):
            texts[child.tag]=child.text
        return texts

def getXml(filepath):
    with open(filepath, 'rb') as f:
        xml = f.read()
    root = etree.fromstring(xml)
    return root

def create_catalog(data, category):
    
    if(data.get('Type') and (data.get('GWLogo') and (data.get("Description")))):
        category.Type        = data["Type"]
        category.GWLogo      = data["GWLogo"]
        category.Description = data['Description']
    skuElemnt = objectify.Element("sku")
    
    skuElemnt.Color          = data.get("Color")
    skuElemnt.Size           = data.get("Size")
    skuElemnt.Length         = data.get("Length")
    skuElemnt.Pack           = data.get("Pack")
    skuElemnt.Weight         = data.get("Weight")
    skuElemnt.Strength       = data.get("Strength")
    skuElemnt.Partnum        = data.get("Partnum")
    category.append(skuElemnt)
    return category

def generate(xml, newXml):
    root = objectify.fromstring(newXml)
    category = objectify.Element("category")
    for node in xml.xpath('//category'):
        data=Node.childTexts(node)
        
        if(data.get('Type')):
            category = objectify.Element("category")
            category.Type        = data["Type"]
            category.GWLogo      = data["GWLogo"]
            category.Description = data['Description']

            skuElemnt = objectify.Element("sku")
            
            skuElemnt.Color          = data.get("Color")
            skuElemnt.Size           = data.get("Size")
            skuElemnt.Length         = data.get("Length")
            skuElemnt.Pack           = data.get("Pack")
            skuElemnt.Weight         = data.get("Weight")
            skuElemnt.Strength       = data.get("Strength")
            skuElemnt.Partnum        = data.get("Partnum")

            category.append(skuElemnt)

        else:
            skuElemnt = objectify.Element("sku")
            
            skuElemnt.Color          = data.get("Color")
            skuElemnt.Size           = data.get("Size")
            skuElemnt.Length         = data.get("Length")
            skuElemnt.Pack           = data.get("Pack")
            skuElemnt.Weight         = data.get("Weight")
            skuElemnt.Strength       = data.get("Strength")
            skuElemnt.Partnum        = data.get("Partnum")
            
            category.append(skuElemnt)

        root.append(category)

    return root

def cleanup(root):
    objectify.deannotate(root, cleanup_namespaces=True, xsi_nil=True)

    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = BytesIO(etree.tostring(root))
    tree = etree.parse(file_obj, parser)

    with open ("finix.xml", "wb") as xml_writer:
        tree.write(xml_writer, pretty_print=True)


if __name__ == "__main__":
    xml = getXml('catalog.xml')
    newXml = '''<!--?xml version="1.0" encoding="UTF-8"?-->
                <catalog>
                </catalog>
    '''
    root = generate(xml, newXml)
    cleanup(root)
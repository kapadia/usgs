
# Template XML requests required by the USGS Inventory Service
# Requesting data like it's 1999

from xml.etree.ElementTree import Element, SubElement, tostring
from usgs import CATALOG_NODES, USGSApiKeyRequiredError, USGSCatalogNodeDoesNotExist, USGSDependencyRequired


def create_root_request():
    root = Element("soapenv:Envelope")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.set("xmlns:soapenv", "http://schemas.xmlsoap.org/soap/envelope/")
    root.set("xmlns:soap", "http://earthexplorer.usgs.gov/inventory/soap")

    header = SubElement(root, "soapenv:Header")
    body = SubElement(root, "soapenv:Body")
    
    return (root, body)


def create_request_type(parent, request_type):
    el = SubElement(parent, "soap:%s" % request_type)
    el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    return el


def create_api_key_element(parent, api_key):
    el = SubElement(parent, "apiKey")
    el.set("xsi:type", "xsd:string")
    el.text = api_key


def create_node_element(parent, node):
    
    if node not in CATALOG_NODES:
        raise USGSCatalogNodeDoesNotExist("Catalog nodes include %s" % ", ".join(CATALOG_NODES))
    
    el = SubElement(parent, "node")
    el.set("xsi:type", "xsd:string")
    el.text = node


def create_dataset_element(parent, dataset):
    el = SubElement(parent, "datasetName")
    el.set("xsi:type", "xsd:string")
    el.text = dataset


def create_entity_ids_element(parent, entityids):
    
    if isinstance(entityids, str):
        
        el = SubElement(parent, "entityId")
        el.set("xsi:type", "xsd:string")
        el.text = entityids
    
    else:
        
        el = SubElement(parent, "entityIds")
        el.set("xsi:type", "soap:ArrayOfString")
        
        for entityid in entityids:
            child = SubElement(el, "item")
            child.set("xsi:type","xsd:string")
            child.text = entityid


def create_service_class_coordinate(parent, name, latitude=None, longitude=None):
    
    el = SubElement(parent, name)
    el.set("xsi:type", "soap:Service_Class_Coordinate")
    
    lat_el = SubElement(el, "latitude")
    lat_el.set("xsi:type", "xsd:double")
    lat_el.text = str(latitude)
    
    lng_el = SubElement(el, "longitude")
    lng_el.set("xsi:type", "xsd:double")
    lng_el.text = str(longitude)


def clear_bulk_download_order(dataset, node, api_key=None):
    """
    This method is used to clear bulk download order information from the item basket.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = create_request_type(body, "clearBulkDownloadOrder")
    
    create_node_element(el, node)
    create_dataset_element(el, dataset)
    create_api_key_element(el, api_key)
    
    return tostring(root)


def clear_order(dataset, node, api_key=None):
    """
    This method is used to clear order information from the item basket.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = create_request_type(body, "clearOrder")
    
    create_node_element(el, node)
    create_dataset_element(el, dataset)
    create_api_key_element(el, api_key)
    
    return tostring(root)


def datasets(dataset, node, ll=None, ur=None, start_date=None, end_date=None, api_key=None):
    """
    This method is used to find datasets available for searching.
    By passing no parameters except node, all available datasets
    are returned. Additional parameters such as temporal range
    and spatial bounding box can be used to find datasets that 
    provide more specific data. The dataset name parameter can
    be used to limit the results based on matching the supplied
    value against the dataset name with assumed wildcards at the
    beginning and end. All parameters are optional except for 
    the 'node' parameter.
    
    :param dataset:
        Dataset Identifier
    
    :param ll:
        Lower left corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary
        
        e.g. { "longitude": 0.0, "latitude": 0.0 }
    
    :param ur:
        Upper right corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary
        
        e.g. { "longitude": 0.0, "latitude": 0.0 }
    
    :param start_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand
    
    :param end_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand
    
    :param node:
        The requested Catalog
    
    :param api_key:
        API key is not required.
        
    """
    
    root, body = create_root_request()
    
    el = create_request_type(body, "datasets")
    
    create_node_element(el, node)
    if dataset:
        create_dataset_element(el, dataset)
    
    if api_key:
        create_api_key_element(el, api_key)
    
    if ll and ur:
        
        create_service_class_coordinate(el, "lowerLeft", latitude=ll["latitude"], longitude=ll["longitude"])
        create_service_class_coordinate(el, "upperRight", latitude=ur["latitude"], longitude=ur["longitude"])
        
    if start_date:
        
        start_date_el = SubElement(el, "startDate")
        start_date_el.set("xsi:type", "xsd:string")
        start_date_el.text = start_date
        
    if end_date:
        
        end_date_el = SubElement(el, "endDate")
        end_date_el.set("xsi:type", "xsd:string")
        end_date_el.text = end_date
    
    return tostring(root)


def dataset_fields(dataset, node, api_key=None):
    """
    This request is used to return the metadata filter
    fields for the specified dataset. These values can
    be used as additional criteria when submitting search
    and hit queries.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is not required.
    """
    
    root, body = create_root_request()
    
    el = create_request_type(body, "datasetFields")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    
    if api_key:
        create_api_key_element(el, api_key)
    
    return tostring(root)


def download(dataset, node, entityids, products, api_key=None):
    """
    The use of this request will be to obtain valid data download URLs.
    
    :param dataset:
    
    :param entityIds:
        list
    
    :param products:
        list
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = create_request_type(body, "download")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    create_api_key_element(el, api_key)
    create_entity_ids_element(el, entityids)
    
    products_el = SubElement(el, "products")
    products_el.set("xsi:type", "soap:ArrayOfString")
    
    for product in products:
        product_el = SubElement(products_el, "item")
        product_el.set("xsi:type","xsd:string")
        product_el.text = product
        
    return tostring(root)


def download_options(dataset, node, entityids, api_key=None):
    """
    The use of the download options request is to discover the different download
    options for each scene. Some download options may exist but still be unavailable
    due to disk usage and many other factors. If a download is unavailable
    it may need to be ordered.
    
    :param dataset:
    
    :param node:
    
    :param entityIds:
    
    :param api_key:
        API key is not required.
    """
    
    root, body = create_root_request()
    
    el = create_request_type(body, "downloadOptions")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    
    if api_key:
        create_api_key_element(el, api_key)
    
    create_entity_ids_element(el, entityids)
    
    return tostring(root)


def get_bulk_download_products(dataset, node, entityids, api_key):
    """
    Retrieve bulk download products on a scene-by-scene basis.
    
    :param dataset:
    
    :param node:
    
    :param entityid:
        String or list of strings.
    
    :param api_key:
        API key is required.
        
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = create_request_type(body, "getBulkDownloadProducts")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    create_api_key_element(el, api_key)
    create_entity_ids_element(el, entityids)
    
    return tostring(root)


def get_order_products(dataset, node, entityids, api_key=None):
    """
    Retrieve orderable products on a scene-by-scene basis.
    
    :param dataset:
    
    :param node:
    
    :param entityid:
    
    :param api_key:
        API key is required.
    
    .. todo:: Support multiple scene request.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = create_request_type(body, "getOrderProducts")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    create_api_key_element(el, api_key)
    create_entity_ids_element(el, entityids)
    
    return tostring(root)


def item_basket(api_key=None):
    """
    Returns the current item basket for the current user.
    
    :param api_key:
        API key is required.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = create_request_type(body, "itemBasket")
    create_api_key_element(el, api_key)
    
    return tostring(root)


def login(username, password):
    """
    This method requires SSL be used due to the sensitive nature of
    users passwords. Upon a successful login, an API key will be
    returned. This key will be active for one hour and should be
    destroyed upon final use of the service by calling the logout
    method. Users must have "Machine to Machine" access based on
    a user-based role in the users profile.
    
    :param username:
    
    :param password:
    """
    
    root, body = create_root_request()
    
    el = create_request_type(body, "login")
    
    username_el = SubElement(el, "username")
    username_el.set("xsi:type", "xsd:string")
    username_el.text = username
    
    password_el = SubElement(el, "password")
    password_el.set("xsi:type", "xsd:string")
    password_el.text = password
    
    return tostring(root)


def logout(api_key=None):
    """
    Remove the users API key from being used in the future.
    
    :param api_key:
        API key is required.
    """
    
    root, body = create_root_request()
    
    el = create_request_type(body, "logout")
    create_api_key_element(el, api_key)
    
    return tostring(root)


def metadata(dataset, node, sceneids, api_key=None):
    """
    The use of the metadata request is intended for those who have
    acquired scene IDs from a different source. It will return the
    same metadata that is available via the search request.
    
    :param dataset:
    
    :param node:
    
    :param sceneid:
    
    :param api_key:
    """
    root, body = create_root_request()
    
    el = create_request_type(body, "metadata")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    
    if api_key:
        create_api_key_element(el, api_key)
    
    create_entity_ids_element(el, sceneids)
    
    return tostring(root)


def remove_bulk_download_scene():
    raise NotImplementedError


def remove_order_scene():
    raise NotImplementedError


def search(dataset, node, lat=None, lng=None, distance=100, ll=None, ur=None, start_date=None, end_date=None, where=None, max_results=50000, starting_number=1, sort_order="DESC", api_key=None):
    """
    :param dataset:
    
    :param node:
    
    :param lat:
    
    :param lng:
    
    :param ll:
    
    :param distance:
    
    :param ur:
    
    :param start_date:
    
    :param end_date:
    
    :param where:
        Specify additional search criteria
    
    :param max_results:
    
    :param starting_number:
    
    :param sort_order:
    
    :param api_key:
        API key is not required.
    """
    root, body = create_root_request()
    
    el = create_request_type(body, "search")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    
    # Latitude and longitude take precedence over ll and ur
    if lat and lng:
        
        try:
            import pyproj
            from shapely import geometry
        except ImportError:
            raise USGSDependencyRequired("Shapely and PyProj are required for spatial searches.")
        
        prj = pyproj.Proj(proj='aeqd', lat_0=lat, lon_0=lng)
        half_distance = 0.5 * distance
        box = geometry.box(-half_distance, -half_distance, half_distance, half_distance)
        
        lngs, lats = prj(*box.exterior.xy, inverse=True)
        
        ll = { "longitude": min(*lngs), "latitude": min(*lats) }
        ur = { "longitude": max(*lngs), "latitude": max(*lats) }
    
    if ll and ur:
        
        create_service_class_coordinate(el, "lowerLeft", latitude=ll["latitude"], longitude=ll["longitude"])
        create_service_class_coordinate(el, "upperRight", latitude=ur["latitude"], longitude=ur["longitude"])
        
    if start_date:
        
        start_date_el = SubElement(el, "startDate")
        start_date_el.set("xsi:type", "xsd:string")
        start_date_el.text = start_date
        
    if end_date:
        
        end_date_el = SubElement(el, "endDate")
        end_date_el.set("xsi:type", "xsd:string")
        end_date_el.text = end_date
    
    if where:
        
        # TODO: Support more than AND key/value equality queries
        additional_criteria_el = SubElement(el, "additionalCriteria")
        
        filter_type_el = SubElement(additional_criteria_el, "filterType")
        filter_type_el.text = "and"
        
        child_filters_el = SubElement(additional_criteria_el, "childFilters")
        for field_id, value in where.iteritems():
            child_item_el = SubElement(child_filters_el, "item")
            field_id_el = SubElement(child_item_el, "fieldId")
            field_id_el.text = str(field_id)
            item_filter_type_el = SubElement(child_item_el, "filterType")
            item_filter_type_el.text = "value"
            operand_el = SubElement(child_item_el, "operand")
            operand_el.text = "="
            value_el = SubElement(child_item_el, "value")
            value_el.text = str(value)

    if max_results:
        
        max_results_el = SubElement(el, "maxResults")
        max_results_el.set("xsi:type", "xsd:int")
        max_results_el.text = str(max_results)
        
    if starting_number:
        
        starting_number_el = SubElement(el, "startingNumber")
        starting_number_el.set("xsi:type", "xsd:int")
        starting_number_el.text = str(starting_number)
        
    if sort_order:
        
        sort_order_el = SubElement(el, "sortOrder")
        sort_order_el.set("xsi:type", "xsd:string")
        sort_order_el.text = sort_order
    
    if api_key:
        create_api_key_element(el, api_key)
    
    return tostring(root)


def submit_bulk_order():
    raise NotImplementedError


def submit_order():
    raise NotImplementedError


def update_bulk_download_scene():
    raise NotImplementedError


def update_order_scene():
    raise NotImplementedError

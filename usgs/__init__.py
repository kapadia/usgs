
__version__ = "0.3.1"

# The USGS API endpoint
USGS_API_DEPRECATED = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.0"
USGS_API = "https://m2m.cr.usgs.gov/api/api/json/stable"

#
# Two catalogs are available for querying
#

CATALOG_NODES = ["EE", "HDDS"]

# http://earthexplorer.usgs.gov/
EARTH_EXPLORER_CATALOG_NODE = "EE"

# http://hddsexplorer.usgs.gov/
HDDS_EXPLORER_CATALOG_NODE = "HDDS"

class USGSError(Exception):
    pass

class USGSApiKeyRequiredError(Exception):
    pass

class USGSAmbiguousNode(Exception):
    pass

class USGSDependencyRequired(ImportError):
    pass
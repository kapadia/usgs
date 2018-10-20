
__version__ = "0.2.5"

# The USGS API endpoint
USGS_API = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.0"

#
# Four catalogs are available for querying
#

CATALOG_NODES = ["CWIC", "EE", "HDDS", "LPVS"]

# http://lsiexplorer.cr.usgs.gov/
CWIC_LSI_EXPLORER_CATALOG_NODE = "CWIC"

# http://earthexplorer.usgs.gov/
EARTH_EXPLORER_CATALOG_NODE = "EE"

# http://hddsexplorer.usgs.gov/
HDDS_EXPLORER_CATALOG_NODE = "HDDS"

# http://lpvsexplorer.cr.usgs.gov/
LPCS_EXPLORER_CATALOG_NODE = "LPCS"

class USGSError(Exception):
    pass

class USGSApiKeyRequiredError(Exception):
    pass

class USGSAmbiguousNode(Exception):
    pass

class USGSDependencyRequired(ImportError):
    pass

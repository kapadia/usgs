
# The USGS API endpoint
endpoint = "https://earthexplorer.usgs.gov/inventory/soap"

#
# Four catalogs are available for querying
#

# http://lsiexplorer.cr.usgs.gov/
CWIC_LSI_EXPLORER_CATALOG_NODE = "CWIC"

# http://earthexplorer.usgs.gov/
EARTH_EXPLORER_CATALOG_NODE = "EE"

# http://hddsexplorer.usgs.gov/
HDDS_EXPLORER_CATALOG_NODE = "HDDS"

# http://lpvsexplorer.cr.usgs.gov/
LPVS_EXPLORER_CATALOG_NODE = "LPVS"

class USGSApiKeyRequiredError(Exception):
    pass
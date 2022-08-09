# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

class BaseConfig(object):

    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present
    WORKSPACE_ID = '3bce5991-023e-481c-b6ca-68a68b562f93'
    
    # Report Id for which Embed token needs to be generated
    REPORT_ID = 'c5fe6639-c22d-4bd5-90bf-de33ee26bd48'
    
    # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
    TENANT_ID = '3491150f-78a4-4b5f-8be2-eb365ecbcac6'
    
    # Client Id (Application Id) of the AAD app
    CLIENT_ID = '41c7bcce-5f1a-4d0b-8978-a4f90d782709'
    
    # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
    CLIENT_SECRET = 'N8D8Q~NcSFD-IvVyy7hNv83NP8saQrDyyKExyafv'
    
    # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
    SCOPE = ['https://analysis.usgovcloudapi.net/powerbi/api/.default']
    
    # URL used for initiating authorization request
    AUTHORITY = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode.
    POWER_BI_USER = ''
    
    # Master user email password. Required only for MasterUser authentication mode.
    POWER_BI_PASS = ''
import json
import boto3
import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Argumentos CLI
parser = argparse.ArgumentParser(description="Etiquetado automático de recursos en AWS o Azure.")
parser.add_argument("--cloud", choices=["aws", "azure"], required=True, help="Proveedor de nube (aws o azure)")
parser.add_argument("--subscription", help="ID de suscripción de Azure")
parser.add_argument("--resourcegroup", help="Nombre del resource group en Azure")
parser.add_argument("--awsaccount", help="ID de cuenta AWS")

args = parser.parse_args()

# Cargar configuración de tags
with open("tags.json", "r", encoding="utf-8") as f:
    required_tags = [tag["key"] for tag in json.load(f) if tag.get("required")]

with open("default_tags.json", "r", encoding="utf-8") as f:
    default_values = json.load(f)

# ======================= AWS =======================
def etiquetar_recursos_aws(account_id_filter):
    print("\n🔧 Etiquetando recursos en AWS...")

    sts = boto3.client("sts")
    current_account = sts.get_caller_identity()["Account"]
    if account_id_filter and current_account != account_id_filter:
        print(f"⛔ Cuenta AWS actual ({current_account}) no coincide con la permitida ({account_id_filter})")
        return

    client = boto3.client("resourcegroupstaggingapi")
    paginator = client.get_paginator("get_resources")

    for page in paginator.paginate(ResourcesPerPage=50):
        for resource in page["ResourceTagMappingList"]:
            arn = resource["ResourceARN"]
            current_tags = {tag["Key"]: tag["Value"] for tag in resource.get("Tags", [])}
            missing = [key for key in required_tags if key not in current_tags]
            if missing:
                tags_to_add = {key: default_values[key] for key in missing if key in default_values}
                if tags_to_add:
                    boto3.client("resourcegroupstaggingapi").tag_resources(
                        ResourceARNList=[arn],
                        Tags=tags_to_add
                    )
                    print(f"✅ AWS: {arn} → Tags agregados: {tags_to_add}")

# ======================= AZURE =======================
def etiquetar_recursos_azure(subscription_id, resource_group=None):
    print("\n🔧 Etiquetando recursos en Azure...")
    credential = DefaultAzureCredential()
    client = ResourceManagementClient(credential, subscription_id)

    resources = client.resources.list_by_resource_group(resource_group) if resource_group else client.resources.list()

    for resource in resources:
        if subscription_id not in resource.id:
            continue  # Saltear si no es la suscripción indicada

        current_tags = resource.tags or {}
        missing = [key for key in required_tags if key not in current_tags]
        if missing:
            tags_to_add = {key: default_values[key] for key in missing if key in default_values}
            if tags_to_add:
                merged_tags = current_tags.copy()
                merged_tags.update(tags_to_add)
                client.tags.update_at_scope(
                    scope=resource.id,
                    parameters={"properties": {"tags": merged_tags}}
                )
                print(f"✅ Azure: {resource.id} → Tags agregados: {tags_to_add}")

# ============ EJECUCIÓN ============
try:
    if args.cloud == "aws":
        etiquetar_recursos_aws(args.awsaccount)
    elif args.cloud == "azure":
        if not args.subscription:
            raise ValueError("Debes especificar --subscription para Azure")
        etiquetar_recursos_azure(args.subscription, args.resourcegroup)
except Exception as e:
    print("⚠️ Error:", e)
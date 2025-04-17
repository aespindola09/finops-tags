import json
from pathlib import Path

def cargar_tags_json(path='tags.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generar_azure_policy(tags):
    conditions = []
    for tag in tags:
        if tag.get('required', False):
            if tag.get('allowed_values'):
                conditions.append({
                    "field": f"tags['{tag['key']}']",
                    "notIn": tag["allowed_values"]
                })
            else:
                conditions.append({
                    "field": f"tags['{tag['key']}']",
                    "exists": "false"
                })

    return {
        "properties": {
            "displayName": "Validación de tags FinOps corporativos",
            "policyType": "Custom",
            "mode": "Indexed",
            "description": "Asegura que los recursos tengan los tags requeridos con valores válidos.",
            "metadata": {
                "category": "Tags"
            },
            "parameters": {},
            "policyRule": {
                "if": {
                    "anyOf": conditions
                },
                "then": {
                    "effect": "deny"
                }
            }
        }
    }

def generar_aws_policy(tags):
    aws_tags = {}
    for tag in tags:
        if "aws" in tag.get("applies_to", []):
            tag_block = {}
            if tag.get("allowed_values"):
                tag_block["tag_value"] = {
                    "enforced_values": tag["allowed_values"]
                }
            if tag.get("required", False):
                tag_block["tag_key"] = {
                    "enforced_for": ["ec2:instance", "s3:bucket", "rds:db"]
                }
            aws_tags[tag["key"]] = tag_block

    return {"tags": aws_tags}

def guardar_politicas(tags_path='tags.json', salida='tag-policy-output'):
    tags = cargar_tags_json(tags_path)
    azure = generar_azure_policy(tags)
    aws = generar_aws_policy(tags)

    output_dir = Path(salida)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "azure-policy.json", "w", encoding="utf-8") as f:
        json.dump(azure, f, indent=2)

    with open(output_dir / "aws-tag-policy.json", "w", encoding="utf-8") as f:
        json.dump(aws, f, indent=2)

    print(f"✔️ Políticas generadas en: {output_dir.absolute()}")

if __name__ == "__main__":
    guardar_politicas()
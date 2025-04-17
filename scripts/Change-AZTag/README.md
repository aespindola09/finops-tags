# 🛠️ Cambiar etiquetas en Azure (Masivo)

⏱️ **Tiempo de lectura: 3 minutos**

## 📄 Descripción

Este script en PowerShell busca todos los recursos y grupos de recursos en Azure que tienen la etiqueta `owner: valorA` y la cambia a `owner: valorB`. El script puede ejecutarse en una suscripción específica o en un grupo de recursos específico.

## Parámetros

- **SubscriptionId**: ID de la suscripción de Azure donde se ejecutará el script.
- **ResourceGroupName**: Nombre del grupo de recursos donde se ejecutará el script. Si no se especifica, el script se ejecutará en toda la suscripción.

## 📝 Uso

1. Guarda el script en un archivo `.ps1`, por ejemplo `Change-Tags.ps1`.
2. Abre PowerShell y navega al directorio donde guardaste el script.
3. Ejecuta el script con los parámetros adecuados:

### 🔧 Ejemplos

#### Ejecutar en una suscripción específica

```powershell
.\Change-AZTags.ps1 -SubscriptionId "tu-suscripcion-id"
```
#### Ejecutar en un grupo de recursos específica

```
.\Change-AZTags.ps1 -SubscriptionId "tu-suscripcion-id" -ResourceGroupName "tu-grupo-de-recursos"
```
### 💻 Script 


```
<#
.SYNOPSIS
    Script para cambiar la etiqueta 'owner: valorA' por 'owner: ValorB' en recursos y grupos de recursos en Azure.
.DESCRIPTION
    Este script busca todos los recursos y grupos de recursos en Azure que tienen la etiqueta 'owner: TEC-IT BUSINESS B' y la cambia a 'owner: TEC-IT BUSINESS RETAIL'.
.PARAMETER SubscriptionId
    ID de la suscripción de Azure donde se ejecutará el script.
.PARAMETER ResourceGroupName
    Nombre del grupo de recursos donde se ejecutará el script. Si no se especifica, el script se ejecutará en toda la suscripción.
.AUTHOR
    Alexis Espindola
#>

param (
    [string]$SubscriptionId,
    [string]$ResourceGroupName
)

# Iniciar sesión en Azure
Connect-AzAccount

# Seleccionar la suscripción si se especifica
if ($SubscriptionId) {
    Set-AzContext -SubscriptionId $SubscriptionId
}

# Definir las etiquetas a buscar y reemplazar
$oldTag = "ValorA"
$newTag = "ValorB"

# Función para cambiar el color del texto
function Write-Color {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Message,

        [Parameter(Mandatory=$true)]
        [string]$Color
    )
    switch ($Color.ToLower()) {
        "red" { Write-Host $Message -ForegroundColor Red }
        "green" { Write-Host $Message -ForegroundColor Green }
        "yellow" { Write-Host $Message -ForegroundColor Yellow }
        "cyan" { Write-Host $Message -ForegroundColor Cyan }
        default { Write-Host $Message }
    }
}

# Obtener todos los recursos con la etiqueta 'owner: TEC-IT BUSINESS DWS'
if ($ResourceGroupName) {
    $resources = Get-AzResource -ResourceGroupName $ResourceGroupName -Tag @{owner=$oldTag}
} else {
    $resources = Get-AzResource -Tag @{owner=$oldTag}
}

# Cambiar la etiqueta de los recursos
foreach ($resource in $resources) {
    $resource.Tags['owner'] = $newTag
    Set-AzResource -ResourceId $resource.ResourceId -Tag $resource.Tags -Force
    Write-Color -Message "Etiqueta cambiada para el recurso: $($resource.Name)" -Color "Green"
}

# Obtener todos los grupos de recursos con la etiqueta 'owner: TEC-IT BUSINESS DWS'
if ($ResourceGroupName) {
    $resourceGroups = Get-AzResourceGroup -ResourceGroupName $ResourceGroupName -Tag @{owner=$oldTag}
} else {
    $resourceGroups = Get-AzResourceGroup -Tag @{owner=$oldTag}
}

# Cambiar la etiqueta de los grupos de recursos
foreach ($resourceGroup in $resourceGroups) {
    $resourceGroup.Tags['owner'] = $newTag
    Set-AzResourceGroup -Name $resourceGroup.ResourceGroupName -Tag $resourceGroup.Tags
    Write-Color -Message "Etiqueta cambiada para el grupo de recursos: $($resourceGroup.ResourceGroupName)" -Color "Cyan"
}

Write-Color -Message "Proceso completado." -Color "Yellow"

```

### 📝 Notas

Asegúrate de tener los permisos adecuados para modificar las etiquetas de los recursos y grupos de recursos en la suscripción de Azure especificada.

El script requiere que tengas instalado el módulo Az de Azure PowerShell. Si no lo tienes, puedes instalarlo con el siguiente comando:

```
Install-Module -Name Az -AllowClobber -Force

```
Para iniciar sesión en Azure, se utiliza el cmdlet:

```
Connect-AzAccount

```
Asegúrate de que tus credenciales tengan acceso a la suscripción y los recursos necesarios.

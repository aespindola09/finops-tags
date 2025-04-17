<#
.SYNOPSIS
    Script para cambiar la etiqueta 'owner: ValorA' por 'owner: ValorB' en recursos y grupos de recursos en Azure.
.DESCRIPTION
    Este script busca todos los recursos y grupos de recursos en Azure que tienen la etiqueta 'owner: ValorA' y la cambia a 'owner: ValorB'.
.PARAMETER SubscriptionId
    ID de la suscripción de Azure donde se ejecutará el script.
.PARAMETER ResourceGroupName
    Nombre del grupo de recursos donde se ejecutará el script. Si no se especifica, el script se ejecutará en toda la suscripción.
.AUTHOR
    Alexis Espindola - aespindola09@gmail.com
#>

param (
    [string]$SubscriptionId,
    [string]$ResourceGroupName
)

# Iniciar sesion en Azure
Connect-AzAccount

# Seleccionar la suscripcion si se especifica
if ($SubscriptionId) {
    Set-AzContext -SubscriptionId $SubscriptionId
}

# Definir las etiquetas a buscar y reemplazar
$oldTag = "valorA"
$newTag = "valorB"

# Funcion para cambiar el color del texto
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

# Obtener todos los recursos con la etiqueta 'owner: $oldtag'
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

# Obtener todos los grupos de recursos con la etiqueta 'owner: $oldtag'
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


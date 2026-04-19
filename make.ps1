param([string]$command="ayuda",
      [string]$ARCHIVO="arbol_diretorio"
    )

switch($command){
    "arbol_archivos"{
        cmd /c "tree /f /a" | Out-File -FilePath ".\$ARCHIVO.txt"
    }
    "limpieza"{
        
    }
    default {
        Write-Host "--MENU AYUDA" -ForegroundColor Red
        Write-Host "comandos"
        Write-Host ".\make.ps1 arbol_archivos ARCHIVO.txt"
    }
}
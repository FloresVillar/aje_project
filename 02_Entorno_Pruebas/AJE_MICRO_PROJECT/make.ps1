param([string]$command="ayuda",
      [string]$ARCHIVO="arbol_directorio"
    )

switch($command){
    "arbol_archivos"{
        cmd /c "tree /f /a" | Out-File -FilePath ".\$ARCHIVO.txt"
    }
    "limpieza"{
        
    }
    "levantar_sistema"{
        docker compose up --build
    }
    "buscar_errores"{
        ruff check .
    }
    "activar_entorno_virtual"{
        .\.venv_aje\Scripts\Activate.ps1
    }
    default {
        Write-Host "--MENU AYUDA" -ForegroundColor Red
        Write-Host "comandos"
        Write-Host ".\make.ps1 arbol_archivos ARCHIVO.txt"
    }
}
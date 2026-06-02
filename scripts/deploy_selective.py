#!/usr/bin/env python3
"""
Deploy selectivo - Sube Sony-Web EXCEPTO IMG (muy pesada)
Uso:
  python scripts/deploy_selective.py
  python scripts/deploy_selective.py --auto
  python scripts/deploy_selective.py --merge
"""
import argparse
import subprocess
import sys
import os
import datetime


def run(cmd, cwd=None, show_output=False):
    """Ejecuta comando y retorna resultado"""
    if show_output:
        print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if show_output and r.stdout:
        print(r.stdout)
    return r


def git_root():
    """Obtiene raiz del repo git"""
    r = run(['git', 'rev-parse', '--show-toplevel'])
    if r.returncode != 0:
        print('❌ No se encontró un repositorio Git', file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()


def get_changed_files(path_prefix):
    """Obtiene archivos modificados en Sony-Web EXCEPTO IMG"""
    r = run(['git', 'status', '--porcelain', path_prefix])
    if r.returncode != 0:
        return []
    
    files = []
    for line in r.stdout.strip().split('\n'):
        if not line:
            continue
        # Formato: " M Sony-Web/index.html" o "?? Sony-Web/file"
        status = line[:2]
        filepath = line[3:]
        
        # Excluir IMG/
        if 'IMG/' in filepath or 'IMG\\' in filepath:
            continue
        files.append({'status': status.strip(), 'path': filepath})
    
    return files


def main():
    p = argparse.ArgumentParser(description='Deploy selectivo (Sony-Web sin IMG)')
    p.add_argument('--auto', '-a', action='store_true', help='No pedir confirmación (auto)')
    p.add_argument('--merge', '-M', action='store_true', help='Merge a main después de push')
    p.add_argument('--target', '-t', default='main', help='Branch target para merge')
    args = p.parse_args()

    root = git_root()
    os.chdir(root)
    
    path_prefix = 'Sony-Web'
    
    # Obtener archivos a subir
    files_to_upload = get_changed_files(path_prefix)
    
    if not files_to_upload:
        print(f"✓ No hay cambios en {path_prefix} para subir")
        return
    
    # Listar archivos
    print(f"\n📁 Archivos a subir ({len(files_to_upload)}):\n")
    for f in files_to_upload:
        status_icon = "✏️  " if f['status'] == 'M' else "🆕" if f['status'] == 'A' else "🗑️  "
        print(f"  {status_icon} {f['path']}")
    
    if not args.auto:
        print(f"\n¿Confirmar upload? (s/n): ", end='')
        choice = input().strip().lower()
        if choice != 's':
            print("❌ Cancelado")
            return
    
    # Crear rama
    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    branch_name = f"deploy-sony-web-{ts}"
    
    print(f"\n🔄 Creando rama: {branch_name}")
    r = run(['git', 'checkout', '-b', branch_name], show_output=False)
    if r.returncode != 0:
        print(f"❌ Error al crear rama: {r.stdout}")
        sys.exit(1)
    
    # Agregar archivos
    print(f"📝 Agregando {len(files_to_upload)} archivo(s)...")
    for f in files_to_upload:
        filepath = f['path']
        run(['git', 'add', filepath])
    
    # Commit
    msg = f"Deploy: Sony-Web updates ({len(files_to_upload)} files) - {datetime.datetime.now().isoformat()}"
    print(f"💾 Commit: {msg}")
    r = run(['git', 'commit', '-m', msg], show_output=False)
    if r.returncode != 0:
        print(f"❌ Commit falló: {r.stdout}")
        sys.exit(1)
    
    # Push
    print(f"📤 Push a origin/{branch_name}...")
    r = run(['git', 'push', '-u', 'origin', branch_name], show_output=False)
    if r.returncode != 0:
        print(f"❌ Push falló: {r.stdout}")
        sys.exit(1)
    
    print(f"✅ Rama subida: {branch_name}")
    
    # Mostrar PR link
    remote = run(['git', 'config', '--get', 'remote.origin.url'])
    if remote.returncode == 0:
        rurl = remote.stdout.strip()
        if 'github.com' in rurl:
            if rurl.startswith('git@'):
                repo = rurl.split(':', 1)[1].rstrip('.git')
            else:
                repo = rurl.split('github.com/')[-1].rstrip('.git')
            pr_url = f"https://github.com/{repo}/pull/new/{branch_name}"
            print(f"\n🔗 Crear PR: {pr_url}")
        else:
            print(f"Remote: {rurl}")
    
    # Merge opcional
    if args.merge:
        print(f"\n🔀 Mergeando a {args.target}...")
        run(['git', 'checkout', args.target], show_output=False)
        run(['git', 'pull', 'origin', args.target], show_output=False)
        
        r = run(['git', 'merge', '--no-ff', branch_name, '-m', f"Merge {branch_name}"], show_output=False)
        if r.returncode != 0:
            print(f"❌ Merge falló: {r.stdout}")
            sys.exit(1)
        
        r = run(['git', 'push', 'origin', args.target], show_output=False)
        if r.returncode != 0:
            print(f"❌ Push a {args.target} falló: {r.stdout}")
            sys.exit(1)
        
        print(f"✅ Mergeado a {args.target}")
    
    print("\n✅ ¡Listo! Deploy completado.")


if __name__ == '__main__':
    main()

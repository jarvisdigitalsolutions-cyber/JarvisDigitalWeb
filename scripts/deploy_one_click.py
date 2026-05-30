#!/usr/bin/env python3
"""
One-click deploy script (Python)
Usage examples:
  python scripts/deploy_one_click.py --path Sony-Web
  python scripts/deploy_one_click.py -p Sony-Web --merge
"""
import argparse
import subprocess
import sys
import os
import datetime


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return r


def git_root():
    r = run(['git','rev-parse','--show-toplevel'])
    if r.returncode != 0:
        print('No se encontró un repositorio Git en el directorio actual.', file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--path','-p', default='Sony-Web', help='Directorio a añadir/commitear')
    p.add_argument('--branch','-b', default='', help='Branch a crear/subir (por defecto auto)')
    p.add_argument('--message','-m', default='', help='Mensaje de commit')
    p.add_argument('--merge','-M', action='store_true', help='Intentar merge al branch target (use con precaución)')
    p.add_argument('--target','-t', default='main', help='Branch target para merge')
    args = p.parse_args()

    root = git_root()
    os.chdir(root)

    if not os.path.exists(args.path):
        print(f"Ruta no encontrada: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not args.branch:
        ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        safe = args.path.replace(os.sep, '-').replace('/', '-').replace(' ', '-')
        args.branch = f"deploy-{safe}-{ts}"
    if not args.message:
        args.message = f"Auto: deploy {args.path} updates - {datetime.datetime.now().isoformat()}"

    # create or checkout branch
    r = run(['git','rev-parse','--verify', args.branch])
    if r.returncode == 0:
        print(f"Usando branch existente: {args.branch}")
        run(['git','checkout', args.branch])
    else:
        run(['git','checkout','-b', args.branch])

    run(['git','add','--all', args.path])
    status = run(['git','status','--porcelain'])
    if not status.stdout.strip():
        print(f"No hay cambios para commitear en '{args.path}'")
        sys.exit(0)

    commit = run(['git','commit','-m', args.message])
    if commit.returncode != 0:
        print('Commit falló:', commit.stdout)
        sys.exit(1)

    push = run(['git','push','-u','origin', args.branch])
    if push.returncode != 0:
        print('Push falló:', push.stdout)
        sys.exit(1)

    # Remote hint
    remote = run(['git','config','--get','remote.origin.url'])
    if remote.returncode == 0:
        rurl = remote.stdout.strip()
        repo = None
        if 'github.com' in rurl:
            if rurl.startswith('git@'):
                repo = rurl.split(':',1)[1].rstrip('.git')
            else:
                repo = rurl.split('github.com/')[-1].rstrip('.git')
        if repo:
            print(f"Crear PR: https://github.com/{repo}/pull/new/{args.branch}")
        else:
            print('Remote origin:', rurl)

    if args.merge:
        print(f"Intentando merge a {args.target} ...")
        run(['git','checkout', args.target])
        run(['git','pull','origin', args.target])
        m = run(['git','merge','--no-ff', args.branch, '-m', f"Merge {args.branch} -> {args.target} (auto)"])
        if m.returncode != 0:
            print('Merge falló:', m.stdout)
            sys.exit(1)
        run(['git','push','origin', args.target])

    print('Hecho.')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# Gera os temas VoidBR-Mac (base WhiteSur, MIT) com GTK2/3/4, xfwm4 (X11),
# labwc (Wayland) e Plank, em claro/escuro e 9 cores de destaque.
#
# uso: tools/gerar.py <clone-do-WhiteSur-gtk-theme> <raiz-do-repositorio>
#   git clone https://github.com/vinceliuice/WhiteSur-gtk-theme /tmp/ws
#   rm -rf usr/share/themes/VoidBR-Mac-* usr/share/plank/themes/VoidBR-Mac-*
#   python3 tools/gerar.py /tmp/ws .
# precisa do libsass do Python (pip install libsass) ou python3-libsass.
import os, re, shutil, sys, glob
import sass

src, out = sys.argv[1], sys.argv[2]
work = os.path.join(out, ".work")
shutil.rmtree(work, ignore_errors=True)
shutil.copytree(os.path.join(src, "src"), work)
shutil.copytree(os.path.join(src, "other"), os.path.join(out, ".other"), dirs_exist_ok=True)
S = work
nome = "VoidBR-Mac"
cores = ["Light", "Dark"]
temas = ["", "blue", "purple", "pink", "red", "orange", "yellow", "green", "grey"]

shutil.copy(f"{S}/sass/_theme-options.scss", f"{S}/sass/_theme-options-temp.scss")

def cp(a, b):
    for f in glob.glob(a):
        d = b if os.path.isdir(b) or b.endswith("/") else b
        os.makedirs(os.path.dirname(b.rstrip("/")) if not b.endswith("/") else b, exist_ok=True)
        if os.path.isdir(f):
            shutil.copytree(f, os.path.join(b, os.path.basename(f)) if b.endswith("/") else b, dirs_exist_ok=True)
        else:
            shutil.copy(f, d)

def compilar(scss, css):
    os.makedirs(os.path.dirname(css), exist_ok=True)
    with open(css, "w") as fh:
        fh.write(sass.compile(filename=scss, output_style="expanded"))

for tema in temas:
    base = open(f"{S}/sass/_gtk-base.scss").read()
    if tema:
        base = re.sub(r"(\$theme:\s*)'default'", rf"\1'{tema}'", base)
    open(f"{S}/sass/_gtk-base-temp.scss", "w").write(base)
    sufixo = f"-{tema}" if tema else ""
    for cor in cores:
        c = f"-{cor}"
        alvo = f"{out}/usr/share/themes/{nome}{c}{sufixo}"
        shutil.rmtree(alvo, ignore_errors=True)
        os.makedirs(alvo)
        open(f"{alvo}/index.theme", "w").write(
            "[Desktop Entry]\nType=X-GNOME-Metatheme\n"
            f"Name={nome}{c}{sufixo}\n"
            "Comment=Tema estilo macOS do VoidBR (baseado no WhiteSur, MIT)\nEncoding=UTF-8\n\n"
            "[X-GNOME-Metatheme]\n"
            f"GtkTheme={nome}{c}{sufixo}\nMetacityTheme={nome}{c}\n"
            "ButtonLayout=close,minimize,maximize:menu\n")
        for gtk in ("gtk-3.0", "gtk-4.0"):
            d = f"{alvo}/{gtk}"
            if tema:
                # assets iguais em todas as cores: link para o tema base
                os.makedirs(d)
                os.symlink(f"../../{nome}{c}/{gtk}/assets", f"{d}/assets")
                os.symlink(f"../../{nome}{c}/{gtk}/windows-assets", f"{d}/windows-assets")
            else:
                shutil.copytree(f"{S}/assets/gtk/common-assets/assets", f"{d}/assets")
                cp(f"{S}/assets/gtk/common-assets/sidebar-assets/*.png", f"{d}/assets/")
                shutil.copytree(f"{S}/assets/gtk/scalable", f"{d}/assets/scalable")
                shutil.copytree(f"{S}/assets/gtk/windows-assets/titlebutton", f"{d}/windows-assets")
            compilar(f"{S}/main/{gtk}/gtk{c}.scss", f"{d}/gtk.css")
            compilar(f"{S}/main/{gtk}/gtk-Dark.scss", f"{d}/gtk-dark.css")
            shutil.copy(f"{S}/assets/gtk/thumbnails/thumbnail{c}{sufixo}.png", f"{d}/thumbnail.png")
        d = f"{alvo}/gtk-2.0"
        os.makedirs(d)
        shutil.copy(f"{S}/main/gtk-2.0/gtkrc{c}{sufixo}", f"{d}/gtkrc")
        shutil.copy(f"{S}/main/gtk-2.0/menubar-toolbar{c}.rc", f"{d}/menubar-toolbar.rc")
        cp(f"{S}/main/gtk-2.0/common/*.rc", f"{d}/")
        shutil.copytree(f"{S}/assets/gtk-2.0/assets-common{c}", f"{d}/assets")
        cp(f"{S}/assets/gtk-2.0/assets{c}{sufixo}/*.png", f"{d}/assets/")
        # xfwm4 não muda com a cor de destaque: só no tema base de cada cor
        if not tema:
            for dpi in ("", "-hdpi", "-xhdpi"):
                x = f"{out}/usr/share/themes/{nome}{c}{dpi}/xfwm4"
                os.makedirs(x, exist_ok=True)
                cp(f"{S}/assets/xfwm4/assets{c}{dpi}/*.png", f"{x}/")
                shutil.copy(f"{S}/main/xfwm4/themerc{c}", f"{x}/themerc")
            # labwc: moldura das janelas no XFCE em Wayland
            l = f"{alvo}/labwc"
            os.makedirs(l)
            cp(f"{S}/assets/labwc/assets{c}/*.svg", f"{l}/")
            shutil.copy(f"{S}/main/labwc/themerc{c}", f"{l}/themerc")
            p = f"{out}/usr/share/plank/themes/{nome}{c}"
            os.makedirs(p, exist_ok=True)
            cp(f"{out}/.other/plank/theme{c}/*.theme", f"{p}/")
        else:
            # xfwm4 e labwc das variantes de cor apontam para os do tema base
            os.symlink(f"../{nome}{c}/xfwm4", f"{alvo}/xfwm4")
            os.symlink(f"../{nome}{c}/labwc", f"{alvo}/labwc")
    print("ok", tema or "default")

shutil.rmtree(work)
shutil.rmtree(os.path.join(out, ".other"))

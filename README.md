<div align="center">

# 🍎 voidbr-mac-themes

**Temas com visual do macOS para o VoidBR (claro/escuro, 9 cores de destaque)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

</div>

---

Temas com visual do macOS para o VoidBR Linux, usados pelo perfil "Visual Mac" do
`voidbr-xfce-tweaks`. Funcionam no XFCE em X11 (xfwm4) e em Wayland (labwc).

## Variantes

- **Aparência:** `Light` (claro) e `Dark` (escuro)
- **Cor de destaque:** padrão, `blue`, `purple`, `pink`, `red`, `orange`, `yellow`, `green`, `grey`

Nome do tema: `VoidBR-Mac-<Light|Dark>[-cor]`, por exemplo `VoidBR-Mac-Dark-purple`.

| Parte | Onde fica |
|---|---|
| GTK 2, 3 e 4 | `usr/share/themes/VoidBR-Mac-*/gtk-*` |
| Moldura no X11 (xfwm4, botões semáforo) | `usr/share/themes/VoidBR-Mac-Light/xfwm4` e `VoidBR-Mac-Dark/xfwm4` (+ `-hdpi`, `-xhdpi`) |
| Moldura no Wayland (labwc) | `usr/share/themes/VoidBR-Mac-Light/labwc` e `VoidBR-Mac-Dark/labwc` |
| Dock (Plank) | `usr/share/plank/themes/VoidBR-Mac-Light` e `VoidBR-Mac-Dark` |

A moldura (xfwm4 e labwc) não muda com a cor de destaque: nas variantes de cor ela é um
link para a do tema base, assim como os assets do GTK 3 e 4.

## Gerar de novo

Os temas são gerados a partir do código do
[WhiteSur-gtk-theme](https://github.com/vinceliuice/WhiteSur-gtk-theme) (MIT) pelo
`tools/gerar.py`, que só compila o SASS e copia os assets (não roda o instalador do WhiteSur):

```sh
git clone https://github.com/vinceliuice/WhiteSur-gtk-theme /tmp/ws
rm -rf usr/share/themes/VoidBR-Mac-* usr/share/plank/themes/VoidBR-Mac-*
python3 tools/gerar.py /tmp/ws .
```

Precisa do `libsass` do Python. Gerado a partir do WhiteSur `d5782652d412137e26fb8ff55b55a5572e4c6995`.

## Licença

MIT. Os temas derivam do WhiteSur (MIT, Copyright (c) 2021 WhiteSur Developers):
veja `licenses/WhiteSur-COPYING`.

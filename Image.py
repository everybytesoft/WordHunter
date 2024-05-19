import cairosvg


def svg_get_opacity(text):
    return ' opacity="0.3"' if text == ' ' else ''


def svg_square(color, text, x, y):
  return f'<rect fill="url(#{color})" x="{x * 32 + 2}" y="{y * 32 + 2}"{svg_get_opacity(text)} rx="5" width="30" height="30"/><text fill="#fff" x="{x * 32 + 1 + (32-24) * 0.6 * 2}" y="{y * 32 + 24 + 1}">{text}</text>'


def svg_grid(data):
    str = ''
    for i in range(6):
        for j in range(5):
            str+=svg_square(int(data[i][j][1]), data[i][j][0], j, i)
            
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="162" height="194"><style>text{{font:24px monospace}}</style><defs><linearGradient id="0" gradientTransform="rotate(90)"><stop stop-color="#4f4f4f" offset="0"/><stop stop-color="#212121" offset="1"/></linearGradient><linearGradient id="1" gradientTransform="rotate(90)"><stop stop-color="#ffec8e" offset="0"/><stop stop-color="#d1ab00" offset="1"/></linearGradient><linearGradient id="2" gradientTransform="rotate(90)"><stop stop-color="#8eff97" offset="0"/><stop stop-color="#00d10e" offset="1"/></linearGradient></defs><rect fill="#000" width="162" height="194"/>{str}</svg>'

    with open('vector.svg' , 'w') as f:
      f.write(svg)
    
    with open('vector.svg', 'r') as f:
      svg_data = f.read()
    
    cairosvg.svg2png(bytestring=svg, write_to='output.png')

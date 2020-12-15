import ast
import configparser
import getopt
import os
import svgwrite
import sys
import wordclock_tools.wiring as wiring


def searchInWCA(wcl, index):
    for i in range(wcl.WCA_WIDTH):
        for j in range(wcl.WCA_HEIGHT):
            if wcl.getStripIndexFrom2D(i, j) == index:
                return i, j
    return None


def searchInMinutes(wcl, index):
    for i in [1, 2, 3, 4]:
        if wcl.mapMinutes(i) == index:
            return i
    print(('Mapping error for minute: Index: ' + str(index)))
    return None


def get_letter_coords(wca_top_left, x, x_spacing, y, y_spacing, side, col_num):
    if side == 'front':
        return wca_top_left[0] + x * x_spacing, wca_top_left[1] + y * y_spacing
    elif side == 'back':
        return wca_top_left[0] + (col_num - x - 1) * x_spacing, wca_top_left[1] + y * y_spacing


def get_min_coords(width, height, minute_margin, min_num, side):
    if (side == 'front' and min_num == 1) or (side == 'back' and min_num == 2):
        return minute_margin, minute_margin
    elif (side == 'front' and min_num == 2) or (side == 'back' and min_num == 1):
        return width - minute_margin, minute_margin
    elif (side == 'front' and min_num == 3) or (side == 'back' and min_num == 4):
        return minute_margin, height - minute_margin
    elif (side == 'front' and min_num == 4) or (side == 'back' and min_num == 3):
        return width - minute_margin, height - minute_margin
    else:
        print(('ERROR: Invalid ' + str(min_num)))


def create_svg(lang, config, side='front', mode='stencil'):
    if not mode == 'stencil':
        wiring_type = config.get('wordclock_display', 'wiring_layout')
    else:
        wiring_type = ''
    outpt_file = mode + '_' + side + '_' + wiring_type + '.svg'
    print(('Rendering ' + outpt_file + '...'))
    print(('  Side .........: ' + side))
    print(('  Mode .........: ' + mode))
    content = ast.literal_eval(config.get('language_options', lang))
    print(('  Language .....: ' + lang))
    font_type = config.get('stencil_parameter', 'font_type')
    print(('  Font-type.....: ' + font_type))
    font_size = config.get('stencil_parameter', 'font_size')
    print(('  Font-size.....: ' + font_size))
    height = float(config.get('stencil_parameter', 'height'))
    print(('  Height .......: ' + str(height) + 'mm'))
    width = float(config.get('stencil_parameter', 'width'))
    print(('  Width ........: ' + str(width) + 'mm'))
    wca_height = float(config.get('stencil_parameter', 'wca_height'))
    print(('  Wca height ...: ' + str(wca_height) + 'mm'))
    wca_width = float(config.get('stencil_parameter', 'wca_width'))
    print(('  Wca width ....: ' + str(wca_width) + 'mm'))
    row_num = len(content)
    print(('  Wca rows .....: ' + str(row_num)))
    col_num = len(content[0].decode('utf-8'))
    print(('  Wca columns ..: ' + str(col_num)))
    minute_margin = float(config.get('stencil_parameter', 'minute_margin'))
    minute_diameter = float(config.get('stencil_parameter', 'minute_diameter'))
    rm = minute_diameter / 2

    # Create directory to store layout
    file_dir = os.path.join('wordclock_layouts', lang + '_' + str(col_num) + 'x' + str(row_num))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    full_path = os.path.join(file_dir, outpt_file)

    # Set colors
    if mode == 'stencil':
        fg = 'rgb(255,255,255)'
        bg = 'rgb(0,0,0)'
    else:
        fg = 'rgb(0,0,0)'
        bg = 'rgb(255,255,255)'

    # Generate header
    layout = svgwrite.Drawing(full_path,
                              size=(str(width) + 'mm', str(height) + 'mm'), \
                              viewBox=('0 0 ' + str(width) + ' ' + str(height)))
    # Assure set background-color to bg
    layout.add(layout.rect(insert=(0, 0),
                           size=('100%', '100%'), rx=None, ry=None, fill=bg))
    # Create layout-group for text
    text_layout = layout.g(style=
                               'text-anchor:middle;'
                               'fill:' + fg + ';'
                                              'font-family:' + font_type + ';'
                                                                           'font-size:' + str(
                                   font_size if mode == 'stencil' else 6))

    # Process letters
    wca_top_left = [(width - wca_width) / 2, (height - wca_height) / 2]
    x_coords = list(range(0, col_num, 1))
    y_coords = list(range(0, row_num, 1))
    x_spacing = wca_width / (col_num - 1)
    y_spacing = wca_height / (row_num - 1)

    # Additional steps to prepare the plotting of the wiring layout
    x_sub_spacing = x_spacing / 5.0
    y_sub_spacing = y_spacing / 5.0
    wca_index_1d = 0

    # Add annotations
    if not mode == 'stencil':
        layout.add(layout.text(lang + ' --- ' + side + '-view --- ' + wiring_type, insert=(width / 2, minute_margin),
                               style='text-anchor:middle;'
                                     'fill:rgb(0,255,0);'
                                     'font-family:' + font_type + ';'
                                                                  'font-size: 10'))
    # Add the wiring according to the chosen wiring layout
    if mode == 'wiring':
        wcl = wiring.wiring(config)
        led_count = col_num * row_num + 4
        for i in range(0, led_count - 1):
            # Draw wiring from start ...
            wire_start = searchInWCA(wcl, i)
            if wire_start is not None:
                coords_start = get_letter_coords(wca_top_left, wire_start[0], x_spacing, wire_start[1], y_spacing, side,
                                                 col_num)
            else:
                wire_start = searchInMinutes(wcl, i)
                coords_start = get_min_coords(width, height, minute_margin, wire_start, side)
            # ... to end
            wire_end = searchInWCA(wcl, i + 1)
            if wire_end is not None:
                coords_end = get_letter_coords(wca_top_left, wire_end[0], x_spacing, wire_end[1], y_spacing, side,
                                               col_num)
            else:
                wire_end = searchInMinutes(wcl, i + 1)
                coords_end = get_min_coords(width, height, minute_margin, wire_end, side)
            text_layout.add(
                layout.line((coords_start[0], coords_start[1]), (coords_end[0], coords_end[1]), stroke='rgb(255,0,0)'))

    # Draw characters
    for y in y_coords:
        for x in x_coords:
            coords = get_letter_coords(wca_top_left, x, x_spacing, y, y_spacing, side, col_num)
            if mode == 'stencil':
                # Write only characters
                text_layout.add(layout.text((content[y].decode('utf-8')[x]),
                                            insert=(coords[0], coords[1] + float(font_size) / 2.0)))
            else:
                # Write characters (top left)
                coords_tl = coords[0] - x_sub_spacing, coords[1] - y_sub_spacing
                text_layout.add(layout.text((content[y].decode('utf-8')[x]), insert=coords_tl))

                # Write 1D coordinate (top right)
                coords_tr = coords[0] + x_sub_spacing, coords[1] - y_sub_spacing
                text_layout.add(layout.text(str(wca_index_1d), insert=coords_tr))

                # Write 2D coordinate (bottom left)
                coords_bl = coords[0] - x_sub_spacing, coords[1] + y_sub_spacing
                text_layout.add(layout.text(('(' + str(x) + "," + str(y) + ')'), insert=coords_bl))

                # Placeholder for bottom-left
                # coords_br = coords[0]+x_sub_spacing, coords[1]+y_sub_spacing
                # text_layout.add(layout.text((content[y].decode('utf-8')[x]), insert = coords_br, fill=fg, style='text-anchor: middle'))

                # Add cross
                text_layout.add(
                    layout.line((coords[0], coords[1] - y_sub_spacing), (coords[0], coords[1] + y_sub_spacing),
                                stroke=fg))
                text_layout.add(
                    layout.line((coords[0] - x_sub_spacing, coords[1]), (coords[0] + x_sub_spacing, coords[1]),
                                stroke=fg))

            wca_index_1d += 1

    # Process minutes
    for min_num in [1, 2, 3, 4]:
        min_coords = get_min_coords(width, height, minute_margin, min_num, side)
        if mode == 'stencil':
            text_layout.add(layout.circle(
                center=min_coords,
                r=rm, fill=fg)
                )
        else:
            text_layout.add(layout.text(str(min_num),
                                        insert=(min_coords[0] - x_sub_spacing, min_coords[1] - y_sub_spacing),
                                        fill=fg)
                            )
            text_layout.add(layout.line((min_coords[0], min_coords[1] - y_sub_spacing),
                                        (min_coords[0], min_coords[1] + y_sub_spacing), stroke=fg))
            text_layout.add(layout.line((min_coords[0] - x_sub_spacing, min_coords[1]),
                                        (min_coords[0] + x_sub_spacing, min_coords[1]), stroke=fg))

    # Add connection to RPi at minute number 4
    # Since minute number 4 is specific for 'bernds_wiring', we check here, if this is the current wiring type
    if not mode == 'stencil' and wiring_type == 'bernds_wiring':
        min_num = 4
        min_coords = get_min_coords(width, height, minute_margin, min_num, side)
        text_layout.add(layout.line((min_coords[0], min_coords[1]),
                                    (min_coords[0] + 5 * x_sub_spacing * (-1 if side == 'front' else 1), min_coords[1]),
                                    stroke='rgb(255,0,0)'))
        coords_rpi = min_coords[0] + 6 * x_sub_spacing * (-1 if side == 'front' else 1), min_coords[1]
        text_layout.add(layout.text('Connect here to power supply and Raspberry.', insert=coords_rpi,
                                    style=('text-anchor:end;' if side == 'front' else 'text-anchor:start')))

    # Fuse layouts
    layout.add(text_layout)

    # Saving svg-file
    layout.save()
    print(('Saved ' + full_path + '.'))


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ahc:', ['all', 'help', 'config='])
    except getopt.GetoptError as err:
        print((str(err)))
        sys.exit(2)
    configFile = 'wordclock_config/wordclock_config.example.cfg'
    process_all = False
    for o, a in opts:
        if o in ('-a', '--all'):
            process_all = True
        elif o in ('-c', '--config'):
            configFile = a
        elif o in '-h':
            print('Provide config-file using -c option')
            print('Process all layouts using -a option')
            sys.exit(0)
        else:
            assert False, 'unhandled option'

    print(('Using ' + configFile + ' to parse configuration.'))
    print(('Use\n\t' + str(sys.argv[0]) + ' -c "config-file"\nto change'))
    cfg = configparser.ConfigParser()
    cfg.read(configFile)

    if process_all:
        all_languages = cfg.options('language_options')
    else:
        all_languages = [cfg.get('wordclock_display', 'language')]

    for lang in all_languages:
        print(('Processing layouts for ' + str(lang) + '.'))
        create_svg(lang, cfg, side='front', mode='stencil')
        create_svg(lang, cfg, side='front', mode='wiring')
        create_svg(lang, cfg, side='back', mode='wiring')


if __name__ == '__main__':
    main()

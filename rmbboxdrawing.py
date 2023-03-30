#!/bin/env python3
"""
RMB's box drawing module
"""

import unicodedata

class Rmbboxdrawing:

    # In addition to the 128 unicode box drawing characters (code page 2500), I've added (at the end) at least one character from another codepage

    unicode_boxchars = [
                       '─', '━', '│', '┃', '┄', '┅', '┆', '┇', '┈', '┉', '┊', '┋', '┌', '┍', '┎', '┏',

                       '┐', '┑', '┒', '┓', '└', '┕', '┖', '┗', '┘', '┙', '┚', '┛', '├', '┝', '┞', '┟',

                       '┠', '┡', '┢', '┣', '┤', '┥', '┦', '┧', '┨', '┩', '┪', '┫', '┬', '┭', '┮', '┯',

                       '┰', '┱', '┲', '┳', '┴', '┵', '┶', '┷', '┸', '┹', '┺', '┻', '┼', '┽', '┾', '┿',

                       '╀', '╁', '╂', '╃', '╄', '╅', '╆', '╇', '╈', '╉', '╊', '╋', '╌', '╍', '╎', '╏',

                       '═', '║', '╒', '╓', '╔', '╕', '╖', '╗', '╘', '╙', '╚', '╛', '╜', '╝', '╞', '╟',

                       '╠', '╡', '╢', '╣', '╤', '╥', '╦', '╧', '╨', '╩', '╪', '╫', '╬', '╭', '╮', '╯',

                       '╰', '╱', '╲', '╳', '╴', '╵', '╶', '╷', '╸', '╹', '╺', '╻', '╼', '╽', '╾', '╿',

                       '⸱',
                       ]

    # 'box' is a dictionary. For each item..
    #
    #   keys:   The keys are the names of each box character (my names, not the official unicode names (which can be too long for my purposes))
    #   values: The values are the box characters themselves
    #
    # Suffixes for the key names refer to the typeface of its character..
    #
    #     No Suffix - Normal typeface
    #     N - Normal
    #     B - Bold
    #     D - Dotted line
    #     2 - Double line
    #
    # Examples:
    #
    #     --------         ----    --------                       ---------
    #     Dict key         char    Location                       Typefaces
    #     --------         ----    --------                       ---------
    #     'horiz'          '─'     Horizontal bar                 normal
    #     'horizD'         '┈'     Dotted horizontal bar          dotted line
    #     'horizDB'        '┅'     Bold dotted horizontal bar     bold dotted line
    #     'vertB'          '┃'     Vertical bar                   bold
    #     'topleftNB'      '┍'     Top left corner                normal, bold
    #     'bottomrightBN'  '┚'     Bottom right corner            bold, normal
    #     'topteeNNB'      '┮'     Top tee                        normal, normal, bold
    #     'middleNBNB'     '┿'     Middle cross                   normal, bold, normal, bold
    #     'bottomright2S'  '╜'     Bottom Right corner            double line (as in, '2' == 'double'), normal

    box = {
     'bottomleft': '└',
     'bottomleft22': '╚',
     'bottomleft2S': '╙',
     'bottomleftBB': '┗',
     'bottomleftBN': '┖',
     'bottomleftNB': '┕',
     'bottomleftNN': '└',
     'bottomleftS2': '╘',
     'bottomleftSS': '└',
     'bottomright': '┘',
     'bottomright22': '╝',
     'bottomright2S': '╜',
     'bottomrightBB': '┛',
     'bottomrightBN': '┚',
     'bottomrightNB': '┙',
     'bottomrightNN': '┘',
     'bottomrightS2': '╛',
     'bottomrightSS': '┘',
     'bottomtee': '┴',
     'bottomtee222': '╩',
     'bottomteeBBB': '┻',
     'bottomteeBBN': '┹',
     'bottomteeBNB': '┺',
     'bottomteeBNN': '┸',
     'bottomteeNBB': '┷',
     'bottomteeNBN': '┵',
     'bottomteeNNB': '┶',
     'bottomteeNNN': '┴',
     'horiz': '─',
     'horiz2': '═',
     'horizB': '━',
     'horizD': '┈',
     'horizDB': '┅',
     'intersect': '┼',
     'intersect2222': '╬',
     'intersect2N2N': '╫',
     'intersectBBBB': '╋',
     'intersectBBBN': '╊',
     'intersectBBNB': '╇',
     'intersectBBNN': '╄',
     'intersectBNBB': '╉',
     'intersectBNBN': '╂',
     'intersectBNNB': '╃',
     'intersectBNNN': '╀',
     'intersectN2N2': '╪',
     'intersectNBBB': '╈',
     'intersectNBBN': '╆',
     'intersectNBNB': '┿',
     'intersectNBNN': '┾',
     'intersectNNBB': '╅',
     'intersectNNBN': '╁',
     'intersectNNNB': '┽',
     'intersectNNNN': '┼',
     'lefttee': '├',
     'leftteeBBB': '┣',
     'leftteeBBN': '┡',
     'leftteeBNB': '┠',
     'leftteeBNN': '┞',
     'leftteeNBB': '┢',
     'leftteeNBN': '┝',
     'leftteeNNB': '┟',
     'leftteeNNN': '├',
     'leftteeS2S': '╞',
     'middle_dot': '·',
     'middle_dot_2500': '⸱',
     'righttee': '┤',
     'rightteeBBB': '┫', 
     'rightteeBBN': '┩',
     'rightteeBNB': '┨',
     'rightteeBNN': '┦',
     'rightteeNBB': '┪',
     'rightteeNBN': '┥',
     'rightteeNNB': '┧',
     'rightteeNNN': '┤',
     'rightteeS2S': '╡',
     'topleft': '┌',
     'topleft22': '╔',
     'topleft2S': '╓',
     'topleftBB': '┏',
     'topleftBN': '┎',
     'topleftNB': '┍',
     'topleftNN': '┌',
     'topleftS2': '╒',
     'topleftSS': '┌',
     'topright': '┐',
     'topright22': '╗',
     'topright2S': '╖',
     'toprightBB': '┓',
     'toprightBN': '┒',
     'toprightNB': '┑',
     'toprightNN': '┐',
     'toprightS2': '╕',
     'toprightSS': '┐',
     'toptee': '┬',
     'toptee222': '╦',
     'topteeBBB': '┳',
     'topteeBBN': '┱',
     'topteeBNB': '┲',
     'topteeBNN': '┰',
     'topteeNBB': '┯',
     'topteeNBN': '┭',
     'topteeNNB': '┮',
     'topteeNNN': '┬',
     'vert': '│',
     'vert2': '║',
     'vertB': '┃',
     'vertD': '┊',
     'vertDB': '┇',
    }

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    for k, v in Rmbboxdrawing.box.items():
        print(f"    box['{k}']: {v}")

